class HttpRequest:
    def __init__(self, src_mac, dst_mac,
            src_ip, dst_ip, src_port, dst_port,
            host, url, timestamp):
        self._src_mac = src_mac
        self._dst_mac = dst_mac
        self._src_ip = src_ip
        self._dst_ip = dst_ip
        self._src_port = src_port
        self._dst_port = dst_port
        self._url = url
        self._host = host
        self._timestamp = timestamp

    @property
    def src_mac(self):
        return self._src_mac

    @property
    def dst_mac(self):
        return self._dst_mac

    @property
    def src_ip(self):
        return self._src_ip

    @property
    def dst_ip(self):
        return self._dst_ip

    @property
    def src_port(self):
        return self._src_port

    @property
    def dst_port(self):
        return self._dst_port

    @property
    def url(self):
        return self._url

    @property
    def timestamp(self):
        return self._timestamp

    @property
    def host(self):
        return self._host
