import time
import tracemalloc
import functools


class Mark:
    def __init__(self):
        self.passes = 0
        self.after = None
        self.now = None
        self.peak = None
        self.current = None


class FuncMark(Mark):
    def __init__(self, inner_function):
        super().__init__()
        self.inner_function = inner_function
    
    def __call__(self, *args, **kwargs):
        tracemalloc.start()

        value = self.inner_function(*args, **kwargs)

        self.current, self.peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        
        return value


class Itermark(Mark):
    def __call__(self, iterable, label=None):
        tracemalloc.start()

        for item in iterable:
            self.passes += 1
            self.current, self.peak = tracemalloc.get_traced_memory()
            
            yield item

        tracemalloc.stop()



itermark_1 = Itermark()

def go_baby_go():
    a = []
    for i in range(1000):
        a.append([1, 2, 3, 4, 5, 6, 7, 9])

a = []
for i in itermark_1(range(100000)):
    a.append([1, 2, 3, 4, 5, 6, 7, 9])


funcmark_1 = FuncMark(go_baby_go)

funcmark_1()

print(itermark_1.peak)
print(funcmark_1.peak)
