# -*- coding: utf-8 -*-
import string
from functools import wraps
from random import choice

_sequence_counters = {}
_cache_unique = {}

def infinite():
    """
        auto inc generator
    """
    i = 0
    while 1:
        yield i
        i += 1



def text(length, choices=string.ascii_letters):
    """ returns a random (fixed length) string

    :param length: string length
    :param choices: string containing all the chars can be used to build the string

    .. seealso::
       :py:func:`rtext`
    """
    return ''.join(choice(choices) for x in range(length))


def sequence(prefix, cache=None):
    """
    generator that returns an unique string

    :param prefix: prefix of string
    :param cache: cache used to store the last used number

    >>> next(sequence('abc'))
    'abc-0'
    >>> next(sequence('abc'))
    'abc-1'
    """
    if cache is None:
        cache = _sequence_counters
    if cache == -1:
        cache = {}

    if prefix not in cache:
        cache[prefix] = infinite()

    yield "{0}-{1}".format(prefix, next(cache[prefix]))



def unique(func, num_args=0, max_attempts=100, cache=None):
    """
    wraps a function so that produce unique results

    :param func:
    :param num_args:

    >>> import random
    >>> choices = [1,2]
    >>> a = unique(random.choice, 1)
    >>> a,b = a(choices), a(choices)
    >>> a == b
    False
    """
    if cache is None:
        cache = _cache_unique

    @wraps(func)
    def wrapper(*args):
        key = "%s_%s" % (str(func.__name__), str(args[:num_args]))
        attempt = 0
        while attempt < max_attempts:
            attempt += 1
            drawn = cache.get(key, [])
            result = func(*args)
            if result not in drawn:
                drawn.append(result)
                cache[key] = drawn
                return result

        raise MaxAttemptException()

    return wrapper
