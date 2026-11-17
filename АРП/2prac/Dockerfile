
FROM gcc:13 AS builder

WORKDIR /app

COPY main.cpp .

RUN g++ -O2 -static -o cpp-http-server main.cpp


FROM alpine:latest

WORKDIR /root/

COPY --from=builder /app/cpp-http-server .

EXPOSE 8080

CMD ["./cpp-http-server"]