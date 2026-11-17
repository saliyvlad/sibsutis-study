#include <iostream>
#include <string>
#include <cstring>
#include <unistd.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <signal.h>
#include <atomic>


std::atomic<bool> running(true);


void signal_handler(int signum) {
    std::cout << "[INFO] Получен сигнал " << signum 
              << ", корректное завершение работы..." << std::endl;
    running = false;
}


void send_response(int client_socket, const std::string& status, const std::string& body) {
    std::string response = "HTTP/1.1 " + status + "\r\n"
                           "Content-Type: application/json\r\n"
                           "Content-Length: " + std::to_string(body.length()) + "\r\n"
                           "Connection: close\r\n"
                           "\r\n"
                           + body;
    send(client_socket, response.c_str(), response.length(), 0);
}

int main() {
    
    signal(SIGTERM, signal_handler);
    signal(SIGINT, signal_handler);

    
    int server_fd = socket(AF_INET, SOCK_STREAM, 0);
    if (server_fd < 0) {
        std::cerr << "Ошибка создания сокета" << std::endl;
        return 1;
    }

    
    int opt = 1;
    setsockopt(server_fd, SOL_SOCKET, SO_REUSEADDR, &opt, sizeof(opt));

    
    struct sockaddr_in address;
    address.sin_family = AF_INET;
    address.sin_addr.s_addr = INADDR_ANY;  
    address.sin_port = htons(8080);

    
    if (bind(server_fd, (struct sockaddr*)&address, sizeof(address)) < 0) {
        std::cerr << "Ошибка привязки сокета" << std::endl;
        return 1;
    }

    
    if (listen(server_fd, 10) < 0) {
        std::cerr << "Ошибка прослушивания" << std::endl;
        return 1;
    }

    std::cout << "HTTP-сервер запущен на порту 8080" << std::endl;

    
    while (running) {
        
        fd_set readfds;
        FD_ZERO(&readfds);
        FD_SET(server_fd, &readfds);
        
        struct timeval timeout;
        timeout.tv_sec = 1;
        timeout.tv_usec = 0;

        int activity = select(server_fd + 1, &readfds, NULL, NULL, &timeout);
        
        if (activity < 0 && !running) {
            break;
        }
        
        if (activity > 0 && FD_ISSET(server_fd, &readfds)) {
            struct sockaddr_in client_addr;
            socklen_t client_len = sizeof(client_addr);
            int client_socket = accept(server_fd, (struct sockaddr*)&client_addr, &client_len);
            
            if (client_socket < 0) {
                continue;
            }

            
            char buffer[4096] = {0};
            read(client_socket, buffer, sizeof(buffer) - 1);
            
            std::string request(buffer);
            
            
            if (request.find("GET / HTTP") == 0) {
                std::string body = "{\"message\":\"Hello from C++ containerized app!\",\"status\":\"ok\"}";
                send_response(client_socket, "200 OK", body);
            } else if (request.find("GET /health HTTP") == 0) {
                std::string body = "{\"status\":\"ok\"}";
                send_response(client_socket, "200 OK", body);
            } else {
                std::string body = "{\"error\":\"Not Found\"}";
                send_response(client_socket, "404 Not Found", body);
            }

            close(client_socket);
        }
    }

    std::cout << "Закрытие сервера..." << std::endl;
    close(server_fd);
    
    return 0;
}