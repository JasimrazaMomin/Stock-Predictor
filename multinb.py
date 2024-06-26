def get_feature_vector(str):
    irrelevant_word = {'a': 1, 'the' : 1, 'to' : 1, 'and' : 1, 'or' : 1, 'so' : 1, 'is' : 1, 'an' : 1, 'this' : 1, 'that' : 1, 'these' : 1, 'those' : 1, 'in': 1, 'as':1, 'also':1, 'i' : 1}
    feature_dict = dict()
    str = str.split()
    total_words = 0
    unique_values = 0
    for word in str:
        if word.lower() in irrelevant_word:
            continue
        total_words +=1 
        if word in feature_dict:
            feature_dict[word] += 1
        else:
            feature_dict[word] = 1
            unique_values += 1
    return (feature_dict,total_words,unique_values)

test_string = "Donold Trump Turns gay from the the the vaccine THE I ThAt"
print(get_feature_vector(test_string))