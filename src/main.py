from Jumplist import JumpList
from JumplistWithSplit import JumpList2
from JumplistSimple import JumpList3
import random

def reverseOrder(list, n=8, vis=False):
    j = 0
    for i in range(n, 0, -1):
        list.insert(i)
        if vis:
            list.create_visualization(str(j) + " after insert " + str(i))
            j += 1

def randomInsert(list, elements=None, n=50, vis=False):
    i = 0    
    if elements is None:
        elements = [random.randint(1, 3*n) for _ in range(n)]
    # print(elements)
    for x in elements:
        list.insert(x)
        # if not list.holdsProperty(list.head, list.n):
        #     print("List does not hold the property")
        if vis:
            list.create_visualization(str(i) + " after insert " + str(x), list.__class__.__name__)
        i += 1

def customList(list, input):
    u = list.head
    for x,z in input:
        if u.jump is not None and u.jump.back is u:
            u.jump.back = None
        if x is None:
            u.jump = None
        else:
            u.jump = list.getNode(x)
            u.jump.back = u
        u.next_size = z
        u = u.next

def main():
    n = 25
    elements = [random.randint(0, 3*n) for _ in range(n)]

    j = JumpList3()

    randomInsert(j, elements=elements, vis=True)

    
if __name__ == "__main__":
    main()