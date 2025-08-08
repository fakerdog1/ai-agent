from functions.run_python import run_python_file


one = run_python_file("calculator", "main.py")
print(one)
two = run_python_file("calculator", "main.py", ["3 + 5"])
print(two)
three = run_python_file("calculator", "tests.py")
print(three)
four = run_python_file("calculator", "../main.py")
print(four)
five = run_python_file("calculator", "nonexistent.py")
print(five)
