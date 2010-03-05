from python_API_library import BuedaAPI
API_KEY='2EvC9SVR0Y5vBt48dA1xMwkAxv8XP15OZ7ulsw'
"""

bueda=BuedaAPI(API_KEY)
data=bueda.bueda_call(method='enriched', callback='json', tags="kal-el, thesuperman, krypton")

print data.requestString
print data.queries
print data.split_tags
print data.cleanup
print data.semantic
print data.categories


"""

import unittest

class TestSequenceFunctions(unittest.TestCase):
    bueda=BuedaAPI(API_KEY)
    API_KEY='2EvC9SVR0Y5vBt48dA1xMwkAxv8XP15OZ7ulsw'
    request_no_callback=""
    request_json=""
    request_jsonp=""
    queries= ["kal-el", "thesuperman", "superman", "krypton"]
    split_tags= ["kal-el", "the superman", "superman", "krypton"]
    cleanup= ["Superman", "Krypton"]
    semantic= [
      {
        "categories": [
          "Alter Ego", 
          "Film character", 
          "Fictional Character", 
          "TV Character"
        ], 
        "qtoken": [
          "kal-el", 
          "the superman", 
          "superman"
        ], 
        "concept_id": "/en/superman", 
        "name": "Superman"
      }, 
      {
        "categories": [
          "Fictional Setting", 
          "Character Species", 
          "Fictional Planet"
        ], 
        "qtoken": [
          "krypton"
        ], 
        "concept_id": "/guid/9202a8c04000641f8000000000088667", 
        "name": "Krypton"
      }
    ]
    categories= {}

    def setUp(self,):
        bueda=BuedaAPI(self.API_KEY)

    def test_without_callback(self):
        bueda_object=self.bueda.bueda_call(method='enriched', tags="kal-el, thesuperman, superman, krypton")
        #self.assertEqual(bueda_object.requestString, self.request_no_callback)
        self.assertEqual(bueda_object.queries, self.queries)
        self.assertEqual(bueda_object.split_tags, self.split_tags)
        self.assertEqual(bueda_object.cleanup, self.cleanup)
        self.assertEqual(bueda_object.semantic, self.semantic)
        self.assertEqual(bueda_object.categories, self.categories)



if __name__ == '__main__':
    unittest.main()


"""
    def test_with_callback(self):
        bueda_object=bueda.bueda_call(method='enriched', callback='json', tags="kal-el, thesuperman, krypton")
        element = random.choice(self.seq)
        self.assertTrue(element in self.seq)

    def test_tags_as_list(self):
        self.assertRaises(ValueError, random.sample, self.seq, 20)
        for element in random.sample(self.seq, 5):
            self.assertTrue(element in self.seq)

    def test_as_set(self):
        element = random.choice(self.seq)
        self.assertTrue(element in self.seq)
        
"""