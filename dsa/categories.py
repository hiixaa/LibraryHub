class CategoryNode:
    def __init__(self, name, item_count=0):
        self.name = name
        self.item_count = item_count
        self.children = []

    def add_child(self, child):
        self.children.append(child)


def create_category_tree():
    root = CategoryNode("Library", 0)

    root.add_child(CategoryNode("Biography", 1))
    root.add_child(CategoryNode("Fiction", 1))
    root.add_child(CategoryNode("History", 1))
    root.add_child(CategoryNode("Magazines", 1))
    root.add_child(CategoryNode("Reference", 1))

    technology = CategoryNode("Technology", 0)
    technology.add_child(CategoryNode("Programming", 1))
    technology.add_child(CategoryNode("Software Engineering", 1))

    root.add_child(technology)

    return root


def print_tree(node, level=0):
    print("  " * level + f"{node.name} ({node.item_count})")

    for child in node.children:
        print_tree(child, level + 1)


def count_items(node, category_name):
    if node.name == category_name:
        return count_subtree_items(node)

    for child in node.children:
        result = count_items(child, category_name)

        if result is not None:
            return result

    return None


def count_subtree_items(node):
    total = node.item_count

    for child in node.children:
        total += count_subtree_items(child)

    return total

def count_subtree_items_iterative(node):
    total = 0
    stack = [node]

    while stack:
        current = stack.pop()
        total += current.item_count

        for child in current.children:
            stack.append(child)

    return total

def path_to(node, category_name):
    if node.name == category_name:
        return [node.name]

    for child in node.children:
        result = path_to(child, category_name)

        if result is not None:
            return [node.name] + result

    return None


if __name__ == "__main__":
    root = create_category_tree()

    print("CATEGORY TREE")
    print_tree(root)

    print("\nITEM COUNTS")
    print("Technology:", count_items(root, "Technology"))
    print("Library:", count_items(root, "Library"))

    print("\nCATEGORY PATHS")
    print("Software Engineering:", path_to(root, "Software Engineering"))
    print("Cooking:", path_to(root, "Cooking"))

    print("\nRECURSION VS ITERATION")

    recursive_count = count_subtree_items(root)
    iterative_count = count_subtree_items_iterative(root)

    print("Recursive count:", recursive_count)
    print("Iterative count:", iterative_count)