from operation import *


print("\t\t\t/---Калькулятор---\\")
while True:
    num1 = int(input("Введите первое число:"))
    operation = input("Выберите операцию:\nСложение (+)\nВычитание (-)\nУмножение (*)\nДеление (/)")
    while operation != "+" and operation != "-" and operation != "*" and operation !="/":
        print("Выбрана несуществующая операция")
        operation = input("Выберите операцию:\nСложение (+)\nВычитание (-)\nУмножение (*)\nДеление (/)")
    if operation == "/":
        num2 = int(input("Введите второе число:"))
        while num2 == 0:
            print("Нельзя делить на ноль")
            num2 = int(input("Введите второе число:"))
        print(f"Результат деления: {div(num1, num2)}")
    else:
        num2 = int(input("Введите второе число:"))
        if operation == "+":
            print(f"Результат сложения: {summa(num1, num2)}")
        if operation == "-":
            print(f"Результат вычитания: {sub(num1, num2)}")
        if operation == "*":
            print(f"Результат умножения: {sub(num1, num2)}")
    stop = input("Введите (stop) если хотите закрыть калькулятор, если хотите продолжить, нажмите Enter\n")
    if stop == "stop":
        break
print("Калькулятор завершил работу")