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
from kiteconnect import KiteConnect
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
    def add_zerodha_credentials(self,collectionname,ownername,argv):
        arg=[]
        
        for data in argv:
            
            arg.append(data)
        
        if len(list(self.collection_dict[collectionname].find({"owner":ownername})))>0:
                     
                     self.collection_dict[collectionname].update({"owner":ownername},{"$set":{"API_KEY":arg[0],"API_Secret":arg[1],"User_ID":arg[2],"PW":arg[3],"PIN":arg[4],"ACCESS_TOKEN":arg[5],"REQUEST_TOKEN":arg[6]}})
                     return "Details Updated Successfully"
        else:
            
            try:
                
               
                self.collection_dict[collectionname].insert({"owner":ownername,"API_KEY":arg[0],"API_Secret":arg[1],"User_ID":arg[2],"PW":arg[3],"PIN":arg[4],"ACCESS_TOKEN":arg[5],"REQUEST_TOKEN":arg[6]})
                return "Details Added Successfully"
            except Exception as e:
                
                return e
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
    
    
    if st.session_state['userid']!="":
        #st.success("Logged in as "+st.session_state.userid)
        if st.session_state.kite is None:
            #.....Fetching Zerodha Details....................
                            
            Collection_Zerodha="Zerodha_Credentials"
            share_Prediction=Access("mongodb://localhost:27017/","Stock")
            share_Prediction.create_Collection(Collection_Zerodha)
            cur=share_Prediction.returncollection(Collection_Zerodha).find({"owner":st.session_state.userid.upper()})
            details=[]
            if len(list(share_Prediction.returncollection(Collection_Zerodha).find({"owner":st.session_state.userid.upper()})))>0:
                for x in range(0,len(list(share_Prediction.returncollection(Collection_Zerodha).find({"owner":st.session_state.userid.upper()})))):
                    details.append(cur[x]['owner'])
                    details.append(cur[x]['API_KEY'])
                    details.append(cur[x]['API_Secret'])
                    details.append(cur[x]['User_ID'])
                    details.append(cur[x]['PW'])
                    details.append(cur[x]['PIN'])
                    details.append(cur[x]['ACCESS_TOKEN'])
                    details.append(cur[x]['REQUEST_TOKEN'])
            st.session_state.access_token =details[6]
            st.session_state.api_key = details[1]
            st.session_state.kite = KiteConnect(api_key=st.session_state.api_key)
            st.session_state.kite.set_access_token(st.session_state.access_token.strip())
            
        
        st.session_state.client=st.session_state.userid
        Collection_Access_Given="Access_Given"
        Collection_Access_Granted="Access_Granted"
        share_Prediction=Access("mongodb://localhost:27017/","Stock")
        share_Prediction.create_Collection(Collection_Access_Given,Collection_Access_Granted)
            
        st.session_state.clientaccount_access=[]
        st.session_state.clientaccount_access.append(st.session_state.userid)
        cur=share_Prediction.returncollection(Collection_Access_Given).find({"owner":st.session_state.userid.upper()})
        for x in range(0,len(list(share_Prediction.returncollection(Collection_Access_Given).find({"owner":st.session_state.userid.upper()})))):
                
                st.session_state.clientaccount_access.extend(cur[x]['list'])

          
        option = st.selectbox(
        'List of Account Access Managed By You',
        tuple(st.session_state.clientaccount_access))
        
        
        st.session_state.client=option       
        st.write("Go To Setting to Add or remove Access")
        components.html("""<hr style="height:10px;border:none;color:#ff5733;background-color:#ff5733;" /> """)

        col1,col2,col3,col4=st.columns([2,3,0.5,1])
        with col1:
            trading_country=["India","US"]
            st.session_state.tradingcountry=st.radio("Select Trading Country",trading_country)
        with col2:
            currency=["INR","USD"]
            st.session_state.currency=st.radio("Select Currency",currency)
        #os.chdir('C:\\Users\\PRIYABRATANAYAK\\Documents\\Python Tutorial\\sharereport')
        #display = Image.open('5-oceans-map-for.jpg')
        #display = np.array(display)
        #st.image(display, width = 400)
        #print(os.path.isfile(os.path.join(os.getcwd(), "access_token.txt")))
        #print(os.path.isfile(os.path.join(os.getcwd(), "../access_token.txt")))
        #print(os.path.isfile(os.path.join(os.getcwd(), "../../access_token.txt")))
        #print(os.path.isfile(os.path.join(os.getcwd(), "../../../access_token.txt")))
        #st.subheader(os.path.isfile(os.path.join(os.getcwd(), "access_token.txt")))
        
        #...............................................
        #Use this path in Heroku
        
        #access_token = open(os.path.join(os.getcwd(), "access_token.txt"),'r').read().split()
        #key_secret = open(os.path.join(os.getcwd(), "api_key.txt"),'r').read().split()
        #...............................................
        
    else:
        placeholder.warning("Kindly Login To Access The Page")