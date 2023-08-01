import multiprocessing as mp


def timeout(func, args=(), kwargs={}, time_limit=999999, default=None):
    """
    Runs a function, interrupting it and returning
    a 'default' value after a time limit.
    kudos: https://stackoverflow.com/a/13822315/1251716
    :param func: the function to run
    :param args: function args
    :param kwargs: function keyword args
    :param time_limit: time limit, in seconds
    :param default: default value to be returned on timeout
    :return:
    """
    pool = mp.Pool(processes=1)
    result = pool.apply_async(func, args=args, kwds=kwargs)
    try:
        val = result.get(timeout=time_limit)
    except mp.TimeoutError:
        pool.terminate()
        return default
    else:
        pool.close()
        pool.join()
        return val
