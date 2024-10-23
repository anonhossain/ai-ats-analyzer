import PyPDF2 as pdf
import google.generativeai as genai
import os

# Configure the Generative AI with API key
def configure_genai():
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to get Gemini AI response
def get_gemini_response(prompt):
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content(prompt)
    return response.text

# Function to extract text from the uploaded PDF resume
def input_pdf_text(resume_file):
    reader = pdf.PdfReader(resume_file)
    text = ""
    for page in range(len(reader.pages)):
        page_text = reader.pages[page].extract_text()
        text += str(page_text)
    return text

# Function to process resume based on the user's selected action
def process_resume(job_desc, resume_text, action):
    if action == 'tell_resume':
        prompt = f"""
        You are an experienced Technical Human Resource Manager. Review the following resume and compare it to the provided job description.

        Job Description:
        {job_desc}

        Resume:
        {resume_text}

        Please provide your professional evaluation, highlighting the strengths and weaknesses of the applicant in relation to the job requirements. Also, shorten the resume by focusing on skills, education, projects, and work experience.
        """
    elif action == 'improvise_skills':
        prompt = f"""
        You are a Technical Human Resource Manager tasked with evaluating the resume in light of the provided job description.

        Job Description:
        {job_desc}

        Resume:
        {resume_text}

        Highlight the strengths and weaknesses of the applicant and offer suggestions for improvement in areas like skills, experience, education, and projects.
        """
    elif action == 'percentage_match':
        prompt = f"""
        You are an ATS (Applicant Tracking System) scanner. Please evaluate the following resume against the provided job description.

        Job Description:
        {job_desc}

        Resume:
        {resume_text}

        Only give the percentage match and missing keywords, nothing else.
        """
    elif action == 'question_generator':
        prompt = f"""
        You are an interviewer preparing questions based on the candidate's resume and the job description.

        Job Description:
        {job_desc}

        Resume:
        {resume_text}

        Please generate a list of technical and behavioral multiple choice questions that will pop during CV submission. Return in json format.
        """
    elif action == 'viva_questions':
        prompt = f"""
        You are a panel preparing viva questions based on the candidate's resume and the job description.

        Job Description:
        {job_desc}

        Resume:
        {resume_text}

        Provide a set of viva questions that assess the candidate's understanding and experience related to the job. Also generate technical questions from CV Projects and experience.
        """
    else:
        raise ValueError("Invalid action provided")

    # Get the AI response
    response_text = get_gemini_response(prompt)
    return response_text

# Function to process the resume action
async def process_resume_action(data, resume_file):
    resume_text = input_pdf_text(resume_file.file)
    return process_resume(data.job_desc, resume_text, data.action)
