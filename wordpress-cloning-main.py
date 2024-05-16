import subprocess
import sys
import os
from pathlib import Path
import argparse

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
        return "false"
    else:
        run_command(f"git commit -m 'Cloned WordPress post {post_id} for environment {environment}'")
        run_command("git push")
        return "true"
    


def main():
    parser = argparse.ArgumentParser(description="Clone WordPress posts and optionally commit and push changes to GitHub.")
    parser.add_argument("environment", type=str, help="The target environment (QA or PROD)")
    parser.add_argument("post_id", type=str, help="The WordPress post ID to clone.")
    parser.add_argument("wordpress_username", type=str, help="WordPress username.")
    parser.add_argument("wordpress_password", type=str, help="WordPress password.")
    parser.add_argument("--commit", action="store_true", help="Commit and push changes to GitHub.")

    args = parser.parse_args()

    install_dependencies()
    run_script("wordpress-cloning-html-script.py", args.environment, args.post_id, args.wordpress_username, args.wordpress_password, "true")
    run_script("wordpress-cloning-css-script.py", args.environment, args.wordpress_username, args.wordpress_password)
    run_command("npm run wordpress-cloning-purgecss-script")
    run_command("node wordpress-cloning-inlinecss-script.js")
    run_script("wordpress-cloning-img-script.py", args.environment, args.wordpress_username, args.wordpress_password)

    should_run = "false"
    if args.commit:
        configure_git_user()
        should_run= commit_and_push_changes(args.post_id, args.environment)
    else:
        print("Skipping commit and push changes.")
        should_run = "true"
    
    try:
        with open(os.getenv("GITHUB_OUTPUT", "/github/workspace/output.txt"), "a") as f:
            f.write(f"should-run={should_run}\n")
    except:
        print("Not running in GitHub Actions.")
        sys.exit(1)

if __name__ == "__main__":
    main()