def factorial(n):
    if n < 0:
        raise ValueError("Factorial is not defined for negative numbers")

    if n == 0:
        return 1

    return n * factorial(n - 1)


def fibonacci(n):
    if n < 0:
        raise ValueError("Fibonacci is not defined for negative numbers")

    if n == 0:
        return 0

    if n == 1:
        return 1

    return fibonacci(n - 1) + fibonacci(n - 2)


def sum_of_digits(n):
    n = abs(n)

    if n < 10:
        return n

    return (n % 10) + sum_of_digits(n // 10)


if __name__ == "__main__":
    print("Factorial of 5:", factorial(5))
    print("Fibonacci of 6:", fibonacci(6))
    print("Sum of digits of 1234:", sum_of_digits(1234))