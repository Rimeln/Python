class LinkedList:
    class __Node:
        def __init__(self, value):
            self.value = value
            self.next = None

        def __repr__(self):
            return f"value={self.value}"

    def __init__(self):
        self.__head = None
        self.__tail = None

    def add_first(self, value):
        new_node = self.__Node(value)
        if self.__is_empty():
            self.__initialize(new_node)
        else:
            new_node.next = self.__head
            self.__head = new_node

    def add_last(self, value):
        new_node = self.__Node(value)
        if self.__is_empty():
            self.__initialize(new_node)
        else:
            self.__tail.next = new_node
            self.__tail = new_node

    def remove_first(self):
        if self.__is_empty():
            raise ValueError("LinkedList is empty")

        removed_value = self.__head.value

        if self.__has_one_node():
            self.__reset()
        else:
            next = self.__head.next
            self.__head.next = None
            self.__head = next

            return removed_value

    def remove_last(self):
        if self.__is_empty():
            raise ValueError("LinkedList is empty")

        removed_value = self.__tail.value

        if self.__has_one_node():
            self.__reset()
        else:
            prev = self.__get_node_before_last()
            prev.next = None
            self.__tail = prev

        return removed_value

    def remove(self, value):
        if self.__is_empty():
            raise ValueError("LinkedList is empty")

        if self.__head.value == value:
            self.remove_first()
            return

        if self.__tail.value == value:
            self.remove_last()
            return

        current = self.__head
        prev = self.__head

        while current.next:
            if current.value == value:
                prev.next = current.next
                current.next = None
                return

            prev = current
            current = current.next

        raise ValueError("Value not found in the list")

    def get_nth_from_end(self, n):
        if self.__is_empty():
            raise ValueError("LinkedList is empty")

        if n <= 0:
            raise ValueError("Invalid value of n")

        current = self.__head

        for _ in range(n):
            if current is None:
                raise ValueError("n is larger than size of the list")

            current = current.next

        prev = self.__head

        while current:
            current = current.next
            prev = prev.next

        return prev.value

    def reverse(self):
        if self.__is_empty() or self.__has_one_node():
            return

        prev = None
        current = self.__head

        while current:
            next_node = current.next
            current.next = prev

            prev = current
            current = next_node

        self.__tail = self.__head
        self.__head = prev

    def get_midle(self):
        if self.__is_empty():
            raise ValueError("LinkedList is empty")

        slow = self.__head
        fast = self.__head

        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next

        return slow.value

    def __get_node_before_last(self):
        if self.__is_empty() or self.__has_one_node():
            return None
        current = self.__head
        while current.next != self.__tail:
            current = current.next

        return current


    def __has_one_node(self):
        return self.__head == self.__tail

    def __reset(self):
        self.__head = self.__tail = None

    def __is_empty(self):
        return self.__head is None

    def __initialize(self, node):
        self.__head = self.__tail = node