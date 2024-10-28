#!/usr/bin/python3
"""
This script reads stdin line by line and output its result
"""

import re
import pathlib
import argparse


def convert_md_to_html(input_file, output_file):
    '''
    This converts markdown file to HTML file
    '''
    # This will read the content of the input file
    with open(input_file, encoding='utf-8') as w:
        mkdwn_content = w.readlines()

    html_file = []
    for line in mkdwn_content:
        # Check if the line is a heading line
        match = re.match(r'(#){1,6} (.*)', line)
        if match:
            # get th header level
            h_level = len(match.group(1))
            # Get the contents of the heading
            h_content = match.group(2)
            # The append the HTML equivalent of the heading
            html_file.append(f'<h{h_level}>{h_content}</h{h_level}>\n')
        else:
            html_file.append(line)

            # Write the HTML content to the stdout
    with open(output_file, 'w', encoding='utf-8') as f:
        f.writelines(html_file)

if __name__ == '__main__':
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description='Convert markdown to HTML')
    parser.add_argument('input_file', help='path to input markdown file')
    parser.add_argument('output_file', help='path to output HTML file')
    args = parser.parse_args()

    # Check if the input file exists
    input_path = pathlib.Path(args.input_file)
    if not input_path.is_file():
        print(f'Missing {input_path}', file=sys.stderr)
        sys.exit(1)

    # Convert the markdown file to HTML
    convert_md_to_html(args.input_file, args.output_file)
