from requests import Session
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from os import sys


RETRY_COUNT = 5
RETRY_BACKOFF_FACTOR = 1


def http_retry():
    strategy = LoggingRetry(
        total=RETRY_COUNT,
        backoff_factor=RETRY_BACKOFF_FACTOR,
        status_forcelist=[503],
        allowed_methods=["POST"]
    )
    adapter = HTTPAdapter(max_retries=strategy)
    s = Session()
    s.mount("https://", adapter)
    s.mount("http://", adapter)
    return s


class LoggingRetry(Retry):
    def increment(self, *args, **kwargs):
        self.log_increment()
        return super().increment(*args, **kwargs)

    def log_increment(self):
        count = self.retry_count()
        if count == 0:
            return
        if count == 1:
            self.log_failed_http_call()
        if count != RETRY_COUNT:
            self.log_retrying()
        # TODO: last retry failure results in exception
        #           requests.exceptions.RetryError
        #       which needs to be caught in top-level handler.

    def log_failed_http_call(self):
        request = self.failed_request()
        print("{} failed".format(request.method), file=sys.stderr)
        print("URL={}".format(request.url), file=sys.stderr)
        print("STATUS={}".format(request.status), file=sys.stderr)

    def log_retrying(self):
        message = "Retrying in {} seconds ({}/{})".format(
            self.next_backoff_time(),
            self.retry_count(),
            RETRY_COUNT - 1
            )
        print(message, file=sys.stderr, flush=True)

    def retry_count(self):
        return len(self.history)

    def failed_request(self):
        return self.history[-1]

    def next_backoff_time(self):
        return self.backoff_time(self.retry_count())

    def backoff_time(self, n):
        """"
        Retry documentation is at
        https://urllib3.readthedocs.io/en/latest/reference/urllib3.util.html
        It says the backoff algorithm is:
           {backoff factor} * (2 ** ({number of retries} - 1))
        With backoff_factor==1, this gives successive sleeps of:
           [ 0.5, 1, 2, 4, 8, 16, 32, ... ]
        However, self.get_backoff_time() _actually_ returns:
           [ 0, 2, 4, 8 16, 32, ... ]
        It appears this is the value of just-finished sleep.
        Zero would look strange in the log message, so not using it.
        Empirically, this value _is_ the forthcoming sleep.
        """
        return RETRY_BACKOFF_FACTOR * (2 ** n)

    def total_backoff_time(self):
        return sum(self.backoff_time(n) for n in range(0, RETRY_COUNT))