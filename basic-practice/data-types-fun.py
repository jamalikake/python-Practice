def type_value(val):
    if isinstance(val, int):
        if (val%2) == 0 :
            valuetype = "even" 
        else:
            valuetype = "odd"

        return f"integer: {val}, {valuetype}"
    
print(type_value(53))