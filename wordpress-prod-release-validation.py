import requests
from bs4 import BeautifulSoup, Comment
import sys
import time
from urllib.parse import urljoin
from github_writer import GitHubWriter
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

def create_session_with_retries():
    session = requests.Session()
    retries = Retry(total=3, backoff_factor=1, status_forcelist=[500, 502, 503, 504])
    session.mount('http://', HTTPAdapter(max_retries=retries))
    session.mount('https://', HTTPAdapter(max_retries=retries))
    return session

def fetch_url(session, url):
    try:
        response = session.get(url, timeout=5)
        response.raise_for_status()
        return response
    except requests.exceptions.RequestException as e:
        return None

def validate_version(soup, version):
    comments = soup.find_all(string=lambda text: isinstance(text, Comment))
    version_comment = f"Version: {version}"
    for comment in comments:
        if version_comment in comment:
            return True
    return False

def validate_assets(url, version, github_writer, env):
    session = create_session_with_retries()
    response = fetch_url(session, url)
    
    if not response:
        github_writer.write_summary_and_fail(f"Failed to fetch {url}.", env)
        return False

    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Retry mechanism for validate_version
    max_retries = 5
    for attempt in range(max_retries):
        if validate_version(soup, version):
            break
        else:
            if attempt < max_retries - 1:
                github_writer.write_summary(f"Version {version} not found. Retrying... ({attempt + 1}/{max_retries})")
                time.sleep(5)
                response = fetch_url(session, url)
                if not response:
                    github_writer.write_summary_and_fail(f"Failed to fetch {url}.", env)
                    return False
                soup = BeautifulSoup(response.content, 'html.parser')
            else:
                github_writer.write_summary_and_fail(f"Version {version} not found in {url} after {max_retries} attempts.", env)
                return False
    
    # Collect all asset URLs
    assets = []
    assets.extend([img['src'] for img in soup.find_all('img') if 'src' in img.attrs])
    assets.extend([link['href'] for link in soup.find_all('link', rel='stylesheet') if 'href' in link.attrs])
    assets.extend([script['src'] for script in soup.find_all('script') if 'src' in script.attrs])
    
    all_assets_valid = True
    failed_assets = []

    for asset in assets:
        asset_url = urljoin(url, asset)
        if not fetch_url(session, asset_url):
            failed_assets.append(asset_url)
            all_assets_valid = False

    if failed_assets:
        for failed_asset in failed_assets:
            github_writer.write_summary(f"Failed to fetch asset {failed_asset}.", env)
    return all_assets_valid

def main():
    if len(sys.argv) != 3:
        print("Usage: python validate_assets.py <environment> <version>", file=sys.stderr)
        sys.exit(1)

    env = sys.argv[1]
    version = sys.argv[2]
    urls = {
        "QA": "https://homepage-qa.orcid.org/index.html",
        "FALLBACK": "https://homepage-fallback.orcid.org/index.html",
        "PROD": "https://homepage-prod.orcid.org/index.html"
    }

    next_environment_to_be_deployed = {
        "QA": "FALLBACK",
        "FALLBACK": "PROD",
        "PROD": False
    }

    if env not in urls:
        print(f"Unknown environment: {env}", file=sys.stderr)
        sys.exit(1)

    url = urls[env]
    github_writer = GitHubWriter()

    if validate_assets(url, version, github_writer, env):
        github_writer.write_summary(f"All assets are correctly loaded and version {version} is present for {env}.")
        github_writer.write_summary(f"Please check the [{env} deployed homepage]({urls[env]}) for any issues.")
        if next_environment_to_be_deployed[env]:
            github_writer.write_summary(f"Once this deployed has been validated please pesss the button 'Review deployments' to deploy {next_environment_to_be_deployed[env]}.")
        else:
            github_writer.write_summary("All environments have been deployed.")
    else:
        github_writer.write_summary(f"Some assets failed to load or version {version} is missing for {env} environment.", env)
        sys.exit(1)

if __name__ == "__main__":
    main()
