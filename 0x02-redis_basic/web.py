#!/usr/bin/env python3
"""web module
"""
import redis
import requests
from typing import Callable
from functools import wraps

r = redis.Redis()


def count_requests(method: Callable) -> Callable:
    """
    count requests decorate
    """
    @wraps(method)
    def wrapper(url):
        """
        Wrapper for decorator functionality
        """
        r.incr(f"count:{url}")
        cache_html = r.get(f"cached:{url}")
        if cache_html:
            return cache_html.decode('utf-8')
        html = method(url)
        r.setex(f"cached:{url}", 10, html)
        return html
    return wrapper


@count_requests
def get_page(url: str) -> str:
    """
    get page method
    """
    request = requests.get(url)
    return request.text
