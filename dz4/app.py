import os
import argparse
import aiohttp
from requests import get
from pathlib import Path
from time import time
from threading import Thread
from multiprocessing import Process
from asyncio import ensure_future, gather, run, create_task


images = []
with open('images.txt', 'r') as f:
    for image in f.readlines():
        images.append(image.strip())

path_images = Path('images')

def image_download(url, dir_path=path_images):
    start_time_download_file = time()
    response = get(url)
    filename = url.split('/')[-1]
    with open(os.path.join(dir_path, filename), 'wb') as f:
        for data in response.iter_content(1024):
            f.write(data)
    print(f'    Загрузка {filename} заняла {time() - start_time_download_file:.2f} сек')

async def async_image_download(url, dir_path=path_images):
    start_time_download_file = time()
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            item = await response.read()
            filename = url.split('/')[-1]
            with open(os.path.join(dir_path, filename), 'wb') as f:
                f.write(item)
    print(f'    Загрузка {filename} заняла {time() - start_time_download_file:.2f} сек')

def parse():
    parser = argparse.ArgumentParser(description='Парсер изображений по URL-адресам')
    parser.add_argument('-u', '--urls', default=images, nargs='+', type=str, help='Список URL-адресов')
    return parser.parse_args()

def image_download_thread(urls):

    threads = []
    start_time = time()

    for url in urls:
        thread = Thread(target=image_download, args=[url], daemon=True)
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    print(f'\n******Загрузка заняла {time() - start_time:.2f} сек******\n\n')

def image_download_process(urls):

    start_time = time()
    processes = []

    for url in urls:
        process = Process(target=image_download, args=[url], daemon=True)
        processes.append(process)
        process.start()

    for process in processes:
        process.join()

    print(f'\n******Загрузка заняла {time() - start_time:.2f} сек******\n\n')

async def image_download_async(urls):
    tasks = []
    start_time = time()

    for url in urls:
        task = create_task(async_image_download(url))
        tasks.append(task)
    await gather(*tasks)

    print(f'\n******Загрузка заняла {time() - start_time:.2f} сек******')

if __name__ == '__main__':
    urls = parse().urls
    if not os.path.exists(path_images):
        os.mkdir(path_images)

    print(f'Загрузка {len(urls)} изображений через потоки:\n')
    image_download_thread(urls)

    print(f'Загрузка {len(urls)} изображений через процессы:\n')
    image_download_process(urls)

    print(f'Загрузка {len(urls)} изображений асинхронным методом:\n')
    run(image_download_async(urls))