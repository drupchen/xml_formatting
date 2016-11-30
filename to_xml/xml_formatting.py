import os
import re
import yaml

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


def parse_content(content):
    pages = re.split(r'\n*([0-9]+\.tif)\n', content.strip())
    if pages[0] == '':
        del pages[0]
    parsed = []
    for page_num in range(0, len(pages) - 1, 2):
        parsed.append((pages[page_num], pages[page_num + 1].split('\n')))
    return parsed


def format_text(parsed):
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
                formatted_lines = [line_format.format(num + 1, line) for num, line in enumerate(lines)]
                page = '<tei:p unit="page" n="{}">{}</tei:p>'.format(tif, ''.join(formatted_lines))
                formatted_pages.append(page)
    return '<tei:text><tei:body><tei:div>{}</tei:div></tei:body></tei:text>'.format(''.join(formatted_pages))


def format_header(metadata):
    text_title = metadata['text_title'] # pod 5 bod ljongs nag chu sa khul gyi lo rgyus rig gnas
    distributor_comment = metadata['distributor_comment']  # This OCR'd text was generated using UCB's Namsel-OCR application on Jul 23, 2014 at the request of the Tibetan Buddhist Resource Center. Please note this document has not been finalized and is subject to additional changes and corrections.
    TBRC_text_RID = metadata['TBRC_text_RID']  # UT00EGS1016733-I01JW48-0000
    TBRC_RID = metadata['TBRC_RID']  # W00EGS1016733
    SRC_PATH = metadata['SRC_PATH'] # Namsel_OCR/Batch-20140903/W00EGS1016733/xml/W00EGS1016733-I01JW48/W00EGS1016733-I01JW48.xml
    return '<tei:teiHeader><tei:fileDesc><tei:titleStmt><tei:title>{}</tei:title></tei:titleStmt><tei:publicationStmt><tei:distributor>\n{}\n</tei:distributor><tei:idno type="TBRC_TEXT_RID">{}</tei:idno><tei:idno type="page_equals_image">page_equals_image</tei:idno></tei:publicationStmt><tei:sourceDesc><tei:bibl><tei:idno type="TBRC_RID">{}</tei:idno><tei:idno type="SRC_PATH">{}</tei:idno></tei:bibl></tei:sourceDesc></tei:fileDesc></tei:teiHeader>'.format(text_title, distributor_comment, TBRC_text_RID, TBRC_RID, SRC_PATH)


def write_in_folder_structure(metadata, tei):
    out_folder = 'output/{}'.format(metadata[f]['TBRC_text_RID'].split('-')[0])
    if not os.path.exists(out_folder):
        os.makedirs(out_folder)
    work_folder = '{}/{}'.format(out_folder, metadata[f]['TBRC_text_RID'].replace('-0000', ''))
    if not os.path.exists(work_folder):
        os.makedirs(work_folder)
    write_file('{}/{}.xml'.format(work_folder, metadata[f]['TBRC_text_RID']), tei)


in_path = './raw_data'
in_folder = 'W24829-OCR'
metadata = yaml.load(open_file('{}/{}/metadata/meta.txt'.format(in_path, in_folder)))
for f in os.listdir('{}/{}'.format(in_path, in_folder)):
    if f.endswith('.txt'):
        work_name = f.replace('.txt', '')
        # open the OCR'd file and parse its content
        content = open_file('{}/{}/{}'.format(in_path, in_folder, f)).replace('OCR text', '')
        parsed = parse_content(content)
        # format the body of the text
        formatted_text = format_text(parsed)
        # format the xml header
        metadata[f]['SRC_PATH'] = 'To Change. {}/{}'.format(in_folder, f)
        formatted_header = format_header(metadata[f])
        # put the whole xml together
        tei = '<tei:TEI xmlns:tei="http://www.tei-c.org/ns/1.0">{}{}</tei:TEI>'.format(formatted_header, formatted_text)
        # create the folder structure and write the xml files
        write_in_folder_structure(metadata, tei)
