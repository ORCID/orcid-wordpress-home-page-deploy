import requests
from bs4 import BeautifulSoup
import sys

def validate_assets(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Failed to fetch {url}: {e}", file=sys.stderr)
        return False

    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Collect all asset URLs
    assets = []
    
    # Find image sources
    assets.extend([img['src'] for img in soup.find_all('img') if 'src' in img.attrs])
    
    # Find CSS references
    assets.extend([link['href'] for link in soup.find_all('link', rel='stylesheet') if 'href' in link.attrs])
    
    # Find JavaScript sources
    assets.extend([script['src'] for script in soup.find_all('script') if 'src' in script.attrs])
    
    all_assets_valid = True
    for asset in assets:
        asset_url = url + asset if asset.startswith('/') else asset
        try:
            asset_response = requests.get(asset_url)
            asset_response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"Failed to fetch asset {asset_url}: {e}", file=sys.stderr)
            all_assets_valid = False

    return all_assets_valid

def main():
    if len(sys.argv) != 2:
        print("Usage: python validate_assets.py <environment>", file=sys.stderr)
        sys.exit(1)

    env = sys.argv[1]
    urls = {
        "QA": "https://d3055hwma3riwo.cloudfront.net/index.html",
        "FALLBACK": "https://d1kh89kum7j2ji.cloudfront.net/index.html",
        "PROD": "https://d25yxmpntoa26z.cloudfront.net/index.html"
    }

    if env not in urls:
        print(f"Unknown environment: {env}", file=sys.stderr)
        sys.exit(1)

    url = urls[env]
    print(f"Validating assets for {env} environment at {url}...")
    if validate_assets(url):
        print(f"All assets are correctly loaded for {env} environment.")
    else:
        print(f"Some assets failed to load for {env} environment.", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()