from langchain_community.document_loaders import WebBaseLoader
from langchain_core.prompts import PromptTemplate
from langchain_groq import ChatGroq
from langchain_core.output_parsers import JsonOutputParser


def flatten_list(nested_list):
    """Recursively flattens a nested list into a single list."""
    flat_list = []
    for item in nested_list:
        if isinstance(item, list):
            flat_list.extend(flatten_list(item))  # Recursive call for sublist
        else:
            flat_list.append(item)  # Append normal item
    return flat_list

def extract_job_details(url):
    loader = WebBaseLoader(url)
    page_data = loader.load().pop().page_content
    
    prompt_extract = PromptTemplate.from_template(
        """
        ### SCRAPED TEXT FROM WEBSITE:
        {page_data}
        ### INSTRUCTION:
        The scraped text is from the career's page of a website.
        Your job is to extract the job postings and return them in JSON format containing the 
        following keys: `role`, `experience`, `skills` and `description`.
        Only return the valid JSON.
        ### VALID JSON (NO PREAMBLE):    
        """
    )
    
    llm = ChatGroq(temperature=0, api_key="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", model_name="llama-3.1-8b-instant")
    chain_extract = prompt_extract | llm
    res = chain_extract.invoke(input={'page_data': page_data})
    
    json_parser = JsonOutputParser()
    job_details = json_parser.parse(res.content)
    
# Ensure job_details is always a dictionary
    if isinstance(job_details, list):
        job_details = {"Job Posting": job_details[0]}  # Convert list to dict

    # Flatten skills
    for job in job_details.values():
        if 'skills' in job and isinstance(job['skills'], list):
            job['skills'] = flatten_list(job['skills'])  

    return job_details
