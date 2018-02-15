# -*- coding: utf-8 -*-
"""
Created on Wed Nov  1 22:19:38 2017

@author: durak
"""

import re
import pprint
import pickle
import textblob
from textblob import TextBlob
import os
#import nltk

def stringify(li, delimiter):
      fulltext = ''
      for index, l in enumerate(li):
            temp = ''
            temp = re.sub('[^a-zA-Z]', ' ', str(l))
            if (temp == '' or len(temp) < 2):
                  print('Data at index: '+ str(index) + ' may have problem: ' + temp)
            if (index == 0):
                  fulltext = temp   
            else:
                  fulltext = fulltext + delimiter + " " + temp   

     

def onlyLetters(text):
      temp = re.sub('[^a-zA-Z]', ' ', str(text))
      return temp


def stopw(text):
      from nltk.corpus import stopwords

      li = text.lower().split()
      sw = stopwords.words('english')
      
      clean = [w for w in li if w not in sw]
      clean = ' '.join(clean)
      return clean

      
def pp(text):
      pprint.pprint(text)


def save_obj(obj, name ):
    with open('obj/'+ name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)


def load_obj(name ):
    with open('obj/' + name + '.pkl', 'rb') as f:
        return pickle.load(f)
  

def translate(text, lang):
      if (type(text) != textblob.blob.TextBlob):
            text = TextBlob(text)
      try:
            translated = text.translate(to=lang)
            return translated
      except textblob.exceptions.NotTranslated:
            return TextBlob("UNABLE_TO_TRANSLATE_INPUT_TEXT")


def correctText(text):
      if (type(text) != textblob.blob.TextBlob):
            text = TextBlob(text)
      return text.correct()
      
      
def stemmer(text):
      from nltk.stem.porter import PorterStemmer
      text = text.split()
      ps = PorterStemmer()
      text = [ps.stem(word) for word in text] 
      text = ' '.join(text)
      return text


def preprocessing(text): # Uses multiple methods written above. 
      prep = onlyLetters(text)
      prep = prep.lower()
      prep = stopw(prep)
      prep = stemmer(prep)
      return prep



      
def parseDate(date):
      from dateutil import parser
      parsed = parser.parse(date)
      subdate = parsed.date()            
      return subdate
      
      
      
def dayDifference(date1, date2): # should be a datetime.date object
      print(abs((date1-date2).days))
      
      
      


def listFilesInDir(directory = "."):
    for filename in os.listdir(directory):
        print(filename)
        
        
        
def isImage(pathToFile):
    import PIL

    try:
        im=PIL.Image.open(pathToFile)
        return True
    except IOError:
        return False
    
    
    
def renameData(directory):
    counter = 1
    for filename in os.listdir(directory):
            os.rename(filename, directory+counter)   
            counter +=1
            


# =============================================================================
# def splitData(directory, folder1 = test, folder2 = train, rate = 0.2): # Randomly splits given the rate
#     for filename in os.listdir(directory):
#         
# 	 
# =============================================================================
	
	 
      
      
      