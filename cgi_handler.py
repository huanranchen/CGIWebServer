import os
import subprocess
import sys


def handle_cgi(script_path, request=None):
    try:
        env = os.environ.copy()
        python_executable = sys.executable  # 获取当前Python解释器路径

        print(f'Executing CGI script: {script_path} with Python: {python_executable}')

        if request:
            env['REQUEST_METHOD'] = 'POST'
            env['CONTENT_LENGTH'] = str(len(request))
            process = subprocess.Popen([python_executable, script_path], stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                       stderr=subprocess.PIPE, env=env)
            stdout, stderr = process.communicate(input=request.encode('utf-8'))
        else:
            process = subprocess.Popen([python_executable, script_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                       env=env)
            stdout, stderr = process.communicate()

        if process.returncode != 0:
            print(f'CGI script error: {stderr.decode("utf-8")}')
            return response_500(stderr.decode('utf-8'))

        output = stdout.decode('utf-8')
        print(f'Raw CGI output: {output}')

        header_end = output.find("\r\n\r\n")
        if header_end == -1:
            header_end = output.find("\n\n")

        if header_end != -1:
            header = output[:header_end + 4]
            body = output[header_end + 4:]
        else:
            header = 'HTTP/1.0 200 OK\r\nContent-Type: text/html\r\n\r\n'
            body = output

        if not header.startswith("HTTP/"):
            header = 'HTTP/1.0 200 OK\r\n' + header

        response = header.encode('utf-8') + body.encode('utf-8')
        print(f'CGI response: {response}')
        content_length = len(response)
        return response, 200, content_length
    except Exception as e:
        print(f'Error executing CGI script: {e}')
        error_response = response_500(str(e))
        return error_response, 500, len(error_response)


def response_500(message):
    body = f'<html><body>Internal Server Error: {message}</body></html>'
    header = f'HTTP/1.0 500 Internal Server Error\r\nContent-Length: {len(body)}\r\n\r\n'
    return header.encode('utf-8') + body.encode('utf-8')
