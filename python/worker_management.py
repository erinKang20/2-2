import socket
import threading
from common import Message, MessageType, CENTRAL_SERVER_IP, CENTRAL_SERVER_PORT
from socket_util import create_and_connect_socket

def receive_work_order(msg):
    print(f"[보낸 곳: 중앙관리] 작업 지시 수신: {msg.content}")

def receiver_thread(server_socket):
    while True:
        try:
            data = server_socket.recv(1024)
            if not data:
                print("recv 실패 또는 연결 끊김")
                break
            msg = Message.deserialize(data)
            if msg.type == MessageType.WORK_ORDER:
                receive_work_order(msg)
        except Exception as e:
            print(f"수신 스레드 오류: {e}")
            break

if __name__ == "__main__":
    centrol_socket = create_and_connect_socket(CENTRAL_SERVER_IP, CENTRAL_SERVER_PORT)

    # 수신 스레드 시작
    recv_thread = threading.Thread(target=receiver_thread, args=(centrol_socket,))
    recv_thread.start()

    recv_thread.join()
    centrol_socket.close()
