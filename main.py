import threading
import socket
import sys
import optparse
from random import randrange
import datetime
import time

base_log_name = "thread"

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
    p.add_option('--log_clock', '-l', default="7")
    p.add_option('--act_range', '-a', default="11")
    p.add_option('--duration', '-d', default="10")
    options, _ = p.parse_args()
    log_clock_val = int(options.log_clock)
    act_value = int(options.act_range)
    duration = int(options.duration)

    return log_clock_val, act_value, duration

def init_log_file(thread_id, base_file_name=base_log_name):
    """
    Initializes the log files for each thread.
    @Parameter: 
    - thread_id: The id of the thread (0, 1, 2).
    - base_file_name: The base file name for the log files.
    @Returns: None.
    """
    with open("logs/{}".format("{}_{}".format(base_file_name, str(thread_id))), "w+"):
        return

def write_to_log(thread_id, message, base_file_name=base_log_name):
    """
    Writes to the log file.
    @Parameter: 
    - thread_id: The id of the thread (0, 1, 2).
    - queue_len: The length of the message queue.
    - clock_time: The logical clock time.
    - base_file_name: The base file name for the log files.
    @Returns: None.
    """
    # write in the log that it received a message, the global time (gotten from the system), the length of the message queue, and the logical clock time.
    with open("logs/{}".format("{}_{}".format(base_file_name, str(thread_id))), "a") as f:
        f.write(message + "\n")
    return

def send_message(sockets, logical_clock_value):
    """
    Sends message with logical clock value to sockets.
    @Parameter: 
    - sockets: The sockets to send the message to.
    - logical_clock_value: The local logical clock value to send.
    @Returns: None.
    """
    for sock in sockets:
        final_payload = str(logical_clock_value[0])
        sock.sendall(final_payload.encode('utf-8'))


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
        if(message):
            network_queue.append(int(message))
    return
    

def listen_for_connections(sock: socket.socket, network_queue):
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
        start_reading_from_socket(client_socket, network_queue)
        running_sockets.append(client_socket)
        num_connected += 1

def start_reading_from_socket(sock, network_queue):
    """
    Starts a thread to read from a socket.
    @Parameter:
    - sock: The socket to read from.
    - network_queue: The network queue to save the message to.
    @Returns: None.
    """
    # Create constantly running thread to read message from socket into network_queue
    read_msg_thread = threading.Thread(
                target=read_message_from_socket, args=(sock, network_queue,))
    read_msg_thread.start()
    running_threads.append(read_msg_thread)



def do_thread_actions(thread_id, network_queue, clock_val, act_value, logical_clock_value, connected_sockets):
    """
    Performs the actions of the thread.
    @Parameter: 
    - thread_id: The id of the thread (0, 1, 2).
    - network_queue: The network queue to read from.
    - clock_val: The clock ticks per second.
    - act_value: The maximum value for the action range.
    - logical_clock_value: The logical clock value as an array for mutability (i.e. [logical_clock_value]).
    - connected_sockets: The list of connected sockets.
    @Returns: None.
    """
    
    while run_event.is_set():
        if(len(network_queue) > 0):
            # Get the message from the network queue
            log_clock_value = network_queue.pop(0)
            # Update the logical clock value
            logical_clock_value[0] = max(logical_clock_value[0], log_clock_value) + 1
            # Write to the log file
            message = "Received message at time: {} with msg queue: {} with logical clock: {}.".format(datetime.datetime.now().isoformat(),  len(network_queue), logical_clock_value[0])
        else:
            action = randrange(1, act_value)
            # Increment the clock value
            logical_clock_value[0] += 1
            if action == 1:
                send_message([connected_sockets[0]], logical_clock_value)
                message = "Sent message to socket at time: {} with logical clock: {}.".format(datetime.datetime.now().isoformat(), logical_clock_value[0])
            elif action == 2:
                send_message([connected_sockets[1]], logical_clock_value)
                message = "Sent message to other socket at time: {} with logical clock: {}.".format(datetime.datetime.now().isoformat(), logical_clock_value[0])
            elif action == 3:
                send_message(connected_sockets, logical_clock_value)
                message = "Sent message to both sockets at time: {} with logical clock: {}.".format(datetime.datetime.now().isoformat(), logical_clock_value[0])
            else:
                message = "Internal event at time: {} with logical clock: {}.".format(datetime.datetime.now().isoformat(), logical_clock_value[0])

        # Write to the log file
        write_to_log(thread_id, message)
        # Sleep for the clock value
        time.sleep(1.0 / clock_val)

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
                target=listen_for_connections, args=(sock, network_queue))
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


    # Get the arguments from the flags
    log_clock_val, act_value, _ = get_sys_args()
    clock_val = randrange(log_clock_val)
    logical_clock_value = [0]
    do_thread_actions(thread_id, network_queue, clock_val, act_value, logical_clock_value, connected_sockets)

def gracefully_shutdown():
    """
    Gracefully shuts down the server.
    @Parameter: None.
    @Returns: None.
    """
    run_event.clear()
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

