class Node(object):
    def __init__(self, data):
        self.data = data
        self.next = None


class Linked_list:
    def __init__(self, head=None):
        self.head = head

    # append()
    def append(self, node):
        # 1- head node
        if self.head == None:
            self.head = node
        # 2- not head node
        # create point to test
        else:
            temp = self.head
            while temp.next:
                temp = temp.next
            temp.next = node

    # is_empty()
    def is_empty(self):
        return self.head == None

    # get_length()
    def get_length(self):
        length = 0
        current = self.head
        while current:
            current = current.next
            length += 1
        return length

    # insert()
    def insert(self, index, node):
        # go to the index
        # 1- if is the head
        if index == 1:
            temp = self.head
            self.head = node
            node.next = temp
        else:
            current = self.head
            while index - 1 > 1:
                current = current.next
                index -= 1
            temp = current.next
            current.next = node
            node.next = temp

    # remove()
    def remove(self, index, node):
        # border judgement
        length = get_length()

        if index < 1 or index > length:
            raise IndexError("Index out of range")

        # if remove the first node
        if index == 1:
            self.head = self.head.next
        else:
            current = self.head
            while index - 1 > 1:
                current = current.next
                index -= 1
            current.next = current.next.next

    # reverse the linklist
    # *** reverse方法链表中的难点
    # 在一次链表的操作过程当中需要使用三个引用变量来进行
    def reverse(self):
        prev = None
        current = self.head

        while current:
            next_node = current.next
            current.next = prev
            prev = current
            current = next_node
        self.head = prev

    # print the linkedlist
    def print_ll(self):
        current = self.head
        while current:
            print(current.data)
            current = current.next


if __name__ == "__main__":
    ll = Linked_list(Node(2))
    ll.append(Node(12))
    ll.append(Node(23))
    ll.print_ll()

    ll.insert(2, Node(5))
    ll.print_ll()

    print(ll.get_length())

    ll.reverse()
    ll.print_ll()
