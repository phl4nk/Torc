#!/usr/bin/python
import socks
import socket
import requests
from fake_useragent import UserAgent
import base64
import codecs
import random
import threading
from threading import Thread
import sys
import time

class Crawler(Thread):

    def setProxy(self):
        print "[+] Proxy set"
        socks.setdefaultproxy(
            proxy_type=socks.PROXY_TYPE_SOCKS5, addr="127.0.0.1", port=9050)

    # override DNS reslution, push through socket
    def getaddrinfoOveride(self, *args):
        return [(socket.AF_INET, socket.SOCK_STREAM, 6, '', (args[0], args[1]))]

    def getURL(self):
        try:
            print "[+] Retrieving URL", self.URL
            return requests.get(self.URL, headers=self.headers, timeout=(2.45, 5))
        except Exception, e:
            print "[!] Crawling failed:", e
            return None

    def setURL(self,URL):
        self.URL=URL

    def generateRandomOnion(self):
        data = base64.b32encode(codecs.decode(codecs.encode(
            '{0:020x}'.format(random.getrandbits(80))), 'hex_codec'))
        return "http://" + data.lower() + ".onion"

    def run(self):
        while self.alive:
             self.URL = self.generateRandomOnion()
             data = self.getURL();
             if data:
                 print data

    def __init__(self, TOR=True):
        Thread.__init__(self)
        self.URL = None
        self.alive = True
        self.headers = {'User-Agent': UserAgent().random,
                        'Connection': 'close'}
        # setup proxy and DNS
        if TOR:
            self.setProxy()
            socket.socket = socks.socksocket
            print "[+] DNS Override set"
            socket.getaddrinfo = self.getaddrinfoOveride

crawlers = []
#create 10 crawlers
for i in range(10):
    i = Crawler()
    i.start()
    crawlers.append(i)

# CTRL+C to stop crawlers
try:
    while 1:
        time.sleep(.1)
except KeyboardInterrupt:
    for i in crawlers:
        print "[!] Attempting to kill Thread",i
        i.alive = False
        i.join()
