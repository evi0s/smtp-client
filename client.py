#!/usr/bin/env python3
"""SMTP Client"""

import getpass
import argparse
import sys

from debug import *
import smtplib
from email.mime.text import MIMEText
from email.header import Header


def parse_args(parser):
    parser.add_argument(
        "host",
        help="Specify the SMTP Server Host"
    )
    parser.add_argument(
        "port",
        type=int,
        default=25,
        help="specify the SMTP Server Port"
    )
    return parser.parse_args()


def get_password():
    password = getpass.getpass("Please input your password: ")
    debug(f"Password: {password}")
    return password


def get_username():
    username = input('Please input your username: ')
    debug(f'Username: {username}')
    return username


def get_sender():
    sender = input('Sender: ')
    debug(f'Sender: {sender}')
    return sender


def get_receiver():
    receiver = input('Receiver: ')
    debug(f'Receiver: {receiver}')
    return receiver


def get_subject():
    subject = input('Subject: ')
    debug(f'Subject: {subject}')
    return subject


def get_mail_body():
    print('End mail body with :EOF')

    body = ''
    while True:
        input_line = input()

        if input_line == ':EOF':
            body += '\r\n'
            break

        body += input_line
        body += '\r\n'

    debug(f'Mail body: {body}')
    return body


if __name__ == '__main__':

    # Parse CLI args
    parser = argparse.ArgumentParser()
    args = parse_args(parser)

    # Get SMTP Server host and port
    host = args.host
    port = args.port
    debug(f'Host: {host}')
    debug(f'Port: {port}')

    # Try to connect to SMTP server
    try:
        smtp_client = smtplib.SMTP(host, port)

        # Get Debug info
        if 'DEBUG' in os.environ:
            smtp_client.set_debuglevel(1)

        print(f'Connect to server {host} success!')

    except ConnectionRefusedError:
        error(f'Error connecting to server {host}!')
        sys.exit(0)

    # Get username and password
    username = get_username()
    password = get_password()

    # Try to login
    try:
        smtp_client.login(username, password)
    except smtplib.SMTPAuthenticationError:
        error('Login Failed!')

    print('Login success!')

    # Get mail detailed information
    sender = get_sender()
    receiver = get_receiver()
    subject = get_subject()
    mail_body_raw = get_mail_body()

    mail_body = MIMEText(mail_body_raw, 'plain', 'utf-8')
    mail_body['From'] = sender
    mail_body['To'] = receiver
    mail_body['Subject'] = Header(subject, 'utf-8')

    # Try to deliver mail
    try:
        smtp_client.sendmail(sender, receiver, mail_body.as_string())
        smtp_client.quit()
        print(f'Your mail has delivered to {receiver} successfully')
    except Exception as e:
        error(f'Error in Sending mail: {e.args}')
        sys.exit(0)
