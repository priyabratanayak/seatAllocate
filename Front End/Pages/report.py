
import plotly.express as px
import plotly.graph_objects as go
# Security
#passlib,hashlib,bcrypt,scrypt
import hashlib
import sqlite3
import streamlit as st
import pandas as pd
import numpy as np
import base64
import time
from PIL import  Image
import os
from pathlib import Path
from kiteconnect import KiteConnect
conn = sqlite3.connect('data.db')
from dateutil import parser
#from streamlit_autorefresh import st_autorefresh
import datetime as dt
import yfinance as yf
import bcrypt
import pymongo
import pickle
import seaborn as sns
import matplotlib.pyplot as plot
import plotly.express as px



filepath_team_attendance="Front End\\Data\\Team_Weely_Attendance"
filepath_team_attendance_mumbai="Front End\\Data\\Team_Weely_Attendance_Mumbai"

#filepath_team_attendance="C:\\Users\\028906744\\Documents\\Python Tutorial\\LTI\\seatAllocate\\Front End\\Data\\Team_Weely_Attendance"
#filepath_team_attendance_mumbai="C:\\Users\\028906744\\Documents\\Python Tutorial\\LTI\\seatAllocate\\Front End\\Data\\Team_Weely_Attendance_Mumbai"
#os.chdir('C:\\Users\\028906744\\Documents\\Python Tutorial\\LTI\\seatAllocate')
from AccessValidation import Access

