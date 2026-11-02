from dsa.recursion import factorial, fibonacci, sum_of_digits
from dsa.categories import (
    create_category_tree,
    count_items,
    count_subtree_items,
    count_subtree_items_iterative,
    path_to,
)


def test_factorial():
    assert factorial(5) == 120
    assert factorial(0) == 1


def test_factorial_negative():
    try:
        factorial(-5)
        assert False
    except ValueError:
        pass


def test_fibonacci():
    assert fibonacci(0) == 0
    assert fibonacci(1) == 1
    assert fibonacci(6) == 8


def test_fibonacci_negative():
    try:
        fibonacci(-2)
        assert False
    except ValueError:
        pass


def test_sum_of_digits():
    assert sum_of_digits(1234) == 10
    assert sum_of_digits(5) == 5
    assert sum_of_digits(0) == 0
    assert sum_of_digits(-123) == 6


def test_count_items():
    root = create_category_tree()

    assert count_items(root, "Technology") == 2
    assert count_items(root, "Library") == 7
    assert count_items(root, "Cooking") is None


def test_print_tree(capsys):
    root = create_category_tree()

    from dsa.categories import print_tree
    print_tree(root)

    output = capsys.readouterr().out

    assert "Library (0)" in output
    assert "Technology (0)" in output
    assert "Programming (1)" in output


def test_recursive_and_iterative_counts():
    root = create_category_tree()

    assert count_subtree_items(root) == 7
    assert count_subtree_items_iterative(root) == 7


def test_path_to_category():
    root = create_category_tree()

    assert path_to(root, "Software Engineering") == [
        "Library",
        "Technology",
        "Software Engineering",
    ]

    assert path_to(root, "Cooking") is None