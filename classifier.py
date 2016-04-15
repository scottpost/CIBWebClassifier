import random
import pymongo
import datetime

class ArticleClassificationPackage:
    def __init__(self, username, password):
        ''' Constructor for this class. '''
        self.description = 'Article Classification Package. Software Group, Spring 2016. Capital Investments at Berkeley.'
        self.username = username
        self.password = password
        self.uri = 'mongodb://' + username + ':' + password + '@ds023490.mlab.com:23490/ciberkeley_nlp'
        self.client = pymongo.MongoClient(self.uri)
        self.db = self.client['ciberkeley_nlp'] # or db = client.ciberkeley_nlp if it already exists
        self.collection = self.db['articles']
        self.classifications = self.db['classify']


    def get_loughran_mcdonald(self):
        cursor = csv.reader(open('data/LoughranMcDonald_MasterDictionary_2014.csv', 'rU'))
        lm_dict = []
        for item in cursor:
            lm_dict.append(item[0])
        return lm_dict


    def get_article(self, query_string = None):
        result_list = self.collection.find()
        result = result_list[random.randint(0, result_list.count())]
        if self.classifications.find_one({'_id': result['_id']}) != None:
            print 'Article already graded: ' + str(result['_id'])
        return result

    def get_text(self, document):
        return document['text']

    def classify(self, document, _class = 0):
        if int(_class) != _class:
            print 'Classification Score must be an integer'
            return None
        article_id = document['_id']
        json = {"article_id": article_id, "username": self.username,
         "_class": (_class % 2), 'date': datetime.datetime.now()}
        mongo_insert_object = self.classifications.insert_one(json)
        mongo_id = mongo_insert_object.inserted_id
        return mongo_id

