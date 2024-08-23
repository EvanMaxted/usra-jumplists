'''
Implements split functionality for when jumps are too big (> 2/3).
  - "pull" jumps back on the first half, "push" jumps in the second half (opposite of a merge)
  - u will jump to u.next.jump and then u.next will jump to u.next.jump.prev and cascade
  - u.next.jump will jump to u.jump.prev and cascade
'''
from Jumplist import JumpList

class JumpList2(JumpList):    
    #splits one jump into two jumps
    def split(self, u):
        v = u.next
        q = u.jump

        #pulling the jumps backwards for the first half of the split
        j = 1
        while v.jump is None:
            if v.back is not None:
                return
            v = v.next
            j += 1
        if v is u.jump:
            return
        u.jump.back = None
        u.jump = v.jump
        u.jump.back = u
        u.next_size = v.next_size + j

        w = v.jump
        next_size = w.next_size
        while v is not None and v is not w.prev:
            w = w.prev
            v.jump = w
            v.next_size -= 1
            temp = w.back
            w.back = v
            v = temp
        if w.prev == v:
            v.jump = None

        #pushing the jumps forwards for the second half of the split
        u = u.jump
        v = u

        j = 1
        while v.jump is None:
            if v.next is None:
                return
            v = v.next
            j += 1
        x = v.jump
        u.jump = q
        u.jump.back = u
        u.next_size = v.next_size + j

        w = u.next

        if w == x:
            w.back = None
        while w is not x and x is not None:
            y = w.jump
            if w.jump is not None:
                w.jump.back = None
            w.jump = x
            w.jump.back = w
            temp_next_size = w.next_size
            w.next_size = next_size - 1
            next_size = temp_next_size
            x = y
            w = w.next