import os
import re
import requests
import shutil


def sanitize_filename(filename):
    # Replace non-English letters and spaces with underscores
    return re.sub(r'[^a-zA-Z0-9_.]', '_', filename)


def download_image_if_not_exists(full_img_url, local_filepath, headers, auth, env, writer):
    # Ensure the URL has a protocol
    if full_img_url.startswith("//"):
        full_img_url = "https:" + full_img_url
    elif not full_img_url.startswith(("http://", "https://")):
        full_img_url = "https://" + full_img_url

    # Sanitize the local file path
    local_dir, local_filename = os.path.split(local_filepath)
    sanitized_filename = sanitize_filename(local_filename)
    sanitized_filepath = os.path.join(local_dir, sanitized_filename)

    # Download and save the image if it doesn't exist locally
    if not os.path.exists(sanitized_filepath):
        try:
            img_data = requests.get(full_img_url, stream=True, headers=headers, auth=auth)
            if img_data.status_code != 200:
                writer.write_summary_and_fail_on_prod(f"- 🚨 Failed to download image: {full_img_url}, status code: {img_data.status_code}\n", env)
                return
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