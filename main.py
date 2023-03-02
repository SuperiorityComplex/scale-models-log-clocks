import threading
import socket
import sys
import optparse
from random import randrange

# Stores all the threads that are running. (Used for graceful shutdown)
running_threads = []

# Stores all the sockets that are running. (Used for graceful shutdown)
running_sockets = []

def get_sys_args():
    """
    Gets the arguments from the flags
    @Parameter: None.
    @Returns: 
    - log_clock_val: Maximum value for the clock tick range
    - act_value: Maximum value for the action range.
    """
    p = optparse.OptionParser()
    p.add_option('--log_clock', '-l', default="6")
    p.add_option('--act_range', '-a', default="6")
    options, _ = p.parse_args()
    log_clock_val = int(options.log_clock)
    act_value = int(options.act_range)

    return log_clock_val, act_value

# def write_message_to_socket(message, source_thread, dest_thread):
#     """
#     Writes a message to the socket between the two threads.
#     @Parameter:
#     - message: The message to be sent.
#     - from_thread: The thread that is sending the message.
#     - to_thread: The thread that is receiving the message.
#     @Returns: None.
#     """
#     return

# def init_log_files(base_file_name="log"):
#     """
#     Initializes the log files for each thread.
#     @Parameter: 
#     - base_file_name: The base file name for the log files.
#     @Returns: None.
#     """
#     return

# def write_log_to_file():
#     """
#     Writes the log to a file.
#     @Parameter: None.
#     @Returns: None.
#     """
#     return

# def send_message():
#     """
#     Determines which threads to send to and sends the message.
#     @Parameter: None.
#     @Returns: None.
#     """
#     return

def read_message_from_socket(socket, network_queue):
    """
    Reads a message from a socket and save it to the network queue.
    @Parameter:
    - socket: The socket to read from.
    - network_queue: The network queue to save the message to.
    @Returns: None.
    """
    while True: 
         message = socket.recv(1024).decode('utf-8')

    return
    

def listen_for_connections(sock: socket.socket):
    """
    Listens for connections from clients.
    @Parameter:
    1. sock: The socket to listen for connections.
    @Returns: None.
    """
    print("Server is listening and accepting connections...")
    num_connected = 0
    while num_connected < 2:
        client_socket, client_address = sock.accept()
        print(f'New connection from {client_address}')
        running_sockets.append(client_socket)
        num_connected += 1

def start_thread_process(thread_id, clock_val):
    """
    Defines the actions of the thread process.
    @Parameter:
    - thread_id: The id of the thread (0, 1, 2).
    - clock_val: The number of clock ticks per (real world) second.
    @Returns: None.
    """
    # Initialize the network queue for the process
    network_queue = []
    
    # Create socket to listen for messages for this process
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(("127.0.0.1", 3000 + thread_id))
    sock.listen()
    running_sockets.append(sock)
    
    # Create a running thread to listen for two connections
    accept_thread = threading.Thread(
                target=listen_for_connections, args=(sock,))
    accept_thread.start()
    running_threads.insert(0, accept_thread)

    # Ensure that all sockets are connected for writing
    connected_sockets = []
    for port_inc in range(1, 3):
        c_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Ensure that the socket does not timeout
        c_socket.settimeout(None)
        c_socket.connect(("127.0.0.1", 3000 + (thread_id + port_inc) % 3))
        connected_sockets.append(c_socket)
        running_sockets.append(sock)

    print(connected_sockets)
    
    # Create constantly running thread to read message from socket into network_queue
    # read_msg_thread = threading.Thread(
    #             target=read_message_from_socket, args=(sock, network_queue,))
    # read_msg_thread.start()
    # running_threads.insert(0, read_msg_thread)


    return

def gracefully_shutdown():
    """
    Gracefully shuts down the server.
    @Parameter: None.
    @Returns: None.
    """
    try:
        for thread in running_threads:
            thread.join()
        for socket in running_sockets:
            socket.shutdown(socket.SHUT_RDWR)
    except (OSError):
        # This occurs when the socket is already closed.
        pass
    print("threads and sockets successfully closed.")
    sys.exit(0)

def start_threads(log_clock_val):
    """
    Starts the threads.
    @Parameter:
    - log_clock_val: The number of clock ticks per (real world) second.
    @Returns: None.
    """
    try:
        thread0 = threading.Thread(
            target=start_thread_process, args=(0, randrange(log_clock_val)))
        thread0.start()
        thread1 = threading.Thread(
            target=start_thread_process, args=(1, randrange(log_clock_val)))
        thread1.start()
        thread2 = threading.Thread(
            target=start_thread_process, args=(2, randrange(log_clock_val)))
        thread2.start()
        running_threads.append(thread0)
        running_threads.append(thread1)
        running_threads.append(thread2)
    # This includes KeyboardInterrupt (i.e. Control + C) and other errors
    except:
        gracefully_shutdown()

def main():
    log_clock_val, act_value = get_sys_args()
    start_threads(log_clock_val)


main()

