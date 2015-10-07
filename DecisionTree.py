#!/usr/bin/python
# -*- coding: utf-8 -*-

from collections import Counter
import unittest
import math
import xlrd
from IlyssasDataTools import excel_to_dictionary,pretty_tree

def decision_tree(filename, target_attribute):
    data = excel_to_dictionary(filename)
    attributes = data[0].keys()
    attributes.remove(target_attribute)
    return decision_tree_helper(data, target_attribute, attributes)


def decision_tree_helper(data, target_attribute, attributes):
    target_attribute_values = [d[target_attribute] for d in data]
    if target_attribute_values.count(target_attribute_values[0]) \
        == len(target_attribute_values):
        d = Counter(target_attribute_values)
        return (target_attribute_values[0],d)
    if not attributes:
        d = Counter(target_attribute_values)
        return (d.most_common(1)[0][0],d)
    else:
        attributes_infogain = attribute_infogain(data,
                target_attribute, attributes)
        curr_attr = max(attributes_infogain.keys(), key=lambda k: \
                        attributes_infogain[k])
        attributes = list(attributes)
        attributes.remove(curr_attr)
        tree = {}
        decision = {curr_attr: tree}
        curr_attr_values = set(d[curr_attr] for d in data)
        for value in curr_attr_values:
            data_part = [d for d in data if d[curr_attr] == value]
            if data_part:
                tree[value] = decision_tree_helper(data_part,
                        target_attribute, attributes)
            else:
                return None
    return decision


def attribute_infogain(data, target_attribute, attributes):
    target_attribute_values = set(d[target_attribute] for d in data)
    histogram = Counter(d[target_attribute] for d in data)
    information_before = len(data) * entropy(histogram)

    attribute_infogain = {}
    for attribute in attributes:
        total_information = 0.0
        for value in set(d[attribute] for d in data):
            histogram = Counter(d[target_attribute] for d in data
                                if d[attribute] == value)
            total_information += sum(histogram.values()) \
                * entropy(histogram)
        attribute_infogain[attribute] = information_before \
            - total_information
    return attribute_infogain

def entropy(histogram):
    total = float(sum(histogram.values()))
    if total == 0:
        return 0.0
    return -sum(num / total * math.log(num / total, 2) for num in
                histogram.values() if num > 0)

# taken from stackoverflow
class TestStringMethods(unittest.TestCase):

    def test_decision_tree_helper(self):
        test1 = [{'A': '1', 'B': 'a'}, {'A': '1', 'B': 'b'}]
        self.assertEquals(decision_tree_helper(test1, 'A', ['A']), '1')

        test2 = [{'A': '1', 'B': 'a'}, {'A': '1', 'B': 'b'}, {'A': '2',
                 'B': 'b'}]
        self.assertEquals(decision_tree_helper(test2, 'A', []), '1')

    def test_entropy(self):
        self.assertEquals(entropy(Counter({'A': 5.0, 'B': 9.0})),
                          0.9402859586706309)
    def test_attribute_infogain(self):
        dict_list = excel_to_dictionary('Commute.xlsx')
        out = attribute_infogain(dict_list, 'Commute')
        result = {
            'Accident': 6.454231881430971,
            'Hour': 9.989838434720816,
            'Stall': 3.23495093255735,
            'Weather': 1.6993443792675045,
            }
        self.assertEquals(out, result)


if __name__ == '__main__':

    # unittest.main()

    d = decision_tree('Tennis.xlsx', 'PlayTennis')

    # print d

    pretty_tree(d)
