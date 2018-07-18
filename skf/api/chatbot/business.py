import json, nltk, os

from flask import Flask, jsonify, request
from nltk.stem.lancaster import LancasterStemmer
from skf.api.security import log, val_num, val_alpha_num, val_alpha_num_special
from skf.api.chatbot.scripts import intent_classifier
from skf.api.chatbot.scripts import entity_classifier1
from skf.api.chatbot.scripts import entity_classifier2
from skf.api.chatbot.scripts import code_classify

app = Flask(__name__)

#intent_l=[]   
def answer(question):

        entity=entity_classifier1.entity_recognizer(question.lower())
        if entity is None:
           entity=entity_classifier2.entity(question)
        #if type(entity)==str:
         #  q=des_sol(question,intent)
        #else:
         #  if intent is None:
        #if len(intent_l)==0:
        intent=intent_classifier.predict(question)
        #else:
         #  intent=intent_l[0]

        if intent=="Description" or intent=="Solution":
                  
                  if type(entity)==str:
                       des_sol_ans=des_sol(question,intent)
                       #return des_sol_ans
                  else:
                       #intent_l.insert(0,intent)
                       des_sol_ans=des_sol(question,intent)
                       #intenr_l=[]


                  #print(intent_l)
                  return des_sol_ans
                   
                   #print(des_sol_optn)
                   #des_sol_ans=des_sol(des_sol_optn,intent)

        else:
                  lang=None
                  code_ans=code(question,intent,lang)
                  return code_ans


def des_sol(question,intent):
        entity=entity_classifier1.entity_recognizer(question.lower())
        if entity is None:
           entity=entity_classifier2.entity(question)
        intent=intent  
        read_file = open(os.path.join(app.root_path, "datasets/desc_sol.json"), 'r')
        data = json.load(read_file)
        ite=data['items']
        if type(entity)==str:
            for d in ite:
                 if entity.lower()==d['title'].lower():
                      if intent=="Description":
                          desc="Description for "+d['title']+" is : "+ d[intent]
                          intent="NULL"
                          return desc
                          break
                      else:
                          sol="Solution for "+d['title']+" is : "+ d[intent]
                          intent="NULL"
                          return sol
                          break
        else:
             if len(entity)>0:
                for i in entity:
                    entity[i]=intent+" "+entity[i]
                
                return entity
                #TO_BE_CHANGEDn=int(input("enter your choice "))
                #n=int(n)
                #question=entity[n]
                #des_sol(question,intent)
             else:
                msg="Please be more specific"
                return msg

def code(question,intent,language):
        code_entity=code_classify.entity(question)
        read_file = open(os.path.join(app.root_path, "datasets/code_data.json"), 'r') 
        code_data = json.load(read_file)
        code_ite=code_data['items']
        code_languages=[]
        count=0
        if len(code_entity)==2 and type(code_entity[0])==str:
            entity=str(code_entity[0].strip("\n").lower())
            if language is None:
               language=str(code_entity[-1].strip("\n").lower())
            else:
               language=language
            for d in code_ite:
                 if entity==d['title'].lower():
                    code_languages.append(d['code_lang'])
            for d in code_ite:
                 if entity==d['title'].lower() and language in code_languages:
                    if language==d['code_lang'].lower():
                       code_a="Code for "+ d['content']+"\n Code language is " + d['code_lang']
                       count=count+1
                       return code_a
            if count==0:
                    code_l={}
                    entity=str(code_entity[0].strip("\n").lower())
                    for i in range(len(code_languages)):
                        code_l[i+1]=code_languages[i]      
                    #print("The language you typed is not availabe. Select from the following:")
                    #for i in code_l:
                     #   print(str(i)+":"+code_l[i])
                    #TO_BE_CHANGEDn=int(input("Enter your choice: "))
                    #lang=code_l[n]
                    for d in code_ite:
                        if entity==d['title'].lower() and lang in code_languages:
                              if lang==d['code_lang'].lower():
                                 return d['content']
                                 #print("\n Code language is " + d['code_lang'])
                                 count=count+1
            #TO_BE_CHANGEDques=input("\n Do you have more Questions Y/N ")
            #if(ques=="y" or ques=="Y"):
                   #TO_BE_CHANGEDquestion=input("Enter new question ")
             #      answer(question)
            #else:
             #      print("Thanks for using")
        else:
             if language is None:
               language=str(code_entity[-1].strip("\n").lower())
             else:
               language=language
             #print("Please select from these options ")
             code_list={}
             for i in code_entity[0]:
                 code_list[i]=code_entity[0][i]
             return code_list
             #TO_BE_CHANGEDn=int(input("enter your choice "))
             #question=code_entity[0][n]
             #code(question,"Code",language)

