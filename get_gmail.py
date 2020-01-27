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
    if len(string) == 6:
        return f'{string[3]}-{str2month[string[2]]}-{string[1]}'
    else:
        return f'{string[2]}-{str2month[string[1]]}-{string[0]}'

def findEncodingInfo(txt):    
    info = email.header.decode_header(txt)
    s, encoding = info[0]
    return s, encoding

def get_gmail(email, password):
    global imap
    imap = imaplib.IMAP4_SSL('imap.gmail.com')
    imap.login(email, password)
    imap.select('inbox') # 받은 편지함
    
    resp, data = imap.uid('search', None, 'All') # 받은 편지함 모든 메일 검색
    all_email = data[0].split() # 여러 메일 읽기 (반복)
    
    print(f'====총 {len(all_email)}개의 이메일을 가져왔습니다====')
    return all_email

def open_csv():
    global csvwriter
    global csvfile
    try:
        csvfile = open('./get_gmail.csv', 'a', -1, "utf-8-sig", newline="")
    except:
        print('파일을 찾는데 오류가 발생')
    csvwriter = csv.writer(csvfile)

def mail2csv(all_email, start_idx):
    global csvwriter
    global imap

    N = len(all_email)
    for idx, mail in enumerate(all_email):
        if idx < start_idx:
            continue
        try:
            mail = all_email[idx]
            result, data = imap.uid('fetch', mail, '(RFC822)')
            raw_mail = data[0][1]
            msg = email.message_from_bytes(raw_mail)
            
            # from, address, date 구하기
            string_from, encoding = email.header.decode_header(msg['From'])[0]
            if encoding == None:
                if type(string_from) == str:
                    string_from = string_from.split()
                    if len(string_from) == 1:
                        _from = string_from[0]
                        if '@' in _from:
                            _from = _from.split('@')[0]
                    else:
                        _from = ''
                        for i in range(len(string_from) - 1):
                            _from += string_from[i]
                else:
                    string_from, encoding = email.header.decode_header(msg['From'].split()[0])[1]
                    _from = str(string_from, encoding)
            else:
                _from = string_from.decode(encoding)
            _date = msg['Date']

            _address = msg['From'].split()[-1]
            if _address[-1] == '>':
                _address = _address[1:-1]

            if msg.is_multipart():
                for part in msg.walk():
                    if part.get_content_type() == "text/plain":
                        bytes = part.get_payload(decode=True)
                        tmp = part.get_content_charset()
                        _content = ""
                        for encode in [tmp, "CP949", "euc-kr", "base64", "ks_c_5601-1987", None]:
                            try:
                                _content = html2text.html2text(str(bytes, encode))
                                break
                            except:
                                continue
                        if _content == '':
                            _content = "vacant"
            else:
                bytes = msg.get_payload(decode=True)
                encode = msg.get_content_charset()
                _content = html2text.html2text(str(bytes, encode))
            csvwriter.writerow([idx, _date, _from, _address, _content])
            sys.stdout.write('\r')
            sys.stdout.write(f'{idx+1}/{N}')
        except:
            print(f'{idx}에서 문제가 발생하여 멈췄습니다.')
            return

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
    start_idx = int(input("start idx : "))
    start = time.time()    
    all_email = get_gmail(email, password)
    open_csv()
    mail2csv(all_email, start_idx)
    end = time.time()
    print()
    print(f'총 {int(end-start)}초 걸렸습니다.')
    close_csv_writer()
    close_imap()
    input("end")
    
if __name__ == "__main__":
    main()