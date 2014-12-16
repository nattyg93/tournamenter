#Author: Nathanael Gordon
#Created: 2014-12-16

Class Menu:
    
    def __init__(self, exitString = "Return to previous menu"):
        self.options = []
        self.exitString = exitString
    
    def printMenu(self, values):
        validResult = False
        
        while not validResult:
            count = 0
            result = 0
            for tup, func in self.options:
                if count == 0:
                    print("{0}\n".format(tup))
                else:
                    print("{0} - {1}".format(count, tup))
                count += 1
                
            print("0 - {0}\n".format(self.exitString))
            
            try:
                result = int(input("Selection: "))
                if result < 0 or result >= count: #must be >= since count with be one greater than the largest number printed
                    raise ValueError()
                
                validResult = True
            except ValueError:
                print("\nPlease enter a number in the range of 0 - {0}\n".format(count-1))
            
        return self.options[1](values)
    
    def addOption(self, string, func):
        self.options.append((string, func))
    
    