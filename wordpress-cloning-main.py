import subprocess
import sys
import os
from pathlib import Path
import argparse
from github_writer import GitHubWriter

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
    parser.add_argument("--dry-run", action="store_true", help="Commit and push changes to GitHub.")

    run_command("rm -rf dist")
    Path("dist").mkdir(parents=True, exist_ok=True)
    
    install_dependencies()

    args = parser.parse_args()

    writer = GitHubWriter()
    
    writer.write_summary("# Cloning Wordpress HomePage Summary:\n")

    # Print the markdown table
    writer.write_summary("## Running arguments:\n")
    writer.write_summary("| Variable      | Value         | \n")
    writer.write_summary("| ------------- | ------------- | \n")
    writer.write_summary(f"| Environment   | {args.environment} | \n")
    writer.write_summary(f"| Post ID       | {args.post_id}     | \n")

    writer.write_summary("## Clone JS script:\n")
    run_script("wordpress-cloning-js-script.py", args.environment, args.wordpress_username, args.wordpress_password)

    writer.write_summary("## HTML cloning script:\n")
    run_script("wordpress-cloning-html-script.py", args.environment, args.post_id, args.wordpress_username, args.wordpress_password, "true")
    
    writer.write_summary("## CSS cloning script:\n")
    run_script("wordpress-cloning-css-script.py", args.environment, args.wordpress_username, args.wordpress_password)

    writer.write_summary("## purgecss script:\n")
    run_command("node wordpress-cloning-purgecss-script.js")

    writer.write_summary("## CSS prefixing:\n")
    run_script("wordpress-cloning-css-prefixer-script.py")
    
    writer.write_summary("## Clone images in HTML script:\n")
    run_script("wordpress-cloning-img-in-html-script.py", args.environment, args.wordpress_username, args.wordpress_password)

    writer.write_summary("## Clone images in CSS script:\n")
    run_script("wordpress-cloning-img-in-css-script.py", args.environment, args.wordpress_username, args.wordpress_password)

    writer.write_summary("## Version control changes \n")
    if args.environment == 'PROD' and args.dry_run == False:
        configure_git_user()

        try:
            changes_commmited = commit_and_push_changes(args.post_id, args.environment)
            if (changes_commmited == "true"):
                writer.write_summary(f"- Changes committed and pushed for post {args.post_id} in environment {args.environment}.\n")
            else:
                writer.write_summary("- No changes found when compare to the last run.\n")
                writer.write_output("script-succes", "false")
                raise

        except Exception as e:
            writer.write_summary(f"- 🚨 Error occurred while trying to commit and push changes. \n Error: {e}\n")
            writer.write_output("script-succes", "false")
            raise
            

    elif args.dry_run == True:
        writer.write_summary("- Skipping commit and push changes for dry-run\n")
        writer.write_output("script-succes", "true")

    else:
        writer.write_summary("- Skipping commit and push changes for not PROD environments\n")
        writer.write_output("script-succes", "true")
    
    

if __name__ == "__main__":
    main()