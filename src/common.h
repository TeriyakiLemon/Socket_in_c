//Do not modify this file

#ifndef COMMON_H
#define COMMON_H

#include <arpa/inet.h>
#include <assert.h>
#include <pthread.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <unistd.h>

#define PORT 8080
#define BUFFER_SIZE 1024


int create_server_socket();
int bind_server_socket(int server_socket);
int listen_for_connections(int server_socket);
int accept_client_connection(int server_socket);
void close_socket(int socket_fd);

void handle_client_request(int client_socket, int pipe_fd[2]);
void serve_file(int client_socket, const char *file_path);
void communicate_via_pipe(int pipe_fd[2], const char *message);
void start_serving();


#endif
