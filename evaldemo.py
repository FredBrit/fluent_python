#!/usr/bin/env python3
from builderlib import Builder, deco, Descriptor

print('# evaldemo module start')

@deco # Применить декоратор.
class Klass(Builder): # Унаследовать Builder, чтобы активировать его метод __init_subclass__.
    print('# Klass body')
    attr = Descriptor() # Создать экземпляр дескриптора.
    def __init__(self):
        super().__init__()
        print(f'# Klass.__init__({self!r})')

    def __repr__(self):
        return '<Klass instance>'
    
def main(): # Вызывается, только если модуль запущен как главная программа.
    obj = Klass()
    obj.method_a()
    obj.method_b()
    obj.attr = 999
    
if __name__ == '__main__':
    main()
print('# evaldemo module end')