import threading
import socket
import sys
import optparse
from random import randrange

# Stores all the threads that are running. (Used for graceful shutdown)
running_threads = []

# Stores all the sockets that are running. (Used for graceful shutdown)
running_sockets = []

# Event that is set when threads are running and cleared when you want threads to stop
run_event = threading.Event()

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
    p.add_option('--duration', '-d', default="5")
    options, _ = p.parse_args()
    log_clock_val = int(options.log_clock)
    act_value = int(options.act_range)
    duration = int(options.duration)

    return log_clock_val, act_value, duration

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

def init_log_file(thread_id, base_file_name="thread"):
    """
    Initializes the log files for each thread.
    @Parameter: 
    - thread_id: The id of the thread (0, 1, 2).
    - base_file_name: The base file name for the log files.
    @Returns: None.
    """
    with open("logs/{}".format("{}_{}".format(base_file_name, str(thread_id))), "a+"):
        return

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


def read_message_from_socket(sock, network_queue):
    """
    Reads a message from a socket and save it to the network queue.
    @Parameter:
    - socket: The socket to read from.
    - network_queue: The network queue to save the message to.
    @Returns: None.
    """
    while run_event.is_set(): 
        # Message is just the local logical clock time
        message = sock.recv(1024).decode('utf-8')
        network_queue.append(message)
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


def do_thread_actions():
    """
    Performs the actions of the thread.
    @Parameter: None.
    @Returns: None.
    """
        # Get the arguments from the flags
#     log_clock_val, act_value, _ = get_sys_args()
# clock_val = randrange(log_clock_val)
    while run_event.is_set():
        print( "HI")
    return

def thread_process(thread_id):
    """
    Defines the actions of the thread process.
    @Parameter:
    - thread_id: The id of the thread (0, 1, 2).
    @Returns: None.
    """

    # Initialize the network queue for the process
    network_queue = []

    # Initialize the log file for the process
    init_log_file(thread_id)
    
    # Create socket to listen for messages for this process
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(("127.0.0.1", 3000 + thread_id))
    sock.listen()
    running_sockets.append(sock)
    
    # Create a running thread to listen for two connections
    accept_thread = threading.Thread(
                target=listen_for_connections, args=(sock,))
    accept_thread.start()
    running_threads.append(accept_thread)

    # Ensure that all sockets are connected for writing
    connected_sockets = []
    for port_inc in range(1, 3):
        c_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Ensure that the socket does not timeout
        c_socket.settimeout(None)
        c_socket.connect(("127.0.0.1", 3000 + (thread_id + port_inc) % 3))
        connected_sockets.append(c_socket)
        running_sockets.append(sock)

    # Create constantly running thread to read message from socket into network_queue
    read_msg_thread = threading.Thread(
                target=read_message_from_socket, args=(sock, network_queue,))
    read_msg_thread.start()
    running_threads.append(read_msg_thread)
    do_thread_actions()

def gracefully_shutdown():
    """
    Gracefully shuts down the server.
    @Parameter: None.
    @Returns: None.
    """
    run_event.clear()
    print("SHITDOWN")
    try:
        for sock in running_sockets:
            sock.shutdown(socket.SHUT_RDWR)
        for thread in running_threads:
            thread.join()
    except (OSError):
        # This occurs when the socket is already closed.
        pass
    print("threads and sockets successfully closed.")
    sys.exit(0)

def start_threads():
    """
    Starts the threads.
    @Parameter: None.
    @Returns: None.
    """
    try:
        run_event.set()
        thread0 = threading.Thread(
            target=thread_process, args=(0,))
        thread0.start()
        thread1 = threading.Thread(
            target=thread_process, args=(1,))
        thread1.start()
        thread2 = threading.Thread(
            target=thread_process, args=(2,))
        thread2.start()
        running_threads.append(thread0)
        running_threads.append(thread1)
        running_threads.append(thread2)
    # This includes KeyboardInterrupt (i.e. Control + C) and other errors
    except:
        gracefully_shutdown()

def main():
    _, _, duration = get_sys_args()
    shutdown_thread = threading.Timer(duration, gracefully_shutdown)
    shutdown_thread.start()
    start_threads()


main()

