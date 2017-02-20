
def evalstring(ip):

    result = [] # integer list that acts as a stack
    operator =[] # operator list that acts a stack
    i = 0

    while i < len(ip):
        if ip[i] in ['+', '-']: # if the operator is a '+' or '-' add operator to stack
            operator.append(ip[i])
            i += 1
        elif ip[i] in ['*', '/']: # if operator is '*' or '-' pop element from result stack and perform the evaluation
            if ip[i] == '*':      # do not add operator to stack as we already perform evaluation
                result.append(result.pop() * int(ip[i+1]))
            else:
                result.append(result.pop() / int(ip[i+1]))
            i += 2
        else: # check for length of digits and add all the digits of the number to the result stack
            digit =''
            while i < len(ip) and ip[i].isdigit():
                digit += ip[i]
                i += 1
            result.append(int(digit))

    while operator: # pop operators in operator stack and perform evaluation
        if operator[-1] == '+': # we know the operators will be either a '+' or a '-'
            operator.pop()
            result.append(result.pop() + result.pop())
        else:
            operator.pop()
            result.append((- 1) * (result.pop() - result.pop())) # multiply by -1 to convert sign of values

    return str(result[0])



