"""
File: test_stack.py
Author: Chen Zhang
A test program for stack implementation
"""


from stack_array import ArrayStack


def test(stacktype):
    """Expects a stack type as an argument and runs some tests on objects of that type"""

    lyst = [2020, 9, 24]
    print("The list of added item is:", lyst)
    s1 = ArrayStack(lyst)
    print("Expect 3:", len(s1))
    print("Expect {2020, 9, 24}:", str(s1))
    print("Expect False:", s1.isEmpty())
    print("Expect True:", 2020 in s1)
    print("Expect False:", 2021 in s1)
    print("Expect the items on separate lines:")
    for item in s1:
        print(item)
    s1.clear()
    print("Expect {}:", s1)
    s1.push(2020)
    print("Expect {2020}:", s1)
    s2 = ArrayStack()
    print("Expect {2020}:", s1 + s2)
    print("Expect False:", s2 == s1)
    print("Expect 2020:", s1.peek())
    print("Expect 1:", len(s1))
    s1.pop()
    print("Expect 0:", len(s1))
    print("Expect ValueError:", s1.peek())

    # Expend stack
    # lyst2 = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    # lyst3 = ['A', 'B', 'C']
    # s3 = ArrayStack(lyst2)
    # s4 = ArrayStack(lyst3)
    # print("Expect two of stack:", s3 + s4)
    # print("Expect 12:", len(s3 + s4))


if __name__ == '__main__':
    test(ArrayStack)
