CITIES = {
    'zg': 1,
    'st': 2
}


def add(cities: Dict[str,int], name: string, pop: int):
    cities[name] = pop
    return cities


a = add(CITIES, "a", 1)
print(a)
