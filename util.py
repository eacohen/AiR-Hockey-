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
