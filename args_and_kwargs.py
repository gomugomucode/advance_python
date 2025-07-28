

# # def person(name, age, rollno):
# #   print(f"Name is {name}. Age is {age} and Rollno. is {rollno}")

# # ?by using args?
# # Use when you want to pass multiple values (no names).
# # Inside function, they come as a tuple.

# # # Function to print information based on the number of arguments provided
# # def person(*args):
# #     # Check if 3 arguments are provided: Name, Age, and Rollno
# #     if len(args) == 3:
# #         print(f"Name is {args[0]}. Age is {args[1]} and Rollno. is {args[2]}")
# #     # Check if 2 arguments are provided: Name and Age
# #     elif len(args) == 2:
# #         print(f"Name is {args[0]}. Age is {args[1]}")
# #     # If only 1 argument (Name) is provided
# #     else:
# #         print(f"Name is {args[0]}")

# # # Tuple containing person details
# # data_tuple = ("Anupam", "20", "07")

# # # List containing person details
# # data_list = ["Ravi", "21"]

# # by using **kwargs
# # Use when you want to pass key=value pairs.
# # Inside function, they come as a dictionary.

# def person(**kwargs):
#   for key, value in kwargs.items():
#     print(f"Name is {key} and age is {value}")

# data_dict={
#     "Anupam":20,
#     "Anisha":19

# }




# # Main code execution
# # if __name__ == "__main__":

# #   # ?by *args
# #   #  # Passing them to the function using * to unpack
# #   #   person(*data_tuple)
# #   #   person(*data_list)
# #   #   person("Anupam") 

# #   # by kwargs
# #   person(**data_dict)


def master_function(x, *args, **kwargs):
    print(f"Normal parameter: {x}")
    
    if args:
        print("Args:")
        for i, arg in enumerate(args):
            print(f"  arg[{i}]: {arg}")
    
    if kwargs:
        print("Kwargs:")
        for key, value in kwargs.items():
            print(f"  {key}: {value}")

# --- Values to pass ---
x = 100
args_list = ['alpha', 'beta', 3.14]
kwargs_dict = {'mode': 'test', 'retries': 5}

# --- Call with unpacked list and dict ---
master_function(x, *args_list, **kwargs_dict)
