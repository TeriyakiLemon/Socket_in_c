import unittest
import ctypes
import subprocess
import time
import socket
import os
import threading
import concurrent.futures


class Test1SktConn(unittest.TestCase):
    def setUp(self):
        subprocess.run(["make", "clean"], check=True)
        subprocess.run(["make", "build/libskt_conn.so"], check=True)
        self.libc = ctypes.CDLL("./build/libskt_conn.so")

    def tearDown(self):
        if hasattr(self, 'server_socket'):
            self.libc.close_socket(self.server_socket)
            time.sleep(1)

    def test_1_create_server_socket(self):
        '''Test that the server socket is created successfully'''
        server_socket = self.libc.create_server_socket()
        self.assertNotEqual(server_socket, -1,
                            "Failed to create server socket")
        self.assertIsInstance(server_socket, int,
                              "Server socket is not an integer")
        # self.libc.close_socket(server_socket)
        self.server_socket = server_socket

    def test_2_bind_server_socket(self):
        '''Test that the server socket is bound successfully'''
        server_socket = self.libc.create_server_socket()
        result = self.libc.bind_server_socket(server_socket)
        self.assertEqual(result, 0, "Failed to bind server socket")
        # self.libc.close_socket(server_socket)
        self.server_socket = server_socket

    def test_3_listen_for_connections(self):
        '''Test that the server socket listens for connections'''
        server_socket = self.libc.create_server_socket()
        self.libc.bind_server_socket(server_socket)
        result = self.libc.listen_for_connections(server_socket)
        self.assertEqual(result, 0, "Failed to listen for connections")
        # self.libc.close_socket(server_socket)
        self.server_socket = server_socket

    def test_4_accept_client_connection(self):
        '''Test that the server socket accepts a client connection'''
        server_socket = self.libc.create_server_socket()
        self.libc.bind_server_socket(server_socket)
        self.libc.listen_for_connections(server_socket)

        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.settimeout(1)  # Set a timeout for the client socket
        try:
            client_socket.connect(('localhost', 8080))
            accepted_socket = self.libc.accept_client_connection(server_socket)
            self.assertNotEqual(accepted_socket, -1,
                                "Failed to accept client connection")
            self.assertIsInstance(accepted_socket, int,
                                  "Accepted socket is not an integer")
            # self.libc.close_socket(accepted_socket)
            self.server_socket = server_socket
        except socket.timeout:
            self.fail("Timed out waiting for client connection")
        finally:
            client_socket.close()
            # self.libc.close_socket(server_socket)
            self.server_socket = server_socket


class Test2PipeComm(unittest.TestCase):
    def setUp(self):
        subprocess.run(["make", "clean"], check=True)
        subprocess.run(["make", "build/libpipe_comm.so"], check=True)
        self.libc = ctypes.CDLL("./build/libpipe_comm.so")

    def test_communicate_via_pipe(self):
        '''Test that a message can be sent through a pipe'''
        read_fd, write_fd = os.pipe()

        pipe_fd = (ctypes.c_int * 2)(read_fd, write_fd)

        message = "Test message"
        message_bytes = message.encode()
        self.libc.communicate_via_pipe(pipe_fd, message_bytes)
        read_message = os.read(read_fd, 1024).decode().strip()
        self.assertEqual(read_message, message,
                         "Message sent through pipe does not match")


