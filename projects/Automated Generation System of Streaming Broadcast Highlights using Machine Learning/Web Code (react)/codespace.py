# print ("Welcome to CodeSpace")
import requests 
import json
import sys
import numpy as np
import pandas as pd
from pandas import DataFrame
from pandas import read_csv
from datetime import datetime, timedelta
import datetime
import nltk
# print ("Welcome to ",str (sys.argv))

def geturl(url):
    # URL = url
    # print(url)
    return url

if __name__ == '__main__':
    a = geturl(sys.argv[1])

a = a.split('/')
v_id = a[4]
videoId = v_id.strip()


#채팅 다운로드 
def doubleDigit(num):
    if num < 10 :
        return '0'+str(num)
    else:
        return str(num)

def main(v_id,c_id):   
        
    if sys.version_info[0] == 2:
        reload(sys)
        sys.setdefaultencoding('utf-8')    
    
    # videoId = v_id
    clientId = "hxr989pss9azzdbzfrlwhwbcabjhp2"
    
    chat = []
    time = []
    user = []
    
    nextCursor = ''
    
    params = {}
    params['client_id'] = clientId    
    
    i = 0
    
    while True :
        if i == 0 :
            URL = 'https://api.twitch.tv/v5/videos/'+videoId+'/comments?content_offset_seconds=0' 
            i += 1
        else:
            URL = 'https://api.twitch.tv/v5/videos/'+videoId+'/comments?cursor=' 
            URL +=  nextCursor          
        
        response = requests.get(URL, params=params)
        
        j = json.loads(response.text)
        
        for k in range(0,len(j["comments"])):
            timer = j["comments"][k]["content_offset_seconds"]
            
            timeMinute = int(timer/60)
            
            if timeMinute >= 60 :
                timeHour = int(timeMinute/60)
                timeMinute %= 60
            else :
                timeHour = int(timeMinute/60)
    
            timeSec = int(timer%60)
            
            time.append(doubleDigit(timeHour)+':'+doubleDigit(timeMinute)+':'+doubleDigit(timeSec))
            user.append(j["comments"][k]["commenter"]["display_name"])
            chat.append(j["comments"][k]["message"]["body"])
       
        if '_next' not in j:
            break
        
        nextCursor = j["_next"]
            
    
    f = open(videoId+".txt", 'wt', -1, "utf-8")
    
    for x in range(0, len(time)): 
            f.write('')
            f.write(str(time[x]))
            f.write('')
            f.write('|')
            f.write('')
            f.write(str(user[x]))
            f.write('')
            f.write('|')
            f.write(str(chat[x]))
            f.write("\n")
            
    f.close()
    
    
if __name__ == "__main__":
    main(sys.argv[1],sys.argv[2])


#채팅데이터 read
chat = pd.read_csv("C:\\Users\\KYJ\\Desktop\\url\\web\\"+videoId+".txt",delim_whitespace=False , names=['txt'])
a = chat['txt'].to_numpy()

ar_time = []
ar_id = []
ar_chat = []
for i in a:
    j = i.split('|')
    ar_time.append(j[0])
    ar_id.append(j[1])
    ar_chat.append(j[2])

ar_time = pd.DataFrame(ar_time, columns = ['시간'])
ar_id = pd.DataFrame(ar_id, columns = ['시청자ID'])
ar_chat = pd.DataFrame(ar_chat, columns = ['채팅내용'])

arm = pd.merge(ar_time,  ar_id, left_index = True, right_index=True, how='left')
chat = pd.merge(arm,  ar_chat, left_index = True, right_index=True, how='left')


#노이즈 제거
chat_dot = chat.채팅내용.str.contains('[⠁⠃⠉⠙⠑⠋⠛⠓⠊⠚⠅⠇⠍⠝⠕⠏⠟⠗⠎⠞⠥⠧⠺⠭⠽⠵⠠⠁⠃⠉⠙⠑⠋⠛⠓⠊⠚]',na=False) 
chat = chat[~chat_dot]
chat = chat[chat['시청자ID'] != "Nightbot"]
chat = chat[chat['시청자ID'] != "싹둑"]


#fill missing sec
data1 = chat
id_uni = data1["시청자ID"].unique()
id_num = len(id_uni)

df_grouped = data1.groupby('시간')

df4 = data1.groupby('시간').agg({ 
                             '시청자ID':', '.join,
                             '채팅내용': ' '.join, 
                             }).reset_index()

DataFrame(df4)
df4['시간'] = pd.to_datetime(df4['시간'])
df4['시간'] = df4['시간'].dt.strftime('%H:%M:%S')

last_time = df4['시간']
tc = len(last_time)
num = tc - 1
lasttime = last_time[num]

