def get_value(cls, val):
    enum_val = [i for i in cls if i.value == val]
    if len(enum_val) == 0:
        return val
    return enum_val[0]
