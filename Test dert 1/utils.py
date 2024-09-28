import time
from requests.exceptions import ChunkedEncodingError

def download_with_retries(version, format, retries=3, delay=5):
    for attempt in range(retries):
        try:
            dataset = version.download(format)
            return dataset
        except ChunkedEncodingError as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            if attempt < retries - 1:
                print(f"Retrying in {delay} seconds...")
                time.sleep(delay)
            else:
                print("All retry attempts failed.")
                raise