import os
import re
import numpy as np
import pandas as pd
import xlrd


class WordEmbedding(object):
    def __init__(self, words, vecs):
        # Convert words to dict for O(1) lookup speed
        self.words = {word: words.index(word) for word in words}
        self.vecs = vecs

    def __call__(self, word):
        """Embed a word
        :returns: vector, or None if the word is outside of the vocabulary
        :rtype: ndarray
        """
        idx = self.words.get(word, -1)

        if idx != -1:
            return self.vecs[idx]
        return

    @classmethod
    def from_files(cls, word_file, vec_file):
        """Instanciate an embedding from files
        Example::
            embedding = WordEmbedding.from_files('words.txt', 'vecs.npy.gz')
        :rtype: cls
        """
        # typical class method and invoke __init__() to create an instance
        return cls(load_words(word_file), load_vectors(vec_file))

    def embed_document(self, text):
        """Convert text to vector, by finding vectors for each word and combining
        :param str document: the document (one or more words) to get a vector
            representation for
        :return: vector representation of document
        :rtype: ndarray (1D)
        """
        # tokenize the text
        words_in_text = tokenize(text)
        # create a numpy array by iterating each token based on a set of rules and filters
        # sel(x) invokes __call__() to embed a word
        vectors = np.array(list(filter(None.__ne__, map(lambda x: self(x), words_in_text))))
        if vectors.size:
            return vectors.sum(axis=0)

        return np.zeros(self.vecs.shape[1])
# End of class WordEmbedding(object)

def load_words(filename):
    """Load a file containing a list of words as a python list
    :param str filename: path/name to file to load
    :rtype: list
    """
    with open(filename, 'r') as infile:
        words = infile.read().split()

    return words


def load_vectors(filename):
    """Loads a file containing word vectors to a python numpy array
    :param filename:
    :returns: 2D matrix with shape (m, n) where m is number of words in vocab
        and n is the dimension of the embedding
    :rtype: ndarray
    """
    return np.load(filename)


def load_data(filename, sheet=''):
    """Load student response data
    Note that this only returns first sheet as dataframe.
    Additional sheets will be ignored.
    :param str filename: xlsx file
    :param str sheet: Name of sheet to be loaded as dataframe - default ''
                      indicates first sheet will be loaded
    :returns: dataframe indexed on a hashed github id
    :rtype: DataFrame
    """
    # load .xlsx file
    xls = pd.ExcelFile(filename)
    # get sheet name
    sheetname = sheet if sheet else xls.sheet_names[0]
    # create data frame object
    df = xls.parse(sheetname)
    # replace NaNs with empty strings
    filled = df.fillna('') 
    # set index
    indexed = filled.set_index(filled.columns[0])
    return indexed


def tokenize(text):
    """Tokenize a text string into a list of words
    Note: this skips single letter words like a, I, R - these are being left
        out partially because at this level, it is not possible to distinguish
        them from initials or abbreviations which have different meanings.
    Example:
        >>> tokenize('I have a cat named Moxie')
        ['have', 'cat', 'named', 'moxie']
    :param str text: Text to be tokenized
    :returns: list of words from text (in lowercase)
    :rtype: list
    """
    return [word.lower() for word in re.findall(r"\w[\w']+", text)]


def cosine_similarity(a, b):
    """Compute cosine similarity between two vectors
    :param np.array a: first vector
    :param np.array b: vector to compare first vector to
    :returns: number representing cosine distance if vectors are both non-zero;
        otherwise returns np.nan
    :rtype: float or NaN
    """
    if np.count_nonzero(a) and np.count_nonzero(b):
        return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))
    else:
        return np.nan


def remove_files(*args):
    """Helper function for use by main.py, tests
    Checks if file is present and deletes it if so
    :param *args: one or more filenames as str
    """
    for filename in args:
        if os.path.isfile(filename):
            os.remove(filename)
