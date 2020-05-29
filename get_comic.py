import os

import requests

for number in range(3, 7):
    page = 1
    save_folder = os.path.abspath(os.path.dirname(__file__)) + f'/tmp/{number}'
    if not os.path.isdir(save_folder):
        os.mkdir(save_folder)
    while True:
        url = "http://cn.xzglasses.com:50800/comic/6/2877/0{}/{}.jpg".format(number, ''.join(
            (3 - len(str(page))) * ['0'] + [str(page)]))
        resp = requests.get(url)
        if resp.status_code == 200:
            with open(f'{save_folder}/{page}.png', 'wb') as file:
                file.write(resp.content)
                file.flush()
            file.close()
            page += 1
            # time.sleep(1)
        else:
            print(f'end, {number}, {page}')
            break

# url = "https://bsr.twse.com.tw/bshtm/CaptchaImage.aspx?guid=bebd79c1-369a-4550-acb4-16e401df6f36"
# resp = requests.get(url)
# print(resp)
# with open(os.path.abspath(os.path.dirname(__file__)) + '/abc.png', 'wb') as file:
#     file.write(resp.content)
#     file.flush()
# file.close()
