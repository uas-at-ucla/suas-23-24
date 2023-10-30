import time
import random
import threading
import requests

HOST = "http://vision:8003"


def run():
    while True:
        try:
            requests.get(HOST, timeout=1)
        except requests.RequestException:
            print("cannot connect", HOST)
            time.sleep(1)


if __name__ == "__main__":
    for _ in range(4):
        thread = threading.Thread(target=run)
        thread.daemon = True
        thread.start()

    while True:
        time.sleep(1)
