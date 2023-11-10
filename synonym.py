import math
import re


def norm(vec):
    '''Return the norm of a vector stored as a dictionary, as
    described in the handout for Project 3.
    '''

    sum_of_squares = 0.0
    for x in vec:
        sum_of_squares += vec[x] * vec[x]

    return math.sqrt(sum_of_squares)


def cosine_similarity(vec1, vec2):
    reoccuring_dic = {}
    total = 0
    v1sq = 0
    v2sq = 0

    for key, value in vec1.items():
        if key in vec2:
            reoccuring_dic[key] = [value]
            reoccuring_dic[key].append(vec2[key])


    if list(reoccuring_dic.values()) == []:
        return 0

    else:

        for value_list in reoccuring_dic.values():
            total += value_list[0] * value_list[1]

        for value in vec1.values():
            v1sq += value**2

        for value in vec2.values():
            v2sq += value**2

        cos_sim = total/math.sqrt(v1sq*v2sq)

        return cos_sim



def build_semantic_descriptors(sentences):
    '''return a dictionary of all semantic descriptors'''

    sem_des = {}
    for sen in sentences:
        reoccur_word = []
        for word in sen:
            if word not in reoccur_word:
                reoccuring_word_in_sentence = [word]
                if word not in sem_des:
                    sem_des[word] = {}
                    for new_word in sen:
                        if new_word not in reoccuring_word_in_sentence:
                            if new_word not in sem_des[word]:
                                sem_des[word][new_word] = 1
                            else:
                                sem_des[word][new_word] += 1
                        reoccuring_word_in_sentence.append(new_word)

                else:
                    for new_word in sen:
                        if new_word not in reoccuring_word_in_sentence:
                            if new_word not in sem_des[word]:
                                sem_des[word][new_word] = 1
                            else:
                                sem_des[word][new_word] += 1
                        reoccuring_word_in_sentence.append(new_word)

            reoccur_word.append(word)
    return sem_des



def build_semantic_descriptors_from_files(filenames):
    large_list = []
    for i in range(len(filenames)):
        f = open(filenames[i], "r", encoding="latin1")
        f_n = f.read()
        sentences = re.split('\.|\?|\!', f_n)
        large_list.extend(sentences)

    word_list = []
    for sentence in large_list:
        word = re.split(',|\-|--|\:|;|\n| ', sentence)
        word_list.append(word)

    for lis in word_list:
        for i in range(len(lis)):
            if lis[i] != "":
                lis[i] = lis[i].lower()

    for lis in word_list:
        for word in lis:
            if word == "":
                lis.remove(word)

    return build_semantic_descriptors(word_list)




def most_similar_word(word, choices, semantic_descriptors, similarity_fn):
    sim_score = []
    for i in range(len(choices)):
        if word in semantic_descriptors and choices[i] in semantic_descriptors:
            sim_score.append(similarity_fn(semantic_descriptors[word],semantic_descriptors[choices[i]]))
        else:
            sim_score.append(-1)

    for i in range(len(sim_score)):
        if sim_score[i] == max(sim_score):
            return choices[i]




def run_similarity_test(filename, semantic_descriptors, similarity_fn):

    f = open(filename)
    text = f.read()
    lines = text.split("\n")
    new_lines = []

    for line in lines:
        new_line = line.split()
        new_lines.append(new_line)

    for line in new_lines:
        if len(line) < 4:
            new_lines.remove(line)

    number_of_questions = len(new_lines)
    word_to_check = []
    correct_answer = []
    words_to_compare = []

    for ele in new_lines:
        word_to_check.append(ele[0])
        correct_answer.append(ele[1])
        words_to_compare.append(ele[2:])

    correct_total = 0


    for i in range(len(new_lines)):
        if most_similar_word(word_to_check[i], words_to_compare[i], semantic_descriptors, similarity_fn) == correct_answer[i]:
            correct_total += 1
    return (correct_total/number_of_questions) * 100