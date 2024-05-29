import sys
from langchain_community.document_loaders import PyPDFLoader
import ast
import os 
import re
import shutil
from flask import jsonify
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from langchain.prompts import PromptTemplate
from langchain_community.llms import OpenAI
from langchain.chains import LLMChain
from dotenv import load_dotenv
load_dotenv()
from models import Resume
from app import db

def extract_passout_year(string):
        # Regular expression pattern to match years (4 digits)
            pattern = r'\b\d{4}\b'
        
        # Search for the pattern in the string
            match = re.search(pattern, string)
        
            if match:
                # Extract the matched year and convert it to an integer
                passout_year = int(match.group())
                return passout_year
            else:
                print("No passout year found in the string.")
                return None

def text_to_keywords(text):
    # Download NLTK resources (run only once)
    # nltk.download('punkt')
    # nltk.download('stopwords')
    
    # Tokenize the text into words
    words = word_tokenize(text.lower())  # Convert to lowercase
    
    # Remove stopwords
    stop_words = set(stopwords.words('english'))
    words = [word for word in words if word not in stop_words]
    
    # Initialize Porter stemmer for stemming (optional)
    stemmer = PorterStemmer()
    words = [stemmer.stem(word) for word in words]  # Stem each word (optional)
    
    # Remove non-alphanumeric characters (optional)
    words = [word for word in words if word.isalnum()]
    
    return words

def extract_resume_id(filename):
        match = re.search(r'resume_(\d+)', filename)
        if match:
            return int(match.group(1))
        else:
            raise ValueError("Resume ID not found in the file name")

def extract_float(sentence):
                float_pattern = r"[-+]?\d*\.\d+|\d+"  # Regular expression pattern to match floating-point numbers
                match = re.search(float_pattern, sentence)
                if match:
                    return float(match.group())
                else:
                    return None
                       
