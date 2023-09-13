import spacy
from nltk.corpus import stopwords
import bisect
from abc import ABC, abstractmethod
#nlp_en = spacy.load('en_core_web_lg')
nlp_pt = spacy.load('pt_core_news_lg') 

class IComparator(ABC):
    @abstractmethod
    def compareTextWithKeywords(self, sentences: list[str], keywords: list[str]) -> list[float]:
        pass

class TopMatchsComparator(IComparator):
    def __init__(self, maxBestMatches: int = 10, keyOrderImportance: float = 0.2, prominentPower: float = 2,
                  debug: bool = False):
        self.maxBestMatches = maxBestMatches
        self.keyOrderImportance = keyOrderImportance
        self.prominentPower = prominentPower
        self.debug = debug
        
    def extractBest(self, tokens, keyTokens, numberOfBests):
        """
        Parameters:
        - tokens: A list of spaCy tokens representing the words in a sentence.
        - keyTokens: A list of spaCy tokens representing key words for comparison.
        - numberOfBests: The maximum number of good matches word-keyword in the sentence to consider. Default: 10
        - keyOrderImportance: A parameter controlling the influence of keyword relevance on final score. Default: 0.2 (1: max relevancy to order, 0: order unconsidered)

        Returns:
        - bestTokens: A list of dictionaries containing the best matches and their similarity scores.
        """
        bestTokens = []
        for idx, keyToken in enumerate(keyTokens):
            for token in tokens:
                bisect.insort(bestTokens, {"key": token.similarity(keyToken)*pow((len(keyTokens) - idx)/len(keyTokens), self.keyOrderImportance),
                                        "word": token.text, "nceKeyWord": keyToken},
                                        key = lambda x: -x["key"])
                if(len(bestTokens) > numberOfBests):
                    del bestTokens[-1]
        return bestTokens

    def evaluateScores(self, bests):
        """
        Parameters:
        - bests: A list of dictionaries containing the best matches and their similarity scores.
        - prominentPower: A parameter controlling how much sportlight should have the bests similarity scores.

        Returns:
        - similarity: The single score based on the top scores.
        """
        bestScores = [(best["key"] + 1)**self.prominentPower for best in bests]
        average = sum(bestScores)/len(bestScores)
        similarity = pow(average, 1/self.prominentPower) - 1
        return similarity

    def compare(self, sentences, keywords):
        """
        Parameters:
        - sentences: A list of sentences (strings) to compare against the keywords.
        - keywords: A list of keywords (strings) of one NCE for comparison, in order of relevance (1º more relevant, last one is the less relevant).
        - maxBestMatches: The maximum number of good matches word-keyword in the sentence to consider. Default: 10
        - keyOrderImportance: A parameter controlling the influence of keyword relevance on final score. Default: 0.2 (1: max relevancy to order, 0: order unconsidered)
        - prominentPower: A parameter controlling how much sportlight should have the bests similarity scores.
        
        Returns:
        - results: A list of similarity scores for each sentence compared to the keywords, in order.
        """
        results = []
        keywords = [str(word).lower() + " " for word in keywords]
        keyTokens = nlp_pt("".join([str(keyword).lower() for keyword in keywords]))
        for sentence in sentences:
            words = sentence.split()
            filteredWords = [word for word in words if word not in stopwords.words('portuguese')]
            filteredWords = [str(word) + " " for word in filteredWords]
            tokens = nlp_pt("".join([str(word) for word in filteredWords]))
            top = self.extractBest(tokens, keyTokens, self.maxBestMatches, self.keyOrderImportance)
            results.append(self.evaluateScores(top, self.prominentPower))
        return results

    def compareTextWithKeywords(self, sentences: list[str], keywords: list[str]) -> list[float]:
        return self.compare(sentences, keywords)
