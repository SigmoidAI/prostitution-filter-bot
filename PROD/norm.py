# Importing all needed functions.
from sklearn.base import BaseEstimator, TransformerMixin
import re

class TextNormalizer(BaseEstimator, TransformerMixin):
    def __init__(self, stopwords : list, stemmer : 'nltk.stemmer', tokenizer : 'function') -> None:
        '''
            The constructor of the Transformer class.
        :param stopwords: list
            The list of words to ignore.
        :param stemmer: must impliment the stem function.
            The stemmer object.
        :param tokenizer: function
            The tokenizing function.
        '''
        # Setting up the parameters.
        self.stopwords = stopwords
        self.stemmer = stemmer
        self.tokenizer = tokenizer

    def fit(self, X : 'np.array', y : 'np,array' = None , **fit_params) -> 'TextNormalizer':
        '''
            The fit function.
        :param X: np.array or list
            The list of np.array with textes.
        :param y: np.array or list
            IGNORED
        :param fit_params: dict
            The fitting parameters. sci-kit learn need them.
        :return: TextNormalizer
            The fitted object.
        '''
        return self

    def transform(self, X : 'np.array', y : 'np.array' = None, **fit_params) -> list:
        '''
            The fit function.
        :param X: np.array or list
            The list of np.array with textes.
        :param y: np.array or list
            IGNORED
        :param fit_params: dict
            The fitting parameters. sci-kit learn need them.
        :return: list
            The normalized textes.
        '''
        for i in range(len(X)):
            # Replacing the \n and \r symbols.
            X[i] = X[i].replace('\n', ' ')
            X[i] = X[i].replace('\r', ' ')

            # Extracting all smiles and other unicode data.
            X[i] = re.sub('[^\x00-\x7F]+', '', X[i])

            # Lowering the texts.
            X[i] = X[i].lower()

            # Extracting only the letters from the text.
            X[i] = ' '.join(re.findall('[a-zA-Z]+', X[i]))

            # Extracting stopwords and fords word with fewer than 2 letters.
            X[i] = ' '.join([word for word in self.tokenizer(X[i]) if len(word) >=2 and word not in self.stopwords])

            # Stemming the texts.
            X[i] = ' '.join([self.stemmer.stem(word) for word in self.tokenizer(X[i])])
        return X

    def fit_transform(self, X : 'np.array', y : 'np.array' = None, **fit_params) -> list:
        '''
            Fitting and transforming the normalizer at the same time.
        :param X: np.array or list
            The list of np.array with textes.
        :param y: np.array or list
            IGNORED
        :param fit_params: dict
            The fitting parameters. sci-kit learn need them.
        :return: list
            The normalized textes.
        '''
        return self.fit().transform()