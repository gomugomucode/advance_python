# making triamgle


# height = int(input("Enter height: "))

# for i in range(1, height + 1):
#     for j in range(i):
#         print("*", end="")
#     print()



# Inverted Triangle

# height = int(input("Enter height: "))

# for i in range( height + 1 ,0 ,-1):
#     for j in range(i):
#         print("*", end="")
#     print()





# making pryamid

# height = int(input("Enter height: "))

# for i in range(1, height + 1):

#     # print spaces
#     for j in range(height - i):
#         print(" ", end="")

#     # print stars
#     for k in range(2 * i - 1):
#         print("*", end="")

#     # move to next line
#     print()




# making dimand
height = int(input("Enter height: "))

# top half
for i in range(1, height + 1):
    for j in range(height - i):
        print(" ", end="")
    for k in range(2 * i - 1):
        print("*", end="")
    print()

# bottom half
for i in range(height - 1, 0, -1):
    for j in range(height - i):
        print(" ", end="")
    for k in range(2 * i - 1):
        print("*", end="")
    print()
