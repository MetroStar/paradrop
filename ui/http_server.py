#!/usr/bin/env python3
import http.server

HTTP_SERVER_ADDRESS = '127.0.0.1'
HTTP_SERVER_PORT = 8000


class NoCacheHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def send_response_only(self, code, message=None):
        super().send_response_only(code, message)
        self.send_header('Cache-Control', 'no-store, must-revalidate')
        self.send_header('Expires', '0')


if __name__ == '__main__':
    http.server.test(
        HandlerClass=NoCacheHTTPRequestHandler,
        bind=HTTP_SERVER_ADDRESS,
        port=HTTP_SERVER_PORT
    )
