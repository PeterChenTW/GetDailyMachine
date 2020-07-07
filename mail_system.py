"""
https://blog.taiker.space/python-how-to-send-an-email-with-python/
"""
import configparser
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

config = configparser.ConfigParser()
config.read(f'{os.path.abspath(os.path.dirname(__file__))}/config.ini')


def send(subject, body):
    account = config['email']['account']
    password = config['email']['password']
    msg = MIMEMultipart()
    msg['From'] = account
    msg['To'] = account
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(account, password)
    text = msg.as_string()
    server.sendmail(msg['From'], msg['To'], text)
    server.quit()


if __name__ == '__main__':
    send('hi', 'cool')
