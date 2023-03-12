CITIES = {
    'zg': 1,
    'st': 2
}


def add(cities: map, name: str, pop: int):
    cities[name] = pop
    return cities

def remove(cities : map, name : str):
    if name in cities:
        del cities[name]
        return cities

a = add(CITIES, "a", 1)
print(a)
b = remove(CITIES,"a1")
print(b)

print(max(CITIES.values()))
print(min(CITIES.values()))
keys = list(CITIES.keys())
l = list(CITIES.values())
m = max(l)
index = l.index(m)
print(keys[index])