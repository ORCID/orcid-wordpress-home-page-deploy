import sys
import requests
from requests.auth import HTTPBasicAuth
from github_writer import GitHubWriter

# Language dictionary
language_dict = {
    "en": "",
    "ar": "ar",
    "cs": "cs",
    "de": "de",
    "es": "es",
    "fr": "fr",
    "it": "it",
    "ja": "ja",
    "ko": "ko",
    "pl": "pl",
    "pt": "pt",
    "ru": "ru",
    "tr": "tr",
    "zh-CN": "zh-CN",
    "zh-TW": "zh-TW"
}

def main(environment, post_id, wordpress_staging_username, wordpress_staging_password, language):
    writer = GitHubWriter()
    base_url = "https://info.qa.orcid.org/" if environment != "PROD" else "https://info.orcid.org/"
    if language:
        base_url = f"{base_url}{language}/"
    headers = {
        'Accept': 'application/json',
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
    }

    auth = None
    if environment != "PROD":
        auth = HTTPBasicAuth(wordpress_staging_username, wordpress_staging_password)
    
    file_path = f"dist/index{'' if language == '' else '-' + language}.html"

    try:
        response = requests.get(f"{base_url}wp-json/wp/v2/pages/{post_id}", headers=headers, auth=auth)
        response.raise_for_status()

        with open(file_path, "w") as file:
            file.write("<!doctype html><html><head><link rel=\"stylesheet\" href=\"./combined_styles.css\"></head><body>")
            html_content = response.json()["content"]["rendered"]
            file.write(html_content)
            file.write("</body></html>")
        
        message = f"Successfully cloned post {post_id} to {file_path}"
        writer.write_summary(f"- {message}\n")

    except requests.exceptions.RequestException as e:
        message = f"Failed to fetch post {post_id} from {base_url}. Error: {e}"
        writer.write_summary(f"- {message}\n")
        writer.write_output("script-success", "false")
        raise

if __name__ == "__main__":
    writer = GitHubWriter()
    try:
        if len(sys.argv) != 6:
            raise ValueError("Usage: python wordpress-cloning-script.py <environment> <postID> <wordpress_staging_username> <wordpress_staging_password> <include_languages>")
        
        env = sys.argv[1]
        post_id = sys.argv[2]
        wordpress_staging_username = sys.argv[3]
        wordpress_staging_password = sys.argv[4]
        include_languages = sys.argv[5]

        success = True
        if include_languages == "true":
            for key, value in language_dict.items():
                try:
                    main(env, post_id, wordpress_staging_username, wordpress_staging_password, value)
                except Exception:
                    success = False
        else:
            try:
                main(env, post_id, wordpress_staging_username, wordpress_staging_password, include_languages)
            except Exception:
                success = False

        if success:
            writer.write_output("script-success", "true")
        else:
            writer.write_output("script-success", "false")
            sys.exit(1)

    except Exception as e:
        message = f"Error: {str(e)}"
        writer.write_summary(f"{message}\n")
        writer.write_output("script-success", "false")
        sys.exit(1)