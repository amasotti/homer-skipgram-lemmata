"""
Build vocab & corpus and save them for later use

"""

__author__ = "Antonio Masotti"
__date__ = "Febrauar 2021"

import json
import numpy as np
import math
import random
from argparse import Namespace
from cltk.tokenize.sentence import TokenizeSentence
from cltk.tokenize.word import WordTokenizer
from numpy.testing._private.utils import decorate_methods
from tqdm import tqdm

# Paths (I hate to have constantly to write paths...)
args = Namespace(
    raw_data="../data/raw_data/HomerGesamt_cleaned.txt",
    word2index="../data/vocabs/Homer_word2index_lemmatized.json",
    word_frequencies="../data/vocabs/Homer_word_frequencies_lemmatized.json",
    mappings="../data/vocabs/Homer_vocab_mappings.json",
    corpus='../data/Homer_lemmatized.npy',
    wordlist='../data/vocabs/Homer_lemmaList_preprocessed.csv'
)


def createCorpus(text, mappings, save=True):
    '''
    :params text - the raw text

    returns  + the corpus, a list of list with tokenized sentences
             + the vocab (a dictionary with the frequency of the tokens scaled by the total number of words.

    '''
    # load stopwords
    with open('../data/stopwords.txt', 'r', encoding="UTF-8") as src:
        stopwords = src.read()

    # add punctuation signs
    stopwords = stopwords.split('\n')
    stopwords.extend([".", ",", "?", "!", "-", ":",
                      ";", "·", "”", "“", "«", "»"])

    # tokenize sentences and then words
    Stokenizer = TokenizeSentence('greek')
    Wtokenizer = WordTokenizer('greek')

    sentences = Stokenizer.tokenize(text)
    new_sentences = []
    vocab = dict()

    print('Building corpus and freqDictionary')
    check = 0
    # for each sentence
    for sent in tqdm(sentences, desc="Sentences"):
        # extract the words
        new_sent = Wtokenizer.tokenize(sent)
        check += len(new_sent)
        new_sentences.append(new_sent)

    # Substitute lemmata for word forms
    lemmatized_corpus = []
    for sent in tqdm(new_sentences, desc="Subsitution"):
        lemmatized_sent = []
        for word in sent:
            # Stopword deletion
            if word in stopwords:
                continue
            else:
                for lemma, forms in mappings.items():
                    if word in forms:
                        lemmatized_sent.append(lemma)
        lemmatized_corpus.append(lemmatized_sent)
    print("test lemmatized corpus", lemmatized_corpus[:5])

    # Counting and subsampling
    total_tokens = 0
    for sent in tqdm(lemmatized_corpus, desc="Counting and sampling"):
        for word in sent:
            total_tokens += 1
            if word not in vocab:
                vocab[word] = 1
            else:
                vocab[word] += 1
    vocab_size = len(vocab)

    print("total tokens: ", total_tokens)
    print("total token (incl. stopwords)", check)
    print("vocab_size : ", vocab_size)
    # Subsampling
    treshold = 10e-05
    for k, v in vocab.items():
        # http: // mccormickml.com/2017/01/11/word2vec-tutorial-part-2-negative-sampling/
        # Not really used for subsampling here but to generate the noise distribution
        frac = v / total_tokens
        p_w = (1 + math.sqrt(frac/treshold)) * (treshold/frac)
        vocab[k] = p_w

    if save:
        print('Saving the frequencies')
        with open(args.word_frequencies, 'w', encoding='utf-8') as fp:
            json.dump(vocab, fp, ensure_ascii=False)

        print('Saving the corpus')
        arr = np.array(lemmatized_corpus, dtype=object)
        np.save(args.corpus, arr)

        with open(args.wordlist, "w", encoding="utf-8") as fp:
            for idx, word in tqdm(enumerate(vocab), desc="Building word list"):
                fp.write(str(idx) + "," + word + "\n")

    return new_sentences, vocab


if __name__ == '__main__':
    import os
    # Load data
    with open(args.raw_data, 'r', encoding='utf-8') as src:
        data = src.read()

    with open(args.mappings, "r", encoding="utf-8") as fp:
        mappings = json.loads(fp.read())

    corpus, freq_vocab = createCorpus(text=data, mappings=mappings, save=True)

    # Lookup tables
    word2index = {w: i for i, w in enumerate(freq_vocab.keys())}

    # save lookup dictionary
    with open(args.word2index, 'w', encoding='utf-8') as fp:
        json.dump(word2index, fp, ensure_ascii=False)
