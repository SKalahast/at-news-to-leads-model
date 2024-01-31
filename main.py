import time
import uvicorn
from fastapi import FastAPI, Request, HTTPException
from datetime import date
import streamlit as st
from News2Lead import news_2_leads, all_clients, multi_clients
import pandas as pd
from openai_helper import get_account_name, get_summary, text_filter, industry_type
from datetime import datetime
import datetime
import warnings
import logging
import ssl, sys

warnings.filterwarnings('ignore')

logger = logging.getLogger('ntl-model')
logger.setLevel(logging.INFO)
stream_handler = logging.StreamHandler(sys.stdout)
stream_handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(message)s')
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)

app = FastAPI()

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

comp_list = pd.read_csv('DSC_Company_List.csv')
xls = pd.ExcelFile("inclusion_exclusion.xlsx")
exclusion_sheet = pd.read_excel(xls, 'exclusion_sheet')
inclusion_sheet = pd.read_excel(xls, 'inclusion_sheet').dropna(how='any',axis=0)
# keywords = pd.read_excel(xls, 'keywords')

if comp_list not in  st.session_state:
    st.session_state.comp_list = None

def to_m_d_yyyy(dt):
    return f"{dt.month}/{dt.day}/{dt.year}"

def main():
    st.set_page_config(layout="wide")
    st.markdown("""<style>footer {visibility: hidden;}</style>""", unsafe_allow_html=True)
    
    st.title('DEO (Daily Event Observer)')
    st.markdown("""DEO supports the **News To Leads** initiative by allowing Sales Management to swiftly **harvest leads from news articles**, and placing them in front of our property experts **promptly**.
                   """)
    st.sidebar.title("Digital Start Centre")
    selection = st.sidebar.selectbox("Select an option from dropdown.", ['Single Client','Multiple Client','All Client'])
    
    # inclusion list criteria:
    selected_options = st.sidebar.multiselect('Type of News to Include:', inclusion_sheet['inclusion_list'])
    if not selected_options:
        selected_options = inclusion_sheet['inclusion_list'].tolist()
    dup_check = set(selected_options)
    include_string = "|".join(dup_check).lower().strip()

    # st.sidebar.selectbox("Type of news not required", exclusion_sheet['exclusion_list'])
            
    if selection == 'Single Client':
        client = st.sidebar.selectbox('Client Name',comp_list['Client Name'],index=None)
        if client is None:
            client = st.sidebar.text_input("Enter any new client not available in dropdown",)
    elif selection == 'Multiple Client':
        client = st.sidebar.multiselect("Select client names", comp_list['Client Name'], default=comp_list['Client Name'][0])
    else:
        pass

    start_date = st.sidebar.date_input("Enter Start Date",value=date.today(),min_value=date.today()-datetime.timedelta(days=90),max_value=date.today())
    start_dte = to_m_d_yyyy(start_date)
    
    end_date = st.sidebar.date_input("Enter End Date",value=date.today(),max_value=date.today())
    end_dte = to_m_d_yyyy(end_date)
         
    if st.sidebar.button('Start Process'):
        start_time = datetime.datetime.now()
        
        with st.status("Connected to Google News...", expanded=True) as status:
                            
            time.sleep(1)
            st.write("Downloading and Extracting news...")

            if selection == 'Single Client': 
                df = news_2_leads(client,start_dte,end_dte)
            elif selection == 'Multiple Client':
                df = multi_clients(client,start_dte,end_dte)

            else:
                df = all_clients(start_dte,end_dte)
            st.write("News Extracted...")
            time.sleep(1)
            
            if df.empty:
                pass
            else:
                df = df[df['Headline'].str.lower().str.contains(include_string)]
                df = df.reset_index(drop=True) 
                st.write("Checking Relevant News...")
                df['filter_text'] = df['Headline'].apply(lambda x:text_filter(x))
                df = df[(df["filter_text"].str.lower().str.contains('no such information')==True)]
                df = df.reset_index(drop=True)
                
                st.write("Summarizing the News...")
                df['Summary'] = df['Content'].apply(lambda x:get_summary(x))
                st.write("Summarization Complete...")
                time.sleep(1)
                # st.write("Finding industry type...")
                # df['Industry Type'] = df['Content'].apply(lambda x:industry_type(x))

        status.update(label="All Process complete!", state="complete", expanded=False)   
        if df.empty:
            label = 'News scanned and found no news with the searched criteria'
            st.write(f"### {label}")
        else:
            df = df.merge(comp_list,left_on = 'Account_Name',right_on='Client Name').reindex(
    columns=['News_Date','Headline','Account_Name','Summary','Content','GWS Enterprise Sector Mapping','URL_x','URL_y'])
            df.rename(columns={'GWS Enterprise Sector Mapping':'Account_Type','URL_x':'News_website','URL_y':'Account_website'},inplace=True)
            # df = df.loc[:,['News_Date','Headline','Account_Name','Summary','Content','URL']]
            st.dataframe(df)
            end_time = datetime.datetime.now()
            st.write('Total time to run the Script: ',end_time - start_time)
            
            @st.cache_data
            def convert_df(df):
                return df.to_csv(index=False).encode('utf-8')            
            csv = convert_df(df)                        
            st.download_button("Press to Download", csv, "news2lead.csv", "text/csv")
                         

######################################################################################################################
#                                  This is where the dedupe analysis ends                                           #
######################################################################################################################

# All the other async functions are part of the API that was previously built

# async def print_body(request):
#     print(f"request header: {dict(request.headers.items())}'")
#     print(f"request query parameters: {dict(request.query_params.items())}'")
#     try:
#         result = await request.json()
#         print(f'request json: {result}')
#         return result
#     except Exception as err:
#         # could not parse json
#         body = await request.body()
#         print(f'request body : {body}')
#         return {"undecodeable body": body}


#######################################################################################################################
#                                                                                                                     #
#                  In the predict function we extract all results and send it as output                               #
#                                                                                                                     #
#######################################################################################################################

# async def predict(request):
#     try:
#         input = await request.json()
#         # input = await requests.post(url = "http://127.0.0.1:8000/main",
#         #                         data = json.dumps(inputs))
#         results = generate_results(input)
#         return results
    
#     except Exception as err:
#         raise HTTPException(status_code=400, detail=f"bad data: {err}")


# @app.post("/xero/1.0/event:ntl.class")
# async def classify(request: Request):
#     input = await request.json()
#     result = await predict(request)

#     return result
                
                
if __name__== "__main__":
    main()
    # uvicorn.run(app, host="127.0.0.1", port=8000)
