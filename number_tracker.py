# user_list = []

# def largest_smallest(user_list):
#     if len(user_list) >= 2 :
#             largest = user_list[i]
#             smallest = user_list[i]
#             for i in range(len(user_list)+1):
#                 if user_list[i] > user_list[i+1]:
#                     smallest = user_list[i+1]
#                 elif user_list[i] < user_list[i+1]:
#                     largest = user_list[i]
#             print(f"The largest number in the list is {largest}")
#             print(f"The smallest number in the list is {smallest}")
#     else:
#         print("The largest and smallest number cannot be calculated")


# def sun_calculate(user_list):
#     sun = 0
#     for i in range(len(user_list)):
#         sum = sum + user_list[i]
#     print(f"The sum is {sum}")


# while True:
#     user_input = input("Enter the number (or type exit to quit): ")
    
#     if user_input.lower() == "exit":
#         print(f"The number in the list are {user_list}")
#         print(f"The total count of number in the list is {len(user_list)}")
#         largest_smallest(user_list)
#         sun_calculate(user_list)
#         break
        
#     user_list.append(user_input)




numbers = []


def find_largest_smallest(nums):
    if len(nums) == 0:
        print("No numbers entered.")
        return

    largest = nums[0]
    smallest = nums[0]

    for n in nums:
        if n > largest:
            largest = n
        if n < smallest:
            smallest = n

    print(f"Largest number: {largest}")
    print(f"Smallest number: {smallest}")


def calculate_sum(nums):
    total = 0
    for n in nums:
        total += n
    print(f"Sum: {total}")


while True:
    user_input = input("Enter a number (or type exit): ")

    if user_input.lower() == "exit":
        print(f"\nNumbers entered: {numbers}")
        print(f"Count: {len(numbers)}")
        find_largest_smallest(numbers)
        calculate_sum(numbers)
        break

    try:
        num = int(user_input)
        numbers.append(num)
    except ValueError:
        print("Invalid input. Please enter a number.")
