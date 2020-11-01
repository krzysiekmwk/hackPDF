
input_return = ["has1234.pdf", "10"]
ret = 0
def input(*args):
    global ret
    if ret >= len(input_return):
        ret = 0
    val = input_return[ret]
    ret += 1
    return val

print(input())
print(input())
print(input())
print(input())