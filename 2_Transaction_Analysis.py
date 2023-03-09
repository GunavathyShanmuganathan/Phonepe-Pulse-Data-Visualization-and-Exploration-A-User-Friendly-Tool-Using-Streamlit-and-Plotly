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
st.write('<p style="color:#DC143C;font-size:40px;font:bold;text-align:center">Transaction Analysis</div>',unsafe_allow_html=True)
c1,c2=st.columns(2)
with c1:
    Year = st.selectbox(
            'Please select the Year',
            ('2018', '2019', '2020','2021','2022'))
with c2:
    Quarter = st.selectbox(
            'Please select the Quarter',
            ('1', '2', '3','4'))
year=int(Year)
quarter=int(Quarter)
Transaction_districts=Map_Transaction_df.loc[(Map_Transaction_df['Year'] == year ) & (Map_Transaction_df['Quarter']==quarter) ].copy()
Transaction_Coropleth_States=Transaction_districts[Transaction_districts["State"] == "india"]
Transaction_districts.drop(Transaction_districts.index[(Transaction_districts["State"] == "india")],axis=0,inplace=True)
Aggregated_Transaction=Aggregated_Transaction_df.copy()
Aggregated_Transaction.drop(Aggregated_Transaction.index[(Aggregated_Transaction["State"] == "india")],axis=0,inplace=True)
State_PaymentMode=Aggregated_Transaction.copy() 
      
col1, col2= st.columns(2)
with col1:
        mode = st.selectbox(
            'Please select the Mode',
            ('Recharge & bill payments', 'Peer-to-peer payments', 'Merchant payments', 'Financial Services','Others'),key='a')
with col2:
        state = st.selectbox(
        'Please select the State',
        ('andaman-&-nicobar-islands', 'andhra-pradesh', 'arunachal-pradesh',
        'assam', 'bihar', 'chandigarh', 'chhattisgarh',
        'dadra-&-nagar-haveli-&-daman-&-diu', 'delhi', 'goa', 'gujarat',
        'haryana', 'himachal-pradesh', 'jammu-&-kashmir',
        'jharkhand', 'karnataka', 'kerala', 'ladakh', 'lakshadweep',
        'madhya-pradesh', 'maharashtra', 'manipur', 'meghalaya', 'mizoram',
        'nagaland', 'odisha', 'puducherry', 'punjab', 'rajasthan',
        'sikkim', 'tamil-nadu', 'telangana', 'tripura', 'uttar-pradesh',
        'uttarakhand', 'west-bengal'),key='b')
st.write('<p style="color:#DC143C;font-size:40px;font:bold;text-align:center">Statewise Analysis</div>',unsafe_allow_html=True)
State= state
Year_List=[2018,2019,2020,2021,2022]
Mode=mode
State_PaymentMode=State_PaymentMode.loc[(State_PaymentMode['State'] == State ) & (State_PaymentMode['Year'].isin(Year_List)) & 
                            (State_PaymentMode['Payment_Mode']==Mode )]
State_PaymentMode = State_PaymentMode.sort_values(by=['Year'])
State_PaymentMode["Quarter"] = "Q"+State_PaymentMode['Quarter'].astype(str)
State_PaymentMode["Year_Quarter"] = State_PaymentMode['Year'].astype(str) +"-"+ State_PaymentMode["Quarter"].astype(str)
fig = px.bar(State_PaymentMode, x='Year_Quarter', y='Total_Transactions_count',color="Total_Transactions_count",
                 color_continuous_scale="jet_r")
with st.expander("Show Bar graph representation "):

  st.write('#### '+State.upper()) 
  st.plotly_chart(fig,use_container_width=True)

  st.info(
        """
        Details of BarGraph:
        - State Transaction details
        - X Axis represents years and quarters 
        - Y Axis represents total transactions in selected mode 
        """
        )
st.write('<p style="color:#DC143C;font-size:40px;font:bold;text-align:center">Districtwise Analysis</div>',unsafe_allow_html=True)
col1, col2, col3= st.columns(3)
with col1:
        Year = st.selectbox(
            'Please select the Year',
            ('2018', '2019', '2020','2021','2022'),key='y1')
