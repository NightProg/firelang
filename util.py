import dataclasses as dc

def compare(c1, c2):
    """
    Compare two class
    :param c1: class 1
    :param c2: class 2
    :return: True if c1 is equal to c2
    """
    list_attr_c1 = sorted(filter(lambda x: not x.startswith("__") and not x.endswith("__"), dir(c1)))
    list_attr_c2 = sorted(filter(lambda x: not x.startswith("__") and not x.endswith("__"), dir(c2)))
    if len(list_attr_c1) != len(list_attr_c2):
        print("len error")
        return False
    for attr_c1, attr_c2 in zip(list_attr_c1, list_attr_c2):

        if attr_c1 != attr_c2:
            print("name error")
            
            return False
    for attr_c1, attr_c2 in zip(list_attr_c1, list_attr_c2):
        if getattr(c1, attr_c1) != getattr(c2, attr_c2):
            print("value error")
            return False
    return True 

@dc.dataclass
class A:
    a:int

if __name__ == "__main__":
    a = A(1)
    b = A(1)
    print(compare(a, b))
