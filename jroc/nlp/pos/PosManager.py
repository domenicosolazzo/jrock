from . import OBTManager
from . import NLTKTagger

# List of Pos tagger
POS_TAGGERS = { "no" : OBTManager,
                "nn" : OBTManager,
                "nb" : OBTManager,
                "da" : OBTManager,
                "sv" : OBTManager,
                "en" : NLTKTagger,
                "other": None}

class PosManager(object):
    """
    It select the right pos tagger based on the language
    """
    __language = None
    __posTagger = None
    def __init__(self, language="en"):
        self.__language = language

    def __commonWords(self, pos,  number=100):
        """
        Find common words in the text.
        """
        from nltk import FreqDist

        vocab = FreqDist(pos)

        common = [(word[0], index) for (word, index) in vocab.most_common(100) if word[1] == 'NN' or word[1] == 'NNS'  or word[1] == 'NNP'  or word[1] == 'NNPS']
        return common

    def getPosInstance(self, data=None):
        taggerClass = POS_TAGGERS.get(self.__language, None)
        if taggerClass is None:
            raise Exception("Pos tagger not available for this language: %s" % (self.__language, ) ) # Activate a default tagger
        else:
            tagger = taggerClass(data=data)
        return tagger

    def analyze(self, input):
        """
        Analyze the text and return a PosResult
        """
        data = input
        # Get the right instance of the pos tagger
        self.__posTagger = self.getPosInstance()

        # Analyze the data and return a PosResult
        posResult = self.__posTagger.analyze(data)

        posResult['common_words'] = self.__commonWords(posResult['pos'])

        return posResult


    def findTags(self, input):
        """
        Find tags from a previously calculated text analysis
        """
        data = input
        # Get the right instance of the pos tagger
        self.__posTagger = self.getPosInstance(data)

        # Analyze the data and return a PosResult
        posResult = self.__posTagger.findTags(text_analysis=data)

        return posResult
