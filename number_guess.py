
import random

random_num = random.randint(0,99)
# print(random_num)

def num_gues(num , random_num):
    if num > random_num:
        print("Please ,Enter small number ")
    elif num < random_num:
        print("Please ,Enter bigger number ")
    elif num == random_num:
        print("You have enter correct answer ")
    
num = int(input("Enter the random number you guess : "))
num_gues(num , random_num)


