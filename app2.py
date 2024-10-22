import os
import PyPDF2 as pdf
import google.generativeai as genai

# Set your Google API key environment variable
os.environ['GOOGLE_API_KEY'] = 'api Key'
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to configure Generative AI with API key
def configure_genai():
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to get Gemini AI response
def get_gemini_response(prompt):
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content(prompt)
    return response.text

# Function to extract text from the uploaded PDF resume
def input_pdf_text(resume_file_path):
    with open(resume_file_path, 'rb') as file:
        reader = pdf.PdfReader(file)
        text = ""
        for page in range(len(reader.pages)):
            page_text = reader.pages[page].extract_text()
            text += str(page_text)
    return text

# Function to process resume based on the user's selected action
def process_resume(job_desc, resume_text, action):
    # Create the prompt based on the selected action
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

# Function to load job description from the text file
def input_job_description(job_description_file_path):
    with open(job_description_file_path, 'r') as file:
        job_description = file.read()
    return job_description

# Main function for running the program with predefined file paths
if __name__ == '__main__':
    # Predefined file paths
    job_description_file_path = 'F:/Study/Semester-9/SE 331 Software Engineering Design Capstone Project/jd.txt'
    resume_file_path = 'F:/Study/Semester-9/SE 331 Software Engineering Design Capstone Project/Anon Hossain.pdf'

    # Read the job description and resume
    try:
        job_description = input_job_description(job_description_file_path)
        resume_text = input_pdf_text(resume_file_path)
    except FileNotFoundError as e:
        print(f"Error: {e}")
        exit()

    # Continuously prompt the user until they press "5" to exit
    while True:
        # Prompt the user to select the option
        print("\nChoose an option:")
        print("1. Percentage match")
        print("2. How to improve for this job")
        print("3. Question Generator")
        print("4. Viva Questions")
        print("5. Exit")
        option = input("Enter the number of your choice: ")

        try:
            # Execute based on the user's choice
            if option == "1":
                response = process_resume(job_description, resume_text, 'percentage_match')
                print("\nThe Percentage Match is:\n")
                print(response)

            elif option == "2":
                response = process_resume(job_description, resume_text, 'improvise_skills')
                print("\nSuggestions to Improve for the Job:\n")
                print(response)

            elif option == "3":
                response = process_resume(job_description, resume_text, 'question_generator')
                print("\nQuestion Generator Output:\n")
                print(response)

            elif option == "4":
                response = process_resume(job_description, resume_text, 'viva_questions')
                print("\nViva Questions:\n")
                print(response)

            elif option == "5":
                print("Exiting the program.")
                break

            else:
                print("Invalid option chosen. Please select a valid option.")

        except Exception as e:
            print(f"An error occurred: {e}")
