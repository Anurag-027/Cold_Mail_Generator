import streamlit as st
from logic.extract import extract_job_details
from logic.chroma_db import get_relevant_links
from logic.email_gen import generate_email

def main():
    st.title("Cold Email Generator for Job Proposals")
    
    job_url = st.text_input("Enter the Job Posting URL:")
    
    if st.button("Generate Email"):
        if not job_url:
            st.error("Please enter a valid job URL.")
            return
        
        with st.spinner("Extracting job details..."):
            job_details = extract_job_details(job_url)
        
        if not job_details:
            st.error("Failed to extract job details. Please try another URL.")
            return
        
        st.success("Job details extracted successfully!")
        # st.json(job_details)  # Display extracted job details
        
        with st.spinner("Fetching relevant portfolio links..."):
            portfolio_links = get_relevant_links(job_details)
        
        st.success("Portfolio links retrieved!")
        if isinstance(portfolio_links, list):
            for link in portfolio_links:
                if isinstance(link, dict) and "links" in link:
                    st.markdown(f"- [{link['links']}]({link['links']})")
        
        
        with st.spinner("Generating cold email..."):
            cold_email = generate_email(job_details, portfolio_links)
        
        st.success("Cold email generated!")
        st.text_area("Generated Cold Email:", cold_email, height=300)

if __name__ == "__main__":
    main()