import copy

class Test:
    def __init__(self):
        self.test_list = [["a"]]
        self.test_var = 1
        self.test_set = set([1,2,3])

    def gen_new(self):
        new_test = Test()
        new_test.test_set = copy.copy(self.test_set)
        new_test.test_list = [x[:] for x in self.test_list]
        new_test.test_var = self.test_var

        return new_test

lol = Test()
lol.test_list.append("b")
new_lol = lol.gen_new()
new_lol.test_set.add(4)
new_lol.test_list.append("c")
new_lol.test_list[0].append("d")
new_lol.test_var = 2

print(lol.test_list)
print(new_lol.test_list)

print(lol.test_var)
print(new_lol.test_var)

lol.test_set.update([(1,1), (6,1), (1,6), (6,6)])

print(lol.test_set)
print(new_lol.test_set)