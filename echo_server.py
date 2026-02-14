import socket
import urllib.parse
from http import HTTPStatus


def run_server(host='127.0.0.1', port=8080):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((host, port))
    server.listen(5)

    while True:
        client, addr = server.accept()
        data = client.recv(4096).decode()

        lines = data.split('\r\n')
        first_line = lines[0].split()

        if len(first_line) >= 2:
            method = first_line[0]
            path = first_line[1]

            query = urllib.parse.urlparse(path).query
            params = urllib.parse.parse_qs(query)

            try:
                status = int(params.get('status', ['200'])[0])
                if status not in HTTPStatus._value2member_map_:
                    status = 200
            except:
                status = 200

            headers = {}
            for line in lines[1:]:
                if ': ' in line:
                    k, v = line.split(': ', 1)
                    headers[k] = v

            body = [
                f"Request Method: {method}",
                f"Request Source: {addr}",
                f"Response Status: {status} {HTTPStatus(status).phrase}"
            ]
            for k, v in headers.items():
                body.append(f"{k}: {v}")

            response_body = '\r\n'.join(body) + '\r\n'

            response = (
                f"HTTP/1.1 {status} {HTTPStatus(status).phrase}\r\n"
                f"Content-Type: text/plain\r\n"
                f"Content-Length: {len(response_body.encode())}\r\n"
                f"\r\n"
                f"{response_body}"
            )
            client.send(response.encode())

        client.close()

if __name__ == "__main__":
    run_server()