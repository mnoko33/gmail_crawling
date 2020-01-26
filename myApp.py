import imaplib
import email
import html2text
import csv
import time
import sys
import base64, quopri
import re

str2month = {
    "Jan": "01",
    "Feb": "02",
    "Mar": "03",
    "Apr": "04",
    "May": "05",
    "Jun": "06",
    "Jul": "07",
    "Aug": "08",
    "Sep": "09",
    "Oct": "10",
    "Nov": "11",
    "Dec": "12"
}

def convert_datetime(string):
    string = string.split()
    return f'{string[3]}-{str2month[string[2]]}-{string[1]}'

def findEncodingInfo(txt):    
    info = email.header.decode_header(txt)
    s, encoding = info[0]
    return s, encoding

def get_gmail(email, password):
    global imap
    imap = imaplib.IMAP4_SSL('imap.gmail.com')
    # email = 'mnoko92@gmail.com'
    # password = 'slikifzvedcxtsck'
    imap.login(email, password)
    imap.select('inbox') # 받은 편지함
    resp, data = imap.uid('search', None, 'All') # 받은 편지함 모든 메일 검색
    all_email = data[0].split() # 여러 메일 읽기 (반복)
    print(f'====총 {len(all_email)}개의 이메일을 가져왔습니다====')
    return all_email

def open_csv():
    global csvwriter
    global csvfile
    csvfile = open('gmail.csv', 'w', -1, "utf-8-sig", newline="")
    csvwriter = csv.writer(csvfile)

def mail2csv(all_email):
    global csvwriter
    global imap
    for idx, mail in enumerate(all_email):
        result, data = imap.uid('fetch', mail, '(RFC822)')
        msg = email.message_from_bytes(data[0][1])
        s, encoding = email.header.decode_header(msg['From'])[0]

        _from = ''
        if encoding == None:
            if type(s) == str:
                s = s.split()
                if len(s) == 1:
                    _from = s[0]
                    if '@' in _from:
                        _from = _from.split('@')[0]
                else:
                    for i in range(len(s) - 1):
                        _from += s[i]
            else:
                s, encoding = email.header.decode_header(msg['From'].split()[0])[1]
                _from = str(s, encoding)
        else:
            _from = s.decode('euc-kr')

        _date = convert_datetime(msg['Date']) 

        _address = msg['From'].split()[-1]
        if _address[-1] == '>':
            _address = _address[1:-1]

        if msg.is_multipart():
            for part in msg.walk():
                if part.get_content_type() == 'text/plain':
                    bytes = part.get_payload(decode = True)    
                    encode = part.get_content_charset()
                    _content = str(bytes, encode) 

        else:
            bytes = msg.get_payload(decode=True)
            encode = msg.get_content_charset()
            _content = html2text.html2text(str(bytes, encode))
        csvwriter.writerow([_date, _from, _address, _content])
        sys.stdout.write('\r')
        sys.stdout.write(f'{int(((idx+1) / len(all_email)) * 100)}%')
        sys.stdout.flush()
        time.sleep(0.25)

def close_csv_writer():
    global csvfile
    csvfile.close()

def close_imap():
    global imap
    imap.close()
    imap.logout()

def main():
    email = input("email : ")
    password = input("password : ")
    start = time.time()    
    all_email = get_gmail(email, password)
    open_csv()
    mail2csv(all_email)
    end = time.time()
    print()
    print(f'총 {int(end-start)}초 걸렸습니다.')
    close_csv_writer()
    close_imap()
    input("end")
    
if __name__ == "__main__":
    main()