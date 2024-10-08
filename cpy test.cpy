
#int counterFunctionCalls
#int multiplier

def max3(x,y,z):
#{
    #int m
    global counterFunctionCalls
    counterFunctionCalls = counterFunctionCalls + 1
    if x>y and x>z:
        m = x
    elif y>x and y>z:
        m = y
    else:
        m = z
    return m
#}


def fib(x):
#{
    global counterFunctionCalls
    counterFunctionCalls = counterFunctionCalls + 1
    if x<0:
        return -1
    elif x==0 or x==1:
        return 1
    else:
        return fib(x-1)+fib(x-2)
#}
     
     
def isPrime(x):
#{
    ## declarations for isPrime ##
    #int i

    def divides(x,y):
    #{
        ## body of divides ##
        global counterFunctionCalls
        counterFunctionCalls = counterFunctionCalls + 1
        if y == (y//x)*x:
            return 1
        else:
            return 0
    #}

    ## body of isPrime ##
    global counterFunctionCalls
    counterFunctionCalls = counterFunctionCalls + 1
    i = 2
    while i < x:
    #{
        if divides(i,x) == 1:
            return 0
        i = i + 1
    #}
    return 1
#}

     
def quad(x):
#{
    #int y
    
    ## nested function sqr ##
    def sqr(x):
    #{
        ## body of sqr ##
        global counterFunctionCalls
        counterFunctionCalls = counterFunctionCalls + 1
        return x*x
    #}
    
    ## body of quad ##
    global counterFunctionCalls
    counterFunctionCalls = counterFunctionCalls + 1
    y = sqr(x)*sqr(x)
    return y
#}


def leap(year):
## returns 1 if year is a leap year, otherwise it returns 0 ##
#{
    global counterFunctionCalls
    counterFunctionCalls = counterFunctionCalls + 1
    if year%4==0 and year%100!=0 or year%400==0:
        return 1
    else:
        return 0 
#}        

def table(x):
## prints a table of x by x dimensions ##
#{
    #int i, j

    global multiplier
    i = 1
    j = 1
    multiplier = (x * 2)
    while i <= x:
    #{
        while j <= x:
        #{
            print(x)
            j = j + 1
        #}
        i = i + 1
    #}
#}
        
def decisions(flag):
#{
    global multiplier
    global counterFunctionCalls
    if flag <= 1:
       return 1821
    elif flag >= 2 and flag <= 10:
    #{
        if flag < 5:
            print(5)
        else:
            print(10)
    #}
    elif flag <= 20:
    #{
        if flag < 13:
        #{
            print(13)
        #}
        elif flag <=18:
            print(18)
        else:
            print(20)
    #}
    elif flag <= 30:
        print(30)
    else:
        print(40)
    return decisions(flag // 2)
#}

        
#def main
#int i 
counterFunctionCalls = 0
multiplier = 2

i = int(input())
print(i)


i = 1600
while i<=2000:
#{
    print(leap(i))
    i = i + 400
#}
print(leap(2023))
print(leap(2024))
print(quad(3))
print(fib(5))
print(leap(decisions(45)))

i=1
while i<=12:
#{
    print(isPrime(i))
    i = i + 1
#}

print(counterFunctionCalls)