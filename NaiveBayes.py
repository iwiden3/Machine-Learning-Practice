from collections import Counter,defaultdict
import unittest
import math
from IlyssasDataTools import excel_to_dictionary,pretty_tree

def Naive_Bayes(data,target_attribute):
    attributes = data[0].keys()
    attributes.remove(target_attribute)
    pairs = []
    for d in data:
        for attr in attributes:
            pairs.append((attr,d[attr],d[target_attribute]))
    model = Counter(pairs)  
    return model

def try_naive_bayes(filename,target_attribute,case):
    data = excel_to_dictionary(filename)
    model = Naive_Bayes(data,target_attribute)
    values = set(d[target_attribute] for d in data)
    likelihoods = defaultdict(list)
    for v in values:
        likelihood = 1
        for attr in case:
            likelihood *= model[(attr,case[attr],v)]
        likelihoods[v] =likelihood
    result = max(likelihoods.items(),key = lambda x : likelihoods[x[0]])
    return (result[0],result[1]/float(sum(likelihoods.values()))*100)

# taken from stackoverflow
class TestStringMethods(unittest.TestCase):
    def test_try_naive_Bayes(self):
        test_case = {"Color":"Red","Type":"SUV","Origin":"Domestic"}
        r = try_naive_bayes("CarTheft.xlsx","Stolen",test_case)
        self.assertEquals(r,(u'No',75))


if __name__ == '__main__':

    test_case = {"Color":"Red","Type":"SUV","Origin":"Domestic"}
    #r = try_naive_bayes("CarTheft.xlsx","Stolen",test_case)
    #print r
    unittest.main()