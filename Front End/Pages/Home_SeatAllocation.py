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
#import Seat_Allocation_5days
import pymongo
from os.path import exists
import streamlit.components.v1 as components
from subprocess import Popen
import streamlit as st
import pandas as pd
from pathlib import Path
from kiteconnect import KiteConnect
import os
import random
import numpy
import plotly.express as px
import plotly.graph_objects as go
# Security
# passlib,hashlib,bcrypt,scrypt
import os.path
import hashlib
import sqlite3
import streamlit as st
import pandas as pd
import numpy as np
import base64
import time
from datetime import date
import calendar
import sys
import csv
from PIL import Image
import collections
import pickle

filepath_tracker_bangalore = "Front End\\Data\\Team_Attendance_bangalore"
lastgenerationdate_path="Front End\\Data\\report_last_run"
filepath_tracker_chennai = "Front End\\Data\\Team_Attendance_chennai"
filepath_tracker_mumbai = "Front End\\Data\\Team_Attendance_mumbai"
filepath_tracker_pune = "Front End\\Data\\Team_Attendance_pune"
filepath_tracker_delhi = "Front End\\Data\\Team_Attendance_delhi"
filepath_tracker_hyderabad = "Front End\\Data\\Team_Attendance_hyderabad"

filepath = "Front End\\Data\\Seat_Allocation_Details_sample.xlsx"
filepath_tracker = "Front End\\Data\\Team_Attendance"
filepath_team_attendance="Front End\\Data\\Team_Weely_Attendance"
filepath_team_attendance_mumbai="Front End\\Data\\Team_Weely_Attendance_Mumbai"
filepath_output="Front End\\Data\\Seat_Allocation_Details_output_"+str(date.today())+".xlsx"
tday_date=str(date.today())
occupied_seats_mumbaifinal=[]
seat_allc=None
leader_details=None
team_depend=None
df_team_details=None
list_Teams=None
list_Mumbai=None
combo_list_mumbai=None
team_count = 0
primary_team_dependant_name = {}
primary_team_dependant_percent = {}
reserved_for_leadership_bang=20
occupied_seats_location=[]
teams = []
teams_with_locationwise_count={}
day_wise_team = []
day_wise_seat = []
week_days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
location=["Bangalore","Chennai","Pune","Mumbai","Hyderabad","Delhi"]
df_mumbai_final=pd.DataFrame()
df_bangalore_final=pd.DataFrame()
df_chennai_final=pd.DataFrame()
df_pune_final=pd.DataFrame()
df_hyderabad_final=pd.DataFrame()
df_delhi_final=pd.DataFrame()
attendance_bangalore_list=[]
attendance_chennai_list=[]
attendance_pune_list=[]
attendance_hyderabad_list=[]
attendance_delhi_list=[]
attendance_lt_3=[]
writer=None
mumbai_min_attendance_team_final=None
def find_least_strength_In_week(day_wise_seat):
    smallest_index=1000
    
    index_smallest=-1
    for ind,data in enumerate(day_wise_seat):
         
        bang_seat=day_wise_seat[ind][0]
        bang_seat=bang_seat.split(":")
        first_part=bang_seat[0]
        second_part=bang_seat[1].split("/")
        if int(second_part[0])<smallest_index:
            smallest_index=int(second_part[0])
            index_smallest=ind
    return index_smallest
    
def getCurrentDayOfWeek():
    my_date = date.today()
    return calendar.day_name[my_date.weekday()]



