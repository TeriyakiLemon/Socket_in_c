#include "common.h"
#include <assert.h>
#include <stdio.h>

void communicate_via_pipe(int pipe_fd[2], const char *message) {

  //write message to pipe_fd
  if(message == NULL){
    perror("Failed to write to pipe");
    exit(1);
  }
  ssize_t ssize = write(pipe_fd[1], message, strlen(message));
  if(ssize == -1){
    perror("Failed to write to pipe");
    exit(1);
  }
    
}

// // assertion to test all functions, only uncomment when testing
// int main() {
//   int pipe_fd[2];
//   if (pipe(pipe_fd) == -1) {
//     perror("Failed to create pipe");
//     exit(1);
//   }

//   char *message = "Hello, pipe!";

//   communicate_via_pipe(pipe_fd, message);

//   char buffer[BUFFER_SIZE];
//   ssize_t bytes_read = read(pipe_fd[0], buffer, BUFFER_SIZE);
//   if (bytes_read == -1) {
//     perror("Failed to read from pipe");
//     exit(1);
//   }
//   assert(strcmp(buffer, message) == 0);
//   printf("%s\n", buffer);

//   return 0;
// }
