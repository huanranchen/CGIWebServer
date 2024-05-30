import os
from urllib.parse import parse_qs
from log_handler import log_request, get_log_time
from cgi_handler import handle_cgi

WEBROOT = './webroot'


def handle_http_request(client_connection, address):
    client_ip, client_port = address
    request = client_connection.recv(1024).decode('utf-8')
    headers = request.split('\n')
    method, path, _ = headers[0].split()

    referrer = ''
    for header in headers:
        if header.startswith('Referer:'):
            referrer = header.split(' ')[1].strip()
            break

    date_time = get_log_time()
    identity = '-'
    user_id = '-'

    if method == 'GET':
        response, status_code, content_length = handle_get(path)
    elif method == 'POST':
        headers = {}
        post_data = ''
        is_header = True
        for line in request.split('\r\n'):
            if is_header:
                if ': ' in line:
                    key, value = line.split(': ', 1)
                    headers[key] = value
                elif line == '':
                    is_header = False
            else:
                post_data += line

        content_length = int(headers.get('Content-Length', 0))
        if len(post_data) < content_length:
            post_data += client_connection.recv(content_length - len(post_data)).decode('utf-8')

        post_data = post_data.replace('\n', '')
        print(f'Received POST data: {post_data}')  # 调试输出接收到的POST数据
        response, status_code, content_length = handle_post(path, post_data)
    elif method == 'HEAD':
        response, status_code, content_length = handle_head(path)
    else:
        response = response_400()
        status_code = 400
        content_length = len(response)

    log_request(client_ip, identity, user_id, date_time, method, path, status_code, content_length, referrer)
    client_connection.sendall(response)
    client_connection.close()


def handle_get(path):
    if path == '/':
        path = '/index.html'

    file_path = WEBROOT + path
    if os.path.isfile(file_path):
        if path.startswith('/cgi-bin/'):
            return handle_cgi(file_path)
        else:
            with open(file_path, 'rb') as file:
                body = file.read()
            header = 'HTTP/1.0 200 OK\r\nContent-Length: {}\r\n\r\n'.format(len(body))
            response = header.encode('utf-8') + body
            status_code = 200
            content_length = len(body)
    elif os.path.isdir(file_path):
        header = 'HTTP/1.0 403 Forbidden\r\nContent-Length: 23\r\n\r\n<html><body>Forbidden</body></html>'
        response = header.encode('utf-8')
        status_code = 403
        content_length = 23
    else:
        with open(os.path.join(WEBROOT, '404.html'), 'rb') as file:
            body = file.read()
        header = 'HTTP/1.0 404 Not Found\r\nContent-Length: {}\r\n\r\n'.format(len(body))
        response = header.encode('utf-8') + body
        status_code = 404
        content_length = len(body)

    return response, status_code, content_length


def handle_post(path, request):
    if path.startswith('/cgi-bin/'):
        parsed_data = parse_qs(request)
        print(f'Parsed POST data: {parsed_data}')  # 调试输出解析后的POST数据
        return handle_cgi(WEBROOT + path, request)
    else:
        header = 'HTTP/1.0 200 OK\r\nContent-Length: 32\r\n\r\n<html><body>POST Received</body></html>'
        response = header.encode('utf-8')
        status_code = 200
        content_length = 32
        return response, status_code, content_length


def handle_head(path):
    if path == '/':
        path = '/index.html'

    file_path = WEBROOT + path
    if os.path.isfile(file_path):
        header = 'HTTP/1.0 200 OK\r\nContent-Length: {}\r\n\r\n'.format(os.path.getsize(file_path))
        response = header.encode('utf-8')
        status_code = 200
        content_length = os.path.getsize(file_path)
    elif os.path.isdir(file_path):
        header = 'HTTP/1.0 403 Forbidden\r\n\r\n'
        response = header.encode('utf-8')
        status_code = 403
        content_length = 0
    else:
        header = 'HTTP/1.0 404 Not Found\r\n\r\n'
        response = header.encode('utf-8')
        status_code = 404
        content_length = 0

    return response, status_code, content_length


def response_400():
    header = 'HTTP/1.0 400 Bad Request\r\nContent-Length: 22\r\n\r\n<html><body>Bad Request</body></html>'
    return header.encode('utf-8')


def response_500(message):
    with open(os.path.join(WEBROOT, '500.html'), 'rb') as file:
        body = file.read()
    header = f'HTTP/1.0 500 Internal Server Error\r\nContent-Length: {len(body)}\r\n\r\n'
    return header.encode('utf-8') + body