def homePage():
    
    # print(os.getcwd())
    
    teams_cameto_office = {}
    location_resource = {}
    location_seatcount = {}
    occupied_seats_location.clear()
    
    counter = 1
    attended = 0
    mandatory_attendance = 3
    
    loopcounter = 11#11 team per day
    teams_cameto_office = {}
    day_wise_team.clear()
    day_wise_seat.clear()
    day_wise_bangalore_count = []
    
    
    seats_office_bangalore_today = []
    seats_office_Chennai_today = []
    seats_office_Pune_today = []
    seats_office_Mumbai_today = []
    seats_office_Hyderabad_today = []
    seats_office_Delhi_today = []
    
    
    df_seatcount_location = pd.read_excel(
        filepath, sheet_name='seatcount_location')
    df_Leader_details = pd.read_excel(filepath, sheet_name='Leader_details')
    df_Team_details = pd.read_excel(filepath, sheet_name='Team_details')

    df_Team_dependency = pd.read_excel(filepath, sheet_name='Team_dependency')
    df_seatcount_location = df_seatcount_location.iloc[:, 0:2]
    df_seatcount_location.set_index("Location", drop=True, inplace=True)
    df_Team_dependency = df_Team_dependency.iloc[:, 0:3]
    df_Team_details = df_Team_details.iloc[:, 0:9]
    df_Team_details = df_Team_details.fillna(0)
    # df_Team_details.apply(pd.to_numeric)
    df_Team_details['Total Count'] = df_Team_details.sum(axis=1)
    location="Bangalore"
    global attendance_lt_3
    if os.path.isfile(filepath_tracker) :
        with open(filepath_tracker, mode ='rb')as file:
           attendance_lt_3 = pickle.load(file)  
           
    
    
    location_seatcount["Bangalore"] = int(
        df_seatcount_location.loc['Bangalore', :])
    location_seatcount["Chennai"] = int(
        df_seatcount_location.loc['Chennai', :])
    location_seatcount["Pune"] = int(df_seatcount_location.loc['Pune', :])
    location_seatcount["Mumbai"] = int(df_seatcount_location.loc['Mumbai', :])
    location_seatcount["Hyderabad"] = int(
        df_seatcount_location.loc['Hyderabad', :])
    location_seatcount["Delhi"] = int(df_seatcount_location.loc['Delhi', :])

    location_resource["Bangalore"] = int(df_Team_details['Bangalore'].sum())
    location_resource["Chennai"] = int(df_Team_details['Chennai'].sum())
    location_resource["Pune"] = int(df_Team_details['Pune'].sum())
    location_resource["Mumbai"] = int(df_Team_details['Mumbai'].sum())
    location_resource["Hyderabad"] = int(df_Team_details['Hyderabad'].sum())
    location_resource["Delhi"] = int(df_Team_details['Delhi'].sum())

    primary_team_dependant_name_temp = dict(
        zip(df_Team_dependency['Primary_team'], df_Team_dependency['Dependent_on_team']))
    primary_team_headcount = dict(
        zip(df_Team_details['Team'], df_Team_details['Total Count']))

    for ind, data in primary_team_dependant_name_temp.items():
        try:

            li_temp = data.split(",")

            team_temp = [value[0:value.index(":")] for value in li_temp]
            percent_temp = [
                float(value[value.index(":")+1:])/100for value in li_temp]
            primary_team_dependant_name[ind] = team_temp
            primary_team_dependant_percent[ind] = percent_temp

        except:
            primary_team_dependant_name[ind] = ['NA']
            primary_team_dependant_percent[ind] = [0.0]
    teams = list(primary_team_dependant_name.keys())

    teams_to_index = {}
    for ind, data in enumerate(teams):
        teams_to_index[data] = ind
    team_count = df_Team_details.shape[0]-1

    
    
    
    for days in range(5):  # number of working days in a week =5
        li_counter = []
        print("Days:", days+1)
        for data in range(20):
            li_counter.append(data)

        # ............................
        li_counter.sort()

        length_li = len(li_counter)

        li_firsthalf = li_counter[0:int(length_li/2)]
        li_secondhalf = li_counter[int(length_li/2):]
        li_secondhalf.sort(reverse=True)
        li_counter = []
        for ind in range(len(li_firsthalf)):
            li_counter.append(li_secondhalf[ind])
            li_counter.append(li_firsthalf[ind])

        if length_li > len(li_counter):
            #print(len(li_secondhalf)-(length_li -len(li_counter)))
            # print(li_secondhalf[len(li_secondhalf)-(length_li -len(li_counter)):]):
            for data in li_secondhalf[len(li_secondhalf)-(length_li - len(li_counter)):]:
                li_counter.append(data)
        # ............................
        # print("days:",days+1)
        # ---------To Restrict the team to come to office not more than 3 days
        if len(teams_cameto_office) > 0:
            for key, value in teams_cameto_office.items():
                attended = value

                if attended > mandatory_attendance-1:
                    li_counter.remove(teams_to_index[key])
        # ---------End-----------------------------

        teams_cameto_office_today = []
        dependant_team_today = []
        
        if len(li_counter) < loopcounter:
            loopcounter = len(li_counter)-1

        # Loop counter=12. i.e. Total Team should come in a day
        for today_teams in range(loopcounter):
            random_team = 0
            # print("today_teams",today_teams)

            if len(li_counter) > 0:
                # xxxxxxxxxxxx

                # To select a random primary team
                random_team = li_counter[loopcounter-today_teams]
                # print("loopcounter:",loopcounter,today_teams,random_team,li_counter)
                # To remove the randomly picked value from the list so that it wont appear again for the pick up
                li_counter.remove(random_team)
                # xxxxxxxxxxxxxxxxx
                seatcount_bangalore = 0

                if (teams[random_team] in teams_cameto_office) and (teams_cameto_office[teams[random_team]] >= 3):
                    continue
                else:
                    # To add the Team Name in an list
                    teams_cameto_office_today.append(teams[random_team])

                    if len(teams_cameto_office) == 0 or teams[random_team] not in teams_cameto_office:
                        teams_cameto_office[teams[random_team]] = 1
                        try:
                            for dependant in primary_team_dependant_name[teams[random_team]]:
                                #print("Inner:",teams[random_team]," :dependant: ",dependant)

                                # -------If the dependent team already came for 3 days then skip
                                if (dependant in teams_cameto_office) and (teams_cameto_office[dependant] >= 3):
                                    continue
                                else:
                                    if dependant != "NA":
                                        # ---If the dependant team is not already in the today's attendance list then update today's attendance list
                                        if dependant not in dependant_team_today:
                                            if dependant not in teams_cameto_office_today:
                                                dependant_team_today.append(
                                                    dependant)
                                        if dependant in teams_cameto_office:
                                            pass

                                        else:
                                            teams_cameto_office[dependant] = 0
                            # print("\n\nteams_cameto_office_today",teams_cameto_office_today)
                            # print("dependant_team_today",dependant_team_today)
                            #print("\n\nInner final:",teams_cameto_office,len(teams_cameto_office))
                        except Exception as e:
                            #print("error 133:",e)
                            pass
                        # print(".............................")

                    else:

                        if teams[random_team] not in dependant_team_today:

                            attended = teams_cameto_office[teams[random_team]]

                            attended += 1
                            teams_cameto_office[teams[random_team]] = attended

                        for dependant in primary_team_dependant_name[teams[random_team]]:
                            if dependant != "NA":
                                # print("\nouter:",teams[random_team],":",dependant,"\n")
                                # -------If the dependent team already came for 3 days then skip
                                if (dependant in teams_cameto_office) and (teams_cameto_office[dependant] >= 3):
                                    continue
                                else:

                                    # ---If the dependant team is not already in the today's attendance list then update today's attendance list

                                    if dependant not in dependant_team_today:
                                        if dependant not in teams_cameto_office_today:
                                            dependant_team_today.append(
                                                dependant)
                                    if dependant not in teams_cameto_office:
                                        teams_cameto_office[dependant] = 0

                        #print("\n\nOuter  primary:",teams[random_team])
                        # print("\ndependant_team_today:",dependant_team_today)

                        #print("\n\nOuter final:",teams_cameto_office,len(teams_cameto_office))

                    #print("\nouter dependant_team_today:",dependant_team_today)
        # .............To update the count of dependent team in overall weekly team
        # It counts the number of days a particular team came in a week
        for data in dependant_team_today:
            if data in teams_cameto_office:
                attended = teams_cameto_office[data]
                # if attended <3:
                attended += 1
                teams_cameto_office[data] = attended
                # else:
                #   print("attended",attended)
        teamscame = []

        for ind, data in teams_cameto_office.items():
            if data < mandatory_attendance:
                teamscame.append(ind)
        seats_bangalore = 0
        seats_chennai = 0
        seats_pune = 0
        seats_mumbai = 0
        seats_hyderabad = 0
        seats_delhi = 0
        #print("Outer teams_cameto_office_today:",teams_cameto_office_today)
        
        seats_office_bangalore_today_temp = []
        seats_office_Chennai_today_temp = []
        seats_office_Pune_today_temp = []
        seats_office_Mumbai_today_temp = []
        seats_office_Hyderabad_today_temp = []
        seats_office_Delhi_today_temp = []
        
        
        for data in teams_cameto_office_today:

            seats_bangalore += df_Team_details['Bangalore'][df_Team_details[df_Team_details['Team']
                                                                            == data]['Bangalore'].index[0]]
            seats_chennai += df_Team_details['Chennai'][df_Team_details[df_Team_details['Team']
                                                                        == data]['Chennai'].index[0]]
            seats_pune += df_Team_details['Pune'][df_Team_details[df_Team_details['Team']
                                                                  == data]['Pune'].index[0]]
            seats_mumbai += df_Team_details['Mumbai'][df_Team_details[df_Team_details['Team']
                                                                      == data]['Mumbai'].index[0]]
            seats_hyderabad += df_Team_details['Hyderabad'][df_Team_details[df_Team_details['Team']
                                                                            == data]['Hyderabad'].index[0]]
            seats_delhi += df_Team_details['Delhi'][df_Team_details[df_Team_details['Team']
                                                                    == data]['Delhi'].index[0]]
            
            #------------------------
            bangalore=df_Team_details['Bangalore'][df_Team_details[df_Team_details['Team']== data]['Bangalore'].index[0]]
            
            seats_office_bangalore_today_temp.append(int(bangalore))
            chennai=df_Team_details['Chennai'][df_Team_details[df_Team_details['Team']
                                                                        == data]['Chennai'].index[0]]
            seats_office_Chennai_today_temp.append(int(chennai))
            
            
            pune=df_Team_details['Pune'][df_Team_details[df_Team_details['Team']
                                                                  == data]['Pune'].index[0]]
            seats_office_Pune_today_temp.append(int(pune))
            
            mumbai=df_Team_details['Mumbai'][df_Team_details[df_Team_details['Team']
                                                                      == data]['Mumbai'].index[0]]
            seats_office_Mumbai_today_temp.append(int(mumbai))
            
            hyderabad=df_Team_details['Hyderabad'][df_Team_details[df_Team_details['Team']
                                                                            == data]['Hyderabad'].index[0]]
            seats_office_Hyderabad_today_temp.append(int(hyderabad))
            
            delhi=df_Team_details['Delhi'][df_Team_details[df_Team_details['Team']
                                                                    == data]['Delhi'].index[0]]

            seats_office_Delhi_today_temp.append(int(delhi))
        
        
        seats_office_bangalore_today.append(seats_office_bangalore_today_temp)
        seats_office_Chennai_today.append(seats_office_Chennai_today_temp)
        seats_office_Pune_today.append(seats_office_Pune_today_temp)
        seats_office_Mumbai_today.append(seats_office_Mumbai_today_temp)
        seats_office_Hyderabad_today.append(seats_office_Hyderabad_today_temp)
        seats_office_Delhi_today.append(seats_office_Delhi_today_temp)
        
        
        
        
        
        seats_temp = []

        seats_temp.append("Total seat occupied in Bangalore:" +
                          str(int(seats_bangalore))+"/"+str(location_seatcount["Bangalore"]))
        seats_temp.append("Total seat occupied in Chennai:" +
                          str(int(seats_chennai))+"/"+str(location_seatcount["Chennai"]))
        seats_temp.append("Total seat occupied in Pune:" +
                          str(int(seats_pune))+"/"+str(location_seatcount["Pune"]))
        seats_temp.append("Total seat occupied in Mumbai:" +
                          str(int(seats_mumbai))+"/"+str(location_seatcount["Mumbai"]))
        seats_temp.append("Total seat occupied in Hyderabad:" +
                          str(int(seats_hyderabad))+"/"+str(location_seatcount["Hyderabad"]))
        seats_temp.append("Total seat occupied in Delhi:" +
                          str(int(seats_delhi))+"/"+str(location_seatcount["Delhi"]))
        
        day_wise_seat.append(seats_temp)

        day_wise_bangalore_count.append(
            (location_seatcount["Bangalore"]-int(seats_bangalore)))
        day_wise_team.append(teams_cameto_office_today)

        #print("\nteams_cameto_office_today",teams_cameto_office_today,len(teams_cameto_office_today),"\n.................................\n")#
        #print(seats_office_bangalore_today)
        # .........................................................................
        print("teams_cameto_office_today",len(teams_cameto_office_today),": ",teams_cameto_office_today)
        print("seats_bangalore",int(seats_bangalore))
        #print("\nTeam came to office:", teams_cameto_office, len(teams_cameto_office), "\n.......................\n")
        print("\n========================================================\n")
        

    
    depteam_percent = primary_team_dependant_percent[teams[random_team]]

    team_to_adjust = pd.DataFrame.from_dict({"Team": list(
        teams_cameto_office.keys()), "Attendance": list(teams_cameto_office.values())})
    team_to_adjust = team_to_adjust[team_to_adjust['Attendance'] < 3]
    team_to_adjust = team_to_adjust.sort_values('Attendance')
    attendance_1 = team_to_adjust[team_to_adjust['Attendance'] < 2]
    attendance_2 = team_to_adjust[team_to_adjust['Attendance'] == 2]

    # .........To adjust the team whose weekly attendance is 1
    days_reamaing = []
    for team in (list(attendance_1['Team'])):

        adjustment_team = int(
            df_Team_details.at[df_Team_details[df_Team_details['Team'] == team].index[0], 'Bangalore'])
        
        #day_wise_bangalore_count: It gives the day wise difference in max seat and resource came
        #day_wise_bangalore_count: It provides information on remaining seat
        for ind, value in enumerate(day_wise_bangalore_count):
            if int(adjustment_team) <= int(value):
                
                if ind not in days_reamaing:
                    seats_office_bangalore_today[ind].append(adjustment_team)
                    day_wise_team[ind].append(team)
                    bang_seat=day_wise_seat[ind][0]
                    bang_seat=bang_seat.split(":")
                    first_part=bang_seat[0]
                    second_part=bang_seat[1].split("/")
                    
                    updated_value=first_part+":"+str(int(second_part[0])+adjustment_team)+"/"+second_part[1]
                    day_wise_bangalore_count[ind]=day_wise_bangalore_count[ind]-adjustment_team
                    day_wise_seat[ind][0]=updated_value
                    teams_cameto_office[team] = teams_cameto_office[team]+1                    
                    break

    # .........To adjust the team whose weekly attendance is 2

    days_reamaing = []
    #print("before:",day_wise_seat)
    #print("seats_office_bangalore_today:",seats_office_bangalore_today)
    for team in (list(attendance_2['Team'])):

        adjustment_team = int(
            df_Team_details.at[df_Team_details[df_Team_details['Team'] == team].index[0], 'Bangalore'])
        #print("...............................")
        #print("adjustment_team size: ",adjustment_team)
        #print("day_wise_bangalore_count",day_wise_bangalore_count)
        
        #day_wise_bangalore_count: It gives the day wise difference in max seat and resource came
        #day_wise_bangalore_count: It provides information on remaining seat
        for ind, value in enumerate(day_wise_bangalore_count):
            if int(adjustment_team) <= int(value):
                
                if ind not in days_reamaing:
                    #print("Seat Remaining:",location_seatcount["Bangalore"]-value)
                    #print("inner",ind,team)
                    seats_office_bangalore_today[ind].append(adjustment_team)
                    day_wise_team[ind].append(team)
                    bang_seat=day_wise_seat[ind][0]
                    #print("before",bang_seat)
                    bang_seat=bang_seat.split(":")
                    first_part=bang_seat[0]
                    second_part=bang_seat[1].split("/")
                    
                    updated_value=first_part+":"+str(int(second_part[0])+adjustment_team)+"/"+second_part[1]
                    day_wise_bangalore_count[ind]=day_wise_bangalore_count[ind]-adjustment_team
                    day_wise_seat[ind][0]=updated_value
                    #print("updated_value:",day_wise_seat[ind])
                    teams_cameto_office[team] = teams_cameto_office[team]+1

                    
                    break
    
    print("teams_cameto_office",teams_cameto_office)
    
    
    #-------To get the location wise seats. Ex:[95, 25, 20, 57, 0, 0]
    #values are for location Bangalore, Chennai, Pune, Mumbai, Hyderabad, Delhi
    occupied_seats_location.clear()
    for ind,value in enumerate(day_wise_seat):
        
        temp=[]
        
        for ind_inner, value_inner in enumerate(value):
                   
                    seat=value_inner                    
                    seat=seat.split(":")
                    first_part=seat[0]
                    
                    second_part=seat[1].split("/")
                    #print(second_part)
                    temp.append(int(second_part[0]))
        
        occupied_seats_location.append(temp)
             #[95, 25, 20, 57, 0, 0]
             #95,23
    
     #---------------ToAdjust Excess Seats---------------------
    
    for ind_excess, value_excess in enumerate(day_wise_bangalore_count):
       # print("day_wise_bangalore_count",day_wise_bangalore_count)
    
        for ind, value in enumerate(day_wise_bangalore_count):
                if (int(value_excess)<0) and (int(value_excess) <= int(value)) and (value>0):
                    
                    if ind not in days_reamaing:
                        #print("Seat Remaining:",location_seatcount["Bangalore"]-value)
                        #print("inner",ind_excess,ind,team)
                        day_wise_bangalore_count[ind]=day_wise_bangalore_count[ind]+day_wise_bangalore_count[ind_excess]
                        day_wise_bangalore_count[ind_excess]=day_wise_bangalore_count[ind_excess]-day_wise_bangalore_count[ind_excess]
                        seats_office_bangalore_today[ind].append(adjustment_team)
                        
                        
                        day_wise_team[ind].append(team)
                        bang_seat=day_wise_seat[ind][0]
                        #print("before",bang_seat)
                        bang_seat=bang_seat.split(":")
                        first_part=bang_seat[0]
                        second_part=bang_seat[1].split("/")
                        
                        updated_value=first_part+":"+str(int(second_part[0])+adjustment_team)+"/"+second_part[1]
                        day_wise_bangalore_count[ind]=day_wise_bangalore_count[ind]-adjustment_team
                        day_wise_seat[ind][0]=updated_value
                        #print("updated_value:",day_wise_seat[ind])
                        teams_cameto_office[team] = teams_cameto_office[team]+1   
                        
                        break
                        
    #--------------------------------------------------------------
   
    
    for ind, data in enumerate(day_wise_seat):
        team_count=[]
        
        for in_ind, in_data in enumerate(data):
            if in_ind == 0:
                temp = in_data.split(":")[1].split("/")
                current_seat = int(temp[0])
                max_seat = int(temp[1])
                #print("source",current_seat, max_seat)
                difference=current_seat - max_seat
                if difference>0:
                    teams=day_wise_team[ind]               
                    #print(teams)
                    
                    for team in teams:
                        team_count.append(int(df_Team_details['Bangalore'][df_Team_details[df_Team_details['Team'] == team]['Bangalore'].index[0]]))
                    team_count.sort(reverse=False)
                    
                    #print("team_count",team_count)
                    #Loop to get the teams to swap 
                    for ind_comp, data_comp in enumerate(day_wise_seat):
                        comp_team_count=[]
                        if ind_comp !=ind:
                            if (difference!=0):
                                for inner_ind, ind_datacomp in enumerate(data_comp):
                                    if inner_ind == 0:
                                        temp_dest = ind_datacomp.split(":")[1].split("/")
                                        current_seat_dest = int(temp_dest[0])
                                        max_seat_dest = int(temp_dest[1])
                                        difference_dest=current_seat_dest - max_seat_dest
                                        if difference_dest<0:
                                            difference_dest=abs(difference_dest)
                                            #print("desitination",current_seat_dest, max_seat_dest)
                                            
                                            #print("difference_dest",difference_dest)
                                            
                                            if difference<=difference_dest:
                                                    
                                                    teams=day_wise_team[ind_comp]               
                                                    #print("teams",teams)
                                                    for team in teams:
                                                        comp_team_count.append(int(df_Team_details['Bangalore'][df_Team_details[df_Team_details['Team'] == team]['Bangalore'].index[0]]))
                                                    
                                                    #print("comp_team_count:",comp_team_count)
        #print("..........................")
        
        
    # -----To suffle the team
    week = [0, 1, 2, 3, 4]
    week_suffle = [0, 1, 2, 3, 4]
    week_days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]

    random.shuffle(week_suffle)

    day_wise_team_temp = day_wise_team.copy()
    day_wise_seat_temp = day_wise_seat.copy()
    day_wise_team.clear()
    day_wise_seat.clear()
    for ind in week_suffle:
        day_wise_team.append(day_wise_team_temp[ind])
        day_wise_seat.append(day_wise_seat_temp[ind])
    # -----To suffle th team End---------------------------

    #print("day_wise_team", len(day_wise_seat))
    #print("..................................")
    
    
    smallest_week_strength=find_least_strength_In_week(day_wise_seat)
    
    for data in range(len(week)):
        ind = data  # random.choice(week)
        #print("\n 584 Day:", week_days[data], "\n")
        if ind == smallest_week_strength:
            wednesday = day_wise_team[ind]
            wednesday_bangalore_count = []
            for ind_team in wednesday:
                # print(ind_team)
                wednesday_bangalore_count.append(int(
                    df_Team_details['Bangalore'].at[df_Team_details[df_Team_details["Team"] == ind_team]['Bangalore'].index[0]]))
                backup = wednesday_bangalore_count.copy()
            wednesday_bangalore_count.sort(reverse=False)

            flag = False
            team_count_replace = 0
            for data in wednesday_bangalore_count:
                if flag:
                    break
                elif data >= 20:
                    flag = True
                    team_count_replace = data
            
            #print("Team Came On The Day before:",wednesday)
            ##wednesday[backup.index(team_count_replace)] = "Leadership Team"
            wednesday.append("Leadership Team")
            day_wise_team[ind]=wednesday
            #print("Number of Team:", len(day_wise_team[ind]), "\n")
            
            #print("Team Came On The Day:",day_wise_team[ind])
            #print()
            bang_seat=day_wise_seat[ind][0]
            bang_seat=bang_seat.split(":")
            first_part=bang_seat[0]
            second_part=bang_seat[1].split("/")
            #print("before",day_wise_seat[ind][0],reserved_for_leadership_bang)
            updated_value=first_part+":"+str(int(second_part[0])+reserved_for_leadership_bang)+"/"+second_part[1]
            day_wise_bangalore_count[ind]=day_wise_bangalore_count[ind]-reserved_for_leadership_bang
            day_wise_seat[ind][0]=updated_value
                    
            #print(day_wise_seat[ind][0])
            #print()
            #print(day_wise_seat[ind])
        else:
            #print("Number of Team:", len(day_wise_team[data]), "\n")
            #print(day_wise_team[data])
            #print()
            #print(day_wise_seat[ind])
            pass
        #print("------------------------------------------")
        week.remove(ind)
    #-------------To Move leadership team's attendance to Wednesday
    
    temp_seat=day_wise_seat[2] #2 is wednesday
    temp_team=day_wise_team[2]
   
    day_wise_seat[2]=day_wise_seat[smallest_week_strength]
    day_wise_team[2]=day_wise_team[smallest_week_strength]
    day_wise_seat[smallest_week_strength]=temp_seat
    day_wise_team[smallest_week_strength]=temp_team
    
    #--------------------------------------------------------------
    #--------------To print weekly team---------------
    week = [0, 1, 2, 3, 4]
    
    week_days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]

    #print("============================================")
    for data in range(len(week)):
        
        ind = data  # random.choice(week)
        #print("\nDay:", week_days[data], "\n")
        
        #print("Number of Team:", len(day_wise_team[data]), "\n")
        #print(day_wise_team[data])
        #print()
        #print(day_wise_seat[ind])
            
    
    #---------------------------------------------------
    df_teams_cameto_office = pd.DataFrame({"Team": list(
        teams_cameto_office.keys()), "Attendance": list(teams_cameto_office.values())})
    #print("Weekly Statistics:\n", df_teams_cameto_office)
    
    
    #--------Again adjust occupied_seats_location as day_wise_seat is suffled as done above
    #print(day_wise_seat)
    occupied_seats_location.clear()
    for ind,value in enumerate(day_wise_seat):
        
        temp=[]
        
        for ind_inner, value_inner in enumerate(value):
                   
                    seat=value_inner                    
                    seat=seat.split(":")
                    first_part=seat[0]
                    
                    second_part=seat[1].split("/")
                    #print(second_part)
                    temp.append(int(second_part[0]))
        
        occupied_seats_location.append(temp)
    
    #---------------To adjust seats in Chennai------------------------------
    
    #print(seats_office_bangalore_today)#[10, 3, 2, 7, 12, 20, 10, 6, 10, 0, 14, 1]
    #print(day_wise_seat)#'Total seat occupied in Bangalore:95/95'
    #print(location_seatcount)#'Bangalore': 95, 'Chennai': 23
    #print(location_seatcount)#{'Bangalore': 95, 'Chennai': 23, 'Pune': 20, 'Mumbai': 28, 'Hyderabad': 0, 'Delhi': 0}
    #occupied_seats_location:[[95, 25, 20, 57, 0, 0], [94, 25, 20, 57, 0, 0], [94, 25, 20, 57, 0, 0], [75, 6, 5, 9, 0, 0], [38, 6, 5, 9, 0, 0]]
    Total_seats_chennai=location_seatcount["Chennai"]
    Total_seats_bangalore=location_seatcount["Bangalore"]
    Total_seats_pune=location_seatcount["Pune"]
    for ind,value in enumerate(occupied_seats_location):        
        temp=[]   
        # seat excceds in chennai location that needs to be adjusted
        #comp1: team wise resources total
        comp1=value
        
        #To adjust Chennai Location select index 1
        #exceeded resource in chennai for a particular day
        diff1=comp1[1]-Total_seats_chennai#Seats that arecrossing for chennai location. We need to adjust those teams in other day
        diff1_bang=comp1[0]-Total_seats_bangalore
        diff1_pune=comp1[2]-Total_seats_pune
        #--To check if adjustment is required or not
        if diff1>0:
            #print("-------------------------------------------------")
            #print("Adjustment required for the day",ind+1,":",value)
            #print("occupied_seats_location",occupied_seats_location)
            for ind_inner, value_inner in enumerate(occupied_seats_location):
                #print("Day ",ind_inner+1)
                if ind!=ind_inner:
                    #ind_inner=1
                    #print("ind_inner",ind_inner)
                    #comp2: team wise resources total for the day where we need to swap
                    comp2=value_inner 
                    #comp2=occupied_seats_location[1]
                    #To adjust Chennai Location select index 1
                    diff2=Total_seats_chennai-comp2[1]#Seats available in chennai location for a day
                    diff2_bang=Total_seats_bangalore-comp2[0]#Seats available in Bagalore location for a day
                    diff2_pune=Total_seats_pune-comp2[2]#Seats available in Pune location for a day
                   
                    #To check if any additional seats are available in this day
                        
                    if diff1>0:
                        if (diff2 >0) and (diff2 >= diff1):   
                            #print("At day ",ind_inner+1,"Chennai: seat remaing in a day,seat required:",diff2,diff1)
                            #print("At day ",ind_inner+1,"Bangalore: seat remaing in a day,seat required:",diff2_bang,diff1_bang)
                            #print("At day ",ind_inner+1,"Pune: seat remaing in a day,seat required:",diff2_pune,diff1_pune)
                            
                            
                            #Bangalore
                            #print("On Day",ind_inner+1,"occupied_seats_location:",occupied_seats_location)
                            #print("On Day",ind_inner+1,"day_wise_team:",day_wise_team[ind_inner])
                            
                            
                            #---------For Bangalore Location------------------
                            var1=day_wise_count_from_teamlist(df_Team_details,day_wise_team,occupied_seats_location,'Bangalore')[ind_inner]
                            var1_reference=day_wise_count_from_teamlist(df_Team_details,day_wise_team,occupied_seats_location,'Bangalore')[ind]
                                                        
                            var1_team=day_wise_team[ind_inner]
                            var1_team_reference=day_wise_team[ind]
                            
                            #print("At day ",ind_inner+1,var1,"bangalore total:",sum(var1))
                            #print("At day ",ind+1,var1_reference,"bangalore total:",sum(var1_reference))      
                            
                            var1,var1_team=index_ofsorting_dict(var1,var1_team)
                            var1_reference,var1_team_reference=index_ofsorting_dict(var1_reference,var1_team_reference)
                            #-------------------------------------
                            
                            
                            #---------For Chennai Location------------------
                            var2=day_wise_count_from_teamlist(df_Team_details,day_wise_team,occupied_seats_location,'Chennai')[ind_inner]
                            var2_team=day_wise_team[ind_inner]
                            
                            var2_reference=day_wise_count_from_teamlist(df_Team_details,day_wise_team,occupied_seats_location,'Chennai')[ind]
                            var2_team_reference=day_wise_team[ind]
                            
                            
                            var2,var2_team=index_ofsorting_dict(var2,var2_team)
                            var2_reference,var2_team_reference=index_ofsorting_dict(var2_reference,var2_team_reference)
                            #print("On day",ind_inner+1,"Bangalore team count:",var1,"Chennai",var2)
                            #print("On day",ind+1,"reference Bangalore team count:",var1_reference,"Chennai",var2_reference)
                            #--------------------------------------------------
                            
                            
                            #---------For Pune Location------------------
                            var3=day_wise_count_from_teamlist(df_Team_details,day_wise_team,occupied_seats_location,'Pune')[ind_inner]
                            var3_team=day_wise_team[ind_inner]
                            
                            var3_reference=day_wise_count_from_teamlist(df_Team_details,day_wise_team,occupied_seats_location,'Pune')[ind]
                            var3_team_reference=day_wise_team[ind]
                            
                            
                            var3,var3_team=index_ofsorting_dict(var3,var3_team)
                            var3_reference,var3_team_reference=index_ofsorting_dict(var3_reference,var3_team_reference)
                            #print("On day",ind_inner+1,"Bangalore team count:",var1,"Chennai",var2,"Pune",var3)
                            #print("On day",ind+1,"reference Bangalore team count:",var1_reference,"Chennai",var2_reference,"Pune",var3_reference)
                            
                            #--------------------------------------------------
                            
                            
                            flag_Bang_availability=False
                            flag_pune_availability=False
                            if diff2_bang>0 and((diff2_bang-diff1)>0):
                                flag_Bang_availability=True
                            
                            if diff2_pune>0 and((diff2_pune-diff1_pune)>0):
                                flag_pune_availability=True
                            ind2_bang=0
                            li_map_chennai=[]
                            li_map_pune=[]
                            
                            #print("flag_pune_availability",flag_pune_availability)
                            for ind2,val2 in enumerate(var2):
                                
                                if(flag_Bang_availability and flag_pune_availability and val2>0 and val2<=diff2 ):
                                    #print("val2",val2,"diff:",diff2)
                                    remaining=abs(val2-diff2)
                                    diff1=diff1-val2
                                    #print("seat required:",diff1)
                                    
                                    #print("On Day ",ind_inner+1,"remaining",remaining,"out of:",diff2)
                                    diff2=remaining
                                    #print("occupied_seats_location before",occupied_seats_location)
                                    
                                    #Update the to be adjusted list with chennai count
                                    ###occupied_seats_location[ind][1]=occupied_seats_location[ind][1]-val2# [1]: for chennai
                                    #Update list where adjustment is done withchennai location
                                    ####occupied_seats_location[ind_inner][1]=occupied_seats_location[ind_inner][1]+val2# [1]: for chennai
                                    
                                    li_map_chennai.append(val2)
                                    #print("seat adjusted",val2)
                                    if diff1<=0:
                                        #-----------------Adjust Bangalore Location
                                        li_map_bang=[]#index for bangalore Location To be Moved
                                        sum_bang=0
                                        #print(var1,diff2_bang,)
                                        for ind2_bang,val2_bang in enumerate(var1):
                                             if diff2_bang>=val2_bang:
                                                 sum_bang=sum_bang+val2_bang
                                                 li_map_bang.append(val2_bang)
                                                 if ind2<=sum_bang:
                                                     break
                                        #print("var1 final",var1)
                                        for data in li_map_bang:
                                            #Update the to be adjusted list with Bangalore count
                                            occupied_seats_location[ind][0]=occupied_seats_location[ind][0]-var1_reference[data]# [1]: for chennai
                                            #Update list where adjustment is done with bangalore location
                                            occupied_seats_location[ind_inner][0]=occupied_seats_location[ind_inner][0]+var1_reference[data]# [1]: for chennai
                                        
                                        for data in li_map_chennai:
                                            #Update the to be adjusted list with Bangalore count
                                            occupied_seats_location[ind][1]=occupied_seats_location[ind][1]-var2[data]# [1]: for chennai
                                            #Update list where adjustment is done with bangalore location
                                            occupied_seats_location[ind_inner][1]=occupied_seats_location[ind_inner][1]+var2[data]# [1]: for chennai
                                          
                                        #print("Bangalore index:",li_map_bang)
                                        #print("occupied_seats_location",occupied_seats_location)
                                        break
                                    
                                  
                                    
                            #--------Needs to be updated at the end
                            #day_wise_bangalore_count[ind]=day_wise_bangalore_count[ind]-adjustment_team
                            #day_wise_seat[ind][0]=updated_value
                            #print("updated_value:",day_wise_seat[ind])
                            #teams_cameto_office[team] = teams_cameto_office[team]+1
                            #-------------------------
                            break
            
    
