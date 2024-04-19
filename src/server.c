#include "common.h"

void start_serving() {
  int server_socket = create_server_socket();
  bind_server_socket(server_socket);
  listen_for_connections(server_socket);

  while (1) {
    int client_socket = accept_client_connection(server_socket);

    int pipe_fd[2];
    if (pipe(pipe_fd) == -1) {
      perror("Failed to create pipe");
      exit(1);
    }

    pid_t pid = fork();
    if (pid == -1) {
      perror("Failed to fork process");
      exit(1);
    } else if (pid == 0) {
      //fill code here
      close(pipe_fd[0]);
      handle_client_request(client_socket, pipe_fd);
      //fill code here
      close(pipe_fd[1]);
      close(client_socket);
      exit(0);

    } else {
      // Parent process
      close(client_socket);
      close(pipe_fd[1]);
      char buffer[BUFFER_SIZE];
      ssize_t bytes_read = read(pipe_fd[0], buffer, BUFFER_SIZE);
      if (bytes_read == -1) {
        perror("Failed to read from pipe");
        exit(1);
      }
      printf("%s\n", buffer);
      close(pipe_fd[0]);
      wait(NULL);
      
    }
  }

  close(server_socket);
}
