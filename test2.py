'''
Created on Dec 31, 2013

@author: Dang Minh Nguyen
'''
ALPHABET = 'abcdefghijklmnopqrstuvwxyz'
import pickle
import random
import copy

def addDeg1(a,b):
    return a^b

def multiple2Deg1(num1, num2, numVar = None):
    if type(num1) == type(1):
        num1 = convertVar(num1, numVar)
        num2 = convertVar(num2, numVar)
    size = len(num1)
    result = [[0 for i in range(0, size)] for j in range(0, size)]

    for i in range(0, size):
        for j in range(0,i):
            if num1[i] == 1 and num2[j] == 1:
                if num2[i] == 1 and num1[j] == 1:
                    result[i][j] = 0
                else:
                    result[i][j] = 1
            else:
                if num2[i] == 1 and num1[j] == 1:
                    result[i][j] = 1
    return result

def printDeg1(num1, numVar = None):
    if type(num1) == type(1):
        num1 = convertVar(num1, numVar)
    size = len(num1)
    result = ''
    for i in range(0,size):
        if num1[i] == 1:
            result += ALPHABET[i]
            result += '+'
    return result[:-1]

def printDeg2(deg2Poly):
    size = len(deg2Poly)
    result = ''
    for i in range(0,size):
        for j in range(0,i):
            if deg2Poly[i][j] == 1:
               result += ALPHABET[i] + ALPHABET[j] + '+'
    return result[-2::-1]

def checkEquivClass(multTable, zeroTermTable, verbose=False, letter=False):
    numVar = len(multTable[0][0])
    size = len(multTable)
    listOfClasses = [[] for i in range(0,size)]
##    checkedTerms = set(range(1,size))
    for i in range(1,size):
        listOfClasses[i].append(i)
        for j in range(1,i):
            if zeroTermTable[str(multTable[i][j])] == 0:
                listOfClasses[i].append(j)
        for j in range(i+1,size):
            if zeroTermTable[str(multTable[j][i])] == 0:
                listOfClasses[i].append(j)
        if verbose:
            if letter:
                print('[', end='')
                for k in listOfClasses[i]:
                    print(printDeg1(k,numVar),end=',')
                print(']')
            else:
                print(listOfClasses[i])
    return listOfClasses

def add2Deg2(a,b):
    numVar = len(a)
    result = [[0 for i in range(0,numVar)] for j in range(0,numVar)]
    for i in range(0,numVar):
        for j in range(0,i):
            result[i][j] = a[i][j] ^ b[i][j]
    return result

def convertVar(number,numVar):
    binary = bin(number)[2:]
    binary = binary.zfill(numVar)
    result = []
    for i in range(numVar):
        result.append(int(binary[i]))
    return result

def updateZeroList(zeroList, multTable, zeroTermTable, deg2Poly):
#     numVar = len(deg2Poly)
    tempList = []
    for term in zeroList:
        temp = add2Deg2(term, deg2Poly)
        if temp not in zeroList:
            tempList.append(temp)
            if str(temp) in zeroTermTable:
                zeroTermTable[str(temp)] = 0
    zeroList += tempList
    return

def zeroDeg2(numVar):
    return [[0 for i in range(0, numVar)] for j in range(0, numVar)]

def isStarGraph(zeroClasses):
    size = len(zeroClasses)
    myset = set(range(0,size))
    count = 0
    while len(myset) > 0:
        a = myset.pop()
        for i in zeroClasses[a]:
            for j in zeroClasses[a]:
                if i not in zeroClasses[j]:
                    return -1
        for i in zeroClasses[a]:
            if i != a:
                myset.remove(i)
        count += 1
    return count

class PolyField:
    numVar = 0
    size = 0
    multTable = []
    zeroTermTable = []
    zeroList = []
    listOfClasses = []
    marked_terms = set()
    allTerms = set()

    def __init__(self,numVar):
        self.numVar = numVar
        self.size = pow(2,numVar)
        str1 = 'MultTable' + str(numVar) + '.txt'
        str2 = 'zeroTermTable' + str(numVar) + '.txt'
        self.multTable = pickle.load(open(str1,'rb'))
        self.zeroTermTable = pickle.load(open(str2,'rb'))
        self.zeroList = [zeroDeg2(numVar)]
        self.listOfClasses = [[] for i in range(0,pow(2,numVar))]
        self.allTerms = set(range(1,self.size))
        self.marked_terms = set()

    def updateZeroList(self,deg2Poly):
        tempList = []
        for term in self.zeroList:
            temp = add2Deg2(term, deg2Poly)
            if temp not in self.zeroList:
                tempList.append(temp)
                if str(temp) in self.zeroTermTable:
                    self.zeroTermTable[str(temp)] = 0
        self.zeroList += tempList
        return

    def checkEquivClass(self, verbose=False, letter=False):
        """ Update the equivalent classes in the ring
        
        :param verbose whether or not to print out the list
        :param letter whether or not to use letters for variables
        """
        tempListOfClasses = [[] for i in range(0,self.size)]
        
        for i in range(1,self.size):
            tempListOfClasses[i].append(i)
            for j in range(1,i):
                if self.zeroTermTable[str(self.multTable[i][j])] == 0:
                    tempListOfClasses[i].append(j)
            for j in range(i+1,self.size):
                if self.zeroTermTable[str(self.multTable[j][i])] == 0:
                    tempListOfClasses[i].append(j)
            if verbose:
                if letter:
                    printStr = "["
                    for k in tempListOfClasses[i]:
                        printStr += printDeg1(k,self.numVar) + ','
                    printStr = printStr[:-1]
                    printStr += ']'
                    print(printStr)
                else:
                    print(tempListOfClasses[i])
        self.listOfClasses = tempListOfClasses
        return

    def checkStarGraph(self, verbose=False, letter=False):
        """ Check if the ring forms a star graph """
        temp = set()
        myset = set(range(1,self.size))
        count = 0
        while len(myset) > 0:
            a = myset.pop()
            for i in self.listOfClasses[a]:
                for j in self.listOfClasses[a]:
                    if i not in self.listOfClasses[j]:
                        return -1
            for i in self.listOfClasses[a]:
                if i != a and i in myset:
                    myset.remove(i)
            count += 1
            if (len(self.listOfClasses[a]) > 1):
                temp.update(set(self.listOfClasses[a]))
            if verbose:
                if letter:
                    printStr = "["
                    for k in self.listOfClasses[a]:
                        printStr += printDeg1(k,self.numVar) + ','
                    printStr = printStr[:-1]
                    printStr += ']'
                    print(printStr)
                else:
                    print(self.listOfClasses[a])
        self.marked_terms.update(temp)    
        return count+1

