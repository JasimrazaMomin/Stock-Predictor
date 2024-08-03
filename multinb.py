import json
import math

def get_feature_vector(feature_list): # rest of the feature vector changes actually happen here
    feature_vector = dict()
    for word in feature_list:
        if word in feature_vector:
            feature_vector[word] += 1
        else:
            feature_vector[word] = 1
    return feature_vector
    
def prediction(feature_string_list,prob_conditional_word_dict,prob_class_dict):
    # feature string gets turned into feature vector
    # prob_word_dict will be class : conditional dict we made, so we will have 2 keys, positive and negative
    # prob_class_dict will be the class : class probability, since stored separate in json, we will have to make a dict positive : prob, negative : prob
    feature_vector = get_feature_vector(feature_string_list)
    summed_logarithmic_probability = 0
    probabilites = dict()
    for class_name in prob_class_dict:
        for word in feature_vector:
            summed_logarithmic_probability += (feature_vector[word])*(math.log(prob_conditional_word_dict[class_name][word]))
        probabilites[class_name] = math.log(prob_class_dict[class_name]) + summed_logarithmic_probability
        summed_logarithmic_probability = 0
    prob_max = 0
    prob_name = ""
    for prob in probabilites:
        if probabilites[prob] > prob_max:
            prob_max = probabilites[prob]
            prob_name = prob
    return (prob_name,prob_max)

def training(test_data): # data should be passed in as follows [ [date,label,headline], ...]
    with open('vocab.json','r') as json_file:
        vocab = json.load(json_file)
    
    # want to keep track of number of docs per classes
    positive_counter = 0 #1
    negative_counter = 0 #0
    # need to get total number of words per class
    total_positive_words = 0
    total_negative_words = 0
    # need to get frequency of words per class
    word_count_positive = dict()
    word_count_negative = dict()

    for data in test_data:
        if data[1] == 1:
            positive_counter += 1
            total_positive_words += len(data[2])
            for word in data[2]:
                if word in word_count_positive:
                    word_count_positive[word] += 1
                else:
                    word_count_positive[word] = 1
        else:
            negative_counter += 1
            total_negative_words += len(data[2])
            for word in data[2]:
                if word in word_count_negative:
                    word_count_negative[word] += 1
                else:
                    word_count_negative[word] = 1

    # getting class probabilities
    probability_positive = positive_counter / (positive_counter + negative_counter)
    probability_negative = 1 - probability_positive
    # laplace smoothing
    smoothing_param = 1
    # from calculated vocab
    unique_words = 56651  
    
    # to store it all into a json, will make a dict then write into a file ------- decided to just reutrn the model instead of doing json
    # first key will be for positive probability, second key for negative probability
    # third key will be for conditionals for positive class, fourth key will be for conditionals for negative class

    positive_conditionals = dict()
    negative_conditionals = dict()

    for word in vocab:
        positive_conditionals[word] = (word_count_positive[word] + smoothing_param) / (total_positive_words + (smoothing_param * unique_words))
        negative_conditionals[word] = (word_count_negative[word] + smoothing_param) / (total_negative_words + (smoothing_param * unique_words))

    model = {"positive_probability" : probability_positive, 
            "negative_probability" : probability_negative,
            "positive_conditional" : positive_conditionals,
            "negative_conditional" : negative_conditionals}
    
    return model