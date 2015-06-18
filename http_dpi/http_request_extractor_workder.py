from multiprocessing import Process

from http_dpi.dtos import HttpRequest


class HttpRequestExtractorWorker(Process):
    def __init__(self, context):
        self._context = context
        # logger
        super().__init__()

    def run(self):
        http_request_dao = self._context.daos['http_request']
        http_request_queue = self._context.queues['http_request']
        while True:
            http_request = http_request_queue.get()
            if not isinstance(http_request, HttpRequest):
                break
            http_request_dao.save(http_request)
