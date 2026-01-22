def calculate(num1: float, num2: float, operation: str):
    if operation == "+":
        return num1 + num2
    elif operation == "-":
        return num1 - num2
    elif operation == "*":
        return num1 * num2
    elif operation == "/":
        if num2 == 0:
            return "Cannot divide by zero"
        return num1 / num2
    else:
        return "Invalid operation"
