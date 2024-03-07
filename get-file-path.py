import os
import re
import sys

output_file = os.getenv('GITHUB_OUTPUT')

if len(sys.argv) > 1:
    file_dir = sys.argv[1]
else:
    raise ValueError("Missing file path argument")

with open('SUMMARY.md', encoding='utf-8') as summary_f:
    contents = summary_f.read()
    summary_f.close()

# Remove backslashes
contents = re.sub(r'\\', r'', contents)

scheme_header_pattern = re.compile(r'(?:^|\n)## +(\S.*)\n+')
link_lst_item_pattern = re.compile(r'( *)\* \[(.+)\]\((.+)\)')

if not scheme_header_pattern.search(contents):
    raise ValueError("Invalid file structure")

scheme_files = scheme_header_pattern.split(contents)
for i in range(1, len(scheme_files), 2):
    scheme = scheme_files[i]
    content_lst = scheme_files[i+1].split('\n')
    page_path = []
    curr_indent = 0
    for content_item in content_lst:
        matches = link_lst_item_pattern.search(content_item)
        if matches:
            spaces, page_title, page_link = matches.groups()

            if len(spaces) == 0:
                page_path = [scheme, page_title]
            elif len(spaces) == curr_indent + 2:
                page_path = page_path + [page_title]
            elif len(spaces) == curr_indent - 2:
                page_path = page_path[:-1]
            elif len(spaces) == curr_indent:
                page_path = page_path[:-1] + [page_title]
            curr_indent = len(spaces)

            if page_link == file_dir:
                with open(output_file, 'a') as out:
                    out.write(f'page_path={page_path}')
                break
