import os
import sys
import requests
import shutil
from urllib.parse import urljoin
from requests.auth import HTTPBasicAuth
from github_writer import GitHubWriter

def download_image_if_not_exists(full_img_url, local_filepath, headers, auth, env, writer):
    # Ensure the URL has a protocol
    if full_img_url.startswith("//"):
        full_img_url = "https:" + full_img_url
    elif not full_img_url.startswith(("http://", "https://")):
        full_img_url = "https://" + full_img_url

    # Download and save the image if it doesn't exist locally
    if not os.path.exists(local_filepath):
        try:
            img_data = requests.get(full_img_url, stream=True, headers=headers, auth=auth)
            if img_data.status_code != 200:
                writer.write_summary_and_fail_on_prod(f"- 🚨 Failed to download image: {full_img_url}, status code: {img_data.status_code}\n", env)
                return
            with open(local_filepath, 'wb') as file:
                img_data.raw.decode_content = True
                shutil.copyfileobj(img_data.raw, file)
            writer.write_summary(f"- Successfully downloaded image: {full_img_url} \n")
        except requests.exceptions.MissingSchema:
            writer.write_summary_and_fail_on_prod(f"- Please use a full URL for {full_img_url}. \n", env)
        except Exception as e:
            writer.write_summary_and_fail_on_prod(f"Error: {str(e)}\n", env)

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
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
    }

    css_file = 'dist/wordpress-homepage.css'
    folder_path = './dist/assets'
    base_path = './assets'

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
        local_filename = os.path.basename(url)
        local_filepath = os.path.join(folder_path, local_filename)
        download_image_if_not_exists(url, local_filepath, headers, auth, environment, writer)
        new_url = os.path.join(base_path, local_filename)
        css_content = css_content.replace(url, new_url)

    # Write the updated CSS content back to the file
    with open(css_file, 'w') as file:
        file.write(css_content)

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