def app():
    
    placeholder=st.empty()
    all_team_weekly_mumbai=[]
    all_team_weekly=[]
    temp={}
    temp_mumbai={}
    details=[]
    #st.session_state['userid']='priyabrata'
    if True or st.session_state['userid']!="":
        st.success("Logged in as "+st.session_state.userid)
        
                            
        Collection_Zerodha="seatAllocate"
        share_Prediction=Access("mongodb://localhost:27017/","Allocation")
        share_Prediction.create_Collection(Collection_Zerodha)
        cur=share_Prediction.returncollection(Collection_Zerodha).find({"owner":st.session_state.userid.upper()})
        
        if len(list(share_Prediction.returncollection(Collection_Zerodha).find({"owner":st.session_state.userid.upper()})))>0:
            for x in range(0,len(list(share_Prediction.returncollection(Collection_Zerodha).find({"owner":st.session_state.userid.upper()})))):
                details.append(cur[x]['owner'])
                details.append(cur[x]['User_ID'])
                details.append(cur[x]['PW'])
                    
            
        
        st.session_state.client=st.session_state.userid
        Collection_Access_Given="Access_Given"
        Collection_Access_Granted="Access_Granted"
        share_Prediction=Access("mongodb://localhost:27017/","Allocation")
        Collection_Access_Admin="Admin"
           
        share_Prediction.create_Collection(Collection_Access_Given,Collection_Access_Granted,Collection_Access_Admin)
            
        st.session_state.clientaccount_access=[]
        #st.session_state.clientaccount_access.append(st.session_state.userid)
        
        cur=share_Prediction.returncollection(Collection_Access_Given).find({"owner":st.session_state.userid.upper()})
        for x in range(0,len(list(share_Prediction.returncollection(Collection_Access_Given).find({"owner":st.session_state.userid.upper()})))):
                
                st.session_state.clientaccount_access.extend(cur[x]['list'])
        st.session_state.clientaccount_access = [x.upper() for x in st.session_state.clientaccount_access]

        if share_Prediction.returncollection(Collection_Access_Admin).find_one({})["admin"].upper() in st.session_state.clientaccount_access:#{:st.session_state.userid.upper()})
             
            #-----------To store weekly attendance for reporting purpose------------
            
            if os.path.isfile(filepath_team_attendance) :
                with open(filepath_team_attendance, mode ='rb')as file:
                   all_team_weekly = pickle.load(file)  
           
            #-----------------------------------------------------------------------
            
            
            if os.path.isfile(filepath_team_attendance_mumbai) :
                with open(filepath_team_attendance_mumbai, mode ='rb')as file:
                   all_team_weekly_mumbai = pickle.load(file)  
            
            #-------------------------------------------------------------------------
            
            for data in all_team_weekly:
                for key,value in data.items():
                    if key not in temp:
                        li=[value]
                        temp[key]=li
                    else:
                        li=temp[key]
                        li.append(value)
                        temp[key]=li
            
            new=pd.DataFrame.from_dict(temp)
            new.index=[data+1 for data in range(0,new.shape[0])]
            new['Week']=new.index.tolist()
            
            #---------Create dataframe from mumbai data-------------------
            
            for data in all_team_weekly_mumbai:
                for key,value in data.items():
                    if key not in temp_mumbai:
                        li=[value]
                        temp_mumbai[key]=li
                    else:
                        li=temp_mumbai[key]
                        li.append(value)
                        temp_mumbai[key]=li
            new_mumbai = pd.DataFrame.from_dict(temp_mumbai)
            new_mumbai.index=[data+1 for data in range(0,new_mumbai.shape[0])]
            
            
            expander = st.expander("Team Attendance for Bangalore, Chennai,Pune Location", expanded=False)
    
            with expander:
               
                locationwise_df=new.copy()
                
                
                locationwise_df.index=["Week "+str(data+1)for data in range(0,locationwise_df.shape[0])]
                st.table(locationwise_df)
            expander_mumbai = st.expander("Team Attendance for Mumbai Location", expanded=False)
    
            with expander_mumbai:
               
                mumbai_df=new_mumbai.copy()
                mumbai_df.index=["Week "+str(data+1)for data in range(0,mumbai_df.shape[0])]
                st.table(mumbai_df)
            #-----------------------------------------------------------
            
            if len(all_team_weekly)<1 or len(all_team_weekly_mumbai)<1:
                placeholder.warning("Not Enough Data to Generate the report")
            else:
                team_graph = st.expander("Graphical Representation of Team Attendance", expanded=False)
    
                with team_graph:
                    option = st.selectbox(
                'Select a Team to generate the graph',
                ("All Team",)+tuple(new.columns.tolist()))
                    weekno = st.selectbox(
                        'Select a Week to generate the graph',
                        ("All Week",)+tuple(new['Week'].tolist()))
                    st.subheader("BAR Plot")
                    if option=="All Team":
                        if weekno=="All Week":
                            fig = px.bar(new, x="Week", y=new.columns.tolist()[:-1], barmode='group',labels={"variable": "Team Name"} ,height=400,width=600)
                            # st.dataframe(df) # if need to display dataframe
                            fig.update_yaxes( 
                            title_text="Weekly Attendance"
                            )
                        else:
                            fig = px.bar( new[new["Week"]==int(weekno)], x="Week", y=new.columns.tolist()[:-1], barmode='group',labels={"variable": "Team Name"} ,height=400,width=600)
                            # st.dataframe(df) # if need to display dataframe
                            fig.update_yaxes( 
                            title_text="Weekly Attendance"
                            )
                       
                    else:
                        if weekno=="All Week":
                            fig = px.bar(new, x="Week", y=option, barmode='group',labels={"variable": "Team Name"} ,height=400,width=600)
                            # st.dataframe(df) # if need to display dataframe
                            fig.update_yaxes( 
                            title_text="Weekly Attendance"
                            )
                        else:
                            fig = px.bar(new[new["Week"]==int(weekno)], x="Week", y=option, barmode='group',labels={"variable": "Team Name"} ,height=400,width=600)
                            # st.dataframe(df) # if need to display dataframe
                            fig.update_yaxes( 
                            title_text="Weekly Attendance"
                            )
                    
                    st.plotly_chart(fig)
                    st.subheader("BOX Plot")
                    if weekno=="All Week":
                            fig = px.box(new, x="Week", y=new.columns.tolist()[:-1])
                    else:
                            fig = px.box(new[new["Week"]==int(weekno)], x="Week", y=new.columns.tolist()[:-1])
                            
                    
                    fig.update_yaxes( 
                    title_text="Team Distribution"
                    )
                    st.plotly_chart(fig)
                    

        else:
            
            placeholder.warning("You Do not Have access to view the report. Kindly contact Admin")

       
        
    else:
        placeholder.warning("Kindly Login To Access The Page")