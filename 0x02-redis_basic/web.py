import requests
import time
from functools import wraps

# Decorator function for caching and tracking
def cache_and_track(func):
    cache = {}  # Cache dictionary to store results
    counts = {}  # Dictionary to store access counts

    @wraps(func)
    def wrapper(url):
        # Check if URL is in cache and not expired
        if url in cache and time.time() < cache[url]['expiration']:
            cache[url]['count'] += 1  # Increment access count
            return cache[url]['content']

        # Retrieve the HTML content using requests
        response = requests.get(url)
        content = response.text

        # Update cache with the new content and expiration time
        cache[url] = {
            'content': content,
            'expiration': time.time() + 10  # Cache expires after 10 seconds
        }

        # Initialize access count if URL is accessed for the first time
        if url not in counts:
            counts[url] = 0
        counts[url] += 1  # Increment access count

        # Print the access count
        print(f"Access count for {url}: {counts[url]}")

        return content

    return wrapper

# Decorate the get_page function with the cache_and_track decorator
@cache_and_track
def get_page(url):
    return requests.get(url).text


# Example usage
print(get_page("http://slowwly.robertomurray.co.uk/delay/5000/url/http://www.example.com"))
time.sleep(5)
print(get_page("http://slowwly.robertomurray.co.uk/delay/5000/url/http://www.example.com"))
time.sleep(10)
print(get_page("http://slowwly.robertomurray.co.uk/delay/5000/url/http://www.example.com"))

