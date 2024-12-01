from collections import Counter

with open("day_01/input.txt") as f:
    pairs = [[int(y) for y in x.strip().split("   ")] for x in f.readlines()]

left, right = sorted([x[0] for x in pairs]), sorted([x[1] for x in pairs])
mults = Counter(right)

p1 = sum(abs(right[i] - left[i]) for i in range(len(left)))
p2 = sum(left[i] * mults[left[i]] for i in range(len(left)))

print(f"P1 Solution is: {p1}")
print(f"P2 Solution is: {p2}")
