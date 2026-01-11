#хороший ребенок
t = int(input())
for _ in range(t):
    n = int(input())
    numbers =  list(map(int, input().split()))
    min_n = min(d for d in numbers)
    min_i = numbers.index(min_n)
    numbers[min_i] += 1
    result = 1
    for d in numbers:
        result *= d
    print(result)
    
#арбуз
w = int(input())
if w > 2 and w % 2 == 0:
    print("yes")
else:
    print("no")
  
#вставь цифру
t = int(input())
for _ in range(t):
    n, d = map(int, input().split())
    number = input().strip()
    d_str = str(d)
    for i in range(n):
        if d > int(number[i]):
            result = number[:i] + d_str + number[i:]
            print(result)
            break
    else:
        print(number + d_str)

#Леша и разбиение массива
n = int(input())
a = list(map(int, input().split()))

if sum(a) != 0:
    print("YES")
    print(1)
    print(1, n)
else:
    found = False
    for i in range(n - 1):
        if sum(a[:i+1]) != 0 and sum(a[i+1:]) != 0:
            print("YES")
            print(2)
            print(1, i+1)
            print(i+2, n)
            found = True
            break
    
    if not found:
        print("NO")


            




