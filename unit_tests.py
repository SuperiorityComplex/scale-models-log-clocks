# unit tests for main

from main import init_log_file, write_to_log


import os
import unittest

class TestInitLog(unittest.TestCase):

    # init_log_file(thread_id, base_file_name)
    # expected behavior: open log file on path "logs/<base_file_name>_<thread_id>"

    # normal behavior (0, "process")
    def test_normal(self):
        # clean up
        path = "logs/test_0"
        if os.path.exists(path):
            os.remove(path)

        init_log_file(0, "test")

        self.assertTrue(os.path.exists(path))

        os.remove(path)

    # existing file (open one, then open it again. ensure old contents overwritten)
    def test_overwrite(self):
        # clean up
        path = "logs/test_1"
        if os.path.exists(path):
            os.remove(path)

        f = open(path, "w")
        f.write("Existing stuff")
        f.close()

        # file has contents
        self.assertTrue(os.stat(path).st_size != 0)

        init_log_file(1, "test")

        # file no longer has contents
        self.assertTrue(os.stat(path).st_size == 0)

        os.remove(path)

    # pass in letter for thread_id
    def test_other_thread_id(self):
        # clean up
        path = "logs/test_A"
        if os.path.exists(path):
            os.remove(path)

        init_log_file("A", "test")

        self.assertTrue(os.path.exists(path))

        os.remove(path)

class TestWriteLog(unittest.TestCase):
    # def write_to_log(thread_id, message, base_file_name)
    # expected behavior: appends message to file on path "logs/<base_file_name>_<thread_id>"

    # normal behavior: init file and add one line
    def test_normal(self):
        # clean up
        path = "logs/test_0"
        if os.path.exists(path):
            os.remove(path)

        f = open(path, "w")
        f.close()

        write_to_log(0, "hello world", "test")

        self.assertTrue(os.path.exists(path))

        f = open(path, "r")
        self.assertTrue(f.read() == "hello world\n")
        f.close()

        os.remove(path)

    # normal behavior: write one line, write next line, first should still exist
    def test_append(self):
        # clean up
        path = "logs/test_1"
        if os.path.exists(path):
            os.remove(path)

        f = open(path, "w")
        f.close()

        write_to_log(1, "hello world 1", "test")

        f = open(path, "r")
        self.assertTrue(f.read() == "hello world 1\n")
        f.close()

        write_to_log(1, "hello world 2", "test")

        f = open(path, "r")
        self.assertTrue(f.read() == "hello world 1\nhello world 2\n")
        f.close()

        os.remove(path)

    # try to write when file doesn't exist, should init the file
    def test_not_init(self):
        # clean up
        path = "logs/test_2"
        if os.path.exists(path):
            os.remove(path)

        write_to_log(2, "hello world", "test")

        self.assertTrue(os.path.exists(path))

        f = open(path, "r")
        self.assertTrue(f.read() == "hello world\n")
        f.close()

        os.remove(path)

    def test_other_thread_id(self):
        # clean up
        path = "logs/test_A"
        if os.path.exists(path):
            os.remove(path)

        write_to_log("A", "hello world", "test")

        self.assertTrue(os.path.exists(path))

        f = open(path, "r")
        self.assertTrue(f.read() == "hello world\n")
        f.close()

        os.remove(path)

if __name__ == '__main__':
    unittest.main()