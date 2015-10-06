#!/usr/bin/python
# -*- coding: utf-8 -*-
import unittest
import math
import xlrd

def entropy(input_list):
    result = 0
    s = sum(input_list)
    for num in input_list:
        n = num / s
        result -= n * math.log(n, 2)
    return result

def best_attributes(dict_list,target_attribute):
	target_attribute_outputs = attribute_outputs(dict_list,target_attribute)
	attributes = dict_list[0].keys()
	result_dict = {}
	for attribute in attributes:
		attribute_output_list = attribute_outputs(dict_list,attribute)
		d_2 = {}
		for attribute_output in attribute_output_list:
			d_1 = {}
			for target_attrbute_output in target_attribute_outputs:
				count = len([d for d in dict_list if d[attribute] == attribute_output and d[target_attribute] == target_attrbute_output])
				d_1[target_attrbute_output] = count
			d_2[attribute_output] = d_1
		result_dict[attribute] = d_2
	return result_dict




def excel_to_dictionary(filename):
	book = xlrd.open_workbook(filename)
	first_sheet = book.sheet_by_index(0)
	col_names = first_sheet.row_values(0)
	dict_list = []
	for row_index in xrange(1,first_sheet.nrows):
		d ={}
		for col_index in xrange(first_sheet.ncols):
			d[col_names[col_index]] = first_sheet.cell(row_index,col_index).value
		dict_list.append(d)
	return dict_list

def attribute_outputs(dict_list,attribute):
	outputs = set()
	for d in dict_list:
		outputs.add(d[attribute])
	return list(outputs)

#def count_target_attribute_outputs(dict_list,attribute,target_attributes):


class TestStringMethods(unittest.TestCase):

    def test_entropy(self):
        self.assertEquals(entropy([5.0, 9.0]), 0.9402859586706309)

    def test_target_attribute_outputs(self):
    	dict_list = [{"a":"1"},{"a":"2"},{"a":"1"}]
    	out = attribute_outputs(dict_list,"a")
    	self.assertEquals(len(out),2)
    	self.assertTrue("1" in out)
    	self.assertTrue("2" in out)


if __name__ == '__main__':
    unittest.main()
