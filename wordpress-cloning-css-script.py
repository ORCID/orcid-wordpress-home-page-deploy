import sys
import requests
from requests.auth import HTTPBasicAuth

def clone_css_files(environment, wordpress_staggin_username, wordpress_staggin_password):
    # Define the base URL based on the environment
    base_url = "https://info.qa.orcid.org/" if environment != "PROD" else "https://info.orcid.org/"
    
    # URLs to clone
    css_urls = [
        f"{base_url}wp-content/themes/orcid-outreach-pro/style.css",
        f"{base_url}wp-includes/css/dist/block-library/style.css",
        f"{base_url}wp-content/plugins/genesis-blocks/dist/style-blocks.build.css",
        f"{base_url}wp-content/uploads/theplus_gutenberg/theplus-post-25163.min.css",
        f"{base_url}wp-content/uploads/theplus_gutenberg/plus-global.css",
        f"{base_url}wp-content/uploads/theplus_gutenberg/plus-css-25163.css",
        f"{base_url}wp-content/plugins/elementor/assets/css/frontend-msie.min.css",
    ]
    
    # Set up authentication if not in production environment
    auth = None
    if environment != "PROD":
        auth = HTTPBasicAuth(wordpress_staggin_username, wordpress_staggin_password)

    # Headers for the request
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
    }

   # Open file to write CSS content
    with open('dist/combined_styles.css', 'w') as file:
        for url in css_urls:
            response = requests.get(url, headers=headers, auth=auth)
            if response.status_code == 200:
                file.write(f"/* CSS from {url} */\n")
                file.write(response.text + "\n\n")
                print(f"Successfully added CSS from {url} to combined_styles.css")
            else:
                print(f"Failed to fetch {url}: HTTP {response.status_code}")

if __name__ == "__main__":
    print(sys.argv)
    if len(sys.argv) != 4:
        print("Usage: python css-cloning-script.py <environment> <wordpress_staggin_username> <wordpress_staggin_password>")
        sys.exit(1)
    
    env = sys.argv[1]
    wordpress_staggin_username = sys.argv[2]
    wordpress_staggin_password = sys.argv[3]
    clone_css_files(env, wordpress_staggin_username, wordpress_staggin_password)