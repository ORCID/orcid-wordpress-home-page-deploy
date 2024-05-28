import json
import os
import sys
import subprocess
from github_writer import GitHubWriter

# Get the version from the command line arguments
version = sys.argv[1]

# Initialize GitHubWriter
gh_writer = GitHubWriter()

try:
    # Path to the dist/index.html
    index_path = os.path.join('dist', 'index.html')

    # Path to the package.json
    package_json_path = 'package.json'

    # Update the version in package.json
    with open(package_json_path, 'r') as f:
        package_json = json.load(f)

    package_json['version'] = version

    with open(package_json_path, 'w') as f:
        json.dump(package_json, f, indent=2)

    # Read the index.html file
    with open(index_path, 'r') as f:
        data = f.read()

    # Add the version as a comment at the top of the file
    version_comment = f'<!-- Version: {version} -->\n'
    updated_data = version_comment + data

    # Write the updated data back to index.html
    with open(index_path, 'w') as f:
        f.write(updated_data)

    print('Version injected successfully!')
    gh_writer.write_summary(f"Version {version} injected into index.html and package.json")

    # Configure git user
    subprocess.run(['git', 'config', '--global', 'user.name', 'github-actions[bot]'])
    subprocess.run(['git', 'config', '--global', 'user.email', 'github-actions[bot]@users.noreply.github.com'])

    # Add the modified files
    subprocess.run(['git', 'add', index_path, package_json_path])

    # Commit the changes
    commit_message = f'Inject version {version} into index.html and update package.json'
    subprocess.run(['git', 'commit', '-m', commit_message])

    # Push the changes
    subprocess.run(['git', 'push'])

except Exception as e:
    error_message = f"Error while injecting version: {e}"
    gh_writer.write_summary_and_fail_on_prod(error_message, os.getenv('ENVIRONMENT', ''))
    sys.exit(1)