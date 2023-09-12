from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from enum import Enum
from similarityComparison import compare
import json

username = json.load(open("credentials.json"))['username']
password = json.load(open("credentials.json"))['password']

URI = f'''mongodb+srv://{username}:{password}@lattes-pfc-2023.twn2hk2.mongodb.net/?retryWrites=true&w=majority
'''


client = MongoClient(URI,server_api = ServerApi('1'))

class Education:
    def __init__(self, institution: str, course: str, thesisTitle: str):
        self.institution = institution
        self.course = course
        self.thesisTitle = thesisTitle

    def __str__(self):
        return self.course + " " + self.thesisTitle
    
class HighLevelEducation(Education):
    def __init__(self, master: dict):
        super.__init__(master)
        self.thesisTitle = master['ThesisTitle']
        self.areas = " ".join(master['Areas'])
        self.keywords = " ".join(master['Keywords'])
    def __str__(self):
        return self.course + " " + self.thesisTitle + " " + self.areas + " " + self.keywords

class Masters(HighLevelEducation):
    def __init__(self, master: dict):
        super.__init__(master)

    def __str__(self):
        return super.__str__()
    
class Doctorate(HighLevelEducation):
    def __init__(self, master: dict):
        super.__init__(master)

    def __str__(self):
        return super.__str__()

def get_summary_similarity(cv: dict, keywords: list) -> float:
    return compare([cv['summary']], keywords)[0]

def get_undergrad_similarities(cv: dict, keywords: list) -> list:
    return compare([str(Education(u['Institution'], u['Course'], u['ThesisTitle'])) for u in  cv['undergrad']], keywords)

def get_posgrad_similarity(cv: dict, keywords: list) -> float:
    return compare([cv['posgrad']['Course'] + " " + cv['posgrad']['ThesisTitle'] ], keywords)[0]

def get_masters_similarity(cv: dict, keywords: list) -> float:
    return compare([str(Masters(cv['masters']))], keywords)[0]

def get_doctorate_similarity(cv: dict, keywords: list) -> float:
    return compare([str(Doctorate(cv['doctorate']))], keywords)[0]

# def get_workexp_similarities(cv: dict, keywords: list) -> list: 
#     return compare([str(WorkExp(workexpDict)) for workexpDict in  cv['workexp']], keywords)

def get_areasList_similarities(cv: dict, keywords: list) -> list: 
    return compare([areaDict['Specialty'] + " " + areaDict['KnowledgeArea'] for areaDict in  cv['areas']], keywords)

def get_articles_similarities(cv: dict, keywords: list) -> list: 
    return compare([article for article in cv['articles']], keywords)

database = client["lattes"]
collection = database["resumes"]
documents = collection.find({"_id" : "5431165627826233"})
for document in documents:
    print(document['articles'])
    print(get_articles_similarities(document, ["Computação", "Segurança", "Leis", "Legislação", "Redigir"]))
    print(get_undergrad_similarities(document, ["Computação", "Segurança", "Leis", "Legislação", "Redigir"]))
    print(get_areasList_similarities(document, ["Computação", "Segurança", "Leis", "Legislação", "Redigir"]))
    print(get_doctorate_similarity(document, ["Computação", "Segurança", "Leis", "Legislação", "Redigir"]))
    print(get_posgrad_similarity(document, ["Computação", "Segurança", "Leis", "Legislação", "Redigir"]))
    print(get_masters_similarity(document, ["Computação", "Segurança", "Leis", "Legislação", "Redigir"]))

    
client.close()