with col2:
        state = st.selectbox(
        'Please select the State',
        ('andaman-&-nicobar-islands', 'andhra-pradesh', 'arunachal-pradesh',
        'assam', 'bihar', 'chandigarh', 'chhattisgarh',
        'dadra-&-nagar-haveli-&-daman-&-diu', 'delhi', 'goa', 'gujarat',
        'haryana', 'himachal-pradesh', 'jammu-&-kashmir',
        'jharkhand', 'karnataka', 'kerala', 'ladakh', 'lakshadweep',
        'madhya-pradesh', 'maharashtra', 'manipur', 'meghalaya', 'mizoram',
        'nagaland', 'odisha', 'puducherry', 'punjab', 'rajasthan',
        'sikkim', 'tamil-nadu', 'telangana', 'tripura', 'uttar-pradesh',
        'uttarakhand', 'west-bengal'),key='dk')
with col3:
        Quarter = st.selectbox(
            'Please select the Quarter',
            ('1', '2', '3','4'),key='qwe')
districts=Map_Transaction_df.loc[(Map_Transaction_df['State'] == state ) & (Map_Transaction_df['Year']==int(Year))
                                          & (Map_Transaction_df['Quarter']==int(Quarter))]
l=len(districts)    
fig = px.bar(districts, x='Place_Name', y='Total_Transactions_count',color="Total_Transactions_count",
                 color_continuous_scale="Viridis")   
with st.expander("Show Bar graph representation "):
   st.write('#### '+state.upper()+' WITH '+str(l)+' DISTRICTS')
   st.plotly_chart(fig,use_container_width=True)

   st.info(
        """
        Details of BarGraph:
        - X Axis represents the districts of selected state
        - Y Axis represents total transactions        
        """
        )
st.write('<p style="color:#DC143C;font-size:40px;font:bold;text-align:center">PaymentMode and Year</p>',unsafe_allow_html=True)
col1, col2= st.columns(2)
with col1:
        M = st.selectbox(
            'Please select the Mode',
            ('Recharge & bill payments', 'Peer-to-peer payments', 'Merchant payments', 'Financial Services','Others'),key='D')
with col2:
        Y = st.selectbox(
        'Please select the Year',
        ('2018', '2019', '2020','2021','2022'),key='F')
Year_PaymentMode=Aggregated_Transaction.copy()
Year=int(Y)
Mode=M
Year_PaymentMode=Year_PaymentMode.loc[(Year_PaymentMode['Year']==Year) & 
                            (Year_PaymentMode['Payment_Mode']==Mode )]
States_List=Year_PaymentMode['State'].unique()
State_groupby_YP=Year_PaymentMode.groupby('State')
Year_PaymentMode_Table=State_groupby_YP.sum()
Year_PaymentMode_Table['states']=States_List
del Year_PaymentMode_Table['Quarter'] 
del Year_PaymentMode_Table['Year']
Year_PaymentMode_Table = Year_PaymentMode_Table.sort_values(by=['Total_Transactions_count'])
fig2= px.bar(Year_PaymentMode_Table, x='states', y='Total_Transactions_count',color="Total_Transactions_count",
                color_continuous_scale="Viridis",)   
with st.expander("Show Bar graph representation "):
   st.write('#### '+str(Year)+' DATA ANALYSIS')
   st.plotly_chart(fig2,use_container_width=True) 
   st.info(
        """
        Details of BarGraph:
        - X Axis represents the states in increasing order based on Total transactions
        - Y Axis represents total transactions        
        """
        )    
years=Aggregated_Transaction.groupby('Year')
years_List=Aggregated_Transaction['Year'].unique()
years_Table=years.sum()
del years_Table['Quarter']
years_Table['year']=years_List
total_trans=years_Table['Total_Transactions_count'].sum() # this data is used in sidebar 
st.write( '<p style="color:#DC143C;font-size:40px;font:bold;text-align:center">Increase in Transaction</p>',unsafe_allow_html=True)   
fig1 = px.pie(years_Table, values='Total_Transactions_count', names='year',color_discrete_sequence=px.colors.sequential.Viridis, title='TOTAL TRANSACTIONS (2018 TO 2022)')
with st.expander("Show Pie graph representation "):
       st.plotly_chart(fig1)  
st.write('<p style="color:#DC143C;font-size:40px;font:bold;text-align:center">Year Wise Transaction Analysis in India</p>',unsafe_allow_html=True)      
with st.expander("Show the Table"):
      st.markdown(years_Table.style.hide(axis="index").to_html(), unsafe_allow_html=True)
     
