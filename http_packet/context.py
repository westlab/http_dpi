from multiprocessing import Queue


config = dict(
        db='interop2015',
        user='interop',
        password='interop',
        host='quercus.westlab'
        )


class Context:
    daos = dict(
            http_request=HttpRequest(**config)
            )

    queues = dict(
            http_request=Queue()
            )

context = Context()
