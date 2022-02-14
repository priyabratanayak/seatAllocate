
import pymongo
import pandas as pd
import streamlit as st
import bcrypt
class SigninDetails():
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
    def add_stock_names(self,*argv):
        self.stocks=[]
        for name in argv:
            self.stocks.extend(name)
        print(self.stocks)
    def Delete_UserID(self,username):
        keys=self.collection_dict.keys()
        
        
        for key in keys:
            
            if key =="Credentials":
                if self.collection_dict[key].count_documents({"userid":username})>0:
                        self.collection_dict[key].delete_one({"userid":username})
                        
                        return("User Deleted Successfully")
                else:
                        return ("User Not Found")
    def validate_credentials(self,username,pw):
        keys=self.collection_dict.keys()
        
        
        for key in keys:
            
            if key =="Credentials":
                
                for col in self.collection_dict[key].find():
                    
                    if bcrypt.checkpw(pw, col['password']) and username==col['userid']:
                        return True
                
                return False
    def create_credentials(self,username,pw):
        keys=self.collection_dict.keys()
        
        for key in keys:
            
            if key =="Credentials":
                searchresult=False
                
                for col in self.collection_dict[key].find():
                    #if bcrypt.checkpw(username, col['userid']):
                    if username.strip().upper()==col['userid']:
                        searchresult= True
                
                if searchresult:
                        return ("User Name Exists")
                        
                else:
                        hashed_userid=bcrypt.hashpw(username.encode('utf-8'),bcrypt.gensalt())
                        hashed_pw=bcrypt.hashpw(pw,bcrypt.gensalt())
                        
                        try:
                            ids=self.collection_dict[key].insert_many( [{"userid":username.strip().upper(),"password":hashed_pw}])
                            return("Success")
                        except Exception as e:
                            st.write(e)
                            
    
    def clear_All_Collections(self):
        keys=self.collection_dict.keys()
        for key in keys:
                self.collection_dict[key].remove({})
    def get_Records_Collection(self,fetch_date,collection_Name,stockName=None):
        return self.collection_dict[collection_Name].find({"$and":[{"Stock":stockName},{"Date_Str":fetch_date}]})
    
        