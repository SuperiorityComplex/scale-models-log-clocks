# unit tests for main

from main import init_log_file, write_to_log

import unittest

init_log_file(thread_id, base_file_name=base_log_name)
# expected behavior: open log file on path "logs/<base_file_name>_<thread_id>"
'''
Tests for this function:
- normal behavior (0, "process")
- existing file (open one, then open it again. ensure old contents overwritten)
- wrong param, try to pass in float or something
'''


def write_to_log(thread_id, message, base_file_name=base_log_name)
# expected behavior: appends message to file on path "logs/<base_file_name>_<thread_id>"
'''
Tests for this function:
- normal behavior: init file, (0, "hello world", "process"), check that contents are there
- normal behavior: file exists, add another line, ensure earlier line still there
- if file doesn't exist
- wrong param, try to pass in float or something for thread_id / message
'''

class TestStringMethods(unittest.TestCase):

    def test_upper(self):
        self.assertEqual('foo'.upper(), 'FOO')

    def test_isupper(self):
        self.assertTrue('FOO'.isupper())
        self.assertFalse('Foo'.isupper())

    def test_split(self):
        s = 'hello world'
        self.assertEqual(s.split(), ['hello', 'world'])
        # check that s.split fails when the separator is not a string
        with self.assertRaises(TypeError):
            s.split(2)

if __name__ == '__main__':
    unittest.main()