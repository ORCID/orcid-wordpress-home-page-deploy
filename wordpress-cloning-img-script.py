import os
import sys
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import requests
import shutil
from requests.auth import HTTPBasicAuth
from github_writer import GitHubWriter

def download_image_if_not_exists(full_img_url, local_filepath, headers, auth, env):
    if not os.path.exists(local_filepath):
        try:
            img_data = requests.get(full_img_url, stream=True, headers=headers, auth=auth)
            if img_data.status_code != 200:
                writer.write_summary_and_fail_on_prod(f"- 🚨 Failed to download image: {full_img_url}, status code: {img_data.status_code}\n", env)
     
            with open(local_filepath, 'wb') as file:
                img_data.raw.decode_content = True
                shutil.copyfileobj(img_data.raw, file)
            writer.write_summary(f"- Successfully downloaded image: {full_img_url} \n")
        except requests.exceptions.MissingSchema:
            writer.write_summary_and_fail_on_prod(f"- Please use a full URL for  {full_img_url}. \n", env)
        except Exception as e:
            writer.write_summary_and_fail(f"Error: {str(e)}\n", env)



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

        for img in images:
            img_url = img.get('src')
            if img_url and (not img_url.startswith('data:image')):
                local_filename = os.path.basename(img_url)
                local_filepath = os.path.join(folder_path, local_filename)
                download_image_if_not_exists(img_url, local_filepath, headers, auth, environment)
                img['src'] = os.path.join(base_path, local_filename)
    

            img_srcset = img.get('srcset')
            if img_srcset and (not img_srcset.startswith('data:image')):
                new_srcset = []
                srcset_items = img_srcset.split(',')
                for item in srcset_items:
                    url, size = item.strip().split(' ')
                    local_filename = os.path.basename(url)
                    local_filepath = os.path.join(folder_path, local_filename)
                    download_image_if_not_exists(url, local_filepath, headers, auth, environment)
                    new_srcset.append(f"{os.path.join(base_path, local_filename)} {size}")

                img['srcset'] = ', '.join(new_srcset)

        for element in elements_with_style:
            style = element.get('style')
            if 'url(' in style:
                urls = extract_urls_from_style(style)
                for url in urls:
                    local_filename = os.path.basename(url)
                    local_filepath = os.path.join(folder_path, local_filename)
                    download_image_if_not_exists(url, local_filepath, headers, auth, environment)
                    new_url = os.path.join(base_path, local_filename)
                    style = style.replace(url, new_url)
 
                element['style'] = style

        with open(html_file, 'w') as file:
            file.write(str(soup))

def extract_urls_from_style(style):
    urls = []
    start = style.find('url(')
    while start != -1:
        start += 4  # Skip 'url('
        end = style.find(')', start)
        url = style[start:end].strip('\'"')
        urls.append(url)
        start = style.find('url(', end)
    print('urls:', urls)
    return urls

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