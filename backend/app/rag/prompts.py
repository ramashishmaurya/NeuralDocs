
from langchain_core.prompts import PromptTemplate
from langchain_core.load import dumps

templates = PromptTemplate(
    template=""" i am going to ask about this toopics right now {topics} and explain all in {lines}""" , 
    input_variables=['topics' , 'lines'] , 
    validate_template=True
)

json_str  = dumps(templates)
print(json_str)

with open("prompt.json", "w") as f:
    f.write(json_str)


