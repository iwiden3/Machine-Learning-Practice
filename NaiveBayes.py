from collections import Counter,defaultdict
import unittest
import math
from IlyssasDataTools import excel_to_dictionary,pretty_tree


def Naive_Bayes2(filename,target_attribute,test_case):
    data = excel_to_dictionary(filename)
    target_attribute_values = set(d[target_attribute] for d in data)
    result = {}
    m = 3
    p = 1/float(len(target_attribute_values))
    for value in target_attribute_values:
        data_slice = [d for d in data if d[target_attribute] == value]
        total = len(data_slice)/float(len(data))
        n = len(data_slice)
        for attr in test_case:
            n_c = len([d for d in data_slice if d[attr] == test_case[attr]])
            prob = (n_c + m*p)/(n+m)
            total *= prob
        result[value] = total
    return max(result.items(),key = lambda k:result[k[0]])

def Naive_Bayes(data,target_attribute):
    attributes = data[0].keys()
    attributes.remove(target_attribute)
    pairs = []
    for d in data:
        for attr in attributes:
            pairs.append((d[attr],d[target_attribute]))
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
            likelihood *= model[(case[attr],v)]
        likelihoods[v] =likelihood
    result = max(likelihoods.items(),key = lambda x : likelihoods[x[0]])
    return (result[0],result[1]/float(sum(likelihoods.values))*100)




# taken from stackoverflow
class TestStringMethods(unittest.TestCase):
    def Nfaive_Bayes(self):
        test_case = {"Color":"Red","Type":"SUV","Origin":"Domestic"}
        r = Naive_Bayes("CarTheft.xlsx","Stolen",test_case)
        self.assertEquals(r,(u'No', 0.0692138671875))


if __name__ == '__main__':

    test_case = {"Color":"Red","Type":"SUV","Origin":"Domestic"}
    r = try_naive_bayes("CarTheft.xlsx","Stolen",test_case)
    print r
     #unittest.main()