class ProcessResume:    
    def process_resumes(self):
        # Define the path to the resumes folder
        resumes_folder = os.path.join(os.getcwd(), "resumes")
        processed_folder = os.path.join(os.getcwd(), "processed_resumes")
        os.makedirs(processed_folder, exist_ok=True)

        # Get the list of all resume files in the resumes folder
        resume_files = [f for f in os.listdir(resumes_folder) if f.endswith('.pdf')]

        for resume_file in resume_files:
            resume_path = os.path.join(resumes_folder, resume_file)
            resume_id = extract_resume_id(os.path.basename(resume_file))
            
            # Load and split the resume PDF
            loader = PyPDFLoader(resume_path)
            pages = loader.load_and_split()
            
            # Perform any additional processing with resume_id and pages
            print(f"Processed resume ID: {resume_id}, Number of pages: {len(pages)}")
            
            promt_template_10percentage =PromptTemplate(
            input_variables=['Resume'],
            template="Following is a Resume of a Student \n {Resume} \n\n Find his 10th Class Percentage and Return it as only Floating-point number DO NOT MAKE UP THINGS "
            )

            promt_template_12percentage =PromptTemplate(
                input_variables=['Resume'],
                template="Following is a Resume of a Student \n {Resume} \n\n Find his 12th Class Percentage and Return it as only Floating-point number DO NOT MAKE UP THINGS DO NOT ADD DESCRIPTION "
            )

            promt_template_CGPA =PromptTemplate(
                input_variables=['Resume'],
                template="Following is a Resume of a Student \n {Resume} \n\n Find his Graduation CGPA and Return it as only Floating-point numbers DO NOT MAKE UP THINGS "
            )


            promt_template_skills =PromptTemplate(
                input_variables=['Resume'],
                template="Following is a Resume of a Student \n {Resume} \n\n Find only technology skill keywords and return it as a comma separated list DO NOT INCLUDE SOFT SKILLS DO NOT MAKE UP THINGS "
            )

            promt_template_projects =PromptTemplate(
                input_variables=['Resume'],
                template="Following is a Resume of a Student \n {Resume} \n\n Find all the projects and the technology associated with it return it as a Dictionary where Key is project name and value is technology associated with it  IF ANYTHING IS NOT PRESENT PUT NA \n DO NOT MAKE UP THINGS \n BE PRECISE ONLY RETURN IN FORM OF DICTIONARY  "
            )

            promt_template_soft_skills=PromptTemplate(
                input_variables=['Resume'],
                template="Following is a Resume of a Student \n {Resume} \n\n Find all the Soft skill keywords and return it as a comma separated list DO NOT INCLUDE TECHNOLOGY SKILLS \n DO NOT MAKE UP THINGS "
            )

            promt_template_education =PromptTemplate(
                input_variables=['Resume'],
                template="Following is a Resume of a Student \n {Resume} \n Find his all educations and return as a Python DICTIONARY FORMAT where 'education title'(10th,12th,engg) is key and'colleage_name' as value DO NOT MAKE UP THINGS BE PRECISE ONLY RETURN IN FORM OF DICTIONARY "
            )

            promt_template_exp =PromptTemplate(
                input_variables=['Resume'],
                template="Following is a Resume of a Student \n {Resume} \n\n Find his all previous experience company name , convert the duration in years return it as a Dictionary where Key is Experience Title and value duration in ONLY years IF ANYTHING IS NOT PRESENT PUT NA \n DO NOT MAKE UP THINGS \n BE PRECISE ONLY RETURN IN FORM OF DICTIONARY  "
            )


            promt_template_pass =PromptTemplate(
                input_variables=['Resume'],
                template="Following is a Resume of a Student \n {Resume} \n\n Find his Passout Year and return it as a integer DO NOT MAKE UP THINGS "
            )

            promt_template_branch =PromptTemplate(
                input_variables=['Resume'],
                template="Following is a Resume of a Student \n {Resume} \n\n Find his Graduation/Engineering Branch and rerurn it as a string DO NOT MAKE UP THINGS "
            )
                
            text=pages[0].page_content
            llm=OpenAI()

            chain=LLMChain(llm=llm,prompt=promt_template_branch)
            branch=chain.run(text)
            print(branch)

            chain=LLMChain(llm=llm,prompt=promt_template_pass)
            passout_yr_txt=chain.run(text)
            passout_yr = extract_passout_year(passout_yr_txt)
            print(passout_yr)

            chain=LLMChain(llm=llm,prompt=promt_template_education)
            edu_str=chain.run(text)
            dictionary_data = ast.literal_eval(edu_str)

            clg_10=dictionary_data['10th']
            chain=LLMChain(llm=llm,prompt=promt_template_10percentage)
            str=chain.run(text)
            marks_10 = extract_float(str)

            print(clg_10)
            print(marks_10)

            clg_12=dictionary_data['12th']
            chain=LLMChain(llm=llm,prompt=promt_template_12percentage)
            str=chain.run(text)
            marks_12 = extract_float(str)
            print(clg_12)
            print(marks_12)

            chain=LLMChain(llm=llm,prompt=promt_template_CGPA)
            chain.run(text)
            clg_engg=dictionary_data.get("engg", "NA")
            str=chain.run(text)
            marks_engg = extract_float(str)
            print(clg_engg)
            print(marks_engg)

            chain=LLMChain(llm=llm,prompt=promt_template_exp)
            # Your dictionary
            internship_dict = ast.literal_eval(chain.run(text))

            # Initialize variables
            exp_titles = []
            durations = []

            # Iterate over dictionary items and store values in separate lists
            for key, value in internship_dict.items():
                exp_titles.append(key)
                durations.append(value)

            # Assign values to individual variables
            # Assuming you want to limit it to a maximum of 3 entries
            exp_title1 = exp_titles[0] if len(exp_titles) >= 1 else None
            duration_1 = durations[0] if len(durations) >= 1 else None

            print(exp_title1)
            print(duration_1)

            exp_title2 = exp_titles[1] if len(exp_titles) >= 2 else None
            duration_2 = durations[1] if len(durations) >= 2 else None

            print(exp_title2)
            print(duration_2)

            exp_title3 = exp_titles[2] if len(exp_titles) >= 3 else None
            duration_3 = durations[2] if len(durations) >= 3 else None

            print(exp_title3)
            print(duration_3)

            chain=LLMChain(llm=llm,prompt=promt_template_projects)
            # Using eval() to convert string to dictionary
            project_dict = ast.literal_eval(chain.run(text))

            # Initialize variables
            project_titles = []
            p_techs = []

            # Iterate over dictionary items and store values in separate lists
            for key, value in project_dict.items():
                project_titles.append(key)
                p_techs.append(value)

            # Assign values to individual variables
            # Assuming you want to limit it to a maximum of 4 entries
            project_title1 = project_titles[0] if len(project_titles) >= 1 else None
            p_tech1 = p_techs[0] if len(p_techs) >= 1 else None

            print(project_title1)
            print(p_tech1)

            project_title2 = project_titles[1] if len(project_titles) >= 2 else None
            p_tech2 = p_techs[1] if len(p_techs) >= 2 else None
            print(project_title2)
            print(p_tech2)

            project_title3 = project_titles[2] if len(project_titles) >= 3 else None
            p_tech3 = p_techs[2] if len(p_techs) >= 3 else None
            print(project_title3)
            print(p_tech3)

            chain=LLMChain(llm=llm,prompt=promt_template_skills)
            tech_skills=chain.run(text)
            # tech_skills_list = text_to_keywords(skill_str)
            # tech_skills = ', '.join(tech_skills_list)

            print(tech_skills)

            chain=LLMChain(llm=llm,prompt=promt_template_soft_skills)
            soft_skills=chain.run(text)
            # soft_skills_list = text_to_keywords(chain.run(text))
            # soft_skills = ', '.join(soft_skills_list)
            print(soft_skills)


            print(resume_id)
            print(type(branch))
            print(type(passout_yr))
            print(type(clg_10))
            print(type(marks_10))
            print(type(clg_12))
            print(type(marks_12))
            print(type(clg_engg))
            print(type(marks_engg))
            print(type(exp_title1))
            print(type(duration_1))
            print(type(exp_title2))
            print(type(duration_2))
            print(type(exp_title3))
            print(type(duration_3))
            print(type(project_title1))
            print(type(p_tech1))
            print(type(project_title2))
            print(type(p_tech3))
            print(type(project_title3))
            print(type(p_tech3))
            print(type(tech_skills))
            print(type(soft_skills))
            resume = db.session.query(Resume).filter_by(resume_id=resume_id).first()

            resume.branch = branch
            resume.passout_yr = passout_yr
            resume.clg_10 = clg_10  # replace with actual value if available
            resume.marks_10 = marks_10
            resume.clg_12 = clg_12 # replace with actual value if available
            resume.marks_12 = marks_12
            resume.clg_engg = clg_engg  # replace with actual value if available
            resume.marks_engg = marks_engg
            resume.exp_title1 = exp_title1
            resume.duration1 = duration_1
            resume.exp_title2 = exp_title2
            resume.duration2 = duration_2
            resume.exp_title3 = exp_title3
            resume.duration3 = duration_3
            resume.project_title1 = project_title1
            resume.p_tech1 = p_tech1
            resume.project_title2 = project_title2
            resume.p_tech2 = p_tech2
            resume.project_title3 = project_title3
            resume.p_tech3 = p_tech3
            resume.tech_skills = tech_skills
            resume.soft_skills = soft_skills
            db.session.commit()
            processed_resume_path = os.path.join(processed_folder, resume_file)
            shutil.move(resume_path, processed_resume_path)
            return jsonify({"message": "Job processed successfully."}), 200
        return jsonify({"Error": "Something Went wrong."}), 500
    
