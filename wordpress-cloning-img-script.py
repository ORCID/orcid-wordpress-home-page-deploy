import os
import sys
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import requests
import shutil
from requests.auth import HTTPBasicAuth
from github_writer import GitHubWriter

def download_image_if_not_exists(img_url, full_img_url, local_filepath, headers, auth):
    if not os.path.exists(local_filepath):
        img_data = requests.get(full_img_url, stream=True, headers=headers, auth=auth)
        with open(local_filepath, 'wb') as file:
            img_data.raw.decode_content = True
            shutil.copyfileobj(img_data.raw, file)
        return True
    return False

def download_and_update_html(environment, wordpress_staging_username, wordpress_staging_password, folder_path='./dist/'):
    writer = GitHubWriter()
    headers = {
        'Accept': 'application/json',
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
    }

    # Setup authentication if not in production environment
    auth = None
    base_path = None
    if environment != "PROD":
        auth = HTTPBasicAuth(wordpress_staging_username, wordpress_staging_password)
        base_path = 'https://d3055hwma3riwo.cloudfront.net/'
    else:
        base_path = 'https://update-me.cloudfront.net/'

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

        for img in images:
            img_url = img.get('src')
            try:
                if img_url and (not img_url.startswith('data:image')):
                    full_img_url = urljoin(base_path, img_url)
                    local_filename = os.path.basename(img_url)
                    local_filepath = os.path.join(folder_path, local_filename)
                    if download_image_if_not_exists(img_url, full_img_url, local_filepath, headers, auth):
                        img['src'] = os.path.join(base_path, local_filename)
                        writer.write_summary(f"- Successfully downloaded and updated image: {img_url} -> {img['src']}\n")
            except requests.exceptions.RequestException as e:
                writer.write_summary(f"- 🚨 Error occurred while trying to download {img_url}. \n Error: {e}\n")
                writer.write_output("script-success", "false")
                raise

            img_srcset = img.get('srcset')
            if img_srcset and (not img_srcset.startswith('data:image')):
                new_srcset = []
                srcset_items = img_srcset.split(',')
                for item in srcset_items:
                    url, size = item.strip().split(' ')
                    full_img_url = urljoin(base_path, url)
                    try:
                        local_filename = os.path.basename(url)
                        local_filepath = os.path.join(folder_path, local_filename)
                        if download_image_if_not_exists(url, full_img_url, local_filepath, headers, auth):
                            new_srcset.append(f"{os.path.join(base_path, local_filename)} {size}")
                            writer.write_summary(f"- Successfully downloaded and updated srcset image: {url} -> {os.path.join(base_path, local_filename)}\n")
                    except requests.exceptions.RequestException as e:
                        writer.write_summary(f"- 🚨 Error occurred while trying to download srcset image {url}. \n Error: {e}\n")
                        writer.write_output("script-success", "false")
                        raise
                img['srcset'] = ', '.join(new_srcset)

        with open(html_file, 'w') as file:
            file.write(str(soup))
        writer.write_summary(f"- Successfully updated {html_file}\n")

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