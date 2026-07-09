import os
import sys
import requests
import shutil
from urllib.parse import urljoin, urlparse, urlunparse
from requests.auth import HTTPBasicAuth
from github_writer import GitHubWriter
from wordpress_image_downloader import download_image_if_not_exists


def extract_urls_from_style(style):
    # Extract URLs from a CSS style string
    urls = []
    start = style.find('url(')
    while start != -1:
        start += 4  # Skip 'url('
        end = style.find(')', start)
        url = style[start:end].strip('\'"')
        urls.append(url)
        start = style.find('url(', end)
    return urls

def download_and_update_css(environment, wordpress_staging_username, wordpress_staging_password):
    writer = GitHubWriter()
    headers = {
        'Accept': 'application/json',
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36",
    }

    css_file = 'dist/wordpress-homepage.css'
    folder_path = './dist/assets'
    base_path = './assets'
    base_url = "https://orcidhomepage1.wpenginepowered.com/" if environment != "PROD" else "https://info.orcid.org/"
    processed_urls = set()
    failed_urls = []

    # Setup authentication if not in production environment
    auth = None
    if environment != "PROD":
        auth = HTTPBasicAuth(wordpress_staging_username, wordpress_staging_password)

    # Create directory for saving images if it does not exist
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    if not os.path.exists(css_file):
        writer.write_summary(f"- {css_file} does not exist, skipping...\n")
        return

    with open(css_file, "r") as file:
        css_content = file.read()

    # Find all URLs in the CSS content
    urls = extract_urls_from_style(css_content)
    for url in urls:
        if not url:
            continue
        key = url
        if url.startswith("/"):
            key = urljoin(base_url, url)
        elif url.startswith("//"):
            key = "https:" + url
        elif not url.startswith(("http://", "https://")):
            key = urljoin(base_url, url)
        if key in processed_urls:
            continue
        processed_urls.add(key)

        sanitized_filepath = download_image_if_not_exists(url, headers, auth, environment, writer, base_url=base_url)
        if sanitized_filepath is None:
            # Keep the original URL: rewriting to a file that was never
            # downloaded would ship CSS pointing at non-existent assets.
            failed_urls.append(key)
            continue
        new_url = os.path.join(base_path, os.path.basename(sanitized_filepath))
        css_content = css_content.replace(url, new_url)

    # Write the updated CSS content back to the file
    with open(css_file, 'w') as file:
        file.write(css_content)

    if failed_urls:
        writer.write_summary(f"\n### 🚨 {len(failed_urls)} image download(s) failed\n")
        writer.write_summary("| Failed image URL |\n| --- |\n")
        for failed_url in failed_urls:
            writer.write_summary(f"| {failed_url} |\n")
        writer.write_error(f"{len(failed_urls)} CSS image download(s) failed after retries (rate limited by WP Engine?). The CSS keeps the original URLs; this build must not be deployed or tagged.")
        raise RuntimeError(f"{len(failed_urls)} image download(s) failed")


if __name__ == "__main__":
    writer = GitHubWriter()
    try:
        if len(sys.argv) != 4:
            raise ValueError("Usage: python wordpress-css-script.py <environment> <wordpress_staging_username> <wordpress_staging_password>")

        env = sys.argv[1]
        wordpress_staging_username = sys.argv[2]
        wordpress_staging_password = sys.argv[3]
        download_and_update_css(env, wordpress_staging_username, wordpress_staging_password)
        writer.write_output("script-success", "true")
    except Exception as e:
        writer.write_summary(f"Error: {str(e)}\n")
        writer.write_output("script-success", "false")
        sys.exit(1)
