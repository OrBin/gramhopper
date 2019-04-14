import time


FLAKY_MAX_RUNS = 10
FLAKY_MIN_PASSES = 1
FLAKY_TIMEOUT_ON_FAILURE_SEC = 3


def delay_rerun(*args):  # pylint: disable=unused-argument
    time.sleep(FLAKY_TIMEOUT_ON_FAILURE_SEC)
    return True
