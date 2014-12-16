#Author: Nathanael Gordon
#Created: 2014-12-16

Class Menu:
    
    def printMenu(self, strings = None, exitString = "Return to previous menu"):
        validResult = False
        
        while not validResult:
            count = 0
            result = 0
            for string in strings:
                if count == 0:
                    print("{0}\n".format(string))
                else:
                    print("{0} - {1}".format(count, string))
                count += 1
                
            print("0 - {0}\n".format(exitString))
            
            try:
                result = int(input("Selection: "))
                if result < 0 or result >= count: #must be >= since count with be one greater than the largest number printed
                    raise ValueError()
                
                validResult = True
            except ValueError:
                print("\nPlease enter a number in the range of 0 - {0}\n".format(count-1))
            
        return result