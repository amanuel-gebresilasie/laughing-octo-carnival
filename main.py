import socket

HOST = "0.0.0.0"
PORT = 8080
recv_buff = 1024

RUN = True

body = "<h1>hello_world_!</h1>"
conn_num = 0
to_send = f"HTTP/1.1 200 OK\r\nContent-Length: {len(body)}\r\nConnection: close\r\n\r\n{body}\r\n\r\n"
def confirm_exit():
    while True:
        try:
            ex = input(f"Quit?[\033[32myes(y)\033[0m/\033[31mno(n)\033[0m]: ")
            ex = ex.lower()
            print("\033[F\r\033[K", end="")
        except KeyboardInterrupt:
            continue
        if ex == "yes" or ex == "y":
            return True
        elif ex == "no" or ex == "n":
            return False
        else:
            continue
_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
_socket.bind((HOST,PORT))
_socket.listen()
print(f"listening on ({HOST},{PORT})")
while RUN:
    print(f"\n\033[32m[{conn_num}]\033[0m listening...")
    try:
        conn,addr = _socket.accept()
    except KeyboardInterrupt:
        print(f"\n\033[31m[^C]\033[0m interrupted by user.")
        if confirm_exit():
            break
        else:
            continue
    except Exception as e:
        err_type = e.__name__
        err_msg = e.args
        print(f"Error type: {err_type}")

    conn_num += 1
    print(f"\033[32mNew connection: {addr}\033[0m")
    buff = 0
    data = ""
    while not buff:
        buff = conn.recv(recv_buff)
        data += buff.decode("utf-8")
    data_split = data.split("\r\n")
    request_line = data_split[0]
    request_line_split = request_line.split()
    method = request_line_split[0]
    path = request_line_split[1]
    http_ver = request_line_split[2]
    if method == "GET":
        if path != "/":
            conn.close()
            conn_num-=1
            print(f"\nconnection #{conn_num} closed. Due to an unimplemented path.")
            print(f"\033[31mPath: {path}\033[0m")
            continue
        print(f"Http-Ver: {http_ver}")
        print(f"Method: {method}")
        print(f"Path: {path}")
        conn.sendall(to_send.encode("utf-8"))
        print(f"\033[32m200 OK\033[0m\n")
        conn.close()
        conn_num-=1
    else:
        conn.close()
        conn_num-=1
        print(f"\nconnection #{conn_num} closed. Due to an unimplemented method.")
        print(f"\033[31mMethod: {method}\033[0m")

_socket.close()
print("End of life. Socket closed.")
