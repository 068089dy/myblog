from django.test import TestCase

# Create your tests here.


class A:
    def hello(self):
        print("hello")


class B:
    def hello(self):
        print("hello b")


class C(B, A):
    def __init__(self):
        pass
        # print(super().hello())

    class D:
        a = 1


c = C.D()
print(c.a)
