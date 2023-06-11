class BST:
    def __init__(self, data):
        self.data = data
        self.left = None
        self.right = None

    def insert(self, data):
        if data < self.data:
            if self.left is None:
                self.left = BST(data)
            else:
                self.left.insert(data)
        elif data > self.data:
            if self.right is None:
                self.right = BST(data)
            else:
                self.right.insert(data)

    def minvalue(self):
        temp = self
        while temp.left is not None:
            temp = temp.left
        return temp

    def deletenode(self, ddata):
        if self is None:
            return self

        if ddata < self.data:
            self.left = self.left.deletenode(ddata)
        elif ddata > self.data:
            self.right = self.right.deletenode(ddata)
           
        else:
            if self.left is None:
                temp = self.right
                self = None
                return temp
            elif self.right is None:
                temp = self.left
                self = None
                return temp
            else:
                temp = self.right.minvalue()
                self.data = temp.data
                self.right = self.right.deletenode(temp.data)
        return self

    def display(self):
        if self.left:
            self.left.display()
        print(self.data)
        if self.right:
            self.right.display()

b = BST(5)
b.insert(7)
b.insert(9)
b.insert(3)
b.insert(2)
b.deletenode(5)
b.display()