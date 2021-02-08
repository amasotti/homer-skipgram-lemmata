# SkipGram model for Ancient Greek

My implementation (in Pytorch `1.7.0`) of the Word2Vec model (Skip Gram Negative) trained on the homeric texts.
This project is almost exactly the same as [amasotti/homer-skipgram](https://github.com/amasotti/homer-skipgram) but the corpus is completely lemmatized (and thus heavily reduced). The similarities are calculated between lemmata instead of between tokens.

## Predictions

Probable context words for the header word:

| βούλομαι |  λίσσομαι  |   ἔρος    |    θεά    | ἔρχομαι | βαίνω  |
| :------: | :--------: | :-------: | :-------: | :-----: | :----: |
| κρείσσων | μειλίχιος  |  ἐδητύς   | γλαυκῶπις |   εἰς   |  παρά  |
|  ὀφέλλω  |   νεικέω   |   πόσις   |    Ἥρα    |  αὐτός  |  εἶμι  |
|  ἀρείων  |   κηρόθι   |   ἄρχω    |   Ἀθήνη   |   ἐπί   |  ἐπί   |
|  φθονέω  | ὀλοφύρομαι |  ἐνίπτω   | προσεῖπον |  ναῦς   | ἵππος  |
| ἀμήχανος |   ἐλεέω    | θεοειδής  |  ἀμείβω   | μνηστήρ |  ναῦς  |
|  ἐίσκω   |   ποῖος    | προσφωνέω |   αὖτε    |  εἶμι   | ἵστημι |
