import chromadb
import uuid
import pandas as pd

def get_relevant_links(job_details):
    dataf = pd.read_csv("my_portfolio.csv")
    client = chromadb.PersistentClient('vectorstore')
    collection = client.get_or_create_collection(name="portfolio")
    
    if not collection.count():
        for _, row in dataf.iterrows():
            collection.add(documents=row["Techstack"],
                           metadatas={"links": row["Links"]},
                           ids=[str(uuid.uuid4())])
    
    job_title = list(job_details.keys())[0]
    skills = job_details[job_title].get('skills', [])
    
    result =  collection.query(query_texts=skills, n_results=2).get('metadatas', [])
    
     # Flatten the list of links in one step
    extracted_links = [link["links"] for sublist in result for link in sublist if "links" in link]

    return extracted_links
