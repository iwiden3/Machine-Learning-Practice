#!/usr/bin/python
# -*- coding: utf-8 -*-

from collections import Counter
import unittest
import math
import xlrd


def entropy(histogram):
    total = float(sum(histogram.values()))
    if total == 0:
    	return 0.0
    return -sum((num / total) * math.log(num / total, 2)
    			for num in histogram.values() if num > 0)

def attributes_tree(dict_list, target_attribute):
    target_attribute_outputs = attribute_outputs(dict_list,
            target_attribute)
    attributes = dict_list[0].keys()
    attributes.remove(target_attribute)
    result_dict = {}
    for attribute in attributes:
        attribute_output_list = attribute_outputs(dict_list, attribute)
        attribute_output_dict = {}
        for attribute_output in attribute_output_list:
            target_attribute_output_dict = {}
            for target_attrbute_output in target_attribute_outputs:
                count = len([d for d in dict_list if d[attribute]
                            == attribute_output and d[target_attribute]
                            == target_attrbute_output])
                target_attribute_output_dict[target_attrbute_output] = count
            attribute_output_dict[attribute_output] = target_attribute_output_dict
        result_dict[attribute] = attribute_output_dict
    return result_dict

def sort_by_entropy(dict_list,target_attribute):
	tree = attributes_tree(dict_list,target_attribute)


def attribute_infogain(data, target_attribute):
    target_attribute_values = set(d[target_attribute] for d in data)
    attributes = data[0].keys()
    attributes.remove(target_attribute)

    histogram = Counter(d[target_attribute] for d in data)
    information_before = len(data) * entropy(histogram)

    attribute_infogain = {}
    for attribute in attributes:
    	total_information = 0.0
    	for value in set(d[attribute] for d in data):
    		histogram = Counter(d[target_attribute] for d in data if d[attribute] == value)
    		total_information += sum(histogram.values()) * entropy(histogram)
    	attribute_infogain[attribute] = information_before - total_information
    return attribute_infogain

def excel_to_dictionary(filename):
    book = xlrd.open_workbook(filename)
    first_sheet = book.sheet_by_index(0)
    col_names = first_sheet.row_values(0)
    dict_list = []
    for row_index in xrange(1, first_sheet.nrows):
        d = {}
        for col_index in xrange(first_sheet.ncols):
            d[col_names[col_index]] = first_sheet.cell(row_index,
                    col_index).value
        dict_list.append(d)
    return dict_list


def attribute_outputs(dict_list, attribute):
    outputs = set()
    for d in dict_list:
        outputs.add(d[attribute])
    return list(outputs)



class TestStringMethods(unittest.TestCase):

    def entropy(self):
        self.assertEquals(entropy([5.0, 9.0]), 0.9402859586706309)

    def target_attribute_outputs(self):
        dict_list = [{'a': '1'}, {'a': '2'}, {'a': '1'}]
        out = attribute_outputs(dict_list, 'a')
        self.assertEquals(len(out), 2)
        self.assertTrue('1' in out)
        self.assertTrue('2' in out)

    def attribute_attribute_infogain(self):
        dict_list = [{'a': '1', 'c': 't'}, {'a': '2', 'c': 'b'},
                     {'a': '1', 'c': 't'}]
        out = attributes_tree(dict_list, 'a')
        result = {'c': {'t': {'1': 2, '2': 0}, 'b': {'1': 0, '2': 1}}}
        self.assertEquals(out, result)
        self.assertEquals(result['c']['t']['1'], 2)

    def test_attribute_infogain(self):
        dict_list = excel_to_dictionary("Commute.xlsx")
        out = attribute_infogain(dict_list, 'Commute')
        result = {}
        self.assertEquals(out, result)


if __name__ == '__main__':
    unittest.main()
