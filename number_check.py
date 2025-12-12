
num = [2, 4, 6, 0, 1]

def find_min_max(numbers):
    if not numbers:
        return None, None

    maximum = numbers[0]
    minimum = numbers[0]

    for i in numbers[1:]:
        if i > maximum:
            maximum = i
        elif i < minimum:
            minimum = i

    return minimum, maximum

smallest, largest = find_min_max(num)

print(f"The list is: {num}")
print(f"The smallest number is: {smallest}")
print(f"The largest number is: {largest}")

