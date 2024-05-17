import os


class GitHubWriter:
    def __init__(self):
        self.step_summary_path = os.getenv('GITHUB_STEP_SUMMARY')
        self.output_path = os.getenv('GITHUB_OUTPUT')

    def write_summary(self, content):
        if self.step_summary_path:
            with open(self.step_summary_path, 'a') as f:
                f.write(content)
        else:
            print(content)

    def write_output(self, key, value):
        if self.output_path:
            with open(self.output_path, 'a') as f:
                f.write(f"{key}={value}\n")
        else:
            print("GITHUB_OUTPUT not found. Printing to console:")
            print(f"{key}={value}")