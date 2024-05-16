import os
import sys
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import requests
import shutil
from requests.auth import HTTPBasicAuth

def download_and_update_html(environment, wordpress_staging_username, wordpress_staging_password, folder_path='./dist/'):

    headers = {
        'Accept': 'application/json',
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
    }

    # Setup authentication if not in production environment
    auth = None
    if environment != "PROD":
        auth = HTTPBasicAuth(wordpress_staging_username, wordpress_staging_password)

    # Create directory for saving images if it does not exist
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    # Open and read the local HTML file
    with open(f"dist/index.html", "r") as file:
        soup = BeautifulSoup(file, 'html.parser')

    # Find all image tags
    images = soup.find_all('img')

    # Loop through all images, download them, and update their src and srcset attributes
    for img in images:
        # Get the source attribute of the image
        img_url = img.get('src')
        if img_url and (not img_url.startswith('data:image')):
            # Complete the URL if it's relative (not absolute link)
            full_img_url = img_url
            # Download the image
            img_data = requests.get(full_img_url, stream=True, headers=headers, auth=auth)
            # Define the new local filename
            local_filename = os.path.basename(img_url)
            # Save the image locally
            local_filepath = os.path.join(folder_path, local_filename)
            with open(local_filepath, 'wb') as file:
                img_data.raw.decode_content = True
                shutil.copyfileobj(img_data.raw, file)
            # Update the src attribute to the new local path
            img['src'] = os.path.join('./', local_filename)
        
        # Get the srcset attribute of the image
        img_srcset = img.get('srcset')
        if img_srcset and (not img_srcset.startswith('data:image')):
            new_srcset = []
            srcset_items = img_srcset.split(',')
            for item in srcset_items:
                url, size = item.strip().split(' ')
                full_img_url = url
                # Download the image
                img_data = requests.get(full_img_url, stream=True, headers=headers, auth=auth)
                # Define the new local filename
                local_filename = os.path.basename(url)
                # Save the image locally
                local_filepath = os.path.join(folder_path, local_filename)
                with open(local_filepath, 'wb') as file:
                    img_data.raw.decode_content = True
                    shutil.copyfileobj(img_data.raw, file)
                # Add the new srcset item to the list
                new_srcset.append(f"{os.path.join('./', local_filename)} {size}")
            # Update the srcset attribute to the new local paths
            img['srcset'] = ', '.join(new_srcset)

    # Write the updated HTML to a new file
    with open(f"dist/index.html", 'w') as file:
        file.write(str(soup))

if __name__ == "__main__":
    print(sys.argv)
    if len(sys.argv) != 4:
        print("Usage: python wordpress-cloning-script.py <environment> <wordpress_staging_username> <wordpress_staging_password>")
        sys.exit(1)
    
    env = sys.argv[1]
    wordpress_staging_username = sys.argv[2]
    wordpress_staging_password = sys.argv[3]
    download_and_update_html(env, wordpress_staging_username, wordpress_staging_password)