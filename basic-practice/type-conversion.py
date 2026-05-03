# Write a function type_inspector(val) that returns a string describing the type and key properties of any input — e.g. 'int: 42, even, positive'. Handle all 6 basic types.


# Define a function that accepts any value as input
def type_inspector(val):

    # Check if the value is a bool FIRST — because in Python, bool is a subclass of int,
    # so True and False would be caught by the int check if we don't handle bool first
    if isinstance(val, bool):
        return f"bool: {val}"  # Return a string like "bool: True"

    # Check if the value is an integer
    elif isinstance(val, int):
        parity = "even" if val % 2 == 0 else "odd"  # Even if divisible by 2, otherwise odd
        sign = "positive" if val > 0 else "negative" if val < 0 else "zero"  # Determine sign
        return f"int: {val}, {parity}, {sign}"  # e.g. "int: 42, even, positive"

    # Check if the value is a float (decimal number)
    elif isinstance(val, float):
        sign = "positive" if val > 0 else "negative" if val < 0 else "zero"  # Determine sign
        return f"float: {val}, {sign}"  # e.g. "float: 3.14, positive"

    # Check if the value is a string
    elif isinstance(val, str):
        length = len(val)  # Count the number of characters
        case = "uppercase" if val.isupper() else "lowercase" if val.islower() else "mixed case"  # Detect case
        return f"str: '{val}', length {length}, {case}"  # e.g. "str: 'hello', length 5, lowercase"

    # Check if the value is a list
    elif isinstance(val, list):
        length = len(val)  # Count number of items in the list
        return f"list: {val}, length {length}, {'empty' if length == 0 else 'non-empty'}"  # e.g. "list: [1,2,3], length 3, non-empty"

    # Check if the value is a dictionary
    elif isinstance(val, dict):
        keys = len(val)  # Count number of key-value pairs
        return f"dict: {val}, {keys} key(s), {'empty' if keys == 0 else 'non-empty'}"  # e.g. "dict: {...}, 2 key(s), non-empty"

    # If none of the above types matched, handle the unknown type gracefully
    else:
        return f"unknown type: {type(val).__name__}"  # Return the type name as a fallback


# --- Test each type ---
print(type_inspector(42))                          # int: positive, even
print(type_inspector(-7))                          # int: negative, odd
print(type_inspector(3.14))                        # float: positive
print(type_inspector("Jamali"))                    # str: mixed case
print(type_inspector("HELLO"))                     # str: uppercase
print(type_inspector(True))                        # bool
print(type_inspector([1, 2, 3]))                   # list: non-empty
print(type_inspector({"name": "Jamali", "age": 25}))  # dict: non-empty
