import xlrd


def excel_to_dictionary(filename):
    book = xlrd.open_workbook(filename)
    first_sheet = book.sheet_by_index(0)
    col_names = first_sheet.row_values(0)
    dict_list = []
    for row_index in xrange(1, first_sheet.nrows):
        d = {}
        for col_index in xrange(1, first_sheet.ncols):
            d[col_names[col_index]] = first_sheet.cell(row_index,
                    col_index).value
        dict_list.append(d)
    return dict_list

def pretty_tree(d, indent=0):
    for (key, value) in d.iteritems():
        if isinstance(value, dict):
            print '\t' * indent + '%30s: {\n' % str(key).upper()
            pretty_tree(value, indent + 1)
            print '\t' * indent + ' ' * 32 + '} # end of %s #\n' \
                % str(key).upper()
        elif isinstance(value, list):
            for val in value:
                print '\t' * indent + '%30s: [\n' % str(key).upper()
                pretty_tree(val, indent + 1)
                print '\t' * indent + ' ' * 32 + '] # end of %s #\n' \
                    % str(key).upper()
        else:
            print '\t' * indent + '%30s: %s' % (str(key).upper(),
                    str(value))