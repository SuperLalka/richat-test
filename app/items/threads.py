import threading
import time

from app.items.tasks import sync_products_with_stripe


def run_synchronizer():
    def synchronizer():
        while True:
            sync_products_with_stripe()
            time.sleep(60 * 60)

    thread = threading.Thread(target=synchronizer)
    thread.start()
