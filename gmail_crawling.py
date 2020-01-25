# import imaplib

# email = "mnoko92@gmail.com"
# password = "qq036578"

# imap_ssl_host = 'imap.gmail.com'
# imap_ssl_port = 993
# username = email
# password = password
# server = imaplib.IMAP4_SSL(imap_ssl_host, imap_ssl_port)

# server.login(username, password)
# server.select('INBOX')
# print('----------1-----------')
# status, data = server.search(None, "ALL")
# print(status, data)

# for num in data[0].split():
#     status, data = imap.fetch(num, '(RFC822)')
#     print(data)
#     email_msg = data[0][1]

import imaplib
import email

def findEncodingInfo(txt):    
    info = email.header.decode_header(txt)
    s, encoding = info[0]
    return s, encoding

imap = imaplib.IMAP4_SSL('imap.gmail.com')
id = 'mnoko92@gmail.com'
pw = 'obxsshptfqvlsvkt'
imap.login(id, pw)

# 받은 편지함
imap.select('inbox')

# 받은 편지함 모든 메일 검색
resp, data = imap.uid('search', None, 'All')

# 여러 메일 읽기 (반복)
all_email = data[0].split()
print(f'====총 {len(all_email)}개의 이메일을 가져왔습니다====')

for mail in all_email:
    result, data = imap.uid('fetch', mail, '(RFC822)')
    msg = email.message_from_bytes(data[0][1])
    print(msg)

    break
    
    
    # raw_email = data[0][1]
    # email_message = email.message_from_string(raw_email.decode('utf-8'))
    # print('DATE:', email_message['Date'])
    # print('FROM:', email_message['From'])
    # if email_message.is_multipart():
    #     for part in email_message.get_payload():
    #         print(part)
    # # if email_message.is_multipart():
    # #     for part in email_message.get_payload():        
    # #         bytes = part.get_payload(decode = True)    
    # #         encode = part.get_content_charset()        
    # #         print(str(bytes, encode))
    # if not email_message.is_multipart():
    #     break
        # print('sss')
    # else:
        # print('asdasd')
# for mail in all_email:
#     #fetch 명령을 통해서 메일 가져오기 (RFC822 Protocol)
#     result, data = imap.uid('fetch', mail, '(RFC822)')

#     #사람이 읽기 힘든 Raw 메세지 (byte)
#     raw_email = data[0][1]
 
#     #메시지 처리(email 모듈 활용)    
#     email_message = email.message_from_bytes(raw_email)
 
#     #이메일 정보 keys
#     print('DATE:', email_message['Date'])
#     print('FROM:', email_message['From'])
 
#     b, encode = findEncodingInfo(email_message['Subject'])
#     # print('SUBJECT:', str(b, encode))
 
#     #이메일 본문 내용 확인
#     print('[CONTENT]')
#     print('='*80)
#     if email_message.is_multipart():
#         for part in email_message.get_payload():        
#             bytes = part.get_payload(decode = True)    
#             encode = part.get_content_charset()        
#             print(str(bytes, encode))
#     print('='*80)
 
imap.close()
imap.logout()