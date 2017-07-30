import numpy as np
import string
import os
import operator
from nltk import pos_tag, word_tokenize
from datetime import datetime

def remove_punctutation(s):
    return s.translate(None, string.punctuation)

def my_tokenizer(s):
    s = remove_punctutation(s)
    s = s.lower()
    return s.split()
## This function doesn't seem to work
def get_wikipedia_data(n_files, n_vocab, by_paragraph=False):
    #repo_path = os.path.dirname(os.path.realpath('__file__'))
    #print "inside get_wikipedia_data() : current path = %s" %repo_path
    #print "-----------------------------------------------"
    
    #data_path = repo_path + "/data/"
    
    #prefix = '../../data/'
    data_path = '../../data/'
    input_files = [f for f in os.listdir(data_path) if f.startswith('enwiki') and f.endswith('txt')]

    # return variables
    sentences = []
    original_sentence = []
    word2idx = {'START': 0, 'END': 1}
    idx2word = ['START', 'END']
    current_idx = 2
    word_idx_count = {0: float('inf'), 1: float('inf')}

    if n_files is not None:
        input_files = input_files[:n_files]

    for f in input_files:
        #print("reading:", f)
        for line in open(data_path + f):
            line = line.strip()
            # don't count headers, structured data, lists, etc...
            if line and line[0] not in ('[', '*', '-', '|', '=', '{', '}'):
                if by_paragraph:
                    sentence_lines = [line]
                else:
                    sentence_lines = line.split('. ')
                for sentence in sentence_lines:
                    original_sentence.append(sentence)
                    tokens = my_tokenizer(sentence)
                    for t in tokens:
                        if t not in word2idx:
                            word2idx[t] = current_idx
                            idx2word.append(t)
                            current_idx += 1
                        idx = word2idx[t]
                        word_idx_count[idx] = word_idx_count.get(idx, 0) + 1
                    sentence_by_idx = [word2idx[t] for t in tokens]
                    sentences.append(sentence_by_idx)

    # restrict vocab size
    sorted_word_idx_count = sorted(word_idx_count.items(), key=operator.itemgetter(1), reverse=True)
    word2idx_small = {}
    new_idx = 0
    idx_new_idx_map = {}
    for idx, count in sorted_word_idx_count[:n_vocab]:
        word = idx2word[idx]
        #print(word, count)
        word2idx_small[word] = new_idx
        idx_new_idx_map[idx] = new_idx
        new_idx += 1
    # let 'unknown' be the last token
    word2idx_small['UNKNOWN'] = new_idx 
    unknown = new_idx

    #assert('START' in word2idx_small)
    #assert('END' in word2idx_small)
    #assert('king' in word2idx_small)
    #assert('queen' in word2idx_small)
    #assert('man' in word2idx_small)
    #assert('woman' in word2idx_small)

    # map old idx to new idx
    sentences_small = []
    for sentence in sentences:
        if len(sentence) > 1:
            new_sentence = [idx_new_idx_map[idx] if idx in idx_new_idx_map else unknown for idx in sentence]
            sentences_small.append(new_sentence)

    idx2word_dict = {v:k for k, v in word2idx_small.items()}

    return sentences_small, word2idx_small, idx2word_dict , original_sentence


def readWikiData(n_vocab=500):
    repo_path = os.path.dirname(os.path.realpath('__file__'))
    #print "inside get_wikipedia_data() : current path = %s" %repo_path
    #print "-----------------------------------------------"
    
    filePath = repo_path + "/data/en-wiki.txt"
    
    #filePath = "../data/en-wiki.txt"

    # return variables 
    sentences = []
    word2idx = {'START': 0, 'END': 1}
    idx2word = ['START', 'END']
    current_idx = 2 
    word_idx_count = {0: float('inf'), 1: float('inf')}

    for line in open(filePath):
        line = line.strip()
        if line and line[0] not in ('[', '*', '-', '|', '=', '{', '}'):
            sentence_lines = line.split('. ')
            for sentence in sentence_lines:
                tokens = my_tokenizer(sentence)
                for t in tokens:
                    if t not in word2idx:
                        word2idx[t] = current_idx 
                        idx2word.append(t)
                        current_idx += 1
                    idx = word2idx[t]
                    word_idx_count[idx] = word_idx_count.get(idx, 0) + 1
                sentence_by_idx = [word2idx[t] for t in tokens] 
                sentences.append(sentence_by_idx)

    sorted_word_idx_count = sorted(word_idx_count.items(), key=operator.itemgetter(1), reverse=True)
    word2idx_small = {}
    new_idx = 0 
    idx_new_idx_map = {}
    for idx, count in sorted_word_idx_count[:n_vocab]:
        word = idx2word[idx] 
        word2idx_small[word] = new_idx 
        idx_new_idx_map[idx] = new_idx 
        new_idx += 1
    word2idx_small['UNKNOWN'] = new_idx 
    unknown = new_idx 

    sentence_small = []
    for sentence in sentences:
        if len(sentence) > 1:
            new_sentence = [idx_new_idx_map[idx] if idx in idx_new_idx_map else unknown for idx in sentence] 
            sentence_small.append(new_sentence)

    return sentence_small, word2idx_small 
