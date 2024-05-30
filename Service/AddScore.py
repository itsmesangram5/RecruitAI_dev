from flask import Blueprint, jsonify
from models import db, JobApplication, Resume, JobPosting, Score
from sqlalchemy.exc import SQLAlchemyError
import pandas as pd
from langchain_community.document_loaders.csv_loader import CSVLoader
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class AddScore:
    def add_score(self, jobapplication_id):
        try:
            # Load job application details
            job_application = JobApplication.query.get(jobapplication_id)
            resume = Resume.query.get(job_application.resume_id)
            job_posting = JobPosting.query.get(job_application.job_id)

            if not resume or not job_posting:
                return {"message": "Resume or Job Posting not found"}, 404

            # Calculate education score
            marks_10 = float(resume.marks_10)
            marks_12 = float(resume.marks_12)
            marks_engg = float(resume.marks_engg) * 10 if resume.marks_engg <= 10 else float(resume.marks_engg)
            education = (marks_10 + marks_12 + marks_engg) / 3

            # Calculate branch rank percentage
            branch = resume.branch
            branch_percentage = self.calculate_branch_rank_percentage(branch)

            # Calculate college rank percentage
            college = resume.clg_engg
            college_percentage = self.calculate_clg_rank_percentage(college)

            # Calculate company rank percentage based on experience title
            exp_title1 = resume.exp_title1
            company_percentage = self.calculate_company_rank_percentage(exp_title1)

            # Calculate project similarity score
            project_tech_resume = f"{resume.p_tech1} {resume.p_tech2} {resume.p_tech3}"
            project_tech_job = job_posting.project_tech
            project_similarity = self.calculate_text_similarity(project_tech_resume, project_tech_job)

            # Calculate soft skills similarity score
            soft_skills_resume = resume.soft_skills
            soft_skills_job = job_posting.soft_skills
            soft_skill_similarity = self.calculate_text_similarity(soft_skills_resume, soft_skills_job)

            # Calculate technical skills similarity score
            tech_skills_resume = resume.tech_skills
            tech_skills_job = job_posting.tech_skills
            tech_skill_similarity = self.calculate_text_similarity(tech_skills_resume, tech_skills_job)

            # Calculate overall score
            overall = education + branch_percentage + college_percentage + company_percentage + project_similarity + soft_skill_similarity + tech_skill_similarity

            # Add score entry to the Score table
            score = Score(
                job_application_id=jobapplication_id,
                education=education,
                branch=branch_percentage,
                clg=college_percentage,
                experience=company_percentage,
                project=project_similarity,
                soft_skill=soft_skill_similarity,
                tech_skill=tech_skill_similarity,
                overall=overall
            )
            db.session.add(score)
            db.session.commit()

            return {"message": "Score added successfully"}, 200

        except SQLAlchemyError as e:
            db.session.rollback()
            return {"message": "Something went wrong"}, 500

    def calculate_branch_rank_percentage(self, branch):
        loader = CSVLoader(file_path='C://Users//itsme//OneDrive//Documents//RecruitAI_dev//resources//branch_ranking.csv')
        data = loader.load()
        txt=branch

        faiss_index = FAISS.from_documents(data, OpenAIEmbeddings())
        docs = faiss_index.similarity_search(txt, k=1)
        print(type(docs))
        data_row=docs[0]
        row_number = data_row.metadata['row']
        print(row_number)
        print("\n")

        branch_score=((1795-row_number)*100)/1795
        print(branch_score)
        return branch_score

    def calculate_clg_rank_percentage(self, college):
        loader = CSVLoader(file_path='C://Users//itsme//OneDrive//Documents//RecruitAI_dev//resources//clg_ranking.csv')
        data = loader.load()
        txt=college

        faiss_index = FAISS.from_documents(data, OpenAIEmbeddings())
        docs = faiss_index.similarity_search(txt, k=1)
        print(type(docs))
        data_row=docs[0]
        row_number = data_row.metadata['row']
        print(row_number)
        print("\n")

        percentage_clg=((1795-row_number)*100)/1795
        print(percentage_clg)
        return percentage_clg

    def calculate_company_rank_percentage(self, company):
        loader = CSVLoader(file_path='C://Users//itsme//OneDrive//Documents//RecruitAI_dev//resources//company_ranking.csv')
        data = loader.load()
        txt=company

        faiss_index = FAISS.from_documents(data, OpenAIEmbeddings())
        docs = faiss_index.similarity_search(txt, k=1)
        print(type(docs))
        data_row=docs[0]
        row_number = data_row.metadata['row']
        print(row_number)
        print("\n")

        company_score=((1795-row_number)*100)/1795
        print(company_score)
        return company_score

    def calculate_text_similarity(self,text1, text2):
        # Create the Document Term Matrix
        vectorizer = TfidfVectorizer()
        tfidf_matrix = vectorizer.fit_transform([text1, text2])
        
        # Calculate cosine similarity
        similarity_matrix = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])
        similarity=similarity_matrix[0][0]
        return similarity*100

