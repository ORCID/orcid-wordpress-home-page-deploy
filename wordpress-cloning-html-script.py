import sys
import requests
from requests.auth import HTTPBasicAuth


def main(environment, post_id, wordpreess_staggin_username, wordpreess_staggin_password):
    # Define the base URL based on the environment
    base_url = "https://info.qa.orcid.org/" if environment != "PROD" else "https://info.orcid.org/"
    headers = {
        'Accept': 'application/json',
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
    }

    # Setup authentication if not in production environment
    auth = None
    if environment != "PROD":
        auth = HTTPBasicAuth(wordpreess_staggin_username, wordpreess_staggin_password)

    # Make the request with or without authentication based on the environment
    response = requests.get(f"{base_url}wp-json/wp/v2/pages/{post_id}", headers=headers, auth=auth)

    with open(f"dist/index.html", "w") as file:
        file.write("<doctype html><html><head><link rel=\"stylesheet\" href=\"./combined_styles.css\"></head><body>")

        if response.status_code == 200:
            html_content = response.json()["content"]["rendered"]
            file.write(html_content)
            print(f"Successfully cloned post {post_id} to {post_id}.html")
        else:
            print(f"Failed to fetch post: {response}")
    
        file.write("</body></html>")



if __name__ == "__main__":
    print(sys.argv)
    if len(sys.argv) != 5:
        print("Usage: python wordpress-cloning-script.py <environment> <postID> <wordpreess_staggin_username> <wordpreess_staggin_password>")
        sys.exit(1)
    
    env = sys.argv[1]
    post_id = sys.argv[2]
    wordpreess_staggin_username = sys.argv[3]
    wordpreess_staggin_password = sys.argv[4]
    main(env, post_id, wordpreess_staggin_username, wordpreess_staggin_password)