def day_wise_count_from_teamlist(df_Team_details,day_wise_team,occupied_seats_location,location):
    
    team_count=[]
    for ind,data in enumerate(day_wise_team):
        #print("data",data,"\n")
        temp=[]
        for ind_inner,data_inner in enumerate(data):  
            try:                
                temp.append(int(df_Team_details[location][df_Team_details[df_Team_details['Team']== data_inner][location].index[0]]))
            except:
                #print("error:",occupied_seats_location[ind][ind_inner])
                temp.append(reserved_for_leadership_bang)
                #print("team_count",team_count)
                
        team_count.append(temp)
        
    return team_count

def index_ofsorting_dict(li1,li2):
    s = numpy.array(li1)
    sort_index = numpy.argsort(s)
    #print(sort_index)
    li1_temp=[]
    li2_temp=[]
    for data in sort_index:
        li1_temp.append(li1[data])
        li2_temp.append(li2[data])
           
    return li1_temp,li2_temp
def read_exsheet(excel_file,sheet_name):
    sheet = pd.read_excel(excel_file,sheet_name,index_col=0,skiprows=0)
    sheet_dict=sheet.to_dict()
    return sheet_dict
def combinationsum(candidates, target):
    candidates.sort()
    res, curr = [], []
        
    def backtrack(curr, pos, remain):
            
        if remain == 0:
            return res.append(curr[:])
            
        prev = -1
        for i in range(pos, len(candidates)):
            if prev == candidates[i]:
                 continue
            elif remain - candidates[i] < 0:
                break
            curr.append(candidates[i])
            backtrack(curr, i + 1, remain - candidates[i])
            curr.pop()
            prev = candidates[i]
                
    backtrack(curr, 0, target)
    return res
