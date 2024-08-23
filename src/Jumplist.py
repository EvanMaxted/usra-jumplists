'''
Doubly-linked jumplist - next and jump pointers have prev and back respectively
node.next_size keeps track of the size of the next sublist
When inserting, we start at the head of the sublist and look forwards to see if a merge should happen
  - 4 straight next pointers or 2 straight jump pointers will be merged
If we see 2 jumps in a row where neither jump is "good" we merge them
  - we define a good jump as one that jumps over 1/3 of the elements in the sublist
We "push" and "pull" jumps forwards and backwards when merging
  - this means if we merge on u, u.next will jump to u's old jump and cascade through u's sublist
  - similarly, if v were the last node (u.jump.jump) before the merge, then u.jump will jump to v.prev and cascade backwards
    through u.jump's sublist
'''
from math import floor
from Node import Node
import graphviz

class JumpList:
    def __init__(self):
        self.head = Node(-float('inf'))
        self.n = 1
    
    #add x to the jumplist
    def insert(self, x):
        path = self.pathSearch(x)
        u = path[-1]
        if u.data == x:
            return
        v = Node(x)
        v.next = u.next
        if v.next is not None:
            v.next.prev = v
        u.next = v
        v.prev = u
        self.n += 1
        
        #updates the sublist sizes for all nodes on the path to x and return the head of x's sublist
        u, n = self.updateNextSizes(path, x)

        #goes through x's sublist to see if anything needs merged
        self.lookForwards(u, n)

    #updates the sublist sizes based on where x was inserted and returns the head of x's sublist with the size
    def updateNextSizes(self, path, x):
        n = self.n
        lastJump = None #keep track of the head of the sublist we insert into
        lastN = None #keep track of the size of the sublist we insert into
        for u in path:
            if u.jump is None:
                n -= 1
                if u.back is not None: #this means something jumps into u so we'd be exiting the sublist
                    lastJump = u.prev
                    lastN = n
                continue
            if u.jump.data > x:
                u.next_size += 1
                n = u.next_size
            else:
                n = n - u.next_size - 1
            lastJump = u
            lastN = n

        u = self.head
        n = self.n
        if lastJump is not None: #make sure the dummy node isn't the sublist head
            u = lastJump.next
            n = lastN

        #return the head of the sublist we inserted into and the size of the sublist
        return u, n
    
    #goes through the sublist starting at u and checks if anything needs merged
    def lookForwards(self, u, n):
        nCount = 0   #keep track of the number of next nodes we see in a row
        jCount = 0   #keep track of the number of jumps we see in a row
        leftNext = u #keep track of the leftmost node we travel "next" from
        leftJump = u #keep track of the leftmost node we jump from
        i = 0
        while u.next is not None and i < 6: #look forwards through the sublist x was inserted into
            if n == 0: #if we reach the end of the sublist stop searching
                break
            if u.jump is not None:
                nCount = 0
                if jCount == 0:
                    leftJump = u
                jCount += 1
                jump_size = n - u.next_size - 1 
                if self.goodJump(n, u.next_size): #we don't merge jumps that are already "good"
                    jCount = 0
                    break
                u = u.jump
                if jCount == 2:
                    self.mergeJump(leftJump)
                    break
                n = jump_size
            else:
                nCount += 1
                u = u.next
                n -= 1
                if jCount == 0 and u.back is not None: #this means we've exited the sublist
                    break
                if nCount == 4:
                    self.mergeNext(leftNext)
                    break
            i += 1

    #returns a list of all the nodes seen on the search path for x
    def pathSearch(self, x):
        u = self.head
        path = []
        left = u  #keep track of the leftmost jump node for merging
        count = 0 #keep track of the number of jumps we've seen
        n = self.n
        while u.next is not None:
            path.append(u)
            if u.jump is not None:
                if self.goodJump(u, n): #we don't merge jumps that are over n/3
                    count = 0
                if count == 0:
                    left = u
                count += 1
                if count == 2: #merge if we see 2 "bad" jumps in a row
                    count = 0
                    self.mergeJump(left)
                if u.jump.data <= x:
                    n = n - u.next_size - 1
                    u = u.jump
                elif u.next.data <= x:
                    n = u.next_size
                    u = u.next
                    count = 0
                else:
                    return path
            else:
                if u.next.data <= x:
                    n -= 1
                    u = u.next
                else:
                    return path
        path.append(u)
        return path
    
    #returns the largest node less than or equal to x
    def search(self, x):
        return self.pathSearch(x)[-1]
    
    #a jump is good if it jumps over 1/3 of the remaining elements
    def goodJump(self, u, n):
        if 2/3 < (u.next_size+1)/n: #if the jump is over 2/3, split it
            self.split(u)
        return 1/3 <= (u.next_size+2)/n     

    #takes 5 straight next nodes and creates a jump between the first middle and last
    def mergeNext(self, u):
        u.jump = u.next.next
        u.jump.back = u
        u.next_size = 1
        u = u.jump
        u.jump = u.next.next
        u.jump.back = u
        u.next_size = 1

    #merges 2 straight jumps into 1
    def mergeJump(self, u):
        #pushing the jumps forwards for the first half of the merge
        v = u.jump
        w = u.next
        x = u.jump
        temp_next_size = 0
        next_size = u.next_size

        if w == x:
            w.back = None
        while w is not x and x is not None: #pushes jumps forwards
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

        j = 1
        while v.jump is None:
            v = v.next
            j += 1
        u.jump = v.jump
        u.jump.back = u
        u.next_size += v.next_size + j

        #pulling the jumps backwards for the second half of the merge
        w = v.jump
        if w.prev == v:
            v.jump = None
        while v is not None and v is not w.prev and v is not w.prev: #pulls jumps backwards
            w = w.prev
            v.jump = w
            v.next_size -= 1
            temp = w.back
            w.back = v
            v = temp

        return u.jump
    
    def split(self, u):
        return
    
    #checks if every node holds the property that it jumps between 1/3 and 2/3 of the elements in the sublist
    def holdsProperty(self, u, n):
        if u is None or n <= 6 or u.next_size < 5:
            return True
        if u.jump is None:
            return True
        if 2/3 < (u.next_size+1)/n:
            return False
        if 1/3 > (u.next_size+2)/n:
            return False  
        
        return self.holdsProperty(u.next, u.next_size) and self.holdsProperty(u.jump, n-u.next_size-1)
    
    #tracks the total potential of the list, where we define the potential of a node u as floor(|n/2 - u.next_size - 1|)
    def potential(self, u, n):
        if u is None or n <= 1:
            return 0
        if u.jump is None or u.jump is u.next:
            return floor(abs(n/2 - u.next_size - 1)) + self.potential(u.next, n-1)
        return floor(abs(n/2 - u.next_size - 1)) + self.potential(u.next, u.next_size) + self.potential(u.jump, n-u.next_size-1)
    
    #for testing purposes
    def getNode(self, x):
        u = self.head
        while u.next is not None:
            if u.jump is not None and u.jump.data <= x:
                u = u.jump
            elif u.next.data <= x:
                u = u.next
            else:
                return u
        return u

    def display(self):
        u = self.head
        prefix = ""
        while u is not None:
            print(prefix, end="")
            print("(", end="")
            print(u.data, end="")
            print(" -> ", end="")
            if u.jump is not None:
                print(u.jump.data, end="")
            else:
                print("nil", end="")
            print(f"{{{u.next_size}}}", end="")
            print(")", end="")
            prefix = ", "
            u = u.next
        print()

    def create_visualization(self, filename, dir="untitled"):
        graph = graphviz.Digraph(name='jumplist', node_attr={'shape': 'rectangle'})
        graph.attr('graph', rankdir='LR')
        with graph.subgraph(name='backbone') as backbone, graph.subgraph(name='jumps') as jumps:
            curr = self.head
            while curr is not None:
                graph.node(str(curr.data))
                if curr.next:
                    backbone.edge(str(curr.data), str(curr.next.data), weight='1', color='blue')
                if curr.jump:
                    jumps.edge(str(curr.data), str(curr.jump.data), weight='0', color='red')
                curr = curr.next
        graph.render(filename, "views/"+dir, format='png', cleanup=True)