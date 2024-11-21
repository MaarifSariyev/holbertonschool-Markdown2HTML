#!/usr/bin/python3
import sys
import os

def parse_markdown(markdown_file):
    """Parses a Markdown file and converts headers to HTML."""
    html_content = []
    
    with open(markdown_file, 'r') as file:
        for line in file:
            line = line.rstrip()  # Remove trailing spaces/newlines
            
            # Check for header syntax
            if line.startswith("#"):
                # Count the number of # symbols to determine the heading level
                level = line.count("#")
                if 1 <= level <= 6:
                    # Strip the # characters and surrounding spaces, then wrap in the correct HTML tag
                    header_content = line.lstrip("#").strip()
                    html_content.append(f"<h{level}>{header_content}</h{level}>")
            else:
                # If not a header, we can append the line as it is (optional)
                # For now we skip non-header lines, but this can be expanded later
                pass
    
    return html_content

def main():
    if len(sys.argv) < 3:
        print("Usage: ./markdown2html.py README.md README.html", file=sys.stderr)
        sys.exit(1)

    markdown_file = sys.argv[1]
    output_file = sys.argv[2]

    # Check if the markdown file exists
    if not os.path.exists(markdown_file):
        print(f"Missing {markdown_file}", file=sys.stderr)
        sys.exit(1)

    # Parse the markdown file to generate HTML content
    html_content = parse_markdown(markdown_file)

    # Write the HTML content to the output file
    with open(output_file, 'w') as file:
        for line in html_content:
            file.write(line + "\n")

    # Exit successfully
    sys.exit(0)

if __name__ == "__main__":
    main()
