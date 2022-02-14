# -*- coding: utf-8 -*-
"""
Created on Thu Sep 16 16:37:11 2021

@author: 028906744
"""
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
#from multipage import MultiPage
from selenium import webdriver
import pymongo
import os
import datetime
import time
from PIL import  Image
import bcrypt
import pytz
from pathlib import Path
from kiteconnect import KiteConnect
#os.chdir('C:\\Users\\028906744\\Documents\\Python Tutorial\\sharereport\\Front End')
from userValidation import SigninDetails
import sys


import pymongo
#conn = sqlite3.connect('data.db')
#c = conn.cursor()

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
    
        
    
    
def make_hashes(password):
	return hashlib.sha256(str.encode(password)).hexdigest()

def check_hashes(password,hashed_text):
	if make_hashes(password) == hashed_text:
		return hashed_text
	return False
# DB Management
 

def autologin(key_secret):
    token_path = "api_key.txt"
    kite = KiteConnect(api_key=key_secret[1])#API Key
    service = webdriver.chrome.service.Service('./chromedriver')#change it to /usr/bin/chromedriverwhile uploading to linux
    #service = webdriver.chrome.service.Service('/usr/bin/chromedriver')
    
    service.start()
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options = options.to_capabilities()
    driver = webdriver.Remote(service.service_url, options)
    driver.get(kite.login_url())
    driver.implicitly_wait(10)
    username = driver.find_element_by_xpath('/html/body/div[1]/div/div[2]/div[1]/div/div/div[2]/form/div[1]/input')
    password = driver.find_element_by_xpath('/html/body/div[1]/div/div[2]/div[1]/div/div/div[2]/form/div[2]/input')
    
    username.send_keys(key_secret[3])
    password.send_keys(key_secret[4])
    driver.find_element_by_xpath('/html/body/div[1]/div/div[2]/div[1]/div/div/div[2]/form/div[4]/button').click()
    pin = driver.find_element_by_xpath('/html/body/div[1]/div/div[2]/div[1]/div/div/div[2]/form/div[2]/div/input')
    pin.send_keys(key_secret[5])
    
    driver.find_element_by_xpath('/html/body/div[1]/div/div[2]/div[1]/div/div/div[2]/form/div[3]/button').click()
    time.sleep(10)
    request_token=driver.current_url.split('request_token=')[1].split('&action')[0]
    
    key_secret[7]=request_token#assigning REQUEST_TOKEN
    
    driver.quit()
    return key_secret

def login(owner):
    #owner="priyabrata"
    #os.chdir('C:\\Users\\028906744\\Documents\\Python Tutorial\\sharereport\\Front End')

    Collection_Zerodha="Credentials"
    share_Prediction=Access("mongodb://localhost:27017/","Allocation")
    share_Prediction.create_Collection(Collection_Zerodha)
    cur=share_Prediction.returncollection(Collection_Zerodha).find({"owner":owner.upper()})
    details=[]
    
    if len(list(share_Prediction.returncollection(Collection_Zerodha).find({"owner":owner.upper()})))>0:
        for x in range(0,len(list(share_Prediction.returncollection(Collection_Zerodha).find({"owner":owner.upper()})))):
            owner=cur[x]['owner']
            details.append(cur[x]['owner'])
            details.append(cur[x]['User_ID'])
            details.append(cur[x]['PW'])
            
    if not os.path.isfile(os.path.join(os.getcwd(),'access_token.txt')) :
        
        #key_secret=details
        key_secret=autologin(details)
        #generating and storing access token - valid till 6 am the next day
        request_token =details[7] # REQUEST_TOKEN
        kite = KiteConnect(api_key=details[1])# API_KEY
        data = kite.generate_session(request_token, api_secret=key_secret[2])#API_Secret
        details[6]=data["access_token"]        
        credentials=(details[1],details[2],details[3].upper(),details[4],details[5],details[6],details[7])                                    
        msg=share_Prediction.add_zerodha_credentials(Collection_Zerodha,details[0].upper(),credentials)
       
        with open(os.path.join(os.getcwd(),'access_token.txt'), 'w') as file:
                file.write(datetime.datetime.now(pytz.timezone('Asia/Kolkata')).strftime('%Y-%m-%d-%H:%M:%S')+"\n")
                
    else:
        access_token_date = open(os.path.join(os.getcwd(),"access_token.txt"),'r').read().split()
        
        datetime_object = datetime.datetime.strptime(access_token_date[0], '%Y-%m-%d-%H:%M:%S')
        datetime_object_reference = datetime.datetime.strptime(datetime.datetime.now(pytz.timezone('Asia/Kolkata')).strftime('%Y-%m-%d-')+'06:00:00', '%Y-%m-%d-%H:%M:%S')
        
        if int((datetime_object_reference-datetime_object).days)>=0:
            print(os.getcwd())
            details=autologin(details)                                                       
                                    
            #generating and storing access token - valid till 6 am the next day
            request_token =details[7] # REQUEST_TOKEN
            kite = KiteConnect(api_key=details[1])# API_KEY
            data = kite.generate_session(request_token, api_secret=details[2])#API_Secret
            details[6]=data["access_token"]
            
            credentials=(details[1],details[2],details[3].upper(),details[4],details[5],details[6],details[7])                                    
            msg=share_Prediction.add_zerodha_credentials(Collection_Zerodha,details[0].upper(),credentials)
           
            with open(os.path.join(os.getcwd(),'access_token.txt'), 'w') as file:
                    file.write(datetime.datetime.now(pytz.timezone('Asia/Kolkata')).strftime('%Y-%m-%d-%H:%M:%S')+"\n")
            

def app():
       
        if 'msg_placeholder' not in st.session_state:
            st.session_state['msg_placeholder']= None
        
        Collection_Credentials="Credentials"
        share_Prediction=SigninDetails("mongodb://localhost:27017/","Allocation")
        share_Prediction.create_Collection(Collection_Credentials)
        st.subheader("Login Section")
        
        with st.form(key="loginform"):
            if len(st.session_state.userid)>0:
                user_placeholder=st.empty() 
                
                new_user = user_placeholder.text_input("User Name",st.session_state.userid)
            else:
                new_user = st.text_input("User Name",value="priyabrata")
            pw_placeholder=st.empty() 
            new_password = pw_placeholder.text_input("Password",type='password',value="Pinakpani!1")
            
            col1,col2=st.columns([1,1])
            with col1:
                signin=st.form_submit_button("Sign In")
            with col2:
                signout=st.form_submit_button("Sign Out")
            st.session_state['msg_placeholder']=st.empty()
            if signout:
                st.session_state['msg_placeholder'].success("Logged out successfully...")
                st.session_state['userid']=""
            if signin:
                if len(new_user)==0:
                    st.session_state['msg_placeholder'].warning("Enter User Name")
                elif len(new_password)==0:
                    st.session_state['msg_placeholder'].warning("Enter User Password")
                else:
                    
                    #new_user_utf=str(new_user).strip().upper().encode('utf-8')
                    new_user_utf=str(new_user).strip().upper()
                    new_password_utf=str(new_password).strip().encode('utf-8') 
                    #new_user="priyabrata"
                    #login_zerodha(str(new_user).strip().upper())
                    result=share_Prediction.validate_credentials(new_user_utf,new_password_utf)
                    
                    if result:
                        
                        st.session_state['userid']=new_user
                        
                        st.session_state['msg_placeholder'].success("Logged In as {}".format(st.session_state['userid']))
                        
                        st.balloons()
                    else:
                        
                        st.session_state['msg_placeholder'].warning("Incorrect Username/Password") 
            