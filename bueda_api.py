'''
@author: Aayush Kumar
@contact: contact@bueda.com
@organization: Bueda, Inc.
@version: 0.1
@since: 18 February 2010

@summary: A python library file that makes interacting with the Bueda API easier.

Example of usage:

API_KEY=<Your API Key>
bueda=BuedaAPI(API_KEY)
data=bueda.bueda_call(method='enriched', callback='json', tags="kal-el, thesuperman, krypton"<, other list of arguments to be made to the API>)

bueda.bueda_call returns an object of type BuedaObject.  To print the members of the object you can do as follows:  

print data.responseString
print data.queries
print data.split_tags
print data.cleanup
print data.semantic
print data.categories

Note that: 
           responseString is the API response in string format. 
           queries=[] -> an array that stores the initial list of tags
           split_tags=[] -> an array that stores the split tags as returned by the API.
           cleanup=[]  -> an array that stores the cleaned up tags as returned by the API.
           semantic={}  -> has dictionary datatype that stores the semantic data as returned by the API.
           categories=[] -> an array that stores the cleaned up tags as returned by the API.
'''



import urllib2
import json
import warnings
'''
Takes in a set of tags and constructs the API call URL.
'''
def value_to_string(values):
    queryString=""
    for tag in values:
        if (queryString==""):
            queryString+=tag
        else:
            queryString+=", " + tag
    
    return queryString


class BuedaObject:
    # responseString is the API response in string format
    responseString=""
    # queries: an array that stores the initial list of tags
    queries=[]
    # split_tags: an array that stores the split tags as returned by the API.
    split_tags=[]
    # cleanup: an array that stores the cleaned up tags as returned by the API.
    cleanup=[]
    # semantic: has an array of dictionaries datatype that stores the semantic data as returned by the API.
    semantic=[]
    # categories: an array that stores the cleaned up tags as returned by the API.
    categories=[]
    

class BuedaAPI:
    API_KEY=""
    bueda=BuedaObject()
        
    def __init__(self, API_KEY):
        if API_KEY!="" or API_KEY is not None:
            self.API_KEY=API_KEY
        else:
            raise StandardError("API Key can not be None type or empty")
    
    '''
    Processes responses that have callback values as json and jsonp.
    Converts the response string to json readable format and then loads it into 
    the Json object.  It returns this Json object
    ''' 
    def process_response(self, response):
        extract_json=response.split("(")
        response=""
        for i in range(1, len(extract_json)):
            response+=extract_json[i] 
        extract_json=response.split(")")
        response=""
        for i in range(0, len(extract_json)-1):
            response=extract_json[i]
        
        data=json.loads(response)
        return data
    
    '''
    Takes a valid API call URL and returns the API response as a json object
    ''' 
    def get_data(self, apiUrl):
        
        response = urllib2.urlopen(apiUrl)            
        self.bueda.responseString=response.read()
        
        if "callback" in apiUrl:
            return self.process_response(self.bueda.responseString)
        else:
            data=json.loads(self.bueda.responseString)
            return data
        
    '''
    Takes the method_name for the API call, and, a dict of arguments for the API call.
    It converts these arguments into a valid API call URL.
    It returns this API call url.
    ''' 
    def make_API_call_url(self, method_name, **kwargs):
        url="http://api.bueda.com/"+str(method_name)+"?apikey="+str(self.API_KEY)
        
        rest_of_url=""
        for key in kwargs:
            if key=='method':
                continue
            else:
                value=kwargs[key]
                tempString=""
                flag=1
                if isinstance(value, dict):
                    # If it is a dict type then do nothing
                    tempString=""
                    flag=0
                elif isinstance(value, str):
                    tempString=value
                elif isinstance(value, list):
                    tempString=value_to_string(value)
                elif isinstance(value, set):
                    tempString=value_to_string(value)
                else:
                    try:
                        tempString=str(value)
                    except:
                        warnings.warn("Can't convert value to string.  Ignoring key..value pair")
                        flag=0
                
                try:
                    tempString=tempString.decode('ascii')
                except UnicodeDecodeError:
                    warnings.warn("Can't decode url to ascii.  Ignoring request.")
                    return 0
                else:
                    tempString = urllib2.quote(tempString)
                
                if (flag!=0):
                    rest_of_url+="&"+key+"="+tempString
                
        url+=rest_of_url
        return url
        
        
    '''
    Takes in a json object from the API method enriched.
    It then stores that data in separate accessors of the BuedaObject.
    ''' 
    def process_json_data_enriched(self, data):
        self.bueda.queries=data["query"]
        tempDict={}
        tempDict=data["result"]
        self.bueda.split_tags=tempDict["split_tags"]
        self.bueda.cleanup=tempDict["cleanup"]
        self.bueda.semantic=tempDict["semantic"]
        self.bueda.categories=tempDict["categories"]
            
    '''
    This is the function that most users would call.
    It takes in a set of arguments and then converts that to a valid API call URL.
    It then processes the response from the API and parses this data into BuedaObject.
    Return is an object of type BuedaObject which has accessors for each of the components of the API_call
    '''
    def bueda_call(self, **kwargs):
        self.bueda=BuedaObject()
        key='method'
        if key in kwargs:
            method_name=kwargs[key]
        else:
            raise KeyError('Need to have a \'method\' argument to make API call')
        
        url=self.make_API_call_url(method_name, **kwargs)
        data= self.get_data(url)
        
        if data==0:
            return self.bueda
        
        if method_name=="enriched":
            self.process_json_data_enriched(data)
        
        return self.bueda
    
    