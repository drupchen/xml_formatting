import os
import re

def write_file(file_path, content):
    with open(file_path, 'w', -1, 'utf8') as f:
        f.write(content)


def open_file(file_path):
    try:
        with open(file_path, 'r', -1, 'utf-8-sig') as f:
            return f.read()
    except UnicodeDecodeError:
        with open(file_path, 'r', -1, 'utf-16-le') as f:
            return f.read()

in_path = './raw_data'
in_folder = 'W24829-OCR'
for f in os.listdir('{}/{}'.format(in_path, in_folder)):
    work_name = f.replace('.txt', '')
    content = open_file('{}/{}/{}'.format(in_path, in_folder, f)).replace('OCR text', '')
    pages = re.split(r'\n*([0-9]+\.tif)\n', content.strip())
    if pages[0] == '':
        del pages[0]
    parsed = []
    for page_num in range(0, len(pages)-1, 2):
        parsed.append((pages[page_num], pages[page_num+1].split('\n')))

    formatted_pages = []
    for p in parsed:
        tif = p[0]
        lines = p[1]
        if lines == [''] or lines == ['No content captured']:
            page = '<tei:p unit="page" n="{}/>'.format(tif)
            formatted_pages.append(page)
        else:
            if len(lines) == 1:
                page = '<tei:p unit="page" n="{}"/>{}'.format(tif, ''.join(lines))
                formatted_pages.append(page)
            else:
                line_format = '<tei:milestone unit="line" n="{}"/>{}'
                formatted_lines = [line_format.format(num+1, line) for num, line in enumerate(lines)]
                page = '<tei:p unit="page" n="{}">{}</tei:p>'.format(tif, ''.join(formatted_lines))
                formatted_pages.append(page)

    formatted_text = '<tei:text><tei:body><tei:div>{}</tei:div></tei:body></tei:text>'.format(''.join(formatted_pages))

    print('ok')
