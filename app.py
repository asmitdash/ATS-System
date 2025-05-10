import streamlit as st
import google.generativeai as genai
import os
import PyPDF2 as pdf
from dotenv import load_dotenv
import json

load_dotenv() ## load all our environment variables
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(input):
    model=genai.GenerativeModel('gemini-1.5-flash')
    response=model.generate_content(input)
    return response.text

def input_pdf_text(uploaded_file):
    reader=pdf.PdfReader(uploaded_file)
    text=""
    for page in range(len(reader.pages)):
        page=reader.pages[page]
        text+=str(page.extract_text())
    return text

#Prompt Template

input_prompt="""
You are an expert-level ATS (Applicant Tracking System), specialized in evaluating resumes for roles in software engineering, data science, data analysis, and big data. The job market is highly competitive, and your job is to rigorously analyze how well a resume matches a given job description.

You must evaluate the following:

- Skills: Technical and soft skills match with the job description.
- Experience: Relevance, impact, and use of action verbs.
- Education: Relevance to the role, certifications, and notable achievements.
- Projects: How well projects demonstrate required skills.
- Missing Keywords: Important terms from the JD not present in the resume.
- Profile Summary: How well it aligns with the job description.
- Formatting & Structure: ATS-friendliness, clarity, and conciseness.

Return the analysis in **this exact structure**, formatted in bullet points per section:

{
  "Match": "XX%",
  "MissingKeywords": ["keyword1", "keyword2", ...],
  "ProfileSummary": "Evaluation and suggestions for improvement."
}

Now analyze the following:

Resume:
{resume_text}

Job Description:
{job_description}
"""

## streamlit app
st.set_page_config(page_title="ATS Resume Expert")
st.title("Smart ATS")
st.text("Improve Your Resume ATS")
jd=st.text_area("Paste the Job Description")
uploaded_file=st.file_uploader("Upload Your Resume",type="pdf",help="Please uplaod the pdf")

submit = st.button("Submit")

if submit:
    if uploaded_file is not None:
        text=input_pdf_text(uploaded_file)
        response=get_gemini_response(input_prompt)
        st.subheader(response)
