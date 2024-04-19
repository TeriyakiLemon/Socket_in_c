#include "common.h"

void serve_file(int client_socket, const char *file_path) {
  FILE *file = fopen(file_path, "r");
  if (file == NULL) {
    perror("Failed to open file");
    const char *error_response = "HTTP/1.1 404 Not Found\r\nContent-Type: "
                                 "text/html\r\nContent-Length: 0\r\n\r\n";

    //write error_response to client_socket
    send(client_socket, error_response, strlen(error_response), 0);   
    return;
  }

  const char *header_format = "HTTP/1.1 200 OK\r\nContent-Type: "
                              "text/html\r\nContent-Length: %ld\r\n\r\n";
  char header[BUFFER_SIZE];
  fseek(file, 0, SEEK_END);
  long file_size = ftell(file);
  fseek(file, 0, SEEK_SET);
  snprintf(header, BUFFER_SIZE, header_format, file_size);
  
  //write header to client_socket
  send(client_socket, header, strlen(header), 0);

  char buffer[BUFFER_SIZE];
  size_t bytes_read;

  while ((bytes_read = fread(buffer, 1, BUFFER_SIZE, file)) > 0) {
    
    //write buffer to client_socket
    send(client_socket, header, strlen(header), 0);
  }

  fclose(file);
}
