#include "common.h"

void handle_client_request(int client_socket, int pipe_fd[2]) {
  char request[BUFFER_SIZE];
  char method[BUFFER_SIZE];
  char path[BUFFER_SIZE];
  char protocol[BUFFER_SIZE];

  //read from client_socket to request
  ssize_t bytes_received = recv(client_socket, request, BUFFER_SIZE - 1, 0);
  if(bytes_received <= 0){
    if (bytes_received == 0) {
      printf("Client disconnected\n");
    } else {
      perror("Failed to read from client socket");
    }
    return;
  }
  request[bytes_received] = '\0';
  sscanf(request, "%s %s %s", method, path, protocol);
  if(sscanf(request, "%s %s %s", method, path, protocol) < 3){
    perror("Invalid request");
    serve_file(client_socket, "pages/400.html");
    return;
  }


  if (strcmp(path, "/") == 0) {
    serve_file(client_socket, "pages/home.html");
  } else if (strcmp(path, "/about") == 0) {
    serve_file(client_socket, "pages/about.html");
  } else if (strcmp(path, "/contact") == 0) {
    serve_file(client_socket, "pages/contact.html");
  } else {
    serve_file(client_socket, "pages/404.html");
  }

  char message[BUFFER_SIZE];
  snprintf(message, BUFFER_SIZE, "Request processed by child process");
  communicate_via_pipe(pipe_fd, message);

  close(client_socket);
}
