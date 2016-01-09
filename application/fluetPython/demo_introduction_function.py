# coding=UTF-8

# 1. 装饰器：在不改变源代码的情况下修改已经存在的函数
# 装饰器实质上是一个函数，它把一个函数作为输入并且返回另外一个函数。

def document_it(func):
    def new_function(*args,**kwargs):
        print('Running function: ',func.__name__)
        print('Positional arguments: ',args)
        print('Keyword arguments: ',kwargs)
        result = func(*args,**kwargs)
        print('Result: ',result)
        return result
    return new_function

def add_ints(a,b):
    return a + b

if __name__ == '__main__':
    print(add_ints(3,5))
    cooler_add_ints = document_it(add_ints)
    cooler_add_ints(3,5)











