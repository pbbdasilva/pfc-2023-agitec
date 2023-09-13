from . import similarityComparison

class Education:
    def __init__(self, educ: dict):
        self.institution = educ['Institution']
        self.course = educ['Course']
        self.thesisTitle = educ['ThesisTitle']

    def __str__(self):
        return self.course + " " + self.thesisTitle
    
class HighLevelEducation(Education):
    def __init__(self, master: dict):
        super().__init__(master)
        self.thesisTitle = master['ThesisTitle']
        self.areas = " ".join(master['Areas'])
        self.keywords = " ".join(master['Keywords'])
    def __str__(self):
        return self.course + " " + self.thesisTitle + " " + self.areas + " " + self.keywords

class Masters(HighLevelEducation):
    def __init__(self, master: dict):
        super().__init__(master)

    def __str__(self):
        return super().__str__()
    
class Doctorate(HighLevelEducation):
    def __init__(self, master: dict):
        super().__init__(master)

    def __str__(self):
        return super().__str__()

comparator = similarityComparison.BestMatchsComparator()

def get_summary_similarity(cv: dict, keywords: list) -> float:
    try: return comparator.compareTextWithKeywords([cv['summary']], keywords)[0]
    except TypeError: return 0

def get_undergrad_similarities(cv: dict, keywords: list) -> list:
    try: return comparator.compareTextWithKeywords([str(Education(u)) for u in  cv['undergrad']], keywords)
    except TypeError: [0]

def get_posgrad_similarity(cv: dict, keywords: list) -> float:
    try: return comparator.compareTextWithKeywords([cv['posgrad']['Course'] + " " + cv['posgrad']['ThesisTitle'] ], keywords)[0]
    except TypeError: return 0

def get_masters_similarity(cv: dict, keywords: list) -> float:
    try: return comparator.compareTextWithKeywords([str(Masters(cv['masters']))], keywords)[0]
    except TypeError: return 0

def get_doctorate_similarity(cv: dict, keywords: list) -> float:
    try: return comparator.compareTextWithKeywords([str(Doctorate(cv['doctorate']))], keywords)[0]
    except: return 0

# def get_workexp_similarities(cv: dict, keywords: list) -> list: 
#     return comparator.compareTextWithKeywords([str(WorkExp(workexpDict)) for workexpDict in  cv['workexp']], keywords)

def get_areasList_similarities(cv: dict, keywords: list) -> list: 
    try: return comparator.compareTextWithKeywords([areaDict['Specialty'] + " " + areaDict['KnowledgeArea'] for areaDict in  cv['areas']], keywords)
    except: return [0]

def get_articles_similarities(cv: dict, keywords: list) -> list: 
    try: return comparator.compareTextWithKeywords([article for article in cv['articles']], keywords)
    except TypeError: return [0]
