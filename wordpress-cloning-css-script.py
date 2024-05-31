import sys
import requests
from requests.auth import HTTPBasicAuth
from bs4 import BeautifulSoup
import re
from github_writer import GitHubWriter

def clone_css_files(environment, wordpress_staging_username, wordpress_staging_password):
    writer = GitHubWriter()

    base_url = "https://info.qa.orcid.org/" if environment != "PROD" else "https://info.orcid.org/"
    
    css_urls = [
        f"{base_url}homepage-as-post",
        f"{base_url}",  # This will clone the inline CSS on wordpress
        f"{base_url}wp-content/themes/orcid-outreach-pro/style.css",
        f"{base_url}wp-includes/css/dist/block-library/style.css",
        f"{base_url}wp-content/plugins/genesis-blocks/dist/style-blocks.build.css",
        f"{base_url}wp-content/uploads/theplus_gutenberg/theplus-post-25422.min.css",
        f"{base_url}wp-content/uploads/theplus_gutenberg/plus-global.css",
        f"{base_url}wp-content/uploads/theplus_gutenberg/plus-css-25422.css",
        f"{base_url}wp-content/themes/orcid-outreach-pro/homepage.css",
        f"{base_url}wp-content/uploads/maxmegamenu/style.css",
        
    ]
    
    auth = None
    if environment != "PROD":
        auth = HTTPBasicAuth(wordpress_staging_username, wordpress_staging_password)

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
    }


    with open('dist/wordpress-homepage.css', 'w') as file:      
        for url in css_urls:
            try:
                if not url.endswith('.css'):
                    response = requests.get(url, headers=headers, auth=auth)
                    if response.status_code == 200:
                        soup = BeautifulSoup(response.text, 'html.parser')
                        inline_styles = soup.find_all('style')
                        for style in inline_styles:
                            if style and style.string:
                                file.write("/* Inline CSS from HTML */\n")
                                file.write(style.string.strip() + "\n\n")
                        message = f"Successfully added inline CSS from HTML {url}"
                        writer.write_summary(f"- {message}\n")
                    else:
                        message = f"Skipping  {url}: HTTP {response.status_code}"
                        writer.write_summary(f"- {message}\n")
                else:
                    response = requests.get(url, headers=headers, auth=auth)
                    if response.status_code == 200:
                        file.write(f"/* CSS from {url} */\n")
                        data = response.text
                        data = re.sub(r'@charset "UTF-8";\s*', '', data)
                        data = re.sub(r'\*/\s*/\* ROB 10/07/22', '/* ROB 10/07/22', data)
                        file.write(data + "\n\n")
                        message = f"Successfully added CSS from {url}"
                        writer.write_summary(f"- {message}\n")
                    else:
                        message = f"Skipping  {url}: HTTP {response.status_code}"
                        writer.write_summary(f"- {message}\n")

            except requests.exceptions.RequestException as e:
                message = f"Skipping {url}. \n Error: {e}"
                writer.write_summary(f"- {message}\n")
                


if __name__ == "__main__":
    writer = GitHubWriter()
    try:
        if len(sys.argv) != 4:
            raise ValueError("Usage: python css-cloning-script.py <environment> <wordpress_staging_username> <wordpress_staging_password>")
        
        env = sys.argv[1]
        wordpress_staging_username = sys.argv[2]
        wordpress_staging_password = sys.argv[3]

        clone_css_files(env, wordpress_staging_username, wordpress_staging_password)
    except Exception as e:
        message = f"Error: {str(e)}"
        writer.write_summary(f"{message}\n")
        writer.write_output("script-success", "false")
        sys.exit(1)