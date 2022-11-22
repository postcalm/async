

class Test:

    __non_const = 1

    def __init__(self, a):
        self.__non_const = a

    @property
    def const(self):
        return self.__non_const


if __name__ == '__main__':
    a = Test(3)
    print(a.const)
    a.__non_const = 2
    print(a.const)
