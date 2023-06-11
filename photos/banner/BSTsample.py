class BST:
    def __init__(self,data):
        self.data = data
        self.left = None
        self.right = None
    def insertnode(self,data):
        if data < self.data:
            if self.left is None:
                self.left = BST(data)
            else:
                self.left.insertnode(data)
        elif data > self.data:
            if self.right is None:
                self.right = BST(data)
            else:
                self.right.insertnode(data)
        
    def search(self,sdata):
        if sdata == self.data:
            print(self.data,"founded")
        elif sdata < self.data:
            if self.left is None:
                print("value not found")
            else:
                self.left.search(sdata)
        elif sdata > self.data:
            if self.right is None:
                print("value not founded")
            else:
                self.right.search(sdata)
    # def minValue(self):
    #     temp = self.data
    #     if self.left is None:
    #          temp = self.data
    #     else:
    #         self.left.minValue()
    #     print("d",temp)
    #     return

    def print(self):
        if self.left:
            self.left.print()
        print(self.data)
        if self.right:
            self.right.print()
b = BST(5)
b.insertnode(8)
b.insertnode(2)
b.insertnode(4)
b.insertnode(3)
b.print()
b.search(2)
# b.minValue()
# b.deletion(2)
b.print()