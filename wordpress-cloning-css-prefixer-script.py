import cssutils
from github_writer import GitHubWriter

def process_rule(rule, writer):
    new_selector_list = []
    for selector in rule.selectorList:
        try:
            if selector.selectorText == ":root":
                new_selector_list.append(f'{selector.selectorText} .homepage')
            elif selector.selectorText == "body":
                new_selector_list.append(f"#main.homepage")
            elif selector.selectorText.startswith('.homepage'):
                new_selector_list.append(f'#main.homepage {selector.selectorText[len(".homepage"):]}')
            else:
                new_selector_list.append(f'.homepage {selector.selectorText}')
        except Exception as e:
            message = f"Error processing selector '{selector.selectorText}': {e}"
            writer.write_summary(message)
    rule.selectorText = ', '.join(new_selector_list)

def update_css(file_path):
    writer = GitHubWriter()
    try:
        # Read the CSS file
        with open(file_path, 'r') as file:
            css_content = file.read()

        # Parse the CSS
        parser = cssutils.CSSParser(raiseExceptions=False)
        sheet = parser.parseString(css_content)

        # Iterate over the CSS rules
        for rule in sheet:
            if rule.type == rule.STYLE_RULE:
                process_rule(rule, writer)
            elif rule.type == rule.MEDIA_RULE:
                for r in rule.cssRules:
                    if r.type == r.STYLE_RULE:
                        process_rule(r, writer)

        # Serialize the updated CSS
        updated_css = sheet.cssText.decode('utf-8')

        # Write the updated CSS back to the file
        with open(file_path, 'w') as file:
            file.write(updated_css)

        writer.write_summary("CSS file successfully updated.")
        writer.write_output("script-success", "true")

    except Exception as e:
        message = f"Error updating CSS file: {e}"
        writer.write_summary(message)
        writer.write_output("script-success", "false")
        raise

if __name__ == "__main__":
    writer = GitHubWriter()
    try:
        update_css('dist/wordpress-homepage.css')
    except Exception as e:
        message = f"Fatal error: {e}"
        writer.write_summary(message)
        writer.write_output("script-success", "false")
        sys.exit(1)
