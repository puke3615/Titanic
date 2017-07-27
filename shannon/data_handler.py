# coding=utf-8

def mock_data():
    features = ['Name', 'Age', 'Address', 'Number']
    data_set = [
        ['1', '1', '2', '0', 'yes'],
        ['1', '1', '2', '0', 'yes'],
        ['1', '0', '2', '0', 'no'],
        ['0', '1', '3', '1', 'yes'],
        ['0', '1', '9', '0', 'no'],
        ['1', '0', '3', '0', 'no']
    ]
    return data_set, features


def get_titanic_data(file_path, include=None, exclude=None):
    """
    加载Titanic的数据
    :param file_path: 文件路径
    :return: Titanic数据
    """
    import csv
    data_set = []
    reader = csv.reader(file(file_path, 'rb'))
    select = range(10)
    if include is not None:
        select = [s for s in select if s in include]
    elif exclude is not None:
        select = [s for s in select if s not in exclude]

    features = []
    for row, line in enumerate(reader):
        filter = [item for i, item in enumerate(line[2:]) if i in select]
        if row == 0:
            features = filter
        else:
            filter.append(line[1])
            data_set.append(filter)
    return data_set, features


def check_empty(data_set, features):
    empty = {}
    for j, data in enumerate(data_set):
        for i, item in enumerate(data):
            if item == '':
                feature = features[i]
                if not empty.__contains__(feature):
                    empty[feature] = 0
                empty[feature] += 1
    return empty


PATH = '../data/train.csv'

if __name__ == '__main__':
    # ['Pclass', 'Name', 'Sex', 'Age', 'SibSp', 'Parch', 'Ticket', 'Fare', 'Cabin', 'Embarked']
    data_set, features = get_titanic_data(PATH, include=range(2))
    print data_set[:2]
    print features
