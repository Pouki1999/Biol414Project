from tkinter import Tk
from queue import Queue

def main():
    q = Queue(maxsize=5)
    q.put((1,2))
    q.put(7)
    print(q.queue[0])
    print(q.queue[1])


if __name__ == '__main__':
    main()

