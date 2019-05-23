import csv
import math
import copy


def Entropy(volume_once_property, data):  # энтропия выборочного поля
    ent = 0
    for i in data:
        if float(i) > 0:
            ent += -(float(i) / float(volume_once_property)) * math.log((float(i) / float(volume_once_property)), 2)
    return ent


def Entropy_base_property(data):  # энтропия базового поля
    ent = 0
    dict_base_property = dict()  # подсчет общих свойств {'Sunny': 5, 'Overcast': 4, 'Rain': 5}

    for i in data:
        dict_base_property[i] = 0

    for i in data:
        dict_base_property[i] += 1

    for i in dict_base_property.values():
        ent += -i / len(data) * math.log((i / len(data)), 2)

    return ent


def Gain(sample_property, base_property):
    ent = Entropy_base_property(base_property)

    dict_sample_property = dict()  # подсчет общих свойств {'Sunny': 5, 'Overcast': 4, 'Rain': 5}

    for i in sample_property:
        dict_sample_property[i] = 0

    for i in sample_property:
        dict_sample_property[i] += 1

    dict_simple_of_base_property = dict()  # подсчет свойств относительного базового свойства
    # {'SunnyNo': 3, 'SunnyYes': 2, 'OvercastNo': 0, 'OvercastYes': 4, 'RainNo': 2, 'RainYes': 3}

    for i in sample_property:
        for j in base_property:
            dict_simple_of_base_property[i + j] = 0

    for i in range(len(sample_property)):
        dict_simple_of_base_property[sample_property[i] + base_property[i]] += 1

    dict_entropy_sample_property = dict()  # энтропия по значениям dict_simple_of_base_property

    for i in dict_sample_property:
        interim_set = []
        for j in dict_simple_of_base_property:
            if i in j:
                interim_set.append(dict_simple_of_base_property[j])
        dict_entropy_sample_property[i] = Entropy(dict_sample_property[i], interim_set)

    for i in dict_entropy_sample_property:
        a = dict_sample_property[i] / len(sample_property)
        b = dict_entropy_sample_property[i]
        ent -= a * b

    return ent


def definition_sign(data):
    ent = []
    base_property = []
    data_copy = copy.deepcopy(data)

    for i in range(len(data[0]) - 1, len(data[0])):  # отделение последнего столбца
        for j in range(len(data)):
            base_property.append(data[j][i])
            del data_copy[j][i]

    for i in range(len(data_copy[0])):  #  len(data1[0]) определение прироста информации столбцов
        column_sample_property = []
        for j in range(len(data_copy)):
            column_sample_property.append(data_copy[j][i])
        ent.append(Gain(column_sample_property, base_property))

    return ent


def check(data):
    set_check = set()

    for i in range(len(data[0]) - 1, len(data[0])):
        for j in range(len(data)):
            set_check.add(data[j][i])

    if (len(set_check) != 1):
        return True
    else:
        return False

def solve(data):
    set_check = set()

    for i in range(len(data[0]) - 1, len(data[0])):
        for j in range(len(data)):
            set_check.add(data[j][i])

    return set_check.pop()


def id3(data):

    if check(data):
        entropy_data = definition_sign(data)
        partition_property = set()  # уникальные занчения по разбиваемому свойству
        data_update = []  # новые данные после разбиения
        node = []

        for i in range(len(data)):  # определение уникальных значений
            partition_property.add(data[i][entropy_data.index(max(entropy_data))])

        for i in partition_property:  # разбиение данных
            table = []
            for j in data:
                if i == j[entropy_data.index(max(entropy_data))]:
                    del j[entropy_data.index(max(entropy_data))]
                    table.append(j)
            node.append({i : table})
            data_update.append(table)

        for i in node:
            for j in i:
                i[j] = id3(i[j])

        return node
    else:
        return solve(data)


def run(test, tree):
    answer = ''
    if test:
        for i in tree:
            for j in i:
                if test[0] == j:
                    test.pop(0)
                    run(test, i[j])
                    break
        test.pop(0)
        run(test, tree)
        return answer
    else:
        answer = tree
        return answer


def main():
    data = []

    with open('data.csv', 'r') as file:
        reader = csv.reader(file, delimiter=';')
        for row in reader:
            data.append(row)

    tree = id3(data)

    test = ['Sunny', 'Hot', 'High', 'Week']

    # print(tree)

    print(run(test, tree))


if __name__ == '__main__':
    main()