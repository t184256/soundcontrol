#!/usr/bin/python
# written by Alexander Sosedkin, distributed under GNU GPLv3, please see LICENSE

import liblo, time

PATH = '/tick'
ADDRESS = ('localhost', 8000)

def main():
    while True:
        liblo.send(ADDRESS, PATH)
        time.sleep(0.1)

if __name__ == "__main__": main()

