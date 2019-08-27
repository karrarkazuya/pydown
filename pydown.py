#!/usr/bin/python3
import sys
import time
from urllib.request import Request, urlopen


def start(url):
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})

    file_name = url.split('/')[-1]
    stream = urlopen(req)
    f = open(file_name, 'wb')
    meta = stream.info()
    file_size = int(meta['content-length'])

    file_size_readable = readableSize(file_size)

    print("Downloading: " + str(file_name) + " Size: " + str(file_size_readable))

    file_size_dl = 0
    block_sz = 1024
    while True:
        start = int(round(time.time() * 1000))
        buffer = stream.read(block_sz)
        if not buffer:
            break

        file_size_dl += len(buffer)
        f.write(buffer)
        try:
            end = int(round(time.time() * 1000))
            executeTime = end - start  # in ms
            executeTime = float(executeTime * 0.001)  # convert to seconds
        except:
            pass
        if executeTime < 0.01:
            block_sz = block_sz * 2
        elif executeTime > 1:
            if block_sz > 1024:
                block_sz = block_sz / 2

        if executeTime > 0:
            secondsToHit = 1 / executeTime
            speed = getSpeed(block_sz, secondsToHit)
            status = str(speed) + " - " + str(readableSize(file_size_dl)) + " of " + str(file_size_readable) + ", " + str(
                round((file_size_dl * 100. / file_size), 2)) + "%, "+str(findTimeLeft(file_size, file_size_dl, block_sz, secondsToHit))
            print(status)
    f.close()
    status = "0.0 kb/s - " + str(readableSize(file_size_dl)) + " of " + str(file_size_readable) + ", 100.0%, done"
    print(status)


def readableSize(data):
    if data > (1024 * 1024 * 1024):
        return str(round(data / (1024 * 1024 * 1024), 2)) + " GB"
    elif data > (1024 * 1024):
        return str(round(data / (1024 * 1024), 2)) + "MB"
    elif data > 1024:
        return str(round((data / 1024), 2)) + " KB"
    return str(data) + " B"


def getSpeed(block_sz, time):
    data = ((block_sz / 1024) * time)
    if data > (1024 * 1024 * 1024):
        return str(round(data / (1024 * 1024 * 1024), 2)) + " TB/s"
    elif data > (1024 * 1024):
        return str(round(data / (1024 * 1024), 2)) + " GB/s"
    elif data > 1024:
        return str(round((data / 1024), 2)) + " MB/s"
    return str(round(data, 2)) + " KB/s"


def findTimeLeft(total_size, reached_size, block_sz, time):
    total_size = total_size - reached_size
    speed = ((block_sz / 1024) * time)  # KB/S
    tank = 0
    left = 0
    while tank < total_size:
        tank = tank + (speed * 1024)
        left = left + 1
    if left > (60 * 60):
        left = str(int(left / (60 * 60)))+" hours left"
    elif left > 60:
        left = str(int(left / 60))+" mins left"
    else:
        left = str(int(left))+" seconds left"
    return left


if __name__ == '__main__':
    try:
        start(sys.argv[1])
    except:
        print("Error: No url given.")

