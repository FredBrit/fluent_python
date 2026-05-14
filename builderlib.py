print('@ builderlib module start')
class Builder: # Это построитель классов, в котором будет реализован...

    print('@ Builder body')
    def __init_subclass__(cls): # .. метод __init_subclass__
        print(f'@ Builder.__init_subclass__({cls!r})')

        def inner_0(self):
            print(f'@ SuperA.__init_subclass__:inner_0({self!r})')
        cls.method_a = inner_0

    def __init__(self): # Определить функцию, добавляемую в подкласс в присваивании ниже
        super().__init__()
        print(f'@ Builder.__init__({self!r})')

def deco(cls): # Декоратор класса
    print(f'@ deco({cls!r})')

    def inner_1(self): # Функция, добавляемая в декорированный класс
        print(f'@ deco:inner_1({self!r})')
    cls.method_b = inner_1
    return cls # Вернуть класс, полученный в качестве аргумента

class Descriptor: # Дескрипторный класс, демонстрирующий, когда ...

    print('@ Descriptor body')
    def __init__(self): # ... создается экземпляр дескриптора и когда ...
        print(f'@ Descriptor.__init__({self!r})')

    def __set_name__(self, owner, name): # .. вызывается метод __set_name__ при конструировании класса owner.
        args = (self, owner, name)
        print(f'@ Descriptor.__set_name__{args!r}')

    def __set__(self, instance, value): # Как и все прочие методы, этот метод __set__ только распечатывает свои аргументы и больше ничего не делает.
        args = (self, instance, value)
        print(f'@ Descriptor.__set__{args!r}')

    def __repr__(self):
        return '<Descriptor instance>'
print('@ builderlib module end')
