#!/usr/bin/python3

import sys

s = sys.stdin.read()
files = s.split('\n')

with open("list.html", 'w') as H:
    H.write('''<!DOCTYPE html>
    <html> 
    <body>''')

    for file in files:
        if file[-2:] == 'md':
            H.write(f'<input type="checkbox"> <label> {file[:-3]}</label> <br>\n')     

    H.write('''</body>
    </html>''')