def main():


    
#     myring = PolyField(6)
#     myring.updateZeroList(multiple2Deg1(1,2,myring.numVar))
#     myring.updateZeroList(multiple2Deg1(12,16,myring.numVar))
#     myring.updateZeroList(multiple2Deg1(9,4,myring.numVar))
#     myring.updateZeroList(multiple2Deg1(8,18,myring.numVar))
#     myring.updateZeroList(multiple2Deg1(5,10,myring.numVar))
#     myring.updateZeroList(multiple2Deg1(17,6,myring.numVar))
#     myring.updateZeroList(multiple2Deg1(7,32,myring.numVar))
#     myring.updateZeroList(multiple2Deg1(20,48,myring.numVar))


##    print('Starting----')
##    target = [  72]
##    while True:
##        a = test(target)
##        if a != -1:
##            break
##        print('Restarting---')


    print('Initializing the ring set up--------------')
    myring = PolyField(7)
    idealTerms = [[1,2],[1,4],[2,4],[1,8],[2,8],[4,8],[103,87],[59,116],
                  [42,49],[57,17],[110,25],[34,74],[71,24],[121,75],
                  [108,65]]
    print(idealTerms)
    for term in idealTerms:
        a = multiple2Deg1(term[0],term[1],myring.numVar)
        myring.updateZeroList(a)
        print('Added to the ideal:',printDeg2(a),'=',
              printDeg1(term[0],myring.numVar),'x',
              printDeg1(term[1],myring.numVar),)
    
    
    print('Initializing complete---------------Checking-----')
        
    myring.checkEquivClass()
    count = myring.checkStarGraph()
    if count == -1:
        print('Is a star graph:',False)
    else:
        print('Is a star graph:', count)
     

    return

def test(target):
    print('Reinitializing the ring set up--------------')
    myring = PolyField(7)
    myring.updateZeroList(multiple2Deg1(1,2,myring.numVar))
    myring.updateZeroList(multiple2Deg1(1,4,myring.numVar))
    myring.updateZeroList(multiple2Deg1(4,2,myring.numVar))
    myring.updateZeroList(multiple2Deg1(1,8,myring.numVar))
    myring.updateZeroList(multiple2Deg1(2,8,myring.numVar))
    myring.updateZeroList(multiple2Deg1(4,8,myring.numVar))
    
    
    print('Added the starting terms')
    print('Reinitializing complete---------------Checking-----')
#     print('Length of markedTerms is', len(myring.marked_terms))
    myring.checkEquivClass()
    count = myring.checkStarGraph()
#     print(count)
    while count >= 72:
        temp = copy.deepcopy(myring.allTerms)
#         print('Len of allterms is', len(temp))
        temp = temp.difference(copy.deepcopy(myring.marked_terms))
        x = random.sample(temp,1)[0]
        temp.remove(x)
#             reset = False
        works = False
        tried = set()
#         print('x is',x)
#         print('len temp is', len(temp))
        while not works:

            temp2 = copy.deepcopy(temp).difference(tried)
#             print('len temp2 is', len(temp2))
            if len(temp2) == 0:
#                 print('Out of stuff')
                count = -1
                return -1
            i = random.sample(temp2,1)[0]
            if addDeg1(x,i) in myring.marked_terms:
                tried.add(i)
                pass
            else:
                temp.remove(i)
                myring.updateZeroList(multiple2Deg1(x,i,myring.numVar))
                print('Added the term (',x,',',i,')',sep='')
                break
#             if reset:
#                 temp.add(x)
#                 pass
        
        myring.checkEquivClass()
        count = myring.checkStarGraph()
   
        if count == -1:
            print('Is a star graph:',False)
            return -1
        else:
            print('Is a star graph:', count)
        if count in target:
            return count
    return -1
  
 
main()
