import sys
import requests

def main(environment, post_id):
    base_url = "https://info.qa.orcid.org/" if environment == "QA" else "https://info.orcid.org/"
    headers = {'Accept': 'application/json',     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"}

    response = requests.get(f"{base_url}wp-json/wp/v2/posts/{post_id}", headers=headers)
    print(f"Fetching post {post_id} from {base_url}wp-json/wp/v2/posts/{post_id}")
    if response.status_code == 200:
        html_content = response.json()["content"]["rendered"]
        with open(f"{post_id}.html", "w") as file:
            file.write(html_content)
        print(f"Successfully cloned post {post_id} to {post_id}.html")
    else:
        print(f"Failed to fetch post: {response}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python wordpress-cloning-script.py <environment> <postID>")
        sys.exit(1)
    
    env = sys.argv[1]
    post_id = sys.argv[2]
    main(env, post_id)