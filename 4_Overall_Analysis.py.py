import pandas as pd 
import plotly.express as px
import streamlit as st 
import mysql.connector as sql
import plotly.graph_objects as go
from plotly.subplots import make_subplots
conn=sql.connect(
    host="localhost",
    user="root",
    password="1234"
)
mycursor=conn.cursor()
sql='''USE phonepe'''
mycursor.execute(sql)

query = 'select * from lls'
Indian_States = pd.read_sql(query, con = conn)

Aggregated_Transaction_df= pd.read_csv(r'C:/Users/User/datasets/PhonePe-Pulse-Data-2018-2022-Analysis/data/DAT.csv')
Aggregated_User_Summary_df= pd.read_csv(r'C:/Users/User/datasets/PhonePe-Pulse-Data-2018-2022-Analysis/data/DAUS.csv')
Aggregated_User_df= pd.read_csv(r'C:/Users/User/datasets/PhonePe-Pulse-Data-2018-2022-Analysis/data/DAS.csv')
Geo_Dataset =  pd.read_csv(r'C:/Users/User/datasets/PhonePe-Pulse-Data-2018-2022-Analysis/data/DMD.csv')
Coropleth_Dataset =  pd.read_csv(r'C:/Users/User/datasets/PhonePe-Pulse-Data-2018-2022-Analysis/data/DMI.csv')
Map_Transaction_df = pd.read_csv(r'C:/Users/User/datasets/PhonePe-Pulse-Data-2018-2022-Analysis/data/DMT.csv')
Map_User_Table= pd.read_csv(r'C:/Users/User/datasets/PhonePe-Pulse-Data-2018-2022-Analysis/data/DMU.csv')
#Indian_States= pd.read_csv(r'data/Longitude_Latitude_State_Table.csv')
st.write('<p style="color:#5F9EA0;font-size:40px;text-align:center;font:bold">TOP 10 STATES DATA</div>',unsafe_allow_html=True)
c1,c2=st.columns(2)
with c1:
    Year = st.selectbox(
            'Please select the Year',
            ('2022', '2021','2020','2019','2018'),key='y1h2k')
    st.markdown(
    """
<style>
div[role="listbox"] Year{
    background-color:#20B2AA;
}
div[role="listbox"] 2018{
    background-color:MediumAquamarine;
}

</style>
""",
    unsafe_allow_html=True,
)
with c2:
    Quarter = st.selectbox(
            'Please select the Quarter',
            ('1', '2', '3','4'),key='qgwe2')
Map_User_df=Aggregated_User_Summary_df.copy() 
top_states=Map_User_df.loc[(Map_User_df['Year'] == int(Year)) & (Map_User_df['Quarter'] ==int(Quarter))]
top_states_r = top_states.sort_values(by=['Registered_Users'], ascending=False)
top_states_a = top_states.sort_values(by=['AppOpenings'], ascending=False) 


top_states_T=Aggregated_Transaction_df.loc[(Aggregated_Transaction_df['Year'] == int(Year)) & (Aggregated_Transaction_df['Quarter'] ==int(Quarter))]
topst=top_states_T.groupby('State')
x=topst.sum().sort_values(by=['Total_Transactions_count'], ascending=False)
y=topst.sum().sort_values(by=['Total_Amount'], ascending=False)


rt=top_states_r[1:11]
st.markdown('<p style="color:#20B2AA;font-size:24px;">Registered Users</p>',unsafe_allow_html=True)
st.markdown(rt[[ 'State','Registered_Users']].style.hide(axis="index").to_html(), unsafe_allow_html=True)


at=top_states_a[1:11]
st.markdown('<p style="color:#20B2AA;font-size:24px;">PhonePeApp Openings</p>', unsafe_allow_html=True)
st.markdown(at[['State','AppOpenings']].style.hide(axis="index").to_html(), unsafe_allow_html=True)
st.markdown('<p style="color:#20B2AA;font-size:24px;">Total Transactions</p>',unsafe_allow_html=True)
st.write(x[['Total_Transactions_count']][1:11])
st.markdown('<p style="color:#20B2AA;font-size:24px;">Total Amount</p>',unsafe_allow_html=True)
st.write(y['Total_Amount'][1:11])      
        