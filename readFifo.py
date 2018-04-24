import os



FIFO = "/tmp/fifo"

with open(FIFO, mode='rb') as fifo:
    print("FIFO opened!")
    while True:
        data = fifo.read(4)
       # bts = bytes(data, "utf-8")
        print(data)
        print(type(data))
        num = int.from_bytes(data, byteorder="little")
        n = len(data);
        print("data length is " + str(n));
        print("Received: " + str(num));
