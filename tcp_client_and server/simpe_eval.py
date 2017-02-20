import struct

def find(st):

    no_of_exp = struct.unpack('>H', st[0:2])[0]
    start_buffer = 2
    output_list = []
    output_list.append(no_of_exp)
    while no_of_exp > 0:

        length_of_current_exp = struct.unpack('>H', st[start_buffer:start_buffer+2])[0]
        start_buffer += 2
        x = 0

        for i in range ((start_buffer), (start_buffer+length_of_current_exp)):
            if st[i] in ['+', '-', '*', '/']:
                operator = st[i]
                break
            x +=1

        first_operand = int(st[start_buffer: start_buffer + x])
        second_operand = int(st[start_buffer + x + 1: start_buffer + length_of_current_exp])

        if operator == '+':
            result = first_operand + second_operand
        elif operator == '-':
            result = first_operand - second_operand
        elif operator == '*':
            result = first_operand * second_operand
        else:
            result = first_operand / second_operand

        output_list.append(len(str(result)))
        output_list.append(result)

        start_buffer = start_buffer + length_of_current_exp

        no_of_exp -= 1
    print output_list

input = struct.pack('>H', 2) + struct.pack('>H', 4) + "3+12" + struct.pack('>H', 4) + "12*5"
find(input)
#find(struct.pack('<H', 3) + struct.pack('<H', 4) + "3+12" + struct.pack('<H', 4) + "12*5" +
#     struct.pack('<H', 5) + "145+2")