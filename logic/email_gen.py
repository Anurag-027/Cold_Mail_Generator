from langchain_core.prompts import PromptTemplate
from langchain_groq import ChatGroq

def generate_email(job_details, portfolio_links):
    prompt_email = PromptTemplate.from_template(
        """
        ### JOB DESCRIPTION:
        {job_description}
        
        ### INSTRUCTION:
        You are Anurag, a business development executive at CoMG. CoMG is an AI & Software Consulting company dedicated to facilitating
        the seamless integration of business processes through automated tools. 
        Over our experience, we have empowered numerous enterprises with tailored solutions, fostering scalability, 
        process optimization, cost reduction, and heightened overall efficiency. 
        Your job is to write a cold email to the client regarding the job mentioned above describing the capability of AtliQ 
        in fulfilling their needs.
        Also add the most relevant ones from the following links to showcase CoMG's portfolio: {link_list}
        Remember you are Anurag, BDE at CoMG. 
        Do not provide a preamble.
        ### EMAIL (NO PREAMBLE):
        
        """
    )
    
    llm = ChatGroq(temperature=0, api_key= {API_KEY}, model_name="llama-3.1-8b-instant")
    chain_email = prompt_email | llm
    
    return chain_email.invoke({"job_description": str(job_details), "link_list": portfolio_links}).content
