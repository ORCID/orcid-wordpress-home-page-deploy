import sys
import requests
from requests.auth import HTTPBasicAuth
from github_writer import GitHubWriter

def fetch_and_write_js(url, file, headers, auth, writer):
    try:
        response = requests.get(url, headers=headers, auth=auth)
        if response.status_code == 200:
            file.write(f"/* JS from {url} */\n")
            file.write(response.text + "\n\n")
            message = f"Successfully added JS from {url}"
            writer.write_summary(f"- {message}\n")
        else:
            message = f"Skipping {url}: HTTP {response.status_code}"
            writer.write_summary(f"- {message}\n")
    except requests.exceptions.RequestException as e:
        message = f"Skipping {url}. \n Error: {e}"
        writer.write_summary(f"- {message}\n")

def download_js_files(environment, wordpress_staging_username, wordpress_staging_password):
    writer = GitHubWriter()

    base_url = "https://info.qa.orcid.org/" if environment != "PROD" else "https://info.orcid.org/"
    
    js_urls = [
        f"{base_url}wp-includes/js/jquery/jquery.min.js",
        f"{base_url}wp-includes/js/jquery/jquery-migrate.min.js",
        f"{base_url}wp-content/uploads/theplus_gutenberg/theplus-post-25422.min.js",
        # Add more JS URLs as needed
    ]

    auth = None
    if environment != "PROD":
        auth = HTTPBasicAuth(wordpress_staging_username, wordpress_staging_password)

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
    }

    with open('dist/wordpress-homepage.js', 'w') as file:
        for url in js_urls:
            fetch_and_write_js(url, file, headers, auth, writer)

if __name__ == "__main__":
    writer = GitHubWriter()
    try:
        if len(sys.argv) != 4:
            raise ValueError("Usage: python js-cloning-script.py <environment> <wordpress_staging_username> <wordpress_staging_password>")
        
        env = sys.argv[1]
        wordpress_staging_username = sys.argv[2]
        wordpress_staging_password = sys.argv[3]

        download_js_files(env, wordpress_staging_username, wordpress_staging_password)
    except Exception as e:
        message = f"Error: {str(e)}"
        writer.write_summary(f"{message}\n")
        writer.write_output("script-success", "false")
        sys.exit(1)