def read_exsheet(excel_file,sheet_name):
    
    sheet = pd.read_excel(excel_file,sheet_name,index_col=0,skiprows=0)
    sheet_dict=sheet.to_dict()
    return sheet_dict
def loadData():
    global seat_allc,leader_details,team_depend,df_team_details
    seat_allc = read_exsheet(filepath,sheet_name='seatcount_location')
    
    leader_details = read_exsheet(filepath,sheet_name='Leader_details')
    
    team_depend = read_exsheet(filepath,sheet_name='Team_dependency')
    df_team_details = pd.read_excel(filepath,sheet_name='Team_details')
    df_team_details= df_team_details.fillna(0)
    return df_team_details
def processMumbaiData():
    global list_Teams
    
    for city in ['Bangalore','Chennai','Pune','Mumbai','Hyderabad','Delhi']:
        df_team_details[city]=pd.to_numeric(df_team_details[city]).astype('int')
    
    list_Teams=df_team_details["Team"].tolist()  
    list_Mumbai= list(df_team_details['Mumbai'].tolist())
    combo_list_mumbai=list(combinationsum(list_Mumbai.copy(), seat_allc['Seat']['Mumbai']))
    
    return list_Mumbai,combo_list_mumbai

#It will return the indices of the combined_sum_city list
def get_Index_of_Combination(list_city,combined_sum_city):
    list_city_index=[ind for ind in range(len(list_city))]
    temp_list_city=list_city.copy()
    index_temp=[]
    info_index=[]
    info_index_all=[]
    info_data_all=[]

    info_data=[]
    
    for  city_list in combined_sum_city:
        
        info_index.clear()
        info_data.clear()
        for city in city_list:
            
            for ind,data2 in enumerate(temp_list_city):
                if city ==data2:
                    if ind not in info_index:
                        info_index.append(ind)
                        info_data.append(data2)
                        break
        
        info_index_all.append(info_index.copy())
        info_data_all.append(info_data.copy())
    return info_index_all,info_data_all
