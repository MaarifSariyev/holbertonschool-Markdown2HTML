#!/usr/bin/env python3

import sys
import os

def main():
    # Check for the correct number of arguments
    if len(sys.argv) < 3:
        print("Usage: ./markdown2html.py README.md README.html", file=sys.stderr)
        sys.exit(1)
    
    # Get the input and output file names
    input_file = sys.argv[1]
    output_file = sys.argv[2]

    # Check if the Markdown file exists
    if not os.path.exists(input_file):
        print(f"Missing {input_file}", file=sys.stderr)
        sys.exit(1)
    
    # If everything is fine, exit with code 0
    sys.exit(0)

if __name__ == "__main__":
    main()