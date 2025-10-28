from Ship import Ship

s = Ship('Destroyer', 2)
print('Before hits: hits =', s.hits)
s.hit()
print('After 1st hit: hits =', s.hits)
s.hit()
print('After 2nd hit: hits =', s.hits)
print('is_sunk =', s.is_sunk())
