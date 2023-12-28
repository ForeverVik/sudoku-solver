from copy import deepcopy

class Node():
    def __init__(self, board=None):
        self.board = deepcopy(board)
        self.prev = None
        self.next = None
        self.test = None
        self.count = 0
    
    def __str__(self):
        for i in self.board:
            for j in i:
                if j == 0 or (type(j) != int and len(j) > 1):
                    out = '.'
                else:
                    if type(j) == int:
                        out = j
                    else:
                        out = j[0]
                print(f"{out} ", end="")
            print()
        return ""

    def eq(self, other):
        for i in range(len(self.board)):
            for j in range(len(self.board)):
                if self.board[i][j] != other.board[i][j]:
                    return False
        return True

class doublyLinkedList():
    def __init__(self):
        self.emptyBoard = [[0,0,0,0,0,0,0,0,0],
                           [0,0,0,0,0,0,0,0,0],
                           [0,0,0,0,0,0,0,0,0],
                           [0,0,0,0,0,0,0,0,0],
                           [0,0,0,0,0,0,0,0,0],
                           [0,0,0,0,0,0,0,0,0],
                           [0,0,0,0,0,0,0,0,0],
                           [0,0,0,0,0,0,0,0,0],
                           [0,0,0,0,0,0,0,0,0]]
        self.startNode = None
    
    def printLinkedList(self):
        n = self.startNode

        if n is None:
            return
        while True:
            print(f"Board: {n.count} Test: {n.test}\n")
            for i in n.board:
                for j in i:
                    if j == 0 or (type(j) != int and len(j) > 1):
                        out = '.'
                    else:
                        if type(j) == int:
                            out = j
                        else:
                            out = j[0]
                    print(f"{out} ", end="")
                print()

            if n.next is None:
                break
                   
            n = n.next

    def insertToEnd(self, board, test="", delIfSame=False):
        if self.startNode is None:
            newNode = Node(board)
            self.startNode = newNode
            return

        current = self.startNode
        while current.next is not None:
            current = current.next
        newNode = Node(board)
        newNode.test = test
        newNode.count = current.count + 1
        current.next = newNode
        newNode.prev = current

        if delIfSame and current.prev is not None and current.eq(current.prev):
            self.delLast()

    def printLast(self):
        current = self.startNode
        while current.next is not None:
            current = current.next
        print(current.board)
    
    def delLast(self):
        n = self.startNode
        if n.next == None:
            n = None

        while n.next.next is not None:
            n = n.next
        n.next = None

    def delAfterCurrent(self, current):
        while current.next is not None:
            self.delLast()
        