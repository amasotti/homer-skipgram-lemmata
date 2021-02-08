"""
Script to map word forms to lemmata

"""

from argparse import Namespace
from collections import defaultdict
import json

args = Namespace(
    paradigms="data/vocabs/Homer_data_from_xml.txt",
    mappings="data/vocabs/Homer_vocab_mappings.json",
    reversed_mappings="data/vocabs/Homer_reverse_mappings.csv",
    lemmata="data/vocabs/Homer_lemma_list.txt",
    stopwords="data/stopwords.txt"
)


def extract_pairs(raw_data):
    with open(args.stopwords, "r", encoding="utf-8") as stopw:
        stopwords = stopw.read().split("\n")
    stopwords.extend([",", ".", ";", ":", "-"])
    stopwords = set(stopwords)

    with open(raw_data, "r", encoding="utf-8") as fp:
        data = fp.readlines()
    form_lemma = []
    for word in data:
        word_split = word.split("|")[:2]
        if word_split[0] not in stopwords:
            if word_split[1] == "" or word_split[1] == " " or word_split[1] == "-":
                form_lemma.append([word_split[0], "<UNK>"])
            else:
                form_lemma.append(word_split)
    return form_lemma


def mapping(pairs):
    lemmata = []
    mapping = defaultdict(list)
    for pair in pairs:
        if pair[1] not in lemmata:
            lemma = pair[1]
            lemmata.append(lemma)
            mapping[lemma] = []
    for pair in pairs:
        if pair[0] not in mapping[pair[1]]:
            mapping[pair[1]].append(pair[0])
    return lemmata, mapping


pairs = extract_pairs(raw_data=args.paradigms)

with open(args.reversed_mappings, "w", encoding="utf-8") as fp:
    for pair in pairs:
        fp.write(pair[0] + "|" + pair[1] + "\n")


lemma_list, mappings = mapping(pairs=pairs)

with open(args.lemmata, "w", encoding="utf-8") as fp:
    for index, lemma in enumerate(lemma_list):
        fp.write(str(index) + ":" + lemma + "\n")

with open(args.mappings, "w", encoding="utf-8") as fp:
    json.dump(mappings, fp, ensure_ascii=False)
