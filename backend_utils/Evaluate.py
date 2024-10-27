import json
import prompt
from langchain import PromptTemplate
from typing import List, Dict
import google.generativeai as genai
from syllabus import get_syllabus
import prompt
def Evaluate_answer(model:genai.GenerativeModel,Question,User_Answer):
   prompt_template = PromptTemplate(
      input_variables=["Question","User_Answer",],
      template=prompt.evaluation_prompt
   )
   return model.generate_content(contents=prompt_template.format(Question=Question,User_Answer=User_Answer)).text.strip()

# Example usage
if __name__ == "__main__":
   api_key = "AIzaSyDUl_6Ll4iamZy7gp9Ipv4uc_EbFMRxqHk"
   model = genai.GenerativeModel("gemini-pro")
   genai.configure(api_key=api_key)
   print(Evaluate_answer(model,"Which would be the best machine learning method to classify binary data?", "For binary classification you can use classification methods such as decision tree, random forest and logisic regression"))
 
