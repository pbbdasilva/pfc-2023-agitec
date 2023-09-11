import spacy
from nltk.corpus import stopwords
import bisect
#nlp_en = spacy.load('en_core_web_lg')
nlp_pt = spacy.load('pt_core_news_lg') 

def extractBest(tokens, keyTokens, numberOfBests, keyOrderImportance = 10):
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
            bisect.insort(bestTokens, {"key": token.similarity(keyToken)*pow((len(keyTokens) - idx)/len(keyTokens), keyOrderImportance),
                                       "word": token.text, "nceKeyWord": keyToken},
                                       key = lambda x: -x["key"])
            if(len(bestTokens) > numberOfBests):
                del bestTokens[-1]
    return bestTokens

def evaluateScores(bests, prominentPower=2):
    """
    Parameters:
    - bests: A list of dictionaries containing the best matches and their similarity scores.
    - prominentPower: A parameter controlling how much sportlight should have the bests similarity scores.

    Returns:
    - similarity: The single score based on the top scores.
    """
    bestScores = [(best["key"] + 1)**prominentPower for best in bests]
    average = sum(bestScores)/len(bestScores)
    similarity = pow(average, 1/prominentPower) - 1
    return similarity

def compare(sentences, keywords, maxBestMatches = 10, keyOrderImportance = 0.2, prominentPower = 2):
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
        top = extractBest(tokens, keyTokens, maxBestMatches, keyOrderImportance)
        results.append(evaluateScores(top, prominentPower))
    return results
