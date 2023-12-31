import bisect
import spacy
from abc import ABC, abstractmethod
from dotenv import load_dotenv
from nltk.corpus import stopwords
from os import getenv
nlp_pt = spacy.load('pt_core_news_lg') 

class IComparator(ABC):
    @abstractmethod
    def compareTextWithKeywords(self, sentences: list[str], keywords: list[str]) -> list[float]:
        pass

class BestMatchsComparator(IComparator):
    def __init__(self):
        load_dotenv()
        self.maxBestMatches = int(getenv("maxBestMatches"))
        self.keyOrderImportance = float(getenv("keyOrderImportance"))
        self.prominentPower = float(getenv("prominentPower"))
        self.debug = (getenv("debug").lower() == "true")
        
    def extractBest(self, tokens, keyTokens):
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
                if(len(bestTokens) > self.maxBestMatches):
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
            top = self.extractBest(tokens, keyTokens)
            results.append(self.evaluateScores(top))
        results = results if results else [0]
        return results

    def compareTextWithKeywords(self, sentences: list[str], keywords: list[str]) -> list[float]:
        return self.compare(sentences, keywords)
