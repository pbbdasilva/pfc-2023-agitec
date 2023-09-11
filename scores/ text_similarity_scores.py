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

class Undergrad:
    def __init__(self, institution: str, course: str, thesisTitle: str):
        self.institution = institution
        self.course = course
        self.thesisTitle = thesisTitle

    def __str__(self):
        return self.course + " " + self.thesisTitle

class Masters:
    def __init__(self, master: dict):
        self.institution = master['Institution']
        self.course = master['Course']
        self.thesisTitle = master['ThesisTitle']
        self.areas = " ".join(master['Areas'])
        self.keywords = " ".join(master['Keywords'])

    def __str__(self):
        return self.course + " " + self.thesisTitle + " " + self.areas + " " + self.keywords
    
class Doctorate:
    def __init__(self, master: dict):
        self.institution = master['Institution']
        self.course = master['Course']
        self.thesisTitle = master['ThesisTitle']
        self.areas = " ".join(master['Areas'])
        self.keywords = " ".join(master['Keywords'])

    def __str__(self):
        return self.course + " " + self.thesisTitle + " " + self.areas + " " + self.keywords 

class WorkExp:
    def __init__(self, workexpDict: dict):
        self.institution = workexpDict['Institution']
        self.knowledgeArea = workexpDict['KnowledgeArea']

    def __str__(self):
        return self.course + " " + self.thesisTitle + " " + self.areas + " " + self.keywords 

def get_summary_score(cv: dict, keywords: list) -> float:
    return compare([cv['summary']], keywords)[0]

def get_undergrad_scores(cv: dict, keywords: list) -> list:
    return compare([str(Undergrad(u['Institution'], u['Course'], u['ThesisTitle'])) for u in  cv['undergrad']], keywords)

def get_posgrad_score(cv: dict, keywords: list) -> float:
    return compare([cv['posgrad']['Course'] + " " + cv['posgrad']['ThesisTitle'] ], keywords)[0]

def get_masters_score(cv: dict, keywords: list) -> float:
    return compare([str(Masters(cv['masters']))], keywords)[0]

def get_doctorate_score(cv: dict, keywords: list) -> float:
    return compare([str(Doctorate(cv['doctorate']))], keywords)[0]

def get_workexp_scores(cv: dict, keywords: list) -> list:
    return compare([str(WorkExp(workexpDict)) for workexpDict in  cv['workexp']], keywords)

database = client["lattes"]
collection = database["resumes"]
documents = collection.find({"_id" : "4904387541295597"})
for document in documents:
    print(str(Doctorate(document['doctorate'])))
    print(get_masters_score(document, ["Computação", "Segurança", "Leis", "Legislação", "Redigir"]))
    
client.close()