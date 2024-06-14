import os
import asyncio
import requests
from dotenv import load_dotenv
from googleapiclient.discovery import build
from db import create_table, create_connection, fetch_rows
from image_download import download_image_to_db, download_image_as_file

load_dotenv()

CX = os.getenv('CX')
KEY = os.getenv('KEY')
GOOGLE_API_VERSION = os.getenv('GOOGLE_API_VERSION')


async def search_image(search_keyword: str, number_of_images: int):
    search_result = []
    no_more_image = False

    service = build(
        "customsearch", GOOGLE_API_VERSION, developerKey=KEY
    )

    resource = service.cse()
    request = resource.list(q=search_keyword, cx=CX)
    response = request.execute()

    total_results = response['queries']['request'][0]['totalResults']
    items_per_page = response['queries']['request'][0]['count']

    for i in range(0, int(total_results), items_per_page):
        if no_more_image:
            break
        else:
            request = resource.list(q=search_keyword, cx=CX, start = i + items_per_page)
            response = request.execute()

            results = response.get('items', [])

            for image in results:
                if len(search_result) >= number_of_images:
                    no_more_image = True
                    break

                image_title = image['title']

                try:
                    if not image['pagemap']['metatags'][0].get('og:image'):
                        image_url = image['pagemap']['cse_image'][0]['src'] if image['pagemap'].get('cse_image') else None
                        if not image_url:
                            continue
                    else:
                        image_url = image['pagemap']['metatags'][0]['og:image']
                except KeyError as e:
                    continue

                try:
                    # simulate browser request
                    headers = {
                        'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; WOW64) '
                                      'AppleWebKit/537.36 (KHTML, like Gecko) '
                                      'Chrome/27.0.1453.94 '
                                      'Safari/537.36'
                    }
                    requests.head(
                        image_url,
                        timeout=5,
                        allow_redirects=False,
                        headers=headers
                    )
                    path_to_image = await asyncio.get_running_loop().run_in_executor(None, download_image_to_db, image_url, image_title)
                    search_result.append(path_to_image)

                except requests.exceptions.RequestException as e:
                    continue

    return len(search_result)


if __name__ == "__main__":
    create_table()

    loop = asyncio.get_event_loop()

    terminate = False
    while not terminate:
        search_keyword = str(input('Enter your search keyword: '))
        number_of_images_to_search = int(input('Enter number of images you want to download: '))

        loop.run_until_complete(search_image(search_keyword, number_of_images_to_search))

        y_or_n = str(input('Terminate? (y/n): '))
        terminate = True if y_or_n == 'y' else False


    print('###### Rows #######')
    fetch_rows('Image')
