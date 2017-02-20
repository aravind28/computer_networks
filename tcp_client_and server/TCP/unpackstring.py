import struct

def unpackbyteexpr(expr):
    i = 0
    str_expr = ''
    while i < len(expr): # when expr contains digit add it to result string
        if expr[i].isdigit():
            str_expr += expr[i]
            i += 1
        else: # when expr contains hex values, unpack two bytes of data and add to result string
            str_expr += str(struct.unpack('<H', expr[i:i+2])[0])
            i += 2
    return str_expr
