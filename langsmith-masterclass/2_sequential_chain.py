from langchain_groq import ChatGroq
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
import os

os.environ['LANGCHAIN_PROJECT'] = 'Sequential_LLM_App'
load_dotenv(dotenv_path="langsmith-masterclass/.env")

prompt1 = PromptTemplate(
    template='Generate a detailed report on {topic}',
    input_variables=['topic']
)

prompt2 = PromptTemplate(
    template='Generate a 5 pointer summary from the following text \n {text}',
    input_variables=['text']
)

model1 = ChatGroq(model="llama-3.1-8b-instant")
model2 = ChatGroq(model="llama-3.3-70b-versatile")

parser = StrOutputParser()

chain = prompt1 | model1 | parser | prompt2 | model2 | parser

config = {
    'tags': ["llm app", "report generation", "summary generation"],
    'metadata': {"model1": "llama-3.1-8b-instant", "model2": "llama-3.3-70b-versatile", 'parser': 'StrOutputParser'}
}
result = chain.invoke({'topic': 'Unemployment in India'}, config=config)

print(result)
