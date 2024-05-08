import os
import sys
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import requests
import shutil
from requests.auth import HTTPBasicAuth

def download_and_update_html( environment,wordpreess_staggin_username, wordpreess_staggin_password,folder_path='./dist/'):

    headers = {
        'Accept': 'application/json',
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
    }

    # Setup authentication if not in production environment
    auth = None
    if environment != "PROD":
        auth = HTTPBasicAuth(wordpreess_staggin_username, wordpreess_staggin_password)

    # Create directory for saving images if it does not exist
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    # Open and read the local HTML file
    with open(f"dist/index.html", "r") as file:
        soup = BeautifulSoup(file, 'html.parser')

    # Find all image tags
    images = soup.find_all('img')

    # Loop through all images, download them, and update their src attributes
    for img in images:
        # Get the source attribute of the image
        img_url = img.get('src')
        if img_url:  # Check if the image has a source URL
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
            img['src'] = os.path.join('./',local_filename)

    # Write the updated HTML to a new file
    with open( f"dist/index.html" , 'w') as file:
        file.write(str(soup))

if __name__ == "__main__":
    print(sys.argv)
    if len(sys.argv) != 4:
        print("Usage: python wordpress-cloning-script.py <environment> <wordpreess_staggin_username> <wordpreess_staggin_password>")
        sys.exit(1)
    
    env = sys.argv[1]
    wordpreess_staggin_username = sys.argv[2]
    wordpreess_staggin_password = sys.argv[3]
    download_and_update_html(env, wordpreess_staggin_username, wordpreess_staggin_password)