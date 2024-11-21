import sys
import os

def main():
    # Check for the correct number of arguments
    if len(sys.argv) < 3:
        print("Usage: ./markdown2html.py README.md README.html", file=sys.stderr)
        sys.exit(1)

    markdown_file = sys.argv[1]
    output_file = sys.argv[2]

    # Check if the markdown file exists
    if not os.path.exists(markdown_file):
        print(f"Missing {markdown_file}", file=sys.stderr)
        sys.exit(1)

    # Proceed with processing the markdown file here...
    # (The rest of your code for parsing the markdown file and generating the HTML)

if __name__ == "__main__":
    main()
