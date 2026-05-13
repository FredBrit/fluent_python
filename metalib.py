print('% metalib module start')
import collections
class NosyDict(collections.UserDict):
    def __setitem__(self, key, value):
        args = (self, key, value)
        print(f'% NosyDict.__setitem__{args!r}')
        super().__setitem__(key, value)

    def __repr__(self):
        return '<NosyDict instance>'
    
class MetaKlass(type):
    print('% MetaKlass body')

    # __prepare__  следует объявлять как метод класса. Это не метод экземпляра, потому что когда Python вызывает __prepare__, конструируемого класса еще не существует
    @classmethod 
    def __prepare__(meta_cls, cls_name, bases): # Python вызывает метод __prepare__  метакласса, чтобы получить отображение для размещения пространства имен конструируемого класса.
        args = (meta_cls, cls_name, bases)
        print(f'% MetaKlass.__prepare__{args!r}')
        return NosyDict() # Вернуть  экземпляр  NosyDict,  который  будет  использоваться  в  роли  пространства имен.
    
    def __new__(meta_cls, cls_name, bases, cls_dict): # cls_dict – экземпляр NosyDict, возвращенный методом __prepare__
        args = (meta_cls, cls_name, bases, cls_dict)
        print(f'% MetaKlass.__new__{args!r}')

        def inner_2(self):
            print(f'% MetaKlass.__new__:inner_2({self!r})')
        cls = super().__new__(meta_cls, cls_name, bases, cls_dict.data)
        # type.__new__ требует, чтобы в последнем аргументе был настоящий словарь 
        # dict, поэтому я передаю ему атрибут data отображения NosyDict, унаследованного от UserDict
        cls.method_c = inner_2 # Внедрить метод во вновь созданный класс
        return cls # Как обычно, __new__ должен вернуть только что созданный объект – в данном случае новый класс.
    
    def __repr__(cls): # Определение  __repr__  в  метаклассе  позволяет  настроить  представление объектов класса
        cls_name = cls.__name__
        return f"<class {cls_name!r} built by MetaKlass>"
print('% metalib module end')    