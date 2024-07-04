import re
import copy
import json
# def get_feature_vector(str):
#     irrelevant_word = {'a': 1, 'the' : 1, 'to' : 1, 'and' : 1, 'or' : 1, 'so' : 1, 'is' : 1, 'an' : 1, 'this' : 1, 'that' : 1, 'these' : 1, 'those' : 1, 'in': 1, 'as':1, 'also':1, 'i' : 1}
#     feature_dict = dict()
#     str = str.split()
#     total_words = 0
#     unique_values = 0
#     for word in str:
#         if word.lower() in irrelevant_word:
#             continue
#         total_words +=1 
#         if word in feature_dict:
#             feature_dict[word] += 1
#         else:
#             feature_dict[word] = 1
#             unique_values += 1
#     return (feature_dict,total_words,unique_values)

test_data = [["8",0,"The lyrics of the song sounded like fingernails on a chalkboard."],
             ["4",0,"The old rusted farm equipment surrounded the house predicting its demise."],
             ["2",0,"He poured rocks in the dungeon of his mind."],
             ["160",1,"The fish dreamed of escaping the fishbowl and into the toilet where he saw his friend go."],
             ["255",1,"Iguanas were falling out of the trees."],
             ["218",1,"The pigs were insulted that they were named hamburgers."]]

# words that don't change anything in the context of a sentence 
irrelevant_word = {'a': 1, 'the' : 1, 'to' : 1, 'and' : 1, 'or' : 1, 'so' : 1, 'is' : 1, 'an' : 1, 'this' : 1, 'that' : 1, 'these' : 1, 'those' : 1, 'in': 1, 'as':1, 'also':1, 'i' : 1, 'of' : 1}

# need to clean strings (remove all except letters and numbers and make all words lowercase) 

for data in test_data:
    data[2] = data[2].lower()
    data[2] = re.sub(r'[^a-z0-9 ]', '', data[2])

# print(test_data)

# want to keep track of number of docs per classes
positive_counter = 0 #1
negative_counter = 0 #0

# need to make a vocab
# need to get total number of words per class
# need to get frequency of words per class

vocab = set()
total_positive_words = 0
total_negative_words = 0
word_count_positive = dict()
word_count_negative = dict()

for data in test_data:
    broken_string = data[2].split()
    cleaned_string = list(filter(lambda x: x not in irrelevant_word,broken_string))
    vocab.update(set(cleaned_string))
    if data[1] == 1:
        positive_counter += 1
        total_positive_words += len(cleaned_string)
        for word in cleaned_string:
            if word in word_count_positive:
                word_count_positive[word] += 1
            else:
                word_count_positive[word] = 1
    else:
        negative_counter += 1
        total_negative_words += len(cleaned_string)
        for word in cleaned_string:
            if word in word_count_negative:
                word_count_negative[word] += 1
            else:
                word_count_negative[word] = 1
                
# print(f"Positive Number: {positive_counter}. Negative Number: {negative_counter}\n\n")
# print(vocab)
# print(f"\n\nTotal Positive Words: {total_positive_words}. Total Negative Words: {total_negative_words}\n\n")
# print(word_count_positive)
# print(word_count_negative)

# getting class probabilities
probability_positive = positive_counter / (positive_counter + negative_counter)
probability_negative = 1 - probability_positive

# track id of headline
id = 0

# make vocab into a dictionary for feature vectors
vocab_dict = dict()
for item in vocab:
    vocab_dict[item] = 0

# feature vector dictionary (for all documents), will go id : [class, feature vector]
feature_vectors = dict()

for data in test_data:
    broken_string = data[2].split()
    feature_vectors[id] = [data[1],copy.deepcopy(vocab_dict)]
    for word in broken_string:
        if word in feature_vectors[id][1]:
            feature_vectors[id][1][word] += 1
    id += 1

# for vector in feature_vectors:
#     print(feature_vectors[vector][1])
#     print()

# using total pos/neg words as total number of word occurences in a class
# using word count dict to get number of certain word occurences in a class
# get constants needed for conditional probabilities 
smoothing_param = 1
unique_words = len(vocab)

# to store it all into a json, will make a dict then write into a file
# first key will be for positive probability, second key for negative probability
# third key will be for conditionals for positive class, fourth key will be for conditionals for negative class
# fifth key will be for the vocabulary dict

positive_conditionals = dict()
negative_conditionals = dict()

# first deal with positive class
for word in word_count_positive:
    positive_conditionals[word] = (word_count_positive[word] + smoothing_param) / (total_positive_words + (smoothing_param * unique_words))
    
# second deal with negative class
for word in word_count_negative:
    negative_conditionals[word] = (word_count_negative[word] + smoothing_param) / (total_negative_words + (smoothing_param * unique_words))

# since these are all going to turn into floats, we will lose precision, will need to test exactly how much we lose
# if losing too much (ie strays too far from total 1 probability), can use fraction or decimal library or store numerator and denominator to do division later

to_json = {"positive_probability" : probability_positive, 
           "negative_probability" : probability_negative,
           "positive_conditional" : positive_conditionals,
           "negative_conditional" : negative_conditionals,
           "vocab" : vocab_dict}
