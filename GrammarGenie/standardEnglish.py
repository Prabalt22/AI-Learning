from langchain_groq import ChatGroq 
from langchain_core.prompts import PromptTemplate

class StandardEnglish():
    def __init__(self,user_input):
        self.user_input = user_input
        self.llm = ChatGroq(
            groq_api_key = str(open("token.txt").read()),
            temperature=0.0,
            model="llama-3.2-90b-vision-preview",
            max_retries=2,
        )
        
    def convertStandardEnglish(self):
        example_prompt = PromptTemplate.from_template("""
        ### INPUT TEXT:{user_input}
        ### INSTRUCTION:
        our task is to correct any grammatical errors in the provided text while maintaining its original 
        meaning.ensure that the corrected text is clear, well-structured, and free of any spelling or 
        grammar issues. return only the corrected version of the text, without additional commentary or 
        explanation.""")

        chain_extract = example_prompt | self.llm
        res = chain_extract.invoke(input={'user_input':self.user_input})
        return res.content
         