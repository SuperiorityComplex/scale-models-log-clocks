import multiprocessing
import socket
import sys
import optparse

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

# Stores all the sockets between threads
# Format [0-1, 1-0, 0-2, 1-2] = write socket from thread 0 to 1, write socket from thread 1 to 0, socket from thread 0 to 2, socket from thread 1 to 2
# [0-1, 1-0, 0-2, 2-0, 1-2, 2-1]
sockets_connections = []

# Stores all the logical clocks for each thread
# [10, 21, 31] = logical clock for thread 0 = 10, logical clock for thread 1 = 21, logical clock for thread 2 = 31
logical_clocks = []

def write_message_to_socket(message, source_thread, dest_thread):
    """
    Writes a message to the socket between the two threads.
    @Parameter:
    - message: The message to be sent.
    - from_thread: The thread that is sending the message.
    - to_thread: The thread that is receiving the message.
    @Returns: None.
    """
    return

def init_log_files(base_file_name="log"):
    """
    Initializes the log files for each thread.
    @Parameter: 
    - base_file_name: The base file name for the log files.
    @Returns: None.
    """
    return

def write_log_to_file():
    """
    Writes the log to a file.
    @Parameter: None.
    @Returns: None.
    """
    return

def send_message():
    """
    Determines which threads to send to and sends the message.
    @Parameter: None.
    @Returns: None.
    """
    return

def read_message_to_socket(source_thread, dest_thread):
    """
    Reads a message from the socket between the two threads.
    @Parameter:
    - from_thread: The thread that is sending the message.
    - to_thread: The thread that is receiving the message.
    @Returns:
    - message: The message that was received.
    """
    return
    

def thread_process(thread_id, clock_val):
    """
    Defines the actions of the thread process.
    @Parameter:
    - thread_id: The id of the thread (0, 1, 2).
    - clock_val: The number of clock ticks per (real world) second.
    @Returns: None.
    """
    return


def main():
    log_clock_val, act_value = get_sys_args()


main()

