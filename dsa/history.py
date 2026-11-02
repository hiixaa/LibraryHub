class Node:
    def __init__(self, loan):
        self.loan = loan
        self.next = None


class BorrowHistory:
    def __init__(self):
        self.head = None
        self.size = 0

    def add(self, loan):
        node = Node(loan)
        node.next = self.head
        self.head = node
        self.size += 1

    def get_all(self):
        loans = []
        current = self.head

        while current:
            loans.append(current.loan)
            current = current.next

        return loans

    def delete(self, loan_id):
        current = self.head
        previous = None

        while current:
            if current.loan.loan_id == loan_id:
                if previous is None:
                    self.head = current.next
                else:
                    previous.next = current.next

                self.size -= 1
                return True

            previous = current
            current = current.next

        return False

    def reverse(self):
        previous = None
        current = self.head

        while current:
            next_node = current.next
            current.next = previous
            previous = current
            current = next_node

        self.head = previous

    def second_from_end(self):
        if self.head is None or self.head.next is None:
            return None

        slow = self.head
        fast = self.head

        # Move fast two nodes ahead.
        fast = fast.next.next

        while fast:
            slow = slow.next
            fast = fast.next

        return slow.loan

    def __len__(self):
        return self.size