#!/usr/bin/python3
import sys
import os
import hashlib
import re

def md5_hash(content):
    """Generate the MD5 hash (lowercase) of the given content."""
    return hashlib.md5(content.encode('utf-8')).hexdigest()

def remove_c(content):
    """Remove all occurrences of 'c' (case insensitive) from the content."""
    return re.sub(r'(?i)c', '', content)

def parse_markdown(markdown_file):
    """Parses a Markdown file and converts headers, lists, paragraphs, bold, italic, MD5, and remove 'c' to HTML."""
    html_content = []
    in_list = False  # To track if we're currently in a list
    in_ordered_list = False  # To track if we're currently in an ordered list
    in_paragraph = False  # To track if we're currently in a paragraph
    paragraph_content = []  # To collect lines for the current paragraph

    with open(markdown_file, 'r') as file:
        for line in file:
            line = line.rstrip()  # Remove trailing spaces/newlines

            # Process [[Hello]] for MD5 hashing
            line = re.sub(r'\[\[(.*?)\]\]', lambda m: md5_hash(m.group(1)), line)

            # Process ((Hello Chicago)) for removing 'c'
            line = re.sub(r'\(\((.*?)\)\)', lambda m: remove_c(m.group(1)), line)

            # Parse bold and italic syntax for inline text
            line = line.replace("**", "<b>").replace("__", "<em>")

            # Check for header syntax
            if line.startswith("#"):
                # Handle any ongoing paragraph before starting a new header
                if in_paragraph:
                    html_content.append("<p>" + "<br/>".join(paragraph_content) + "</p>")
                    in_paragraph = False
                    paragraph_content = []
                
                level = line.count("#")
                if 1 <= level <= 6:
                    header_content = line.lstrip("#").strip()
                    html_content.append(f"<h{level}>{header_content}</h{level}>")
            
            # Check for unordered list item (starts with "- ")
            elif line.startswith("- "):
                # Close ongoing paragraph if it's open
                if in_paragraph:
                    html_content.append("<p>" + "<br/>".join(paragraph_content) + "</p>")
                    in_paragraph = False
                    paragraph_content = []
                if not in_list:
                    html_content.append("<ul>")
                    in_list = True
                list_item_content = line.lstrip("- ").strip()
                html_content.append(f"<li>{list_item_content}</li>")
            
            # Check for ordered list item (starts with "* ")
            elif line.startswith("* "):
                # Close ongoing paragraph if it's open
                if in_paragraph:
                    html_content.append("<p>" + "<br/>".join(paragraph_content) + "</p>")
                    in_paragraph = False
                    paragraph_content = []
                if not in_ordered_list:
                    html_content.append("<ol>")
                    in_ordered_list = True
                list_item_content = line.lstrip("* ").strip()
                html_content.append(f"<li>{list_item_content}</li>")
            
            # If the line is not empty and not part of a list or header, it's a paragraph line
            elif line:
                if not in_paragraph:
                    # Start a new paragraph
                    in_paragraph = True
                    paragraph_content = [line]
                else:
                    # Continue the paragraph
                    paragraph_content.append(line)
            
            # If the line is empty, close the ongoing paragraph
            else:
                if in_paragraph:
                    html_content.append("<p>" + "<br/>".join(paragraph_content) + "</p>")
                    in_paragraph = False
                    paragraph_content = []

        # Close any open paragraph or list at the end of the file
        if in_paragraph:
            html_content.append("<p>" + "<br/>".join(paragraph_content) + "</p>")
        if in_list:
            html_content.append("</ul>")
        if in_ordered_list:
            html_content.append("</ol>")

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