chat_number = data1.groupby('시간')['채팅내용'].count()
df1 = DataFrame(chat_number)
df1 = df1.reset_index()
df1.rename(columns= {'채팅내용':'채팅수'}, inplace=True)

df1['시간'] = pd.to_datetime(df1['시간'])
df1 = df1.set_index('시간')
date_index = pd.date_range('00:00:00', lasttime, freq='s') 
df1 = df1.reindex(date_index, fill_value=0)

df1 = df1.reset_index()
df1.rename(columns= {'index':'시간'}, inplace=True)
df1['시간'] = df1['시간'].dt.strftime('%H:%M:%S')
df_time = df1.loc[:,['시간']]

merge_outer = pd.merge(df_time,df4, how='outer',on='시간')
fill_val1 = {'채팅내용':"",
           '시청자ID':"",
           }
merge_outer=merge_outer.fillna(fill_val1)
# print(len(merge_outer))

# chat1 = merge_outer['채팅내용'].to_numpy()

#window 생성
windowtab = merge_outer.loc[:,['시간','채팅내용']]

windowtab['value2'] = windowtab['채팅내용'].shift()
windowtab['value3'] = windowtab['value2'].shift()

windowtab['window']= windowtab.loc[2:,['채팅내용', 'value2', 'value3']].apply(lambda x : ' '.join(x.tolist()[::-1]),axis=1).reset_index(drop=True)

window_chat = windowtab.loc[:,['시간','window']]

window2 = merge_outer.loc[:,['시간','시청자ID']]

window2['value2'] = window2['시청자ID'].shift()
window2['value3'] = window2['value2'].shift()

window2['window']= window2.loc[2:,['시청자ID', 'value2', 'value3']].apply(lambda x : ' '.join(x.tolist()[::-1]),axis=1).reset_index(drop=True)
window_chat.rename(columns= {'window':'채팅내용'}, inplace=True)

window_ID = window2.loc[:,['시간','window']]
window_ID.rename(columns= {'window':'시청자ID'}, inplace=True)
window = pd.merge(window_chat, window_ID, left_index=True, right_index=True, how='left', on = '시간')
# print(len(window))


# #window 특성
# #1.채팅빈도 1-(ㄱ)윈도우 내 채팅 수 

df1['시간'] = pd.to_datetime(df1['시간'])
indexer = pd.api.indexers.FixedForwardWindowIndexer(window_size=3)
rolling_count = df1.rolling(window=indexer, min_periods=3).sum()
window2 =pd.merge(window, rolling_count, left_index=True, right_index=True, how='left')
fill_val = {'채팅내용':"",
           '시청자ID':"",
           '채팅수':0}
window3 =window2.fillna(fill_val)
# print(len(window3))

# #1-(ㄴ) 윈도우 내 채팅 참여자 수 비율
id_sub=pd.DataFrame(window3.loc[:,['시간','시청자ID']])

for i,row in id_sub.iterrows():
    if id_sub.at[i,'시청자ID'] == "  ":
        id_sub.at[i,'참여수(중복X)'] = 0
    elif id_sub.at[i,'시청자ID'] == " ":
        id_sub.at[i,'참여수(중복X)'] = 0
    elif id_sub.at[i,'시청자ID'] == "":
        id_sub.at[i,'참여수(중복X)'] = 0    
    else:
        id_sub.at[i,'참여수(중복X)'] = len(set(id_sub.at[i,'시청자ID']))

id_sub['참여비율'] = id_sub['참여수(중복X)'] / id_num
p_id=pd.DataFrame(id_sub.loc[:,['시간','참여비율']])
window_total=pd.merge(window3, p_id, left_index=True, right_index=True, how='left',on='시간')
# print(len(window_total)*2)


# # 1 - (ㄷ) 윈도우 시간 정규화
total_time = len(window3)
for i,row in window_total.iterrows():
    window_total.at[i,'시간정규화'] = (i+1)/total_time   

# print(len(window_total))


# # 2.언어적 빈도
# # 2 - 윈도우 내 (ㄱ)어절 (ㄴ)음절 (ㄷ)낱글자 수 
import re
com = re.compile('[ㄱ-ㅎㅏ-ㅣ]')

# window_total1 = window_total.dropna(axis=0)
# print(len(window_total1))

chat1 = window_total['채팅내용'].to_numpy()



s = chat1[0]
a = 0
Ar = []
for h in chat1:
    tk = nltk.word_tokenize(h)
    a = len(tk)
    Ar.append(a)

df_uh = pd.DataFrame(Ar, columns = ['어절수'])

temp = []

for i in chat1:
    a = len(re.findall("[\S]",i))
    temp.append(a)

df_um = pd.DataFrame(temp, columns = ['음절수'])

sss = chat1[0]
i = 0
aa = 0
single = []
for h in chat1:
    sss = h
    res = com.findall(sss)
    w = len(res)
    single.append(w)
