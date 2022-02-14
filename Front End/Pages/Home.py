# -*- coding: utf-8 -*-

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
import os.path
import time
import streamlit as st
import Seat_Allocation_5days
import pymongo

import streamlit.components.v1 as components


class Access():
    def __init__(self,DEFAULT_CONNECTION_URL = "mongodb://localhost:27017/",DB_NAME=None):
        self.DEFAULT_CONNECTION_URL = DEFAULT_CONNECTION_URL
        self.DB_NAME = DB_NAME
        self.collection_dict={}
        # Establish a connection with mongoDB
        self.client = pymongo.MongoClient(self.DEFAULT_CONNECTION_URL)
        # Create a DB
        dbnames = self.client.list_database_names()
        #if self.DB_NAME not in dbnames:
        self.dataBase = self.client[self.DB_NAME]
        self.cl_price_df = pd.DataFrame()
        self.ohlcv = {}
        self.ohlcv_df = pd.DataFrame()
        self.ohlcv_day = {}
    def create_Collection(self,*argv):
        collection_list = self.dataBase.list_collection_names()
        for name in argv:
                 #if name not in collection_list:
                 self.collection_dict[name]=self.dataBase[name]
    def returncollection(self,collectionname):
        return self.collection_dict[collectionname]
    
    def add_access(self,toAcess,fromAccess,*argv):
        message=[]
        for name in argv:
            if name=="Access_Given":
                accessgivenlist=[]
                if len(list(self.collection_dict["Access_Given"].find({"owner":toAcess})))>0:
                     for x in (self.collection_dict["Access_Given"].find({"owner":toAcess})):
                         accessgivenlist.extend(x['list'])
                     if toAcess not in accessgivenlist:
                         accessgivenlist.append(fromAccess)
                     self.collection_dict["Access_Granted"].update({"owner":toAcess},{"$set":{"list":accessgivenlist}})
                
                else:
                    accessgivenlist.append(fromAccess)
                    self.collection_dict["Access_Given"].insert({"owner":toAcess,"list":accessgivenlist})
                
                message.append("Access Provided Successfully")
            
            if name=="Access_Granted":
                accesslist=[]
                if len(list(self.collection_dict["Access_Granted"].find({"owner":fromAccess})))>0:
                     for x in (self.collection_dict["Access_Granted"].find({"owner":fromAccess})):
                         accesslist.extend(x['list'])
                                              
                     if toAcess not in accesslist:
                        accesslist.append(toAcess)
                     self.collection_dict["Access_Granted"].update({"owner":fromAccess},{"$set":{"list":accesslist}})
                
                else:
                    accesslist.append(toAcess)
                    self.collection_dict["Access_Granted"].insert({"owner":fromAccess,"list":accesslist})
                
               
           
        return message
    def revoke_access(self,toAcess,fromAccess,*argv):
        message=[]
        for name in argv:
            if name=="Access_Given":
                accessgivenlist=[]
                if len(list(self.collection_dict["Access_Given"].find({"owner":toAcess})))>0:
                     for x in (self.collection_dict["Access_Given"].find({"owner":toAcess})):
                         accessgivenlist.extend(x['list'])
                     if len(accessgivenlist)>0:
                         
                         accessgivenlist.remove(fromAccess)
                         self.collection_dict["Access_Granted"].update({"owner":toAcess},{"$set":{"list":accessgivenlist}})
                    
                
                
            if name=="Access_Granted":
                accesslist=[]
                if len(list(self.collection_dict["Access_Granted"].find({"owner":fromAccess})))>0:
                     for x in (self.collection_dict["Access_Granted"].find({"owner":fromAccess})):
                         accesslist.extend(x['list'])
                     if len(accesslist)>0:                         
                         
                         accesslist.remove(toAcess)
                         self.collection_dict["Access_Granted"].update({"owner":fromAccess},{"$set":{"list":accesslist}})
                    
                
                message.append("Access Revoked Successfully")
            
        return message
    def Delete_UserID(self,username):
        keys=self.collection_dict.keys()
        
        
        for key in keys:
            
            if key =="Credentials":
                if self.collection_dict[key].count_documents({"userid":username})>0:
                        self.collection_dict[key].delete_one({"userid":username})
                        
                        return("User Deleted Successfully")
                else:
                        return ("User Not Found")
   
    def fetch_record(self,collection_Name,key):
        return self.collection_dict[collection_Name].find({"owner":key})
                            
    
    def clear_All_Collections(self):
        keys=self.collection_dict.keys()
        for key in keys:
                self.collection_dict[key].remove({})
    def get_Records_Collection(self,fetch_date,collection_Name,stockName=None):
        return self.collection_dict[collection_Name].find({"$and":[{"Stock":stockName},{"Date_Str":fetch_date}]})
    
def app():
    
    placeholder=st.empty()
    
    #st.session_state['userid']='priyabrata'
    if st.session_state['userid']!="":
        st.success("Logged in as "+st.session_state.userid)
        
                            
        Collection_Zerodha="seatAllocate"
        share_Prediction=Access("mongodb://localhost:27017/","Allocation")
        share_Prediction.create_Collection(Collection_Zerodha)
        cur=share_Prediction.returncollection(Collection_Zerodha).find({"owner":st.session_state.userid.upper()})
        details=[]
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
             
            option = st.selectbox(
                        'List Of Admin Names',
            tuple(st.session_state.clientaccount_access))
            
            
            st.session_state.client=option       
            #st.write("Go To Setting to Add or remove Access")
            components.html("""<hr style="height:10px;border:none;color:#ff5733;background-color:#ff5733;" /> """)
            Seat_Allocation_5days.allocation()
        else:
            
            placeholder.warning("You Do not Have access to view the report. Kindly contact Admin")
        
       
        
    else:
        placeholder.warning("Kindly Login To Access The Page")