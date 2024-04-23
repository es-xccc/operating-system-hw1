import threading
import collections
import time
import random

# buffer 大小
BUFFER_SIZE = 4

# 創建共用 buffer
buffer = collections.deque(maxlen=BUFFER_SIZE)

# 創建兩個 semaphore
empty = threading.Semaphore(BUFFER_SIZE)
full = threading.Semaphore(0)

# 創建一個 mutex lock
mutex = threading.Lock()

def producer(num):
    for i in range(1, 11):
        # 等待 buffer 有空位
        empty.acquire()
        # 鎖住，將物品放入 buffer
        mutex.acquire()
        buffer.append(i)
        print(f"Producer {num}: Produced item {i}")
        print(f"Producer {num}: Buffer: {list(buffer)}")
        print()
        # 放完釋放鎖
        mutex.release()
        # 通知消費者有新的物品可消費
        full.release()
        # 隨機睡眠一段時間
        time.sleep(random.randint(0, 5) / 10)
    print(f"*****Producer {num} finished.*****")

def consumer(num):
    for _ in range(1, 11):
        # 等待 buffer 有物品可消費
        full.acquire()
        # 鎖住，從 buffer 取出物品
        mutex.acquire()
        item = buffer.popleft()
        print(f"Consumer {num}: Consumed item {item}")
        print(f"Consumer {num}: Buffer: {list(buffer)}")
        print()
        # 拿完釋放鎖
        mutex.release()
        # 通知生產者有空位可放入新的物品
        empty.release()
        # 隨機睡眠一段時間
        time.sleep(random.randint(0, 10) / 10)
    print(f"*****Consumer {num} finished.*****")

# 創建生產者和消費者 threads 各 2 個
producer_threads = [threading.Thread(target=producer, args=(i+1,)) for i in range(2)]
consumer_threads = [threading.Thread(target=consumer, args=(i+1,)) for i in range(2)]

# 啟動 threads
for thread in producer_threads + consumer_threads:
    thread.start()

# 等待 threads 結束
for thread in producer_threads + consumer_threads:
    thread.join()

print("All done.")