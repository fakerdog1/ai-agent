from functions.get_files_info import get_files_info
from functions.write_file import get_file_content
from functions.write_file import write_file
from functions.run_python import run_python_file

calc_info = get_files_info("calculator", ".")
print(calc_info)

pkg_info = get_files_info("calculator", "pkg")
print(pkg_info)

bin_info = get_files_info("calculator", "/bin")
print(bin_info)

back_info = get_files_info("calculator", "../")
print(back_info)

main_char = get_file_content("calculator", "main.py")
print(main_char)

pkg_char = get_file_content("calculator", "pkg/calculator.py")
print(pkg_char)

cat_char = get_file_content("calculator", "/bin/cat")
print(cat_char)

non_exst_char = get_file_content("calculator", "pkg/does_not_exist.py")
print(non_exst_char)

lorem = write_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum")
print(lorem)
more = write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet")
print(more)
invalid = write_file("calculator", "/tmp/temp.txt", "this should not be allowed")
print(invalid)

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


