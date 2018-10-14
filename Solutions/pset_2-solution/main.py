import numpy as np
import pandas as pd
import re
from pset_02.word_embedding import *
from pset_utils.hashing import hash_str
from pset_utils.io import atomic_write

words = re.compile(r"\w[\w']+")

def make_vecs(wordpath, vecpath, wordlist):
    import spacy
    model = spacy.load('en_core_web_md')

    from pset_utils.io import atomic_write

    present_words, vecs = zip(*[
        (w, model(w).vector) for w in wordlist
        if w in model.vocab
    ])

    with atomic_write(wordpath, overwrite=True) as f:
        for w in present_words:
            f.write(w + '\n')

    with atomic_write(vecpath, mode='wb', overwrite=True) as f:
        np.save(f, vecs)


def findwords(s):
    return words.findall(s)


def load_raw_vocab(path):
    with open(path) as f:
        vocab = f.readlines()

        return [v.strip() for v in vocab if v.strip()]


def load_vocab(path):
    with open(path) as f:
        vocab = f.readlines()

        # Return a dictionary object created by dictionary comprehension
        return {w.strip():i for i, w in enumerate(vocab)}


def score(words, vocab):
    init = np.zeros(300, dtype=float)
    for w in words:
        try:
            init += vecs[vocab[w.lower()], :]
        except KeyError:
            pass
    return init


def similarity(a, b):
    s = np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))
    if not np.isfinite(s):
        return 0.
    return s

def xls_to_dataframe(xls_file, word_file, vector_file, out_file):
    data = load_data(xls_file)
    embedding = WordEmbedding.from_files(word_file, vector_file)
    vectors = data['learn'].apply(embedding.embed_document)
    # print(vectors.shape)
    vectors += data['project'].apply(embedding.embed_document)
    # print(vectors.shape)
    df = pd.DataFrame([v for v in vectors.values], index=vectors.index)
    # return df
    with atomic_write(out_file) as outfile:
        df.to_csv(outfile)
    return data


if __name__ == '__main__':
    # The old way of unit test
    #if False:
    #    wl = load_raw_vocab('data/orig_words.txt')
    #    make_vecs('data/words.txt', 'data/vectors.npy.gz', wl)

    #vocab = load_vocab('data/words.txt')

    #students = pd.read_excel('data/hashed.xlsx').set_index('hashed_id').sort_index()
    #students['learn'].fillna('', inplace=True)
    #students['project'].fillna('', inplace=True)

    #vecs = np.load('data/vectors.npy.gz')


    #def myapply(sentence):
    #    return score(words.findall(sentence), vocab)

    #vectors = students['learn'].apply(myapply) + students['project'].apply(myapply)
    #mat = np.zeros((vectors.shape[0], vectors.iloc[0].shape[0]), dtype=float)
    #me = vectors.iloc[0]  # Arbitrary
    #print("Reference student:", students.index.values[0])
    #dist = vectors.apply(lambda v: 1 - similarity(v, me))
    #nearest = np.argsort(dist)
    #top_n = students.iloc[nearest[:6]]
    #top_n.insert(0, 'dist', dist[nearest[:6]])

    #for row in top_n.itertuples():
    #    print('Student:', row.Index, row.dist)
    #    print(row.learn)
    #    print(row.project)

    #    print('')

    #print('Furthest:')
    #furthest = list(reversed([n for n in nearest if dist[n] < 1][-5:]))
    #bottom_n = students.iloc[furthest]
    #bottom_n.insert(0, 'dist', dist[furthest])

    #for row in bottom_n.itertuples():
    #    print('Student:', row.Index, row.dist)
    #    print(row.learn)
    #    print(row.project)

    remove_files('data/embedded.csv')
    data = xls_to_dataframe('data/hashed.xlsx', 'data/words.txt',
                              'data/vectors.npy.gz', 'data/embedded.csv')

    # $SALT environment variable should already exist
    my_salt = bytes.fromhex(os.environ['SALT'])
    my_id = hash_str('username', salt=my_salt).hex()[:8]
    vectors = pd.read_csv('data/embedded.csv', index_col=0)
    my_vec = vectors.loc[my_id]

    def my_distance(vec):
        return 1 - cosine_similarity(vec, my_vec)

    distances = vectors.apply(my_distance, axis=1)
    distances = distances[pd.notnull(distances)]
    distances = distances[abs(distances) > 1e-10]

    print('5 Nearest Neighbors: \n')
    for idx in distances.sort_values().head().index:
        print('hashed ID: {}'.format(idx))
        print('distance: {}'.format(distances.loc[idx]))
        print('Learn:')
        print(data.loc[idx]['learn'])
        print('Project:')
        print(data.loc[idx]['project'])
        print('\n')
     
    print('5 Farthest: \n')
    for idx in distances.sort_values().tail().index:
        print('hashed ID: {}'.format(idx))
        print('distance: {}'.format(distances.loc[idx]))
        print('Learn:')
        print(data.loc[idx]['learn'])
        print('Project:')
        print(data.loc[idx]['project'])
        print('\n')