def fetch_teams_with_location_wise_resource():
    
    for team in list(primary_team_dependant_name.keys()):
        teams_with_locationwise_count[team]=df_team_details[df_team_details['Team']==team][["Bangalore","Chennai","Pune","Mumbai","Hyderabad","Delhi"]].values[0]
    
def get_attendance_team_weekly(info_index_all,df_team_details):
    teams={}
    team_attendance_min_time=0
    Teams_tobe_adjusted=[]
    info_index_all_3times=[]
    #info_index_all=info_index_all[0:30]
    min_attendance=True
    team_names=df_team_details['Team'].tolist()
    for data in info_index_all:
        df=df_team_details.iloc[data,:].iloc[:,0:9]
        #print("Data:",data)
        temp=df.sum(axis = 0, skipna = True).tolist()[1:]
        #if temp[0]<=95 and temp[1]<=23 and temp[2]<=20  and temp[3]<=28 and temp[4]<=0 and temp[5]<=0:
        temp_list=[]
        for index,data2 in enumerate(team_names):
            if data2 not in teams:
                teams[data2]=1
                try:
                    temp_list.append(data[index])
                except:
                    pass
                
            else:
                count=teams[data2]
                if count<=2:
                    teams[data2]=count+1
                    
                if teams[data2]<=3:
                    try:
                        temp_list.append(data[index])
                    except:
                        pass
                
        list_teams=list(teams.values())        
        list_teams.sort()
        
        #------stop storing when all the teams attended 3 days office
        if min_attendance:
                info_index_all_3times.append(temp_list)
                #print("teams::",info_index_all_3times)
        if list_teams[0]==3:
            
            min_attendance=False
        
      
    print("info_index_all_3times:",info_index_all_3times)
    
    return info_index_all_3times

