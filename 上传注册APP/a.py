class MyType(type):
    def __init__(self, *args, **kwargs):
        super(MyType, self).__init__(*args, **kwargs)

    def __call__(cls, *args, **kwargs):
        v = dir(cls)
        obj = super(MyType, cls).__call__(*args, **kwargs)
        return obj


def with_metaclass(arg,base):
    return MyType('xx', (base,), {})


class Foo(with_metaclass(MyType,object)):
    user = 'wupeiqi'
    age = 18


obj = Foo()