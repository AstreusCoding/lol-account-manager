import threading

def thread_function(func, *args):
    """
    Wrapper for threading.Thread.
    :param func: function to be executed in thread
    :param args: arguments for function
    :return: thread object
    """
    t = threading.Thread(target=func, args=args)
    t.start()
    return t
    