def updateDataframe_locations():
    row_count=0
    row_count_bangalore=0
    row_count_chennai=0
    row_count_pune=0
    row_count_hyderabad=0
    row_count_delhi=0
    global df_bangalore_final,df_chennai_final,df_pune_final,df_hyderabad_final,df_delhi_final
    df_mumbai_final=pd.DataFrame()
    df_bangalore_final=pd.DataFrame()
    df_chennai_final=pd.DataFrame()
    df_pune_final=pd.DataFrame()
    df_hyderabad_final=pd.DataFrame()
    df_delhi_final=pd.DataFrame()
    for index,day in enumerate(week_days):
        df_mumbai=pd.DataFrame()
        df_bangalore=pd.DataFrame()
        df_chennai=pd.DataFrame()
        df_pune=pd.DataFrame()
        df_hyderabad=pd.DataFrame()
        df_delhi=pd.DataFrame()
        
        
        ##print("Day",day,"\n")
        team_name_mumbai=mumbai_min_attendance_team_final[index]
        
        #print("Mumbai Team:",team_name_mumbai,"\n","Attendance:",occupied_seats_mumbaifinal[index],"\n")
        if len(team_name_mumbai)>0 and team_name_mumbai[0] !='':
            
            df_mumbai['Team']=team_name_mumbai
        resource=[]
        day_list=[]
        
        try:
            
            for ind,name in enumerate(list(team_name_mumbai)):
                
                #print("Mumbai Occupied Seats for :",name," : ",teams_with_locationwise_count[name][3])
                resource.append(teams_with_locationwise_count[name][3])
                if (ind<len(list(team_name_mumbai))):
                    day_list.append(day)
                    
        except Exception as e:
            
            pass
        if len(team_name_mumbai)>0 and team_name_mumbai[0] !='':
            df_mumbai['Day']=day_list
            df_mumbai['Resource Count']=resource
            df_mumbai=df_mumbai[df_mumbai['Resource Count']>0]
            df_mumbai.reset_index(inplace=True,drop=True)
            df_mumbai.index=[data+1 for data in range(df_mumbai.shape[0])]
            df_mumbai=df_mumbai[["Day","Team","Resource Count"]]
        #df_mumbai.style.set_properties(**{'text-align': 'left'})
        #print(df_mumbai)
        if df_mumbai.shape[0]>0:
            df_mumbai_final=pd.concat([df_mumbai_final,df_mumbai])
            print("df_mumbai_final",df_mumbai_final)
            df_mumbai.to_excel(writer,sheet_name='Mumbai',startrow=row_count , startcol=0)   
            
            row_count+=df_mumbai.shape[0]+1
                      
        #------------------------------------------------
        team_name=day_wise_team[index]   
        
        if len(team_name)>0 and team_name[0] !='':            
            df_bangalore['Team']=team_name
            df_chennai['Team']=team_name
            df_pune['Team']=team_name
            df_hyderabad['Team']=team_name
            df_delhi['Team']=team_name
            
        #print("\nRest Of the Location:",team_name)
        attendance_bangalore=0
        attendance_chennai=0
        attendance_pune=0
        attendance_hyderabad=0
        attendance_delhi=0
        
        li_attendance_bangalore=[]
        li_attendance_chennai=[]
        li_attendance_pune=[]
        li_attendance_hyderabad=[]
        li_attendance_delhi=[]
        li_day_list_rest=[]
        
        
        try:
            ind=0
            li_day_list_rest.clear()
            #print("team_name",team_name)
            for ind,name in enumerate(list(team_name)):
                if name=="Leadership Team":
                      attendance=[reserved_for_leadership_bang,0,0,0,0]
                else:
                 attendance=list(teams_with_locationwise_count[name][0:3])+list(teams_with_locationwise_count[name][4:])
                #print("Occupied Seats for :",name," : ",attendance)
                #print(name,day)
                li_day_list_rest.append(day)
                
                #print("attendance",attendance)
                attendance_bangalore=attendance_bangalore+attendance[0]
                li_attendance_bangalore.append(attendance[0])
                
                attendance_chennai=attendance_chennai+attendance[1]
                li_attendance_chennai.append(attendance[1])
                
                attendance_pune=attendance_pune+attendance[2]
                li_attendance_pune.append(attendance[2])
                
                
                attendance_hyderabad=attendance_hyderabad+attendance[3]
                li_attendance_hyderabad.append(attendance[3])
                
                
                attendance_delhi=attendance_delhi+attendance[4]
                li_attendance_delhi.append(attendance[4])
            
        except Exception as e:
            #print("error",e)
            pass
        attendance_bangalore_list.append(attendance_bangalore)
        attendance_chennai_list.append(attendance_chennai)
        attendance_pune_list.append(attendance_pune)
        attendance_hyderabad_list.append(attendance_hyderabad)
        attendance_delhi_list.append(attendance_delhi)
        for loc in location:
            #print("loc",loc)
            #print("day_list_rest",li_day_list_rest)
            if len(team_name)>0 and team_name[0] !='':
                #print("li_day_list_rest",len(li_day_list_rest))
                
                #location=["Bangalore","Chennai","Pune","Mumbai","Hyderabad","Delhi"]
                if loc=="Bangalore":
                    df_bangalore['Day']=li_day_list_rest
                    df_bangalore['Resource Count']=li_attendance_bangalore
                    df_bangalore=df_bangalore[df_bangalore['Resource Count']>0]
                    df_bangalore.reset_index(inplace=True,drop=True)
                    df_bangalore.index=[data+1 for data in range(df_bangalore.shape[0])]
                    df_bangalore=df_bangalore[["Day","Team","Resource Count"]]
                elif loc=="Chennai":
                    #print("team_name",len(team_name))
                    df_chennai['Day']=li_day_list_rest
                    #print(li_attendance_chennai)
                    df_chennai['Resource Count']=li_attendance_chennai
                    df_chennai=df_chennai[df_chennai['Resource Count']>0]
                    df_chennai.reset_index(inplace=True,drop=True)
                    df_chennai.index=[data+1 for data in range(df_chennai.shape[0])]
                    df_chennai=df_chennai[["Day","Team","Resource Count"]]
                elif loc=="Pune":
                    df_pune['Day']=li_day_list_rest
                    df_pune['Resource Count']=li_attendance_pune
                    df_pune=df_pune[df_pune['Resource Count']>0]
                    df_pune.reset_index(inplace=True,drop=True)
                    df_pune.index=[data+1 for data in range(df_pune.shape[0])]
                    df_pune=df_pune[["Day","Team","Resource Count"]]
                elif loc=="Hyderabad":
                    df_hyderabad['Day']=li_day_list_rest
                    df_hyderabad['Resource Count']=li_attendance_hyderabad
                    df_hyderabad=df_hyderabad[df_hyderabad['Resource Count']>0]
                    df_hyderabad.reset_index(inplace=True,drop=True)
                    df_hyderabad.index=[data+1 for data in range(df_hyderabad.shape[0])]
                    df_hyderabad=df_hyderabad[["Day","Team","Resource Count"]]
                elif loc=="Delhi":
                    df_delhi['Day']=li_day_list_rest
                    df_delhi['Resource Count']=li_attendance_delhi
                    df_delhi=df_delhi[df_delhi['Resource Count']>0]
                    df_delhi.reset_index(inplace=True,drop=True)
                    df_delhi.index=[data+1 for data in range(df_delhi.shape[0])]
                    df_delhi=df_delhi[["Day","Team","Resource Count"]]
      
        #df_mumbai.style.set_properties(**{'text-align': 'left'})
        #print("\ndf_bangalore\n",df_bangalore)
        if df_bangalore.shape[0]>0:
            df_bangalore_final=pd.concat([df_bangalore_final,df_bangalore])
            
        if df_chennai.shape[0]>0:
            df_chennai_final=pd.concat([df_chennai_final,df_chennai])
            
        if df_pune.shape[0]>0:
            df_pune_final=pd.concat([df_pune_final,df_pune])
            
        if df_hyderabad.shape[0]>0:
            df_hyderabad_final=pd.concat([df_hyderabad_final,df_hyderabad])
            
        if df_delhi.shape[0]>0:
            df_delhi_final=pd.concat([df_delhi_final,df_delhi])
    return df_mumbai_final
def getTeamAttendance(dict,df_bangalore):
    dict={}
    for team in df_bangalore['Team'].tolist():
        if team not in dict:
            dict[team]=1
        else:
            count=dict[team]
            dict[team]=count+1
def getAttendance_all_team():
    dict_temp={}
    for team in day_wise_team:
        for name in team:
            if name not in dict_temp:
                dict_temp[name]=1
            else:
                count=dict_temp[name]
                dict_temp[name]=count+1
    
    team_attendance={}
    
    for key,value in dict_temp.items():
        if key !="Leadership Team":
            
            team_attendance[key]=value
    return dict_temp

def getAttendance_mumbai_team():
    
    dict_temp={}
    for team in mumbai_min_attendance_team_final:
        for name in team:
            if name !="":
                if name not in dict_temp:
                    dict_temp[name]=1
                else:
                    count=dict_temp[name]
                    dict_temp[name]=count+1
        
    team_attendance={}
    
    for key,value in dict_temp.items():
        if key !="Leadership Team":
            
            team_attendance[key]=value
    return dict_temp
def getAttendance_less_than_3():
    temp_attendance=getAttendance_all_team()
    team_attendance_lessthan_3={}
    
    for key,value in temp_attendance.items():
        if temp_attendance[key]<3 and key !="Leadership Team":
            
            team_attendance_lessthan_3[key]=value
    return team_attendance_lessthan_3

