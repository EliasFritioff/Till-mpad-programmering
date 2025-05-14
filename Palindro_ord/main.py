def is_palindrome(word):
    word = word.lower()
    for i in range(len(word)):
        if word[i] != word[-(i + 1)]:
            return False
    return True

# Huvudprogram
user_input = input("Skriv ett ord: ")

if is_palindrome(user_input):
    print(f"'{user_input}' är ett palindrom!")
else:
    print(f"'{user_input}' är inte ett palindrom!")