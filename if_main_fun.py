

import os

# print(os.listdir("/"))

def main():
  print("hey there")


# if __name__=="__main__"    this function is used to protect  the code . while using this function , it prints the contents or function on it only if the file is run directly .  if we are importing the file into another file then the function called after imported is only printed  the other doesnot called  or run in another file

if __name__=="__main__":
  main()

