def bubbel(list):
    n = len(list)
    for i in range(n):
        for j in range(0, n-i-1):
            if list[j] > list[j+1]:
                list[j], list[j+1] = list[j+1], list[j]
    return list

numbers = [9, 6, 7, 6, 5, 2, 3, 7, 1, 0]

letters = [c, g, f, d, k, t, r, z, x, q]

sorted_list_numbers = bubbel(numbers)

print("Sorterad nummer lista:", sorted_list_numbers)

print("Sorterad bokstavs lista:", sorted_list)