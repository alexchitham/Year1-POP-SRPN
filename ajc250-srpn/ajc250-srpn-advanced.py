 #This is your SRPN file. Make your changes here.



# Defining variables that will be needed in multiple functions within the program
stack = []
ignore = False
counter = 0
rValues = [1804289383,846930886,1681692777,1714636915,1957747793,424238335,719885386,1649760492,596516649,1189641421,1025202362,1350490027,783368690,1102520059,2044897763,1967513926,1365180540,1540383426,304089172,1303455736,35005211,521595368]
recCommands = ["*","%","/","+","-","d","r","#","=","^"]
recOperators = ["*","%","/","+","-","^"]
numForInFix = False

# The main function that processes the user input, it takes the user's input as a parameter
def process_command(command):

  splitCommand = command.split() # Splits the input on whitespaces 
  
  for newCommand in splitCommand: # We iterate through each element in the list after it's been split
    if newCommand != " " and newCommand != "":  
      if newCommand == "#":
        global ignore 
        ignore = not ignore # Uses the variable ignore to filter out commands when a # is inputted
        
      if (ignore == False and newCommand != "#"):
        ignoreNumber = False
        octalNumber = 0
        try:
          testCommand = int(newCommand) # Checks to see if the input is a number, and call the numberInput function if it is
          numberInput(newCommand,testCommand,octalNumber,ignoreNumber)
          
        except ValueError:
          if type(newCommand) == str: # Calls the string input function if its not a number
            stringInputs(newCommand)
                
          else:
            return None

# Adds a value to the stack and takes a number as a parameter, does the saturation check to see if a number is too big or too small
def append(value):
  if value > 2147483647:
    stack.append(2147483647)
  elif value < -2147483648:
    stack.append(-2147483648)
  else: stack.append(value)

# Pops the last two numbers off the stack
def popStack():
   stack.pop()
   stack.pop()

# Processes all number inputs, needs 4 variables passed into it as it also checks for octal numbers too
def numberInput(newCommand,testCommand,octalNumber,ignoreNumber):
    if (newCommand[0] == "0" and testCommand != 0): # If its octal
      if (newCommand == "08" or newCommand == "09"):
        newCommand = testCommand # Special case where these numbers are treated as denary starting with a 0
      else:
        for num in newCommand:
          if (num == "8" or num == "9"):
            ignoreNumber = True # Ignored if the octal number has an 8 or 9 in it
        if (ignoreNumber == False):
          for x in range(len(newCommand)-1,0,-1):
            power = (len(newCommand)) - 1 - x
            octalNumber += (int(newCommand[x])) * (8**(power))
          append(octalNumber) # Calculates value of octal number and appends to the stack      
    if len(stack) == 23:
      print("Stack overflow.")
    else: 
      if (ignoreNumber == False and octalNumber == 0):
        newCommand = testCommand
        append(newCommand) # If not octal, just add the number to the stack
  
# Processes all operator inputs, takes the user input as a parameter
def operatorInput(newCommand):
    try: # Tries to look at the last 2 items on the stack
      n2 = stack[-1]
      n1 = stack[-2]
      # For each operator, performs it, removes last two numbers from stack, then appends the answer
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
        if n2 == 0:
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
    except: # If there aren't two items on the stack, is an underflow
      print("Stack underflow.")

# Deals with all complex inputs. This includes where numbers and operators are written with no spaces, and this function iterates through each character in the input string to process. It is able to do basic infix, as well as all reverse polish inputs. Takes the user input string as a parameter
def obscureInput(newCommand):
  # Variables to keep track of what previous characters were, used for the infix part of this function.
  global number
  global operator
  global numOp
  global numForInFix
  global previousNum
  global currentOp
  number = False
  operator = False
  numOp = False
  numForInFix = False
  inFix = False
  counter1 = -1
  partNumber = ""

  for i in newCommand: # Iterates through each character in the input
    counter1 = counter1 + 1
    try: # See if it's a number, and concatenate if many digits are written next to each other
      partCommand = int(i)
      if partCommand == 100:
        partCommand = 0
      operator = False
      if number == False:
        number = True
        numForInFix = True
        partNumber = i
      else:
        partNumber = partNumber + i

      # If at the last character in the string, recursely call the process_command function on the 2 numbers and the operator
      if counter1 == len(newCommand) - 1:
        if numOp == True:
          process_command(previousNum)
          process_command(partNumber)
          process_command(currentOp)
          inFix = True
        else:  process_command(partNumber)


    except ValueError: # If one of the characters is a string
      # If there is a number, then operator, then number, process the 3 in the correct order separately, so the program can manage it
      if numOp == True and number == True:
        process_command(previousNum)
        process_command(partNumber)
        process_command(currentOp)
        inFix = True
      
      if i in recOperators:
        if operator == True:
          process_command(currentOp)
        operator = True
        number = False
        currentOp = i

      # This incorporates r as that also adds a number to the stack, but is not a number itself
      if i == "r":
        number = True
        numForInFix = True
        operator = False
        partNumber = ""
        if numOp == True:
          process_command(previousNum)
          process_command(i)
          process_command(currentOp)
          inFix = True
        else: process_command(i)
      
      # Works out if a second number is present in the string if an operator is found, and processes the one number and operator if not
      elif numForInFix == True and i in recOperators:
        numOp = True
        currentOp = i
        number = False
        operator = True
        numberFollows = False
        previousNum = partNumber
        for y in range(counter1,len(newCommand)):
          isNum = isNumber(newCommand[y])
          if isNum == True or newCommand[y] == "r":
            numberFollows = True
        if numberFollows == False:
          process_command(currentOp)
        if counter1 == len(newCommand) - 1 and numberFollows == True:
          process_command(previousNum)
          process_command(currentOp)
        elif counter1 == len(newCommand) - 1:
          process_command(previousNum)      
      
      
      elif number == True and inFix == False:
        process_command(partNumber)
        process_command(i)
        partNumber = ""
        number = False

      # If the character is not one of the ones that is recognised
      else:
        if i not in recCommands:
          unrecString = 'Unrecognised operator or operand "' + i + '".'
          print(unrecString)
        else:
          if i == "=" and inFix == True:
            if newCommand[counter1-1] == "r":
              print (rValues[counter - 1])
            else: print(partNumber)
          else:
            process_command(i)

# Processes all the inputs that are not numbers
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
    
    # If a string is not recognised, then the obscure function is called
    elif newCommand not in recCommands:
      obscureInput(newCommand)
    # Otherwise the input must be an operator
    else:
      operatorInput(newCommand)

# Checks to see if a character is a number or not
def isNumber(element):
  try:
    element = int(element)
    return True
  except: return False


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
