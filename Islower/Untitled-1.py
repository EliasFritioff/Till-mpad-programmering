words = input("Skriv in din text: ")

result = ""

lowercase = "abcdefghijklmnopqrstuvwxyzåäö "
uppercase = "ABCDEFGHIJKLMNOPQRSTUVWXYZÅÄÖ "

for char in words:
    if char in lowercase:
        index = lowercase.index(char)
        result += uppercase[index]
    elif char in uppercase:
        result += char

print("Text med endast bokstäver i stora bokstäver:")
print(result)