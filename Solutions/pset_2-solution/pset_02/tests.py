import os
import unittest
import numpy as np
import pandas as pd

if __name__ == '__main__':
    # .py uses this form of import statement
    from word_embedding import *
else:
    # pytest uses this form of import statement
    from .word_embedding import * 

from pset_utils.io import atomic_write


class TestWordEmbedding(unittest.TestCase):

    def setUp(self):
        currentdir = os.getcwd()
        remove_files('{}/testdata/test_words.txt'.format(currentdir), '{}/testdata/test_vecs.npy'.format(currentdir))
        with atomic_write('{}/testdata/test_words.txt'.format(currentdir)) as wordfile:
            wordfile.write('cat\ndog\nmoose')

        vectors = np.array([[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 15, 19]])
        np.save('testdata/test_vecs.npy', vectors)
        try:
            self.example = WordEmbedding.from_files('{}/testdata/test_words.txt'.format(currentdir),
                                                     '{}/testdata/test_vecs.npy'.format(currentdir))
        finally:
            remove_files('{}/testdata/test_words.txt'.format(currentdir), '{}/testdata/test_vecs.npy'.format(currentdir))

    def test_word_embedding_call(self):
        called = self.example('moose')
        assert self.example.words['moose'] == 2
        assert self.example.vecs.shape == (3, 4)
        assert called.tolist() == [9, 10, 15, 19]

    def test_embed_document_all_present(self):
        words_all_present = 'Cat cat moose, dog!!'
        output = self.example.embed_document(words_all_present)
        assert output.tolist() == [16, 20, 28, 35]
        assert output.shape == (4,)

    def test_embed_document_some_present(self):
        some_words_present = 'Cat cat skunk, dog!!'
        output = self.example.embed_document(some_words_present)
        assert output.tolist() == [7, 10, 13, 16]
        assert output.shape == (4,)

    def test_embed_document_none_present(self):
        no_words_present = 'Elf frog skunk, elk!!'
        output = self.example.embed_document(no_words_present)
        assert output.tolist() == [0, 0, 0, 0]
        assert output.shape == (4,)


class TestLoadData(unittest.TestCase):

    def test_load_data_default_sheet(self):
        df = load_data('{}/testdata/sample.xlsx'.format(os.getcwd()))
        assert df.loc['row1'][0] == 1.1 and df.shape == (2,2)

    def test_load_data_other_sheet(self):
        df = load_data('{}/testdata/sample.xlsx'.format(os.getcwd()), 'sheet_2')
        assert df.loc['row3'][1] == 23 and df.shape == (3,3)


class TestCosineSimilarity(unittest.TestCase):

    def test_cosine_similarity(self):
        first = cosine_similarity([1, 1], [2, 2])
        second = cosine_similarity([1, 1], [2, 3])
        third = cosine_similarity([1, 1], [2, 4])
        assert first > 0.99999 and first < 1.00001
        assert second > third

if __name__ == '__main__':
    #
    # the old way of unit test
    #

    # test load_data() default sheet
    df = load_data('testdata/sample.xlsx')
    print(df.loc['row1'][0])
 
    # test load_data() other sheet
    df = load_data('testdata/sample.xlsx', 'sheet_2')
    print(df.loc['row3'][1])
    print(df.shape)

    # test load_words()
    f = load_words("../data/words.txt")
    print(f)
 
    # test load_vectors()
    f = np.load("../data/vectors.npy.gz")
    print(f)

    # test tokenize()
    t = tokenize("hello there I am from Mars")
    print(t)

    # test word embedding #1
    remove_files('testdata/test_words.txt', 'testdata/test_vecs.npy')
    
    with atomic_write('testdata/test_words.txt') as wordfile:
        wordfile.write('cat\ndog\nmoose')

    vectors = np.array([[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 15, 19]])
    np.save('testdata/test_vecs.npy', vectors)
    
    try:
         test_example = WordEmbedding.from_files('testdata/test_words.txt',
                                                     'testdata/test_vecs.npy')
    finally:
         remove_files('testdata/test_words.txt', 'testdata/test_vecs.npy')

    called = test_example('moose')
    print(called)

    # test word embedding #2
    words_all_present = 'Cat cat moose, dog!!'
    output = test_example.embed_document(words_all_present)  
    print(output)
   
