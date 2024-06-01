import os
import sys
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import requests
import shutil
from requests.auth import HTTPBasicAuth
from github_writer import GitHubWriter
from wordpress_image_downloader import download_image_if_not_exists

def extract_urls_from_style(style):
    urls = []
    start = style.find('url(')
    while start != -1:
        start += 4  # Skip 'url('
        end = style.find(')', start)
        url = style[start:end].strip('\'"')
        urls.append(url)
        start = style.find('url(', end)
    return urls

def download_and_update_html(environment, wordpress_staging_username, wordpress_staging_password):
    writer = GitHubWriter()
    headers = {
        'Accept': 'application/json',
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
    }

    folder_path = './dist/assets'
    base_path = './assets'

    # Setup authentication if not in production environment
    auth = None
    if environment != "PROD":
        auth = HTTPBasicAuth(wordpress_staging_username, wordpress_staging_password)

    # Create directory for saving images if it does not exist
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    # List of HTML files to be updated
    html_files = [
        'dist/index.html',
        'dist/index-ar.html',
        'dist/index-cs.html',
        'dist/index-de.html',
        'dist/index-es.html',
        'dist/index-fr.html',
        'dist/index-it.html',
        'dist/index-ja.html',
        'dist/index-ko.html',
        'dist/index-pl.html',
        'dist/index-pt.html',
        'dist/index-ru.html',
        'dist/index-tr.html',
        'dist/index-zh-CN.html',
        'dist/index-zh-TW.html'
    ]

    for html_file in html_files:
        if not os.path.exists(html_file):
            writer.write_summary(f"- {html_file} does not exist, skipping...\n")
            continue

        with open(html_file, "r") as file:
            soup = BeautifulSoup(file, 'html.parser')

        images = soup.find_all('img')
        elements_with_style = soup.find_all(style=True)
        header_styles = soup.find_all('style')

        for img in images:
            img_url = img.get('src')
            if img_url and (not img_url.startswith('data:image')):
                local_filename = os.path.basename(img_url)
                local_filepath = os.path.join(folder_path, local_filename)
                download_image_if_not_exists(img_url, local_filepath, headers, auth, environment, writer)
                img['src'] = os.path.join(base_path, local_filename)

            img_srcset = img.get('srcset')
            if img_srcset and (not img_srcset.startswith('data:image')):
                new_srcset = []
                srcset_items = img_srcset.split(',')
                for item in srcset_items:
                    url, size = item.strip().split(' ')
                    local_filename = os.path.basename(url)
                    local_filepath = os.path.join(folder_path, local_filename)
                    download_image_if_not_exists(url, local_filepath, headers, auth, environment, writer)
                    new_srcset.append(f"{os.path.join(base_path, local_filename)} {size}")

                img['srcset'] = ', '.join(new_srcset)

        for element in elements_with_style:
            style = element.get('style')
            if 'url(' in style:
                urls = extract_urls_from_style(style)
                for url in urls:
                    local_filename = os.path.basename(url)
                    local_filepath = os.path.join(folder_path, local_filename)
                    download_image_if_not_exists(url, local_filepath, headers, auth, environment, writer)
                    new_url = os.path.join(base_path, local_filename)
                    style = style.replace(url, new_url)

                element['style'] = style

        for style_tag in header_styles:
            style_content = style_tag.string
            if style_content and 'url(' in style_content:
                urls = extract_urls_from_style(style_content)
                for url in urls:
                    local_filename = os.path.basename(url)
                    local_filepath = os.path.join(folder_path, local_filename)
                    download_image_if_not_exists(url, local_filepath, headers, auth, environment, writer)
                    new_url = os.path.join(base_path, local_filename)
                    style_content = style_content.replace(url, new_url)

                style_tag.string.replace_with(style_content)

        with open(html_file, 'w') as file:
            file.write(str(soup))

if __name__ == "__main__":
    writer = GitHubWriter()
    try:
        if len(sys.argv) != 4:
            raise ValueError("Usage: python wordpress-cloning-script.py <environment> <wordpress_staging_username> <wordpress_staging_password>")
        
        env = sys.argv[1]
        wordpress_staging_username = sys.argv[2]
        wordpress_staging_password = sys.argv[3]
        download_and_update_html(env, wordpress_staging_username, wordpress_staging_password)
        writer.write_output("script-success", "true")
    except Exception as e:
        writer.write_summary(f"Error: {str(e)}\n")
        writer.write_output("script-success", "false")
        sys.exit(1)
