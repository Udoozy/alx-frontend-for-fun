#!/usr/bin/python3
"""
This script reads stdin line by line and outputs HTML equivalent
"""

import re
import pathlib
import argparse
import hashlib

def convert_md_to_html(input_file, output_file):
    '''
    Converts a markdown file to an HTML file
    '''
    # Read the content of the input file
    with open(input_file, encoding='utf-8') as w:
        mkdwn_content = w.readlines()

    html_file = []
    in_list = False

    for line in mkdwn_content:
        line = line.strip()

        #heading convertion
        match = re.match(r'^(#{1,6}) (.*)', line)
        if match:
            h_level = len(match.group(1))
            h_content = match.group(2)
            html_file.append(f'<h{h_level}>{h_content}</h{h_level}>\n')
            continue

        # List items conversion
        if line.startswith('- '):
            if not in_list:
                html_file.append('<ul>\n')
                in_list = True
            list_content = line[2:]
            #Bold formatting and italic
            list_content = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', list_content)
            list_content = re.sub(r'__(.*?)__', r'<em>\1</em>', list_content)
            html_file.append(f'<li>{list_content}</li>\n')
            continue
        elif in_list:
            html_file.append('</ul>\n')
            in_list = False

        #Paragraph and line break
        if line:
            #Bold and italic
            line = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', line)
            line = re.sub(r'__(.*?)__', r'<em>\1</em>', line)
            #applying replacement
            line = re.sub(r'\[\[private\]\]', hashlib.md5(b'private').hexdigest(), line)
            #reming parathesis
            line = re.sub(r'\(\((.*?)\)\)', r'\1', line)

            html_file.append(f'<p>{line}</p>\n')

    #close every list tag
    if in_list:
        html_file.append('</ul>\n')

    #writing HTML contents to the output file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.writelines(html_file)

if __name__ == '__main__':
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description='Convert markdown to HTML')
    parser.add_argument('input_file', help='path to input markdown file')
    parser.add_argument('output_file', help='path to output HTML file')
    args = parser.parse_args()

    # Check if the input file exist
    input_path = pathlib.Path(args.input_file)
    if not input_path.is_file():
        print(f'Missing {input_path}', file=sys.stderr)
        sys.exit(1)

    # Convert the markdown file to HTML
    convert_md_to_html(args.input_file, args.output_file)
