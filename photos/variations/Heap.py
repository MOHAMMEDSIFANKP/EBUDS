class Heap:
    def __init__(self):
        self.heap = []

    def minheap(self, array):
        self.buildheap(array)

    def buildheap(self, array):
        self.heap = array
        for i in range(self.parent(len(self.heap)-1), -1, -1):
            self.shiftdown(i)

    def shiftdown(self, curr):
        end = len(self.heap) - 1
        left = self.leftChild(curr)
        while left <= end:
            right = self.rightChild(curr)
            if right <= end and self.heap[right] > self.heap[left]:
                toshift = right
            else:
                toshift = left
            if self.heap[curr] < self.heap[toshift]:
                self.heap[curr], self.heap[toshift] = self.heap[toshift], self.heap[curr]
                curr = toshift
                left = self.leftChild(curr)
            else:
                return

    def shiftup(self, curr):
        parent = self.parent(curr)
        while curr > 0 and self.heap[parent] < self.heap[curr]:
            self.heap[curr], self.heap[parent] = self.heap[parent], self.heap[curr]
            print(curr)
            print(parent)
            curr = parent
            parent = self.parent(curr)

    def peek(self):
        return self.heap[0]

    def remove(self):
        self.heap[0], self.heap[-1] = self.heap[-1], self.heap[0]
        self.heap.pop()
        self.shiftdown(0)

    def parent(self, i):
        return (i-1) // 2

    def leftChild(self, i):
        return 2*i + 1

    def rightChild(self, i):
        return 2*i + 2

    def display(self):
        print(self.heap)

array = [6, 2, 8, 1, 5, 15, 3]
h = Heap()
h.minheap(array)
# h.remove()
h.display()
