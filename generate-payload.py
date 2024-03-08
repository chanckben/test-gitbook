import json
import re
import sys

if len(sys.argv) > 2:
    file_dir = sys.argv[1]
    commit_sha = sys.argv[2]
    file_list = file_dir.split(',')
else:
    raise ValueError("Missing file path argument")

with open('SUMMARY.md', encoding='utf-8') as summary_f:
    contents = summary_f.read()
    summary_f.close()

# Remove backslashes
contents = re.sub(r'\\', r'', contents)

scheme_header_pattern = re.compile(r'(?:^|\n)## +(\S.*)\n+')
link_lst_item_pattern = re.compile(r'( *)\* \[(.+)\]\((.+)\)')
changed_files_list = []

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

            if page_link in file_list:
                with open(page_link, encoding='utf-8') as page:
                    page_content = page.read()
                    page.close()
                page_object = {
                    "source_link": page_link,
                    "page_path": page_path,
                    "page_content": page_content
                }
                changed_files_list.append(page_object)

output = {
    "event_type": "trigger-workflow",
    "client_payload": {
        "sha": commit_sha,
        "changed_files_list": changed_files_list
    }
}

print(json.dumps(output))
