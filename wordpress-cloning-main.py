import subprocess
import sys
import os
from pathlib import Path

def install_dependencies():
    subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])
    subprocess.check_call([sys.executable, "-m", "pip", "install", "requests", "beautifulsoup4", "tqdm"])

def run_script(script_name, *args):
    script_path = Path(script_name).resolve()
    subprocess.check_call([sys.executable, str(script_path), *args])

def run_command(command):
    subprocess.check_call(command, shell=True)

def configure_git_user():
    run_command("git config user.name 'GitHub Actions'")
    run_command("git config user.email 'actions@github.com'")

def commit_and_push_changes(post_id, environment):
    run_command("git add .")
    result = subprocess.run("git diff --staged --quiet", shell=True)
    if result.returncode == 0:
        print("No changes to commit.")
        should_run = "false"
    else:
        run_command(f"git commit -m 'Cloned WordPress post {post_id} for environment {environment}'")
        run_command("git push")
        should_run = "true"
    
    with open(os.getenv("GITHUB_OUTPUT", "/github/workspace/output.txt"), "a") as f:
        f.write(f"should-run={should_run}\n")

def main():
    environment = sys.argv[1]
    post_id = sys.argv[2]
    wordpress_username = sys.argv[3]
    wordpress_password = sys.argv[4]

    install_dependencies()
    run_script("wordpress-cloning-html-script.py", environment, post_id, wordpress_username, wordpress_password, "true")
    run_script("wordpress-cloning-css-script.py", environment, wordpress_username, wordpress_password)
    run_command("npm run wordpress-cloning-purgecss-script")
    run_command("node wordpress-cloning-inlinecss-script.js")
    run_script("wordpress-cloning-img-script.py", environment, wordpress_username, wordpress_password)
    configure_git_user()
    commit_and_push_changes(post_id, environment)

if __name__ == "__main__":
    main()