class Test3ServeFile(unittest.TestCase):
    def setUp(self):
        subprocess.run(["make", "clean"], check=True)
        subprocess.run(["make", "build/libserve_file.so"], check=True)
        self.libc = ctypes.CDLL("./build/libserve_file.so")

    def create_server_socket(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind(('localhost', 0))
        server_socket.listen(1)
        return server_socket

    def handle_client_connection(self, client_socket, file_path):
        client_fd = client_socket.fileno()
        self.libc.serve_file(client_fd, file_path)
        client_socket.close()

    def test_serve_home_page(self):
        '''Test that the server serves the home page successfully'''
        server_socket = self.create_server_socket()
        file_path = ctypes.c_char_p(b"pages/home.html")
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect(server_socket.getsockname())
        client_thread = threading.Thread(
            target=self.handle_client_connection, args=(client_socket, file_path))
        client_thread.start()
        conn, _ = server_socket.accept()
        response = conn.recv(4096).decode()
        self.assertIn("HTTP/1.1 200 OK", response)
        self.assertIn("Content-Type: text/html", response)
        client_thread.join()
        conn.close()
        server_socket.close()

    def test_serve_about_page(self):
        '''Test that the server serves the about page successfully'''
        server_socket = self.create_server_socket()
        file_path = ctypes.c_char_p(b"pages/about.html")
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect(server_socket.getsockname())
        client_thread = threading.Thread(
            target=self.handle_client_connection, args=(client_socket, file_path))
        client_thread.start()
        conn, _ = server_socket.accept()
        response = conn.recv(4096).decode()
        self.assertIn("HTTP/1.1 200 OK", response)
        self.assertIn("Content-Type: text/html", response)
        client_thread.join()
        conn.close()
        server_socket.close()

    def test_serve_contact_page(self):
        '''Test that the server serves the contact page successfully'''
        server_socket = self.create_server_socket()
        file_path = ctypes.c_char_p(b"pages/contact.html")
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect(server_socket.getsockname())
        client_thread = threading.Thread(
            target=self.handle_client_connection, args=(client_socket, file_path))
        client_thread.start()
        conn, _ = server_socket.accept()
        response = conn.recv(4096).decode()
        self.assertIn("HTTP/1.1 200 OK", response)
        self.assertIn("Content-Type: text/html", response)
        client_thread.join()
        conn.close()
        server_socket.close()

    def test_serve_nonexistent_page(self):
        '''Test that the server serves a 404 page for a nonexistent page'''
        server_socket = self.create_server_socket()
        file_path = ctypes.c_char_p(b"pages/nonexistent.html")
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect(server_socket.getsockname())
        client_thread = threading.Thread(
            target=self.handle_client_connection, args=(client_socket, file_path))
        client_thread.start()
        conn, _ = server_socket.accept()
        response = conn.recv(4096).decode()
        self.assertIn("HTTP/1.1 404 Not Found", response)
        self.assertIn("Content-Type: text/html", response)
        client_thread.join()
        conn.close()
        server_socket.close()


class TestServer(unittest.TestCase):
    def setUp(self):
        subprocess.run(["make", "clean"], check=True)
        subprocess.run(["make"], check=True)
        self.server_process = subprocess.Popen(["./build/server"])
        time.sleep(1)

    def tearDown(self):
        self.server_process.terminate()
        self.server_process.wait()

    def send_request(self, path):
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect(('localhost', 8080))
        request = f"GET {path} HTTP/1.1\r\nHost: localhost\r\n\r\n"
        client_socket.send(request.encode())
        response = client_socket.recv(4096).decode()
        client_socket.close()
        return response

    def load_expected_content(self, file_path):
        with open(os.path.join("pages", file_path), "r") as file:
            return file.read()

    def test_server(self):
        '''Test that the server serves the home, about, and contact pages'''
        paths = ["/", "/about", "/contact", "/nonexistent"]

        # Use a with statement to ensure threads are cleaned up promptly
        with concurrent.futures.ThreadPoolExecutor(max_workers=len(paths)) as executor:
            # Submit all the requests to the executor
            future_to_path = {executor.submit(
                self.send_request, path): path for path in paths}

            for future in concurrent.futures.as_completed(future_to_path):
                path = future_to_path[future]
                try:
                    response = future.result()
                    self.assertIn("HTTP/1.1 200 OK", response)
                    self.assertIn("Content-Type: text/html", response)

                except Exception as exc:
                    print('%r generated an exception: %s' % (path, exc))


if __name__ == '__main__':
    unittest.main()
