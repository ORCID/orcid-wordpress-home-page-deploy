import os
import re
import requests
import shutil
from typing import Optional
from urllib.parse import urlparse, urlunparse, parse_qs
from urllib.parse import urljoin


def sanitize_filename(filename):
    # Replace non-English letters and spaces with underscores
    return re.sub(r'[^a-zA-Z0-9_.]', '_', filename)


def strip_query_params(url):
    parsed_url = urlparse(url)
    return urlunparse(parsed_url._replace(query=''))


def download_image_if_not_exists(full_img_url, headers, auth, env, writer, *, base_url: Optional[str] = None):
    """
    Downloads an image to ./dist/assets if missing, and returns the local filepath.

    - Supports absolute URLs (http/https) and protocol-relative URLs (//example.com/foo.png)
    - Supports site-relative URLs (/wp-content/uploads/foo.png) when base_url is provided
    - Supports relative URLs (wp-content/uploads/foo.png) when base_url is provided
    """
    if not full_img_url:
        return "./dist/assets/"

    # Resolve URL to an absolute URL when possible.
    if full_img_url.startswith("//"):
        full_img_url = "https:" + full_img_url
    elif full_img_url.startswith("/"):
        if base_url:
            full_img_url = urljoin(base_url, full_img_url)
        else:
            full_img_url = "https://" + full_img_url.lstrip("/")
    elif not full_img_url.startswith(("http://", "https://")):
        if base_url:
            full_img_url = urljoin(base_url, full_img_url)
        else:
            full_img_url = "https://" + full_img_url

    # Strip query parameters for filename sanitization only
    url_without_query = strip_query_params(full_img_url)

    # Determine the local file path
    local_dir = './dist/assets'
    if not os.path.exists(local_dir):
        os.makedirs(local_dir)
    sanitized_filename = sanitize_filename(os.path.basename(url_without_query))
    sanitized_filepath = os.path.join(local_dir, sanitized_filename)

    # Download and save the image if it doesn't exist locally
    if not os.path.exists(sanitized_filepath):
        try:
            img_data = requests.get(full_img_url, stream=True, headers=headers, auth=auth)
            if img_data.status_code != 200:
                writer.write_summary_and_fail_on_prod(f"- 🚨 Failed to download image: {full_img_url}, status code: {img_data.status_code}\n", env)
                return sanitized_filepath
            with open(sanitized_filepath, 'wb') as file:
                img_data.raw.decode_content = True
                shutil.copyfileobj(img_data.raw, file)
            writer.write_summary(f"- Successfully downloaded image: {full_img_url} \n")
        except requests.exceptions.MissingSchema:
            writer.write_summary_and_fail_on_prod(f"- Please use a full URL for {full_img_url}. \n", env)
        except Exception as e:
            writer.write_summary_and_fail_on_prod(f"Error: {str(e)}\n", env)
    else:
        writer.write_summary(f"- Image already exists: {sanitized_filepath}\n")
    
    return sanitized_filepath
