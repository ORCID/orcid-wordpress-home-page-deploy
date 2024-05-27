import os


class GitHubWriter:
    def __init__(self):
        self.step_summary_path = os.getenv('GITHUB_STEP_SUMMARY')
        self.output_path = os.getenv('GITHUB_OUTPUT')

    def write_summary(self, content):
        print("> ", content)
        if self.step_summary_path:
            with open(self.step_summary_path, 'a') as f:
                f.write(content)

    def write_summary_and_fail_on_prod(self, content, env):
        print("> ", content)
        print(" ⚠️ WARNING: This error will fail for a prod build ⚠️")
        if self.step_summary_path:
            with open(self.step_summary_path, 'a') as f:
                f.write(content)
                f.write('\n ⚠️ WARNING: This error will fail for a prod build ⚠️\n')

        if env == "PROD":
            self.write_output("script-success", "false")
            raise

    def write_summary_and_fail(self, content, env):
        print("> ", content)
        if self.step_summary_path:
            with open(self.step_summary_path, 'a') as f:
                f.write(content)

        self.write_output("script-success", "false")
        raise 


            



    def write_output(self, key, value):
        print("GITHUB_OUTPUT:")
        print(f"{key}={value}")
        if self.output_path:
            with open(self.output_path, 'a') as f:
                f.write(f"{key}={value}\n")