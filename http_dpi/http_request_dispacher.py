from multiprocessing import Process

import pyshark
from datetime import datetime

from http_dpi.dtos import HttpRequest


class HttpRequestDispacher(Process):
    def __init__(self, context):
        self._context = context

    def run(self):
        pcap_queue = self._context.queues['pcap']
        http_request_queue = self._context.queues['http_request']
        while True:
            pcap = pcap_queue.get()
            for hr in http_request_dispacher(pcap):
                http_request_queue.put(hr)

def http_request_dispacher(pcap_file):
    for p in pyshark.FileCapture(pcap_file):
        try:
            if p.tcp.dstport != '80':
                continue
            if p.http.request_method == 'GET':
                hr = HttpRequest(p.eth.src, p.eth.dst,
                        p.ip.src, p.ip.dst,
                        int(p.tcp.srcport), int(p.tcp.dstport),
                        p.http.host, p.http.request_full_uri,
                        p.sniff_time
                        )
                yield hr
        except AttributeError as e:
            continue


if __name__ == "__main__":
    http_request_dispacher('../tcpdump_20150610_125713.cap')
