# coding=utf-8
import math

from shannon import data_handler


def calc_shannon_entropy(data_set, label_getter=lambda data: data[-1]):
    """
    计算香农熵
    :param data_set: 数据集
    :param label_getter: label获取器, 默认选取最后一列作为label
    :return: 香农熵
    """
    data_size = len(data_set)
    label_prob = {}
    for data in data_set:
        label = label_getter(data)
        if not label_prob.__contains__(label):
            label_prob[label] = 0
        label_prob[label] += 1
    shannon_entropy = 0
    for label in label_prob:
        prob = float(label_prob[label]) / data_size
        shannon_entropy -= prob * math.log(prob, 2)
    return shannon_entropy


def choose_feature(data_set):
    """
    根据最大化信息增益原则选择特征
    :param data_set: 数据集
    :return: 特征索引
    """
    if len(data_set) == 0:
        raise Exception('The data set is empty.')
    current_entropy = calc_shannon_entropy(data_set)
    info_gain = 0
    feature_target = 0
    feature_count = len(data_set[0]) - 1
    for feature_index in range(feature_count):
        feature_result = {}
        for i, data in enumerate(data_set):
            feature = data[feature_index]
            if not feature_result.__contains__(feature):
                feature_result[feature] = []
            feature_result[feature].append(data_set[i])

        data_size = len(data_set)
        entropy = 0
        for f, d in feature_result.items():
            prob = float(len(d)) / data_size
            entropy += prob * calc_shannon_entropy(d)
        current_info_gain = current_entropy - entropy
        if current_info_gain > info_gain:
            feature_target = feature_index
            info_gain = current_info_gain
    return feature_target


def split_data_by_feature(data_set, feature_index):
    """
    通过feature分割数据集
    :param data_set: 数据集
    :param feature_index: 特征索引
    :return: 分割结果
    """
    split_result = {}
    for data in data_set:
        sub_data = [value for i, value in enumerate(data) if i != feature_index]
        feature = data[feature_index]
        if not split_result.__contains__(feature):
            split_result[feature] = []
        split_result[feature].append(sub_data)
    return split_result


def build_tree(data_set, feature_names):
    """
    构造决策树
    :param data_set: 数据集
    :param labels: 标签集
    :return: 决策树
    """
    if len(data_set) == 0:
        raise Exception('The data set is empty.')
    class_list = [data[-1] for data in data_set]
    class_set = set(class_list)
    # 1. 只有一类时, 停止构造
    if len(class_set) == 1:
        return class_list[0]
    feature_size = len(data_set) - 1
    # 2. 特征用完仍然无法分类时, 取最多的
    features = feature_names[:]
    if feature_size == 0:
        index = 0
        max_count = 0
        for i, c in enumerate(class_set):
            count = class_list.count(c)
            if max_count < count:
                max_count = count
                index = i
        return class_list[index]
    # 3. 其余场景, 构造树
    feature_index = choose_feature(data_set)
    feature_name = features[feature_index]
    tree = {feature_name: {}}
    del features[feature_index]
    split_result = split_data_by_feature(data_set, feature_index)
    for feature, sub_data_list in split_result.items():
        tree[feature_name][feature] = build_tree(sub_data_list, features)
    return tree


if __name__ == '__main__':
    # entropy = calc_shannon_entropy(data_set, label_getter=lambda data: data[-2])
    # print entropy

    data, features = data_handler.mock_data()
    # feature = choose_feature(data)
    # print "feature: %d" % feature

    print build_tree(data, features)
