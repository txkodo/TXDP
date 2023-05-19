class C:
    def __lt__(self, other: int):
        print("lt", other)
        return self

    def __gt__(self, other: int):
        print("gt", other)
        return self

    def __bool__(self):
        raise TypeError

print(C())
