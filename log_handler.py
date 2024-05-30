import os
from datetime import datetime

WEBROOT = './webroot'
LOG_DIR = os.path.join(WEBROOT, 'log')
LOG_FILE = os.path.join(LOG_DIR, 'server.log')

if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)


def log_request(client_ip, identity, user_id, date_time, method, path, status_code, content_length, referrer):
    with open(LOG_FILE, 'a') as log_file:
        log_file.write(
            f'{client_ip} {identity} {user_id} [{date_time}] "{method} {path}" {status_code} {content_length} "{referrer}"\n')


def get_log_time():
    return datetime.now().strftime('%d/%b/%Y:%H:%M:%S %z')
