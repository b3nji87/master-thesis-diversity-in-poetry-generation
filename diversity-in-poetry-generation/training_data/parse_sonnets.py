from uniformers.datasets import load_dataset
from gensim.models import Word2Vec
from gensim.models.word2vec import LineSentence
import numpy as np
import string
import os
import argparse
import logging

def get_sonnets(lang):
    """
    Parses QuaTrain data to an input format compatible with Deep-speare and Structured-Adversary.

    Parameters:
    ----------
    lang : Language version of QuaTrain. 'en' loads English data, 'de' loads German data.

    Returns:
    -------
    sonnets_final : List of parsed sonnets 
    """
    sonnets_final = []
    
    quatrains = load_dataset('quatrain', lang=lang, split="train")
    quatrains = quatrains['text']
    sonnets = [quatrains[i:i + 4] for i in range(0, len(quatrains), 4)][:-1]

    for sonnet in sonnets:
        del(sonnet[3][-2:])

    for i in range(len(sonnets)):
        sonnets[i] = [item for sublist in sonnets[i] for item in sublist]
        for j in range(14):
            sonnets[i][j] = sonnets[i][j].rstrip(string.punctuation).rstrip()
    
    for sonnet in sonnets:
        sonnet = ' <eos> '.join(sonnet)
        sonnets_final.append(sonnet + ' <eos>')
    
    return sonnets_final


def split_sonnets(sonnets):
    """
    Creates multiple splits of sonnet data that are used in the training process of Deep-speare
    and Structured-Adversary. A first large split (70%) is used to create word embeddings, while
    the remaining 30% of the data is split into a train, validation and test dataset.
    
    Parameters:
    ----------
    sonnets : List of parsed sonnets obtained from QuaTrain

    Returns:
    -------
    background : Split used to deduce word vectors
    train : Training dataset for Deep-speare/Structured-Adversary
    validate : Validation dataset for Deep-speare/Structured-Adversary
    test : Test dataset for Deep-speare/Structured-Adversary
    """
    background, train_data = np.split(sonnets, [int(len(sonnets)*0.7)])

    train, validate, test = np.split(train_data, [int(len(train_data)*0.8), int(len(train_data)*0.9)])

    return list(background), list(train), list(validate), list(test)


if __name__ == "__main__":

    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    
    parser = argparse.ArgumentParser()
    parser.add_argument('--lang', type=str)
    parser.add_argument('--get_wv', action="store_false")
    parser.add_argument('--vector_size', type=int, default=100)
    parser.add_argument('--alpha', type=float, default=0.025)
    parser.add_argument('--window', type=int, default=5)
    parser.add_argument('--min_count', type=int, default=3)
    parser.add_argument('--sample', type=float, default=0.00001)
    parser.add_argument('--workers', type=int, default=16)
    parser.add_argument('--min_alpha', type=float, default=0.0001)
    parser.add_argument('--sg', type=int, default=1)
    parser.add_argument('--hs', type=int, default=0)
    parser.add_argument('--negative', type=int, default=5)
    parser.add_argument('--epochs', type=int, default=200)
    args = parser.parse_args()

    output_dir="sonnet_data/" + args.lang 

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    sonnets = get_sonnets(lang=args.lang)

    background, train, validate, test = split_sonnets(sonnets)

    with open(output_dir + '/sonnet_background.txt', 'w') as f:
        f.write('\n'.join(background))
    with open(output_dir + '/sonnet_train.txt', 'w') as f:
        f.write('\n'.join(train))
    with open(output_dir + '/sonnet_validate.txt', 'w') as f:
        f.write('\n'.join(validate))
    with open(output_dir + '/sonnet_test.txt', 'w') as f:
        f.write('\n'.join(test))
    
    if args.get_wv:
        
        documents = LineSentence(output_dir + '/sonnet_background.txt')
        model = Word2Vec(documents, 
                         vector_size=args.vector_size,
                         alpha=args.alpha,
                         window=args.window,
                         min_count=args.min_count,
                         sample=args.sample,
                         workers=args.workers,
                         min_alpha=args.min_alpha,
                         sg=args.sg,
                         hs=args.hs,
                         negative=args.negative,
                         epochs=args.epochs)
        
        model.save(output_dir + "/word2vec.bin")
        model.wv.save_word2vec_format(output_dir + "/word2vec.txt", binary=False)

    
