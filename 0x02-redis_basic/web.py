#!/usr/bin/env python3
"""
In this tasks, we will implement a get_page function
(prototype: def get_page(url: str) -> str:).
The core of the function is very simple.
It uses the requests module to obtain
the HTML content of a particular URL and returns it.

Inside get_page track how many times a particular URL was
accessed in the key "count:{url}" and cache the
result with an expiration time of 10 seconds.

Tip: Use http://slowwly.robertomurray.co.uk to
simulate a slow response and test your caching.

Bonus: implement this use case with decorators.
"""
from functools import wraps
import requests as req
import redis


redis_cache = redis.Redis()


def count_url_access(method):
    """counts the no of times a url is accessed"""
    @wraps(method)
    def count(url):
        url_key = url
        cached_data = redis_cache.get(url_key)
        if cached_data:
            return cached_data.decode("utf-8")

        count_key = 'count:{}'.format(url)
        html = method(url)
        redis_cache.incr(count_key)
        redis_cache.setex(url_key, 10, html)
        return html
    return count


@count_url_access
def get_page(url: str) -> str:
    """requests a url and returns the HTML content"""
    html = req.get(url)
    return html.text