def getAttendance_less_than_3_withIp(dict):
    
    team_attendance_lessthan_3={}
    
    for key,value in dict.items():
        if dict[key]<3 and key !="Leadership Team":
            
            team_attendance_lessthan_3[key]=value
    return team_attendance_lessthan_3
def adjustTeamCount():
    
    
    #getTeamAttendance(dict,df_bangalore_final)
    dict=getAttendance_all_team()
    
    for key in list_Teams:
        if key not in dict:
            dict[key]=0
    print("\ndict:",dict,len(dict))
    team_attendance_lessthan_3={}
    dict_3=getAttendance_less_than_3_withIp(dict)
    for key,value in dict_3.items():
        if dict_3[key]<3 and key !="Leadership Team":
            
            team_attendance_lessthan_3[key]=value
    
    print("\nteam_attendance_lessthan_3",team_attendance_lessthan_3)
    print("\nday_wise_team:",len(day_wise_team))
    flag=True
    ind_team={}
    while flag:
        flag=False
        for name in team_attendance_lessthan_3:
            
            team_list=[]
            
            for ind,data in enumerate(attendance_bangalore_list):
                diff=seat_allc['Seat']["Bangalore"]-data
                diff_chennai=seat_allc['Seat']["Chennai"]-attendance_chennai_list[ind]
                diff_pune=seat_allc['Seat']["Pune"]-attendance_pune_list[ind]
                
                if diff >0 and diff_chennai>0 and diff_pune>0:
                    #print(diff,diff_chennai,diff_pune)
                    if team_attendance_lessthan_3[name]<3 and teams_with_locationwise_count[name][0]<=diff and teams_with_locationwise_count[name][1]<=diff_chennai and teams_with_locationwise_count[name][2]<=diff_pune:
                        
                        if ind not in ind_team:
                            
                            team_list.append(name)
                            ind_team[ind]=team_list
                            attendance_bangalore_list[ind]=attendance_bangalore_list[ind]+teams_with_locationwise_count[name][0]
                            attendance_chennai_list[ind]=attendance_chennai_list[ind]+teams_with_locationwise_count[name][1]
                            attendance_pune_list[ind]=attendance_pune_list[ind]+teams_with_locationwise_count[name][2]
                            print("ind",ind)
                            teamtoadd=day_wise_team[ind]
                            teamtoadd.append(name)
                            day_wise_team[ind]=teamtoadd
                            flag=True
                            dict[name]=dict[name]+1
                            team_attendance_lessthan_3[name]=team_attendance_lessthan_3[name]+1
                            break
            
                        else:
                            team_list=ind_team[ind]
                            if name not in team_list:
                                
                                team_list.append(name)
                                ind_team[ind]=team_list
                                attendance_bangalore_list[ind]=attendance_bangalore_list[ind]+teams_with_locationwise_count[name][0]
                                attendance_chennai_list[ind]=attendance_chennai_list[ind]+teams_with_locationwise_count[name][1]
                                attendance_pune_list[ind]=attendance_pune_list[ind]+teams_with_locationwise_count[name][2]
                                teamtoadd=day_wise_team[ind]
                                teamtoadd.append(name)
                                day_wise_team[ind]=teamtoadd
                                flag=True
                                dict[name]=dict[name]+1
                                team_attendance_lessthan_3[name]=team_attendance_lessthan_3[name]+1
                                break
    
def test_teamcount():
    #-----------testing---------------
    print()    
    for i in range(0,5):
        count=0
        for data in day_wise_team[i]    :
            if data=="Leadership Team":
                temp=20
            else:
             temp=teams_with_locationwise_count[data][0]
            count+=temp
        print("count:",count)#validate the result  with attendance_bangalore_list 
    #-------------------------------------------
def getTeamNames_count_gt_team_to_swap(dict_3):
    
    dayno={}
    
    dict_Attendance_all_team=getAttendance_all_team()
    
    print("\n\nadjustment:",dict_3,"\n")
    
    teams_tobe_adjusted=list(dict_3.keys())
    for key,value in dict_3.items():
         if key !="Leadership Team" :
             locationwisecount=teams_with_locationwise_count[key]
             if locationwisecount[0]>0:
                 print("\n1371 locationwisecount:",key,locationwisecount,"\n")
                 
                 for i in range(0,5):
                     if key not in day_wise_team[i]:
                         for names in day_wise_team[i]:
                             if names !="Leadership Team" :
                                 locationwisecount_toswap=teams_with_locationwise_count[names]
                                 if locationwisecount[0]<=locationwisecount_toswap[0]:
                                     if dict_Attendance_all_team[names]==3:
                                         if i not in dayno and dict_Attendance_all_team[key]<3:
                                             temp_team=[]
                                             temp_team.append(names)
                                             dayno[i]=temp_team
                                             
                                         elif i in dayno:
                                             temp_team=dayno[i]
                                             if key not in temp_team and dict_Attendance_all_team[key]<3:
                                                 
                                                 temp_team.append(names)
                                                 dayno[i]=temp_team
                                
    return dayno                                                 
def swap_teams():
    print()
    dayno={}
    dict_to_ignore={}
    print("\n\nreading------------------------",len(attendance_lt_3),attendance_lt_3)
    if len(attendance_lt_3) >0:
        dict_to_ignore=attendance_lt_3
      
    dict_3=getAttendance_less_than_3()
    #print(getTeamNames_count_gt_team_to_swap(dict_3))
    
    dict_Attendance_all_team=getAttendance_all_team()
    
    print("\n\nadjustment:",dict_3,"\n")
    
    teams_tobe_adjusted=list(dict_3.keys())
    for key,value in dict_3.items():
         if key !="Leadership Team" :
             locationwisecount=teams_with_locationwise_count[key]
             if locationwisecount[0]>0:
                 #print("\n",key,locationwisecount,"\n")
                 
                 for i in range(0,5):
                     
                     day_wise_team_data=day_wise_team[i].copy()
                     random.shuffle(day_wise_team_data)
                     if key not in day_wise_team_data:
                         for names in day_wise_team_data:
                             if names !="Leadership Team" :
                                 locationwisecount_toswap=teams_with_locationwise_count[names]
                                 if locationwisecount[0]<=locationwisecount_toswap[0]:
                                     if dict_Attendance_all_team[names]==3:
                                         
                                         if i not in dayno and dict_Attendance_all_team[key]<3 and (names not in dict_to_ignore):
                                             #print("\nlocationwisecount_toswap: ",names,locationwisecount_toswap,"\n")
                                 
                                             dict_Attendance_all_team[names]=dict_Attendance_all_team[names]-1
                                             dict_Attendance_all_team[key]=dict_Attendance_all_team[key]+1
                                             #print(i,names," : ",dict_Attendance_all_team[names],locationwisecount_toswap[0]," : ",key,dict_Attendance_all_team[key],teams_with_locationwise_count[key][0])
                                             team_to_update=day_wise_team[i]
                                             #print("\nTeam update:",team_to_update)
                                             team_to_update.remove(names)                                             
                                             team_to_update.append(key)
                                             day_wise_team[i]=team_to_update
                                             #print("\nTeam update2:",team_to_update)
                                             temp_team=[]
                                             temp_team.append(key)
                                             dayno[i]=temp_team
                                             break
                                         elif i in dayno:
                                             temp_team=dayno[i]
                                             if key not in temp_team and dict_Attendance_all_team[key]<3 and (names not in dict_to_ignore):
                                                 #print("\nlocationwisecount_toswap 2: ",key,dict_Attendance_all_team[key],names,locationwisecount_toswap,"\n")
                                 
                                                 dict_Attendance_all_team[names]=dict_Attendance_all_team[names]-1
                                                 dict_Attendance_all_team[key]=dict_Attendance_all_team[key]+1
                                                 #print(i,names," :inside: ",dict_Attendance_all_team[names]," : ",key,dict_Attendance_all_team[key])
                                                 team_to_update=day_wise_team[i]
                                                 #print("Team update inside:",team_to_update)
                                                 team_to_update.remove(names)                                             
                                                 team_to_update.append(key)
                                                 day_wise_team[i]=team_to_update
                                                 #print("Team update inside2:",team_to_update)
                                                 temp_team.append(key)
                                                 dayno[i]=temp_team
                                                 break
                                            
