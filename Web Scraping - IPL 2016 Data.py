#!/usr/bin/env python
# coding: utf-8

# In[1]:


import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import numpy as np


# In[2]:


url = 'https://www.cricbuzz.com/cricket-series/2430/indian-premier-league-2016/matches';


# In[3]:


web_page = requests.get(url)


# In[4]:


content = web_page.content


# In[5]:


soup = BeautifulSoup(content,'html')


# In[6]:


soup.body


# In[7]:


elements = soup.findAll('div',attrs={'class' : 'cb-col-60 cb-col cb-srs-mtchs-tm'})


# In[8]:


anchors = [];
links = [];
winners = [];
score_card = soup.findAll('a',attrs={'class' : 'cb-text-complete'})
for l in score_card:
    winners.append(l.text.partition('won')[0].upper())
    links.append('https://www.cricbuzz.com' + l['href'])
    anchors.append(l)


# In[9]:


links


# In[10]:


headings = soup.findAll('a',attrs={'class': 'text-hvr-underline'})


# In[11]:


match_heading = [];
for h in headings:
    match_heading.append((h.text).split(',',1)[0])


# In[12]:


first_team = [];
second_team = [];
for h in headings:
    text = (h.text).split(',',1)[0]
    first_team.append(text.partition('vs')[0].upper())
    second_team.append(text.partition('vs')[2].upper())


# In[13]:


ipl_2016 = pd.DataFrame([match_heading,winners])


# In[14]:


new_ipl_data  = ipl_2016.transpose()


# In[15]:


new_ipl_data.columns = ['Match','Winner']


# In[16]:


new_ipl_data


# In[17]:


new_ipl_data.drop(new_ipl_data.tail(2).index,inplace=True)


# In[18]:


new_ipl_data


# In[19]:


new_ipl_data.to_csv('IPL 2016 Matches.csv',index=False)


# In[20]:


match_details_rev = pd.DataFrame([first_team,second_team,winners])
match_details = match_details_rev.transpose()
match_details.columns = ['Team 1','Team 2', 'Winner']


# In[21]:


match_details.drop(match_details.tail(2).index,inplace=True)


# In[22]:


match_details


# In[23]:


match_details.to_csv('IPL 2016 Teams Winners.csv',index=False)


# In[24]:


## getting scores
scores = [];


# In[25]:


scores_elements = [];
for l in links:
    body = requests.get(l)
    scoreContent = body.content
    scoreSoup = BeautifulSoup(scoreContent,'html')
    b = scoreSoup.body
    scores_elements.append(b.findAll('div',attrs={'class':'cb-col cb-col-67 cb-scrs-wrp'} ))


# In[26]:


final_scores = [];


# In[27]:


for scores in scores_elements:
    for s in scores:
        s1 = s.find('div',attrs = {'class':'cb-col cb-col-100 cb-min-tm cb-text-gray'}).text
        s2 = s.find('div',attrs = {'class':'cb-col cb-col-100 cb-min-tm'}).text
        final_scores.append(s1)
        final_scores.append(s2)


# In[28]:


final_scores # each match displays Team name runs/wickets (overs)


# In[29]:


ind_scores = {};
team_names = [];
runs_overs = [];
mi_score = {};
for f in final_scores:
    inside = re.split('(\d+)',f);
    team_names.append(inside[0])
    runs_overs.append(inside[1])


# In[30]:


team_names


# In[31]:


runs_overs


# In[32]:


d = {};
d[1] = ['mi','rcb','kkr']
d[2] = ['srh','rr','csk']


# In[33]:


mi_runs = [];
rsp_runs = [];
kkr_runs = [];
rcb_runs = [];
gl_runs = [];
srh_runs = [];
dd_runs = [];
kxip_runs = [];


# In[34]:


for i in range(0,120):
    if('Mumbai Indians '==team_names[i]):
        mi_runs.append(runs_overs[i])
    elif('Rising Pune Supergiants '==team_names[i]):
        rsp_runs.append(runs_overs[i])
    elif('Kings XI Punjab '==team_names[i]):
        kxip_runs.append(runs_overs[i])
    elif('Royal Challengers Bangalore '==team_names[i]):
        rcb_runs.append(runs_overs[i])
    elif('Delhi Daredevils '==team_names[i]):
        dd_runs.append(runs_overs[i])
    elif('Sunrisers Hyderabad '==team_names[i]):
        srh_runs.append(runs_overs[i])
    elif('Kolkata Knight Riders '==team_names[i]):
        kkr_runs.append(runs_overs[i])
    elif('Gujarat Lions '==team_names[i]):
        gl_runs.append(runs_overs[i])


# In[35]:


teams_runs_dup = pd.DataFrame([mi_runs,rsp_runs,kxip_runs,rcb_runs,dd_runs,srh_runs,kkr_runs,gl_runs])


# In[36]:


teams_runs = teams_runs_dup.transpose()


# In[37]:


teams_runs.columns = ['Mumbai Indians','Rising Pune Supergiants','Kings XI Punjab','Royal Challengers Bangalore',
                     'Delhi Daredevils','Sunrisers Hyderabad','Kolkata Knight Riders','Gujarat Lions']


# In[38]:


teams_runs


# In[39]:


teams_runs['Royal Challengers Bangalore'][16] = '200' #since it is Final match score...to display in last row


# In[40]:


teams_runs['Royal Challengers Bangalore'][15] = np.nan


# In[41]:


teams_runs.index=['match 1','match 2','match 3','match 4','match 5','match 6','match 7','match 8','match 9',
                  'match 10','match 11','match 12','match 13','match 14','Q1/E1','Q2','Final']


# In[42]:


teams_runs


# In[43]:


teams_runs.to_csv('IPL 2016 Teams Runs.csv')

