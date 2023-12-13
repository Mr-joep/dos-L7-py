import aiohttp
import asyncio
import time

async def check_website_once(url):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                response.raise_for_status()
                print(f"Website {url} is online.")
    except aiohttp.ClientError as e:
        print(f"Website {url} is down. Error: {e}")

async def make_request(session, url):
    try:
        async with session.get(url) as response:
            response.raise_for_status()
            return 1
    except aiohttp.ClientError:
        return 0

async def monitor_website(url, duration=10, max_concurrent_requests=50):
    start_time = time.time()
    request_count = 0

    try:
        async with aiohttp.ClientSession() as session:
            while time.time() - start_time < duration:
                tasks = [make_request(session, url) for _ in range(max_concurrent_requests)]
                request_count += sum(await asyncio.gather(*tasks))

                time_elapsed = time.time() - start_time
                if time_elapsed >= 1:
                    print(f"Requests per second: {request_count / time_elapsed:.2f}")
                    start_time = time.time()
                    request_count = 0

    except KeyboardInterrupt:
        pass

    total_time = time.time() - start_time
    average_requests_per_second = request_count / total_time if total_time > 0 else 0
    print(f"\nAverage requests per second: {average_requests_per_second:.2f}")

if __name__ == "__main__":
    website_url = "http://192.168.154.139"

    # Step 1: Check if the website is online
    asyncio.run(check_website_once(website_url))

    # Step 2 and 3: Monitor the website for a specified duration
    asyncio.run(monitor_website(website_url, duration=5, max_concurrent_requests=4000))
