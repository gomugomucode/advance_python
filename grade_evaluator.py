# marks = int(input("Enter the marks : "))

def mark_evaluate():
    nim = int(input("Enter the marks : "))    

    try:
        

        if nim > 100 :
                print("Number is out of range")
        else:
            if nim >= 90 and nim <= 100 :
                print("Grade is A+")
            elif nim >= 80 and nim <= 89 :
                    print("Grade is A")
            elif nim >= 70 and nim <= 79 :
                    print("Grade is B")
            elif nim >= 60 and nim <= 69 :
                    print("Grade is C")
            elif nim >= 50 and nim <= 59 :
                    print("Grade is D")
            elif nim < 50 and nim > 40 :
                    print("Grade is F")
                    print("You failed, but you’re close. Try again with courage.")       
    except ValueError:
        print("Invalid input! Please enter a valid numeric value.")

    except Exception as e:

        print(f"An unexpected error occurred: {e}") 
    



while True:
    mark_evaluate()


    userinput = input("Do you want to enter another mark? (yes/no):")
    if userinput.casefold() != "yes":
         print("See you soon")
         break


       
