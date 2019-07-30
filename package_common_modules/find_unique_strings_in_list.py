'''
'''
def find_unique_strings_in_list(string_list):
    '''
    Finds unique strings in given list of strings for example to find all dated
    of files creation
    '''
    seen = set()
    unique_strings = []
    for i in range (len(string_list)):
        if string_list[i] not in seen:
            unique_strings.append(string_list[i])
            seen.add(string_list[i])
    return unique_strings


if __name__ == '__main__':

    string_list = ['abc','adc','abc','ath','rbd','klp','abc','ath','tbc']
    unique_strings = find_unique_strings_in_list(string_list)
    print(string_list)
    print(unique_strings)