def allocation():
    temp={}
    all_team_weekly=[]
    attendance_bangalore_list.clear()
    #-------To load data from the Excel Template
    df_team_details=loadData()
    # ------To Get the list of combination of Teams/Day that do not cross the maximum allocated size for Mumbai
    list_Mumbai,combo_list_mumbai=processMumbaiData()
    
    # ------To Get the Index of list of combination of Teams/Day that do not cross the maximum allocated size for Mumbai
    #-------From the index we can pull the team names from the df_team_details dataframe
    info_index_all,info_data_all=get_Index_of_Combination(list_Mumbai,combo_list_mumbai)
    
    
    #----------To Get the Index of Mumbai Team list per week with minimum attendance of 3----------------
    mumbai_min_attendance_index=get_attendance_team_weekly(info_index_all,df_team_details)
    
    
    #----------To Get the Mumbai Team list per week with minimum attendance of 3----------------
    mumbai_min_attendance_team=[]
    occupied_seats_mumbai=[]
    for index in mumbai_min_attendance_index:
        df=df_team_details.iloc[info_index_all[0],:].iloc[:,0:7]
        mumbai_min_attendance_team.append(df['Team'].tolist())
    
        df_temp=df_team_details.iloc[index,:].iloc[:,3:7]
        occupied_seats_mumbai.append(df_temp.sum(axis = 0, skipna = True).tolist()[1:][2])
        
    #------Refer day_wise_team that is created in homePage to get the day wise team   
    homePage()
    
    
    #---------To fetch the team along with its location wise resource count
    
    fetch_teams_with_location_wise_resource()
    
    
    # -----To suffle the Days of a week
    week = [0, 1, 2, 3, 4]
    week_suffle = [0, 1, 2, 3, 4]
    
    random.shuffle(week_suffle)
    
    #----update occupied_seats_location with mumbai_min_attendance_team value
    global mumbai_min_attendance_team_final,occupied_seats_mumbaifinal
    mumbai_min_attendance_team_final=[[""],[""],[""],[""],[""],['']]
    occupied_seats_mumbaifinal=[0,0,0,0,0,0]
    for index,day in enumerate(week_suffle[0:len(occupied_seats_mumbai)]):
            occupied_seats_location[day][3]=occupied_seats_mumbai[index]
            mumbai_min_attendance_team_final[day]=mumbai_min_attendance_team[index]
            occupied_seats_mumbaifinal[day]=occupied_seats_mumbai[index]
            
    print("Attendance Mumbai Team:",getAttendance_mumbai_team())
    
    #---------------Writing in an Excel-------------------------------
    # Creating Excel Writer Object from Pandas 
    global writer
    writer = pd.ExcelWriter( filepath_output,engine='xlsxwriter')   
    workbook=writer.book
    worksheet=workbook.add_worksheet('Mumbai')
    writer.sheets['Mumbai'] = worksheet
    
    #------------Initialize Team Attendance  ------------------------
    dict={}
    for data in teams_with_locationwise_count.keys():
        dict[data]=0
    #--------------------------------
    updateDataframe_locations()
    
    adjustTeamCount()  
    #print("\ngetAttendance_less_than_3 before:",getAttendance_less_than_3())
    
    '''
    
    # print("\nxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx\n")\
    #print(dict)
    '''
    
    print("\n",getAttendance_all_team(),len(getAttendance_all_team()),"\n")
    
    #test_teamcount()
    swap_teams()
    #print(getAttendance_all_team())
    test_teamcount()
    df_mumbai_final=updateDataframe_locations()
    
    print("\ngetAttendance_less_than_3:",getAttendance_less_than_3())
    
    
    with open(filepath_tracker, 'wb') as fp:
        pickle.dump(getAttendance_less_than_3(), fp)
    print("---------------------------------------------")
    
    
    # And within an expander
    expander = st.expander("Bangalore Weekly Report", expanded=False)
    
    with expander:
       st.table(df_bangalore_final)
    expander = st.expander("Mumbai Weekly Report", expanded=False)
    with expander:
        st.table(df_mumbai_final)
    expander = st.expander("CHennai Weekly Report", expanded=False)
    with expander:
        st.table(df_chennai_final)
    expander = st.expander("Pune Weekly Report", expanded=False)
    with expander:
        st.table(df_pune_final)
    expander = st.expander("Hyderabad Weekly Report", expanded=False)
    with expander:
        st.table(df_hyderabad_final)
    expander = st.expander("Delhi Weekly Report", expanded=False)
    with expander:
        st.table(df_delhi_final)
    
    row_count=0
    print(())
    
    
    #-----------To store weekly attendance for reporting purpose------------
    
    if os.path.isfile(filepath_team_attendance) :
        with open(filepath_team_attendance, mode ='rb')as file:
           all_team_weekly = pickle.load(file)  
    #----------To store data only for 48 weeks
    if len(all_team_weekly)>48:
        all_team_weekly.clear()
    #print("all_team_weekly before:",len(all_team_weekly))
    all_team_weekly.append(getAttendance_all_team())
    #print("all_team_weekly",len(all_team_weekly))
    with open(filepath_team_attendance, 'wb') as fp:
        pickle.dump(all_team_weekly, fp)
    #-----------------------------------------------------------------------
    
    all_team_weekly_mumbai=[]
    if os.path.isfile(filepath_team_attendance_mumbai) :
        with open(filepath_team_attendance_mumbai, mode ='rb')as file:
           all_team_weekly_mumbai = pickle.load(file)  
    #----------To store data only for 48 weeks
    if len(all_team_weekly_mumbai)>48:
        all_team_weekly_mumbai.clear()
    all_team_weekly_mumbai.append(getAttendance_mumbai_team())
    with open(filepath_team_attendance_mumbai, 'wb') as fp:
        pickle.dump(all_team_weekly_mumbai, fp)
    #print("all_team_weekly_mumbai",len(all_team_weekly_mumbai),len(all_team_weekly))
    #-------------------------------------------------------------------------
    #print("all_team_weekly",len(all_team_weekly))
    for data in all_team_weekly:
        
        for key,value in data.items():
            if key not in temp:
                li=[value]
                temp[key]=li
            else:
                li=temp[key]
                li.append(value)
                temp[key]=li
    print("getAttendance_less_than_3 :",getAttendance_less_than_3(),"\n")
    print("temp:",temp)
    new = pd.DataFrame.from_dict(temp)
    new.index=[data+1 for data in range(0,new.shape[0])]
    #print(new.columns.tolist())
    new.to_csv("Front End\\Data\\report.csv")   
    #--------------------------------------------------------------------------------
    df_bangalore_final.to_excel(writer,sheet_name='Bangalore',startrow=row_count , startcol=0)   
    df_chennai_final.to_excel(writer,sheet_name='Chennai',startrow=row_count, startcol=0)   
    df_pune_final.to_excel(writer,sheet_name='Pune',startrow=row_count, startcol=0)  
    df_hyderabad_final.to_excel(writer,sheet_name='Hyderabad',startrow=row_count , startcol=0)   
    df_delhi_final.to_excel(writer,sheet_name='Delhi',startrow=row_count , startcol=0)   
    
    writer.save()
                                                
if __name__ == '__main__':
    os.chdir("C:\\Users\\028906744\\Documents\\Python Tutorial\\LTI\\seatAllocate\\")
    allocation()
    
    
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
        if exists(lastgenerationdate_path):
            with open(lastgenerationdate_path, 'rb') as fp:
                    date=pickle.load( fp)  
                    placeholder.warning("Last Report Generated On: "+date)
        generate=st.button("Generate Allocation Report")
        if generate:
            p = Popen(r"C:\Users\028906744\Documents\Python Tutorial\LTI\seatAllocate\Front End\Pages\seat_allocation.bat", cwd=r"C:\Users\028906744\Documents\Python Tutorial\LTI\seatAllocate\Front End\Pages")
            stdout, stderr = p.communicate()
            
            with open(filepath_tracker_bangalore, 'rb') as fp:
                df_bangalore_final=pickle.load( fp)    
            with open(filepath_tracker_chennai, 'rb') as fp:
                df_chennai_final=pickle.load( fp)    
            with open(filepath_tracker_pune, 'rb') as fp:
                df_pune_final=pickle.load( fp)    
            with open(filepath_tracker_hyderabad, 'rb') as fp:
                df_hyderabad_final=pickle.load( fp)    
            with open(filepath_tracker_delhi, 'rb') as fp:
                df_delhi_final=pickle.load( fp) 
            with open(filepath_tracker_mumbai, 'rb') as fp:
                df_mumbai_final=pickle.load( fp) 
            # And within an expander
            expander = st.expander("Bangalore Weekly Report", expanded=False)
            
            with expander:
               st.table(df_bangalore_final)
            expander = st.expander("Mumbai Weekly Report", expanded=False)
            with expander:
                st.table(df_mumbai_final)
            expander = st.expander("Chennai Weekly Report", expanded=False)
            with expander:
                st.table(df_chennai_final)
            expander = st.expander("Pune Weekly Report", expanded=False)
            with expander:
                st.table(df_pune_final)
            expander = st.expander("Hyderabad Weekly Report", expanded=False)
            with expander:
                st.table(df_hyderabad_final)
            expander = st.expander("Delhi Weekly Report", expanded=False)
            with expander:
                st.table(df_delhi_final)
            placeholder.success("Report Generated On:"+tday_date)
            with open(lastgenerationdate_path, 'wb') as fp:
                pickle.dump(tday_date, fp)    
       
        
    else:
        placeholder.warning("Kindly Login To Access The Page")