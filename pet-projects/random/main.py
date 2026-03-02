import random


print("/===Угадай число от 1 до 100===\\")
rand_num = random.randint(1, 100)
user_num = int(input("Введите число: \n"))
while user_num != rand_num:
    print("Вы не угадали(")
    if user_num > rand_num:
        print("Загаданное число меньше")

    if user_num < rand_num:
        print("Загаданное число больше")

    user_num = int(input("Введите другое число: \n"))
print(f'Вы угадали число {rand_num}!!!')