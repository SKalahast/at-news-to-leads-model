# -*- coding: utf-8 -*-
"""
Created on Wed Jan 24 12:39:05 2024

@author: RKumar79
"""
from dotenv import load_dotenv
import pandas as pd
import openai
import os

load_dotenv() #This command is used to read any apikey stored in the .env file.
openai.api_type = "azure"
openai.api_base = os.getenv("OPENAI_API_ENDPOINT")
# openai.api_key = os.getenv('OPENAI_API_KEY')
openai.api_key  = "bb2a2b81ceda424e9dfdc0deea13b1f9"
openai.api_version = os.getenv("OPENAI_API_VERSION")

xls = pd.ExcelFile("inclusion_exclusion.xlsx")
exclusion_sheet = pd.read_excel(xls, 'exclusion_sheet')
exclusion = exclusion_sheet['exclusion_list'].tolist()
dup_check = set(exclusion)
exclude_string = ", ".join(dup_check).lower().strip()


def get_completion(prompt, engine ='gpt-4-32k',model_name="gpt-4", temperature=0):
    # openai.api_key = os.getenv('OPENAI_API_KEY')
    messages = [{"role": "user", "content":prompt}]
    response = openai.ChatCompletion.create(
    # response = openai.chat.completions.create(
        engine=engine,
        messages=messages,
        temperature=temperature
    )
     
    return response.choices[0].message["content"]

def get_industry(prompt, engine ='gpt-4-32k',model_name="gpt-4", temperature=0.9):
    # openai.api_key = os.getenv('OPENAI_API_KEY')
    messages = [{"role": "user", "content":prompt}]
    response = openai.ChatCompletion.create(
    # response = openai.chat.completions.create(
        engine=engine,
        messages=messages,
        temperature=temperature
    )
     
    return response.choices[0].message["content"]

def get_account_name(text):
    prod_review = text
    prompt = f""" Get the first company name from the text, Show results without the text: "The company names in the text are" ```{prod_review}``` """
    response = get_completion(prompt)
    return response

def get_summary(text):
    prod_review = text
    prompt = f""" Summarize the text, delimited by triple backticks, in at most 50 words, 
    must provide any monetry deal, ```{prod_review}``` """
    response = get_completion(prompt)
    return response

def text_filter(text):
    prod_review = text
    prompt = f""" Print the text which tells about {exclude_string}, company bought or sells shares or stocks etc. otherwise 
    print No Such information from the text delimited by triple backticks. ```{prod_review}``` """
    response = get_completion(prompt)
    return response

def industry_type(text):
    prod_review = text
    prompt = f""" Give me just the industry type:, from the text delimited by triple backticks." ```{prod_review}```
    if text says about construction and buildings then industry type is "Real Estate",
    if text says about lifestyle, retail brands, stores then industry type is "Variety Stores",
    if text says about medicine, Hospitals then industry type is "Healthcare Industry",
    if text says about innovation, research and development then industry type is "Science & Technology",
    if text says about banking, investment, or finance then industry type is "Banking & Financial Services",
    if text says about law enforcement's, Police, Court, Parliament then industry type is "Law Enforcement",
    if text says about ship building, vehicle manufacturing, heavy industry then industry type is "Manufacturing",
    if text says about Hotels, tour & travels, then industry type is "Travel and Hospitality",
    if text says about Monuments, government buildings then industry type is "Infrastructure & Public Enterprise"."""
    response = get_industry(prompt)
    return response
