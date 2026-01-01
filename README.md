# MedReview: AI-Powered Drug Review & Side-Effect Analysis
Empowering patients with intelligent insights from real-world medication experiences
Overview

MedReview is an innovative web application that utilizes Natural Language Processing (NLP) and Machine Learning (ML) to analyze patient drug reviews, identify common side effects and perform sentiment evaluation in medication experiences.
The platform supports patients, caregivers, and healthcare professionals in making informed medication decisions based on real user feedback.

### Project Structure
MedReview_App
├── images
├── App.py
├── NLTK_download.py
├── preprocess.py
├── Sentiment.py
├── webmd.csv
├── side_effect_reports.csv
├── SideEffect.py
├── Topic.py
├── Project.ipynb
└── requirements.txt

Components

App.py – Streamlit-based application UI.

preprocess.py – Text preprocessing pipeline for drug reviews.

Sentiment.py – Sentiment classification using LLM-based and classical ML models.

SideEffect.py – Extracts and categorizes side effects using rule-based and machine-learning patterns.

requirements.txt – Dependency list for setting up and running the project.

Technologies Used

Python 3.x

Machine Learning: Scikit-learn, LLM-based classification

Streamlit for deploying the web interface

pandas for data management