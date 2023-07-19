#!/usr/bin/env python3
"""
web module

This module provides a function to fetch HTML content from a given URL.
It also includes a decorator to track the number of requests made for a URL
and cache the HTML content with an expiration time of 10 seconds.
"""

import redis
import requests
import time
from typing import Callable
from functools import wraps

# Connect to Redis server
r = redis.Redis()

def count_requests(method: Callable) -> Callable:
    """
    count_requests decorator

    This decorator tracks the number of requests made for a particular URL and caches the result with an
    expiration time of 10 seconds using Redis.

    Args:
        method (Callable): The function to be decorated.

    Returns:
        Callable: The decorated function.
    """
    @wraps(method)
    def wrapper(url: str) -> str:
        """
        Wrapper for count_requests decorator functionality.

        Args:
            url (str): The URL for which HTML content is requested.

        Returns:
            str: The HTML content fetched from the URL.
        """
        # Increment the count for the URL key in Redis
        r.incr(f"count:{url}")

        # Check if the URL's HTML content is cached in Redis
        cache_html = r.get(f"cached:{url}")
        if cache_html:
            # If cached, return the cached HTML content
            return cache_html.decode('utf-8')

        # If not cached, fetch the HTML content using the original function
        html = method(url)

        # Cache the HTML content with an expiration time of 10 seconds
        r.setex(f"cached:{url}", 10, html)

        # Return the fetched HTML content
        return html
    return wrapper

@count_requests
def get_page(url: str) -> str:
    """
    get_page function

    This function fetches the HTML content from the given URL using the requests library.

    Args:
        url (str): The URL for which HTML content is requested.

    Returns:
        str: The HTML content fetched from the URL.
    """
    # Make a request to the given URL using requests library
    request = requests.get(url)
    # Return the HTML content of the response
    return request.text

# Example usage
if __name__ == "__main__":
    # Make requests to different URLs
    print(get_page("http://slowwly.robertomurray.co.uk/delay/5000/url/http://www.example.com"))  # This will take around 5 seconds
    print(get_page("http://slowwly.robertomurray.co.uk/delay/5000/url/http://www.example.com"))  # This will be almost instantaneous

    # Wait for 10 seconds and try again
    time.sleep(10)
    print(get_page("http://slowwly.robertomurray.co.uk/delay/5000/url/http://www.example.com"))  # This will take around 5 seconds again

