import hashlib

from http_packet.maria_dao import MariaDao


INIT_HTTP_REQUEST = """\
CREATE TABLE IF NOT EXISTS http_request (
  id int(11) NOT NULL AUTO_INCREMENT,
  page_id int(11) NOT NULL,
  src_mac varchar(255) NOT NULL,
  dst_mac varchar(255) NOT NULL,
  src_ip varchar(255) NOT NULL,
  dst_ip varchar(255) NOT NULL,
  src_port int(11) NOT NULL,
  dst_port int(11) NOT NULL,
  timestamp datetime NOT NULL,
  browsing_time float,
  PRIMARY KEY (id),
  KEY index_browsing_history_on_timestamp (timestamp),
  KEY index_browsing_history_on_src_ip (src_ip),
  KEY index_browsing_history_on_http_id (page_id)
) ENGINE=TokuDB DEFAULT CHARSET=utf8
"""

INIT_PAGE = """\
CREATE TABLE IF NOT EXISTS page (
  id int(11) NOT NULL AUTO_INCREMENT,
  status int(11) Default 0,
  domain varchar(255) NOT NULL,
  hashed_url varchar(255) NOT NULL,
  url text NOT NULL,
  title text,
  context_type varchar(255),
  PRIMARY KEY (id),
  KEY index_http_on_status (status),
  KEY index_http_on_hashed_url (hashed_url),
) ENGINE=TokuDB DEFAULT CHARSET=utf8
"""

INSERT_PAGE = """\
INSERT INTO page (domain, url, hashed_url)
VALUES
('{domina}', '{url}', {hashed_url}')
"""

FIND_PAGE_BY_URL = """\
SELECT id, url, status FROM page
WHERE url = '{url}'
"""

INSERT_HTTP_REQUEST="""\
INSERT INTO http_request
(
    page_id, src_mac, dst_mac, src_ip, dst_ip, src_port, dst_port
    timestamp
)
VALUES
(
    {page_id}, '{src_mac}', '{dst_mac}', '{src_ip}', '{dst_ip}',
    {src_port}, {dst_port}, '{timestamp}'
)
"""

class HttpRequestDao(MariaDao):
    def __init__(self, host, user, password, db):
        super().__init__(host, user, password, db)
        self._execute(INIT_HTTP_REQUEST)
        self._execute(INIT_PAGE)

    def save_http_request(self, http_request):
        page_id = self.save_or_get_page(http_request.domain, http_request.url)
        sql = INSERT_HTTP_REQUEST.format(
                page_id=page_id,
                src_mac=http_request.src_mac, dst_mac=http_request.dst_mac,
                src_ip=http_request.src_ip, dst_ip=http_request.dst_ip,
                src_port=http_request.src_port, dst_port=http_request.dst_port,
                timestamp=http_request.timestamp
                )
        self._execute(sql)

    def save_or_get_page(self, url):
        page = self.find_page_by_url(url)
        if page:
            return page[0]
        return self.save_page(url)

    def save_page(self, domin, url):
        """
        Save page and return id
        """
        hashed_url = hashlib.md5(url.encode('utf-8')).hexdigest()
        sql = INSERT_PAGE.format(domain=domain, url=url, hashed_url=hashed_url)
        con = self._connect()
        with con:
            cursor = con.cursor()
            cursor.execute(sql)
            return cursor.lastrowid

    def find_page_by_url(self, url):
        sql = FIND_PAGE_BY_URL.format(url=url)
        con = self._connect()
        with con:
            cursor = con.cursor()
            cursor.execute(sql)
            return cursor.fetchone()
