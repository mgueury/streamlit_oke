import streamlit as st
import os
import pypdf as pdf
import json
from dotenv import load_dotenv
from langchain_community.chat_models.oci_generative_ai import ChatOCIGenAI
import pages.utils.config as config  # Import the configuration
from pages.utils.style import set_page_config
set_page_config()
# Load environment variables
load_dotenv()

# Configure OCI LLM

llm = ChatOCIGenAI(
    model_id=config.GENERATE_MODEL,
    service_endpoint=config.ENDPOINT,
    compartment_id=config.COMPARTMENT_ID,
    auth_type="INSTANCE_PRINCIPAL",         
    model_kwargs={"temperature": 0, "max_tokens": 400}
)

def get_oci_response(input_text):
    response = llm.invoke([input_text])
    return response.content

def input_pdf_text(uploaded_file):
    reader = pdf.PdfReader(uploaded_file)
    text = ""
    for page in range(len(reader.pages)):
        page = reader.pages[page]
        text += str(page.extract_text())
    return text

def parse_response(response):
    try:
        print("Ansh i am here")
        print(response)
        response_json = json.loads(response.split('}')[0] + '}')
        jd_match = response_json.get("JD Match", "N/A")
        if isinstance(jd_match, str) and jd_match.endswith('%'):
            jd_match = int(jd_match.rstrip('%'))
        missing_keywords = response_json.get("MissingKeywords", [])
        profile_summary = response_json.get("Profile Summary", "N/A")
        reason = response_json.get("Reason", "N/A")
        return jd_match, missing_keywords, profile_summary, reason
    except (json.JSONDecodeError, IndexError) as e:
        st.error(f"Error parsing response: {e}")
        return "N/A", [], "N/A", "N/A"

# Prompt Template
input_prompt = """
Hey Act Like a skilled or very experienced ATS(Application Tracking System)
with a deep understanding of tech field, software engineering, data science, data analyst
and big data engineer. Your task is to evaluate the resume based on the given job description.
You must consider the job market is very competitive and you should provide 
best assistance for improving the resumes. Assign the percentage Matching based 
on JD and
the missing keywords with high accuracy. You should also explain why the resume
is selected or rejected. Ensure the missing keywords are derived based on a comparison
between the job description and the resume content.
resume:{text}
description:{jd}

I want the response in one single string having the structure
{{"JD Match": "percentage", "MissingKeywords": ["list of missing keywords"], "Profile Summary": "profile summary", "Reason": "reason for selection or rejection"}}
"""

# Streamlit app
st.title("Smart ATS using Oracle Gen AI")
jd = st.text_area("Paste the Job Description")
uploaded_files = st.sidebar.file_uploader("Upload Your Resumes", accept_multiple_files=True, type="pdf", help="Please upload the pdfs")

submit = st.button("Submit")
with st.spinner("Processing. Please wait...."):
    if submit:
        if jd and uploaded_files:
            for uploaded_file in uploaded_files:
                if uploaded_file is not None:
                    resume_text = input_pdf_text(uploaded_file)
                    candidate_name = os.path.splitext(uploaded_file.name)[0]  # Use file name without extension as candidate name
                    formatted_prompt = input_prompt.format(text=resume_text, jd=jd)
                    response = get_oci_response(formatted_prompt)
                    
                    # Print response for debugging
                    # st.text(f"Response for {candidate_name}'s resume: {response}")
                    
                    jd_match, missing_keywords, profile_summary, reason = parse_response(response)

                    # Determine selection status
                    if jd_match != "N/A" and jd_match >= 60:
                        status = "Selected"
                        status_color = "green"
                    else:
                        status = "Rejected"
                        status_color = "red"

                    # Display the result
                    st.markdown(f"## <span style='color:cadetblue'>{candidate_name}'s Resume</span>", unsafe_allow_html=True)
                    st.markdown(f"**<span style='color:Orange'>JD Match:</span>** {jd_match}%", unsafe_allow_html=True)
                    st.markdown(f"**Status:** <span style='color:{status_color}'>{status}</span>", unsafe_allow_html=True)
                    
                    # Create a collapsible section for additional details
                    with st.expander("View More Details"):
                        st.markdown(f"**<span style='color:cadetblue'>Profile Summary:</span>** {profile_summary}", unsafe_allow_html=True)
                        st.markdown(f"**<span style='color:cadetblue'>Missing Keywords:</span>** {', '.join(missing_keywords) if missing_keywords else 'None'}", unsafe_allow_html=True)
                        st.markdown(f"**<span style='color:cadetblue'>Reason:</span>** {reason}", unsafe_allow_html=True)
        else:
            st.error("Please provide both the job description and resumes for matching.")

    
