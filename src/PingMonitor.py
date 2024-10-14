# core
import time
import threading

def StartThread():
  while True:
    print ('.')
    time.sleep(5)

def start():
  thread = threading.Thread(target=StartThread)
  thread.start()
