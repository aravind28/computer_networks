import threading

class thread_sample(threading.Thread):
    def run(self):
        for i in range(10):
            print i, threading.currentThread().getName()

x = thread_sample(name="abc")
y = thread_sample(name="xyz")
x.start()
y.start()

