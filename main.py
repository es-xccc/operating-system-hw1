import threading
import queue
import time
import random

# 定義隊列
q = queue.Queue()

# 生產者類
class Producer(threading.Thread):
    def run(self):
        for i in range(10):
            item = random.randint(1, 100)
            q.put(item)
            print(f"Producer put item: {item} in queue.")
            print(f"Queue now: {list(q.queue)}")  # 顯示隊列內容
            time.sleep(1)

# 消費者類
class Consumer(threading.Thread):
    def run(self):
        while True:
            item = q.get()
            if item is None:
                break
            print(f"Consumer got item: {item} from queue.")
            print(f"Queue now: {list(q.queue)}")  # 顯示隊列內容
            time.sleep(2)
            q.task_done()

# 創建生產者和消費者
producer = Producer()
consumer = Consumer()

# 啟動生產者和消費者
producer.start()
consumer.start()

# 等待生產者結束
producer.join()

# 發送None給消費者,讓其結束
q.put(None)

# 等待消費者結束
q.join()

print("All tasks completed.")