import sys
import requests
from requests.auth import HTTPBasicAuth
from bs4 import BeautifulSoup
import re


def clone_css_files(environment, wordpress_staging_username, wordpress_staging_password):
    # Define the base URL based on the environment
    base_url = "https://info.qa.orcid.org/" if environment != "PROD" else "https://info.orcid.org/"
    
    # URLs to clone (including both HTML and CSS)
    css_urls = [
        f"{base_url}wp-content/themes/orcid-outreach-pro/style.css",
        f"{base_url}wp-includes/css/dist/block-library/style.css",
        f"{base_url}wp-content/plugins/genesis-blocks/dist/style-blocks.build.css",
        f"{base_url}wp-content/uploads/theplus_gutenberg/theplus-post-25163.min.css",
        f"{base_url}wp-content/uploads/theplus_gutenberg/plus-global.css",
        f"{base_url}wp-content/uploads/theplus_gutenberg/plus-css-25163.css",
        f"{base_url}/wp-content/themes/orcid-outreach-pro/homepage.css"
         f"{base_url}",  # This will clone the inline CSS on wordpress
    ]
    
    # Set up authentication if not in production environment
    auth = None
    if environment != "PROD":
        auth = HTTPBasicAuth(wordpress_staging_username, wordpress_staging_password)

    # Headers for the request
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
    }

    # Open file to write CSS content
    with open('dist/combined_styles.css', 'w') as file:
        # Loop through each URL
        for url in css_urls:
            if url.endswith('.css'):  # If it's a CSS file
                response = requests.get(url, headers=headers, auth=auth)
                if response.status_code == 200:
                    file.write(f"/* CSS from {url} */\n")
                    data = response.text
                    # Remove css issues on the original CSS
                    data = re.sub(r'@charset "UTF-8";\s*', '', response.text)
                    data = re.sub(r'\*/\s*/\* ROB 10/07/22', '/* ROB 10/07/22', data)

                    # Remove the error with the original CSS
                    print(f"Successfully added CSS from {url} to combined_styles.css")
                    
                    file.write(data + "\n\n")
                    print(f"Successfully added CSS from {url} to combined_styles.css")
                else:
                    print(f"Failed to fetch {url}: HTTP {response.status_code}")
            else:  # If it's an HTML file
                response = requests.get(url, headers=headers, auth=auth)
                if response.status_code == 200:
                    # Extract inline CSS from HTML
                    soup = BeautifulSoup(response.text, 'html.parser')
                    inline_styles = soup.find_all('style')
                    for style in inline_styles:
                        if (style and style.string): 
                            file.write("/* Inline CSS from HTML */\n")
                            file.write(style.string.strip() + "\n\n")
                    print(f"Successfully added inline CSS from HTML {url} to combined_styles.css")
                else:
                    print(f"Failed to fetch {url}: HTTP {response.status_code}")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python css-cloning-script.py <environment> <wordpress_staging_username> <wordpress_staging_password>")
        sys.exit(1)
    
    env = sys.argv[1]
    wordpress_staging_username = sys.argv[2]
    wordpress_staging_password = sys.argv[3]


    clone_css_files(env, wordpress_staging_username, wordpress_staging_password)