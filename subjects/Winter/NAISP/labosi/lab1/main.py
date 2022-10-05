import  numpy as np

print("Zad1")

names = ["Ana", "Petar", "Ana", "Lucija", "Vanja", "Pavao", "Lucija"]


def reverse_sort(names: list) -> list:
    return sorted(names, reverse=True)


names_desc: list = reverse_sort(names)
print(names_desc)

selected_names = reverse_sort(names)[0:-1]
print(selected_names)

unique_selected_names = set(selected_names)
print(unique_selected_names)

pass_names: list = []

for name in unique_selected_names:
    pass_names.append(name + " - pass")

print(pass_names)

print("Zad2")

person_data : dict = {"Ana":1995,"Zoran":1979,"Lucija":2001,"Anja":1997}
print(person_data)

for person,year in person_data.items():
    person_data[person] = int(year) - 1

print(person_data)

year_age : list = []

for year in person_data.values():
    tup : tuple = (year, 2022-year)
    year_age.append(tup)
print(year_age)

print("Zad3")
vector_a = np.array([1,3,5])
print(vector_a)
vector_b = np.array([[2],[4],[6]])
print(vector_b)
print()

mat_mul = np.multiply(vector_a,vector_b)
print(mat_mul)
print()

vec_dot = np.dot(vector_a, vector_b)
print(vec_dot)
print()

mat_exp = np.power(mat_mul,2)
print(mat_exp)
print()

sub_mat = mat_exp[1:, 1:]
print(sub_mat)
print()

print("Zad4")

class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def increase_age(self):
        self.age = self.age+1

class PersonDetail(Person):
    def __init__(self, name,age,address):
        super().__init__(name,age)
        self.address = address

first_person = Person("Marko", 39)
second_person = Person("Ivan", 17)

second_person.increase_age()
print(second_person.age)

first_person_detail = PersonDetail("Ana",25,"Unska 3")

first_person_detail.increase_age()
print(first_person_detail.age)

