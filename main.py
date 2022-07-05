import random
import re
import requests
import queue
import threading

msg_count=100000
headers = {"User-Agent": "http://mmgc.life  <= visit this"}
tsarvar_api_url="https://tsarvar.com/en/api"
login_email="sekafod728@shbiso.com"
login_pass="sekafod728@shbiso.com"
cookies={}
message_content=open("message.txt","r",encoding="utf-8").read().strip()
msg_number=0

def login_request():
    login_data = {"meta":{},"act":{"user/login":{"email":login_email,"psw":login_pass}}}
    response = requests.post(url=tsarvar_api_url, json=login_data,headers=headers)
    global cookies
    cookies = response.cookies
    if response.text.__contains__("success"):
        print("connected !!")
    else:
        return print("can't connect !!")


def send_msg():
    userid = random.randrange(0, 50000)

    response = requests.get(url="https://tsarvar.com/en/pm/id" + str(userid), cookies=cookies, headers=headers)
    strings = response.text.split()
    sessiontime_found = False
    channelcode_found = False

    for string in strings:
        if sessiontime_found and channelcode_found:
            break
        elif string.__contains__("data-sessionUtime"):
            sessiontime = int(re.search(r'\d+', string).group())
            sessiontime_found = True
        elif string.__contains__("channelCode"):
            channelcode = int(re.search(r'\d+', string).group())
            channelcode_found = True

    # send message
    msg_data = {"meta": {}, "act": {
        "chat/sendChatMsg": {"text": message_content, "sessionUtime": sessiontime, "channel": "private",
                             "channelCode": str(channelcode)}}}
    response = requests.post(url=tsarvar_api_url, json=msg_data, cookies=cookies, headers=headers)

    if response.text.__contains__("newMsgsCount"):
        msg_status = "sended"
    else:
        msg_status = "failed"

    global msg_number
    msg_number+=1
    print("message "+str(msg_number)+": " + msg_status)







login_request()

q = queue.Queue()

for a in range(msg_count):
    t = threading.Thread(target=send_msg, args = ())
    t.daemon = True
    t.start()


print(q.get())