df_single = pd.DataFrame(single, columns = ['낱글자수'])

window_total=pd.merge(window_total, df_uh, left_index=True, right_index=True, how='left')
window_total=pd.merge(window_total, df_um, left_index=True, right_index=True, how='left')
window_total=pd.merge(window_total, df_single, left_index=True, right_index=True, how='left')


# #2- 윈도우 내 한 채팅당 평균 (ㄹ)어절 (ㅁ)음절 (ㅂ)낱글자 수
for i,row in window_total.iterrows():
    if window_total.at[i,'채팅수'] == 0:
        window_total.at[i,'채팅당 어절수'] = 0
    else:
        window_total.at[i,'채팅당 어절수'] = window_total.at[i,'어절수'] / window_total.at[i,'채팅수']

for i,row in window_total.iterrows():
    if window_total.at[i,'채팅수'] == 0:
        window_total.at[i,'채팅당 음절수'] = 0
    else:
        window_total.at[i,'채팅당 음절수'] = window_total.at[i,'음절수'] / window_total.at[i,'채팅수']

for i,row in window_total.iterrows():
    if window_total.at[i,'채팅수'] == 0:
        window_total.at[i,'채팅당 낱글자수'] = 0
    else:
        window_total.at[i,'채팅당 낱글자수'] = window_total.at[i,'낱글자수'] / window_total.at[i,'채팅수']



#형태소 분석
import sys
from konlpy.tag import Okt
okt= Okt()
from collections import Counter
data = window_total

fill_val1 = {'채팅내용':"",
           '시청자ID':"",
           '하이라이트 여부':"X"}
data=data.fillna(fill_val1)

df1 = data["채팅내용"]
chat1 = df1.to_numpy()

arr = []
for h in chat1:
    pos_chat = okt.pos(h, join=True)
    arr.append(pos_chat)

ar = []
for s in arr:
    count = Counter(s)
    ar.append(count)

kon = pd.DataFrame(ar)
kon=kon.fillna(0)

kon_sum = pd.DataFrame(kon.sum())
kon_sum.index.name = '형태소'
kon_sum1=kon_sum.reset_index()

word = kon_sum1['형태소']

