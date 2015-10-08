from collections import Counter
import unittest
import math
from IlyssasDataTools import excel_to_dictionary,pretty_tree


def Naive_Bayes(filename,target_attribute,test_case):
    data = excel_to_dictionary(filename)
    target_attribute_values = set(d[target_attribute] for d in data)
    data_size = len(data)
    result = {}
    m = float(3)
    p = 1/float(len(target_attribute_values))
    for value in target_attribute_values:
        print value
        data_slice = [d for d in data if d[target_attribute] == value]
        prob = len(data_slice)/float(len(data))
        #print prob
        n = len(data_slice)
        #print "n " +str(n)
        for attr in test_case:
            data_c = [d for d in data_slice if d[attr] == test_case[attr]]
            n_c = float(len(data_c))
            print attr
            print "n_c " + str(n_c)
            print "m " + str(m)
            print "p " + str(p)
            prob_temp = (n_c + float(m*p))/float((n+m))
            print "prob " + str(prob_temp)
            prob *= prob_temp
        result[value] = prob
    print result
    return max(result.items(),key = lambda k:result[k[0]])



# taken from stackoverflow
#class TestStringMethods(unittest.TestCase):

 #   def test_decision_tree_helper(self):
  #     self.assertEquals()



if __name__ == '__main__':

    test_case = {"Color":"Red","Type":"SUV","Origin":"Domestic"}
    r = Naive_Bayes("CarTheft.xlsx","Stolen",test_case)
    print r
    # unittest.main()