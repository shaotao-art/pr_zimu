with open('C:\\Users\starfish\pr_zimu\docs\\3.txt', 'r', encoding='utf-8')as f:
    text = f.readlines()
print('我我我')
print('wowowo')
for i in range(0, len(text)):
    print(f'{text[i][0:len(text[i]) - 1]}'.ljust(100), end='')
    print(1)

