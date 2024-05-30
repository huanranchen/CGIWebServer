import socket
import threading
import queue
from http_handler import handle_http_request


def worker_thread(request_queue):
    while True:
        client_connection, address = request_queue.get()
        if client_connection is None:
            break
        handle_http_request(client_connection, address)
        request_queue.task_done()


def start_server():
    host = '127.0.0.1'
    port = 6789
    num_workers = 1
    max_connections = 100

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(max_connections)
    print(f'Serving HTTP on {host} port {port} ...')

    request_queue = queue.Queue()
    threads = []

    for _ in range(num_workers):
        thread = threading.Thread(target=worker_thread, args=(request_queue,))
        thread.start()
        threads.append(thread)

    connections = []

    try:
        while True:
            client_connection, client_address = server_socket.accept()
            if len(connections) >= max_connections:
                oldest_connection = connections.pop(0)
                oldest_connection.close()
            connections.append(client_connection)
            request_queue.put((client_connection, client_address))
    except KeyboardInterrupt:
        print("Server is shutting down...")

    for _ in range(num_workers):
        request_queue.put(None)

    for thread in threads:
        thread.join()


if __name__ == '__main__':
    start_server()
