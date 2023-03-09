 #This is your SRPN file. Make your changes here.



# Defining variables that will be needed in multiple functions within the program
stack = []
ignore = False
counter = 0
rValues = [1804289383,846930886,1681692777,1714636915,1957747793,424238335,719885386,1649760492,596516649,1189641421,1025202362,1350490027,783368690,1102520059,2044897763,1967513926,1365180540,1540383426,304089172,1303455736,35005211,521595368]
recCommands = ["*","%","/","+","-","d","r","#","=","^"]


# The main function that processes the user input, it takes the user's input as a parameter
def process_command(command):

  splitCommand = command.split() # Splits the command input on whitespaces
  
  for newCommand in splitCommand:  # We then treat each element as a separate input so we iterate through them all

    if newCommand != " " and newCommand != "":  # Ignores whitespace
      if newCommand == "#":
        global ignore
        ignore = not ignore # Changes the value of ignore if there's a # for comments
        
      if (ignore == False and newCommand != "#"): # Filtering out comments
        ignoreNumber = False
        octalNumber = 0
        try:
          testCommand = int(newCommand) # If the input is a number, pass it and other necessary values into the numberInput function
          numberInput(newCommand,testCommand,octalNumber,ignoreNumber)
          
        except ValueError:
          if type(newCommand) == str:
            stringInputs(newCommand) # If the input is not a number, is a string, so pass it into the stringInputs function
                
          else:
            return None

#If the size of the number is too big or too small, we add the max / min numbers instead onto the stack
def append(value):
  if value > 2147483647: 
    stack.append(2147483647) 
  elif value < -2147483648:
    stack.append(-2147483648)
  else: stack.append(value) # Otherwise add the number to the stack

# Removes the top 2 items off the stack
def popStack():
   stack.pop()
   stack.pop()

#Process all number inputs, needs 4 variables passed into as it also processes octal numbers
def numberInput(newCommand,testCommand,octalNumber,ignoreNumber):
    if (newCommand[0] == "0" and testCommand != 0): # If it's in the octal format 
      if (newCommand == "08" or newCommand == "09"):
        newCommand = testCommand # Special case where these are treated as denary
      else:
        for num in newCommand:
          if (num == "8" or num == "9"):
            ignoreNumber = True # The octal number is ignored if it contains an 8 or 9
        if (ignoreNumber == False):
          # Iterates through the octal number and finds its value
          for x in range(len(newCommand)-1,0,-1):
            power = (len(newCommand)) - 1 - x
            octalNumber += (int(newCommand[x])) * (8**(power))
          append(octalNumber) # Calls the append function, passing in the octal number     
    if len(stack) == 23:
      print("Stack overflow.") # 23 is the maximum capacity of the stack
    else: 
      if (ignoreNumber == False and octalNumber == 0):
        newCommand = testCommand
        append(newCommand) # If it's not an octal number, just add it to the stack
  

def operatorInput(newCommand):
    try: # Try to look at the last 2 items of the stack
      n2 = stack[-1]
      n1 = stack[-2]

      # For each operator, pop the last 2 numbers, perform the calculation and append the answer to the stack
      if newCommand == "*":
        popStack()
        append(n1 * n2)
      elif newCommand == "+":
        popStack()
        append(n1 + n2)
      elif newCommand == "-":
        popStack()
        append(n1 - n2)
      elif newCommand == "/":
        if n2 == 0: # Causes an error if we divide by 0
          print("Divide by 0.")
        else: 
          popStack()
          append(n1 // n2)
      elif newCommand == "%":
        popStack()
        append(n1 % n2)
      elif newCommand == "^":
        if n2 < 0:
          print("Negative power.")
        else: 
          popStack()
          append(n1 ** n2)
    # If there aren't two items in the stack when an operator is inputted, then we output a stack underflow
    except: 
      print("Stack underflow.")

# For inputs where numbers and operators are written with no spaces, this function iterates through each character within the string to split it up
def obscureInput(newCommand): # Takes the entire user input as a parameter
  global number
  number = False
  counter1 = -1
  partNumber = ""
  for i in newCommand: # Iterates through the whole string
    counter1 = counter1 + 1 # Keeps track of the index of the character
    try: # If the character is a number
      partCommand = int(i)
      if partCommand == 100:
        partCommand = 0
      if number == False:
        number = True
        partNumber = i
      else:
        partNumber = partNumber + i # Concatenate the numbers together

      if counter1 == len(newCommand) - 1:
        process_command(partNumber)

    except ValueError: # If it's a string
      if number == True:
        process_command(partNumber)
        process_command(i)
        partNumber = ""
        number = False
      else:
        if i not in recCommands:
          append(0)
        else:
          process_command(i)

# Deals with all user inputs that aren't just numbers
def stringInputs(newCommand):
    if newCommand == "d":
      if len(stack) == 0:
        print(-2147483648)
      else:  
        for x in stack:
          print(x)
        return None     
    elif newCommand == "r":
      global counter
      if len(stack) == 23:
        print("Stack overflow.")
      else: 
        append(rValues[counter])
        if counter < 21:
          counter = counter + 1
        else: counter = 0
    elif newCommand == "=":
      if len(stack) != 0:  
        print(stack[-1])
      else:
        print("Stack empty.")
    
    # A string input that's not a recognised command is passed to obscureInput
    elif newCommand not in recCommands:
      obscureInput(newCommand)
    # Otherwise call the operator input function
    else:
      operatorInput(newCommand)




#This is the entry point for the program.
#Do not edit the below
if __name__ == "__main__": 
    while True:
        try:
            cmd = input()
            pc = process_command(cmd)
            if pc != None:
                print(str(pc))
        except:
            exit()
