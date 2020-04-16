#!/usr/local/bin/python3

"""
Create a binary of Python's simple http.server using pyinstaller
https://docs.python.org/3/library/http.server.html#http.server.SimpleHTTPRequestHandler
"""

import subprocess

subprocess.call(["pyinstaller", "--clean", "--onefile", "server.py"])
