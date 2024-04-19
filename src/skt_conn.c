#include "common.h"

int create_server_socket() {

  // create socket and store it in server_socket
  int server_socket = socket(AF_INET, SOCK_STREAM, 0);
  if (server_socket == -1) {
    perror("Failed to create socket");
    return -1;
  }

  int option = 1;
  if (setsockopt(server_socket, SOL_SOCKET, SO_REUSEADDR, &option,
                 sizeof(option)) == -1) {
    perror("Failed to set socket option");
    return -1;
  }
  return server_socket;
}

int bind_server_socket(int server_socket) {
  struct sockaddr_in server_address;
  server_address.sin_family = AF_INET;
  server_address.sin_addr.s_addr = INADDR_ANY;
  server_address.sin_port = htons(PORT);

  //bind socket 
  if (bind(server_socket, (struct sockaddr *)&server_address,
           sizeof(server_address)) == -1) {
    perror("Failed to bind socket");
    return -1;
  }

  return 0;
}

int listen_for_connections(int server_socket) {
  //listen for connections 
  if (listen(server_socket, SOMAXCONN) == -1) {
    perror("Failed to listen for connections");
    return -1;
  }
  return 0;
}

int accept_client_connection(int server_socket) {
  struct sockaddr_in client_address;
  socklen_t client_address_length = sizeof(client_address);
  //accept client connection and return the client socket
  int client_socket = accept(server_socket, (struct sockaddr *)&client_address,
                             &client_address_length);
  if (client_socket == -1) {
    perror("Failed to accept client connection");
    return -1;
  }
  return client_socket;
}

void close_socket(int socket_fd) { 
  
  //fill code here
  close(socket_fd);

}

//assertion to test all functions, only uncomment when testing

// int main() {
//   int server_socket = create_server_socket();
//   assert(server_socket != -1);
//   close_socket(server_socket);

//   server_socket = create_server_socket();
//   assert(bind_server_socket(server_socket) != -1);
//   close_socket(server_socket);

//   server_socket = create_server_socket();
//   assert(bind_server_socket(server_socket) != -1);
//   assert(listen_for_connections(server_socket) != -1);
//   close_socket(server_socket);

//   server_socket = create_server_socket();
//   assert(bind_server_socket(server_socket) != -1);
//   assert(listen_for_connections(server_socket) != -1);
//   int client_socket = accept_client_connection(server_socket);
//   assert(client_socket != -1);
//   close_socket(client_socket);
//   close_socket(server_socket);

//   return 0;
// }
