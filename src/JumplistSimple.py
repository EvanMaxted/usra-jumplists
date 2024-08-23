'''
Simplifies the merge and split functionalities by no longer pushing and pulling
  - for a merge on u, we just have u.next jump to the old u.jump
  - for a split on u, we just have u jump to the end of the first jump inside its next sublist
Since we aren't pushing and pulling jumps, a merge can cause 2 nodes to jump into the same node.
This leads to sublist sizes being off by 1 for the inner node jumping to the same node.
Since we aren't pulling jumps anymore we don't need doubly-linked functionality for the jumps anymore.
  - it hasn't been removed since it's used for the "look forwards" while inserting but there should be a way to do it without
'''
from Jumplist import JumpList

class JumpList3(JumpList):                
    #merges 2 straight jumps into 1 without any shifting of inner jumps
    def mergeJump(self, u):
        v = u.jump

        j = 1
        while v.jump is None:
            v = v.next
            j += 1

        u.jump.back = None
        u.jump = v.jump
        u.next_size += v.next_size + j
        u.jump.back = u

        return u.jump
    
    #splits one jump into two jumps
    def split(self, u):
        v = u.next

        j = 1
        while v.jump is None:
            if v.next is None:
                return
            v = v.next
            j += 1
        if v is u.jump:
            return

        u.jump.back = None
        u.jump = v.jump
        u.next_size = v.next_size + j
        u.jump.back = u