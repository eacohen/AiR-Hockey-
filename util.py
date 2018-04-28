# Various useful utility functions

# Return the position in the list with the minimum value
# If the list contains just None, then None is returned
def min_pos(items):

    min_val = None
    min_pos = None

    for pos in range(0,len(items)):
        
        new_val = items[pos]
        if not(new_val is None):
            # Only compare items when they're not None
            
            if min_val is None or new_val < min_val:
                min_val = new_val 
                min_pos = pos

    return min_pos

            #data = fifo.read(4)
            #print(data)
            #print(type(data))
            #num = int.from_bytes(data, byteorder="little")
            #n = len(data);
            #print("data length is " + str(n));
            #print("Received: " + str(num));
            #print(a)
# Returns a number whose binary form consists of n 1's
def bin_1(n):
    return (1 << n) - 1


# Converts raw data from the kinect fifo to queue data
def kin_2_queue_dat(kin_in):
    int_form = int.from_bytes(kin_in, byteorder="little")
    y = 4 * (int_form & bin_1(12))
    x = 4 * ((int_form >> 12) & bin_1(12))
    paddle = (int_form >> 24) & bin_1(8)
    return(paddle, x, y)
