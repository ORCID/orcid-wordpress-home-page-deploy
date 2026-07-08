import os
import re
import requests
import shutil
from typing import Optional
from urllib.parse import urlparse, urlunparse, parse_qs
from urllib.parse import urljoin
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

_session = None


def _get_session():
    # Shared session with retries: WP Engine rate-limits bursts of image
    # downloads with 429s, so back off and honor Retry-After instead of
    # failing on the first response.
    global _session
    if _session is None:
        _session = requests.Session()
        retries = Retry(
            total=5,
            backoff_factor=2,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["GET"],
            raise_on_status=False,
        )
        _session.mount('http://', HTTPAdapter(max_retries=retries))
        _session.mount('https://', HTTPAdapter(max_retries=retries))
    return _session


def sanitize_filename(filename):
    # Replace non-English letters and spaces with underscores
    return re.sub(r'[^a-zA-Z0-9_.]', '_', filename)


def strip_query_params(url):
    parsed_url = urlparse(url)
    return urlunparse(parsed_url._replace(query=''))


def download_image_if_not_exists(full_img_url, headers, auth, env, writer, *, base_url: Optional[str] = None):
    """
    Downloads an image to ./dist/assets if missing, and returns the local filepath.

    Returns None when the download fails. Callers must not rewrite references
    for a None result — otherwise HTML/CSS ends up pointing at files that do
    not exist in dist/assets.

    - Supports absolute URLs (http/https) and protocol-relative URLs (//example.com/foo.png)
    - Supports site-relative URLs (/wp-content/uploads/foo.png) when base_url is provided
    - Supports relative URLs (wp-content/uploads/foo.png) when base_url is provided
    """
    if not full_img_url:
        return None

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
            img_data = _get_session().get(full_img_url, stream=True, headers=headers, auth=auth, timeout=30)
            if img_data.status_code != 200:
                writer.write_error(f"Failed to download image after retries: {full_img_url}, status code: {img_data.status_code}")
                return None
            with open(sanitized_filepath, 'wb') as file:
                img_data.raw.decode_content = True
                shutil.copyfileobj(img_data.raw, file)
            writer.write_summary(f"- Successfully downloaded image: {full_img_url} \n")
        except requests.exceptions.RequestException as e:
            writer.write_error(f"Failed to download image: {full_img_url}, error: {e}")
            return None
        except Exception as e:
            writer.write_error(f"Failed to save image: {full_img_url}, error: {e}")
            return None
    else:
        writer.write_summary(f"- Image already exists: {sanitized_filepath}\n")

    return sanitized_filepath