def shorthead(sentence):
    x = len(sentence)
    for i in range(1, (x // 2)+1):
        if(x % i == 0):
            s = sentence[0:i]
            count = int(x / i)
            if (s*count == sentence):
                return s + s
    return sentence

word2 = []
for i in word:
    if 'KoreanParticle' in i:
        t = i.split('/')[0]
        h = shorthead(t)
        s = h + '/KoreanParticle'
        word2.append(s)
    else:
        word2.append(i)

dfword = pd.DataFrame(word2)
dfword.rename(columns={ 0:'형태소2'}, inplace = True)

score = pd.read_csv("Scoreboard.csv",encoding='cp949')
score = score.drop('Unnamed: 0',axis=1)
s_word = pd.merge(dfword, score, how = 'left', on = '형태소2')
s_word = s_word.fillna(0)

hs = s_word['Hscore']
s1 = pd.Series(hs)
s1.index = word
total_hscore = kon.mul(hs,axis = 1)
hs_sum =total_hscore.sum(axis=1)
HS = pd.DataFrame(hs_sum)
HS.rename(columns= { 0:'Hscore'}, inplace=True)

ns = s_word['Nscore']
s2 = pd.Series(ns)
s2.index = word
total_nscore = kon.mul(ns,axis = 1)
ns_sum = total_nscore.sum(axis=1)
NS = pd.DataFrame(ns_sum)
NS.rename(columns= { 0:'Nscore'}, inplace=True)

ws = kon.sum(axis=1)
word_sum = pd.DataFrame(ws)
word_sum.rename(columns= { 0:'채팅당 형태소수'}, inplace=True)

window = pd.merge(data, word_sum, left_index=True, right_index=True, how='left' )
total = pd.merge(window,HS, left_index=True, right_index=True, how='left' )
total = pd.merge(total,NS, left_index=True, right_index=True, how='left' )

for i,row in total.iterrows():
    if total.at[i,'채팅당 형태소수'] == 0:
        total.at[i,'Hscore'] = 0
        total.at[i,'Nscore'] = 0
    else:
        total.at[i,'Hscore'] = total.at[i,'Hscore']/total.at[i,'채팅당 형태소수']
        total.at[i,'Nscore'] = total.at[i,'Nscore']/total.at[i,'채팅당 형태소수']

final_window = total.drop('채팅당 형태소수',axis=1)
# final_window = final_window.set_index('시간')

final_window1 = final_window.drop(["시간","채팅내용","시청자ID"],axis=1)
# final_window1.to_csv('랄로test.csv', encoding='cp949')

import csv
# csvfile = open('랄로test.csv', 'r')
# jsonfile = open('랄로test.json', 'w')

# fieldnames = ("시간","채팅내용","시청자ID","채팅수","참여비율","시간정규화","어절수","음절수","낱글자수","채팅당 어절수","채팅당 음절수","채팅당 낱글자수","Hscore","Nscore")
# reader = csv.DictReader( csvfile, fieldnames)
# for row in reader:
#     json.dump(row, jsonfile)
#     jsonfile.write('\n')

# csv_file = pd.DataFrame(pd.read_csv("랄로test.csv", sep = ",", header = 0, index_col = False, encoding='cp949'))
# csv_file.to_json("랄로test.json", orient = "records", date_format = "epoch", double_precision = 10, force_ascii = True, date_unit = "ms", default_handler = None)


#머신러닝


data = final_window1.astype({'채팅수':'float', '어절수':'float', '음절수':'float', '낱글자수':'float'})

def make_dataset(data, label, window_size = 1):
    feature_list = []
    label_list = []
    for i in range(len(data) - window_size):
        feature_list.append(np.array(data.iloc[i:i+window_size]))
        
    return np.array(feature_list)

feature_cols = ['채팅수','참여비율','시간정규화','어절수','음절수','낱글자수','채팅당 어절수','채팅당 음절수','채팅당 낱글자수','Hscore','Nscore']

train_feature = data[feature_cols]
train_feature = make_dataset(train_feature, 20)
paka_feature = train_feature

from keras.models import load_model
model = load_model('LSTM.h5')

pred = model.predict_classes(paka_feature)

pk = pd.DataFrame(pred)



# 최종 하이라이트 구간 

tc = len(pk)
num = tc - 1

m, s = divmod(num, 60)
h, m = divmod(m, 60)

lasttime = f'{h:d}:{m:02d}:{s:02d}'

aa = pd.to_datetime(lasttime).strftime('%H:%M:%S')

date_index = pd.date_range('00:00:00', lasttime, freq='s')
df_time = pd.DataFrame(date_index)
df_time.rename(columns= { 0:'시간'}, inplace=True)

df_m = pd.merge(df_time, pk,left_index=True, right_index=True, how='left')
df_m.rename(columns= { 0:'HL'}, inplace=True)

first = df_m.iloc[0:300]

for i,row in  first.iterrows():
    if first.at[i,'HL'] == 1:
        first.at[i,'HL'] = 0

a=len(df_m) - 300
b=len(df_m) - 1

last = df_m.loc[a:b]

for i,row in  last.iterrows():
    if last.at[i,'HL'] == 1:
        last.at[i,'HL'] = 0

df_junho = df_m.drop(df_m.index[0:300])
df_dr = df_junho.drop(df_m.index[a:b+1])
res1 = pd.concat([first,df_dr])
res = pd.concat([res1,last])

for i,row in res.iterrows():
    if res.at[i,'HL'] == 1:
        res.at[i,'start'] = res.at[i,'시간'] - timedelta(seconds = 5)
        res.at[i,'end'] = res.at[i,'시간'] + timedelta(seconds = 5)

df1= res[res['HL']==1]
df2=df1.reset_index(drop=True)

for i,row in df2.iterrows():
    df2.at[i,'START'] = df2.at[i,'start']
    df2.at[i,'END'] = df2.at[i,'end']

df_make = pd.concat([df2, last])
df_make=df_make.reset_index(drop=True)
df_make = df_make.fillna(datetime.datetime.now())
df_make

num = len(df_make) - 150

for j in range(1,100):
    for i,row in df_make.iterrows():
        if i == num:
            break        
        if df_make.at[i,'END'] >= df_make.at[i+j,'start']:
            df_make.at[i+j,'START'] = df_make.at[i,'start']
            df_make.at[i,'END'] = df_make.at[i+j,'end']

for i,row in df_make.iterrows():
    df_make.at[i,'length'] = df_make.at[i,'END'] - df_make.at[i,'START']

bf = len(df2)
af = len(df_make)
df_total = df_make.drop(df_make.index[bf:af])

df_total['START'] = df_total['START'].dt.strftime('%H:%M:%S')
df_total['END'] = df_total['END'].dt.strftime('%H:%M:%S')

total = df_total.loc[:,['START','END']]
Total = total.drop_duplicates()

Total1=Total.set_index('START')
Total1.to_csv("HightligtTime.csv", encoding='cp949')

csv_file = pd.DataFrame(pd.read_csv("HightligtTime.csv", sep = ",", header = 0, index_col = False ))
csv_file.to_json("C:\\Users\\KYJ\\Desktop\\url\\web\\src\\components\\HightligtTime.json", orient = "records", date_format = "epoch", double_precision = 10, force_ascii = True, date_unit = "ms", default_handler = None)

print("Work done!")