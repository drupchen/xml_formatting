from bs4 import BeautifulSoup as Soup
import re
import os

os.chdir('./db/eTextsChunked')

log = ''
summary = ''
total = 0
for Collection in os.listdir('.'):
    if not Collection.startswith('_'):
        msg1 = Collection
        print(msg1)
        log += msg1+'\n'
        counter = 0
        folders = ''
        for Folder in os.listdir(Collection):
            if not Folder.startswith('_'):
                msg2 = '\t\t'+Folder
                print(msg2)
                log += msg2+'\n'
                folders += '"{}", '.format(Folder)
                for File in os.listdir(Collection+'/'+Folder):
                    if not File.startswith('_'):
                        msg3 = '\t\t\t\t'+File
                        print(msg3, end=' ')
                        log += msg3+' '
                        c = 0
                        for Fich in os.listdir(Collection+'/'+Folder+'/'+File):
                            if not Fich.startswith('_'):
                                with open(Collection+'/'+Folder+'/'+File+'/'+Fich, 'r', -1, 'utf-8-sig') as f:
                                    volume = f.read()
                                soup = Soup(volume, 'lxml')
                                output = ''
                                for page in soup.find_all('tei:p'):
                                    text = re.sub(r'\<[^>]+\>', r'', str(page))
                                    output += text + '\n'
                                file_name = Fich.split('.')[0]
                                with open('../../output/'+'{}.txt'.format(file_name), 'w', -1, 'utf-8-sig') as f:
                                    f.write(output)
                                c += 1
                        msg4 = '{} files'.format(c)
                        print(msg4)
                        log += msg4+'\n'
                        counter += c
        msg5 = '{}: {} files.'.format(Collection, counter)
        print(msg5)
        summary += '{} [{}]\n'.format(msg5, folders[:-2])
        total += counter
msg6 = 'Total: {} files'.format(total)
print(msg6)
log += msg6
log = summary+log

with open('./logs/parser_log.txt', 'w', -1, 'utf-8') as f:  # TODO: add a timestamp to the log file or add the folder_name
    f.write(log)