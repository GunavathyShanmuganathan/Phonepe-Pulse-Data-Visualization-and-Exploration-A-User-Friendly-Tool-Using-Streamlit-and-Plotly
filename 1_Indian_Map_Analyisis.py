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

st.write('<p style="color:#191970;font-size:40px;font:bold;text-align:center">India Map Analysis</div>',unsafe_allow_html=True)
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
# Dynamic Scattergeo Data Generation
Transaction_districts = Transaction_districts.sort_values(by=['Place_Name'], ascending=False)
Geo_Dataset = Geo_Dataset.sort_values(by=['District'], ascending=False) 
Total_Amount=[]
for i in Transaction_districts['Total_Amount']:
    Total_Amount.append(i)
Geo_Dataset['Total_Amount']=Total_Amount
Total_Transaction=[]
for i in Transaction_districts['Total_Transactions_count']:
    Total_Transaction.append(i)
Geo_Dataset['Total_Transactions']=Total_Transaction
Geo_Dataset['Year_Quarter']=str(year)+'-Q'+str(quarter)
Coropleth_Dataset = Coropleth_Dataset.sort_values(by=['state'], ascending=False)
Transaction_Coropleth_States = Transaction_Coropleth_States.sort_values(by=['Place_Name'], ascending=False)
Total_Amount=[]
for i in Transaction_Coropleth_States['Total_Amount']:
    Total_Amount.append(i)
Coropleth_Dataset['Total_Amount']=Total_Amount
Total_Transaction=[]
for i in Transaction_Coropleth_States['Total_Transactions_count']:
    Total_Transaction.append(i)
Coropleth_Dataset['Total_Transactions']=Total_Transaction
# -------------------------------------FIGURE1 INDIA MAP------------------------------------------------------------------ 
Indian_States = Indian_States.sort_values(by=['state'], ascending=False)
Indian_States['Registered_Users']=Coropleth_Dataset['Registered_Users']
Indian_States['Total_Amount']=Coropleth_Dataset['Total_Amount']
Indian_States['Total_Transactions']=Coropleth_Dataset['Total_Transactions']
Indian_States['Year_Quarter']=str(year)+'-Q'+str(quarter)
fig=px.scatter_geo(Indian_States,
                    lon=Indian_States['Longitude'],
                    lat=Indian_States['Latitude'],                                
                    text = Indian_States['code'], #It will display district names on map
                    hover_name="state", 
                    hover_data=['Total_Amount',"Total_Transactions","Year_Quarter"],
                    )
fig.update_traces(marker=dict(color="white" ,size=0.4))
fig.update_geos(fitbounds="locations", visible=False)
    # scatter plotting districts
Geo_Dataset['col']=Geo_Dataset['Total_Transactions']
fig1=px.scatter_geo(Geo_Dataset,
                    lon=Geo_Dataset['Longitude'],
                    lat=Geo_Dataset['Latitude'],
                    color=Geo_Dataset['col'],
                    size=Geo_Dataset['Total_Transactions'],     
                    #text = Scatter_Geo_Dataset['District'], #It will display district names on map
                    hover_name="District", 
                    hover_data=["State", "Total_Amount","Total_Transactions","Year_Quarter"],
                    title='District',
                    size_max=15)
fig1.update_layout(margin={"t": 30, "b": 0, "l": 0, "r": 0}, width=1200, height=3600)
fig1.update_traces(marker=dict(symbol="triangle-up".color="#000000" ,line_width=1))   
#coropleth mapping india
fig_ch = px.choropleth(
                    Coropleth_Dataset,
                    geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                    featureidkey='properties.ST_NM',                
                    locations='state',
                    color="Total_Transactions",color_continuous_scale="turbo"                                       
                    )
fig_ch.update_geos(fitbounds="locations", visible=False)
#combining districts states and coropleth
fig_ch.add_trace( fig.data[0])
fig_ch.add_trace(fig1.data[0])
st.plotly_chart(fig_ch, use_container_width=True)
st.info(
    """
    Important Observations:
    - User can observe the Transactions of PhonePe in both State and Districtwide for the given year and quarter.
    - Colors represent the State wide Transaction.
    - Cicles Represents the District wide transaction
    - Hover data will show the details like Total transactions, Total amount
    """
    )
# -----------------------------------------------FIGURE2 HIDDEN SCATTER GRAPH------------------------------------------------------------------------
Coropleth_Dataset = Coropleth_Dataset.sort_values(by=['Total_Transactions'])
fig = px.scatter(Coropleth_Dataset, x='state', y='Total_Transactions',title=str(year)+" Quarter-"+str(quarter),color="state")
with st.expander(" Scatter graph representation "):
    st.plotly_chart(fig, use_container_width=True)
    st.write('<p style="color:#191970;">The above graph shows the higher transaction of States using Phonepe</p>',unsafe_allow_html=True)
