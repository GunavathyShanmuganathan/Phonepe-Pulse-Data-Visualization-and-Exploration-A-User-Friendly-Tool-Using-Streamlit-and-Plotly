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
st.write('<p style="color:#006400;font-size:40px;font:bold;text-align:center">Users Data Analysis </p>',unsafe_allow_html=True)
tab1, tab2, tab3, tab4 = st.tabs(["STATE ANALYSIS", "DISTRICT ANALYSIS","YEAR ANALYSIS","OVERALL ANALYSIS"])

# =================================================U STATE ANALYSIS ========================================================
with tab1:
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
        'uttarakhand', 'west-bengal'),key='W')
    app_opening=Aggregated_User_Summary_df.groupby(['State','Year'])
    a_state=app_opening.sum()
    la=Aggregated_User_Summary_df['State'] +"-"+ Aggregated_User_Summary_df["Year"].astype(str)
    a_state["state_year"] = la.unique()
    sta=a_state["state_year"].str[:-5]
    a_state["state"] = sta
    sout=a_state.loc[(a_state['state'] == state) ]
    ta=sout['AppOpenings'].sum()
    tr=sout['Registered_Users'].sum()
    sout['AppOpenings']=sout['AppOpenings'].mul(100/ta)
    sout['Registered_Users']=sout['Registered_Users'].mul(100/tr).copy()
    fig = go.Figure(data=[
        go.Bar(name='AppOpenings %', y=sout['AppOpenings'], x=sout['state_year'], marker={'color': 'Gold'}),
        go.Bar(name='Registered Users %', y=sout['Registered_Users'], x=sout['state_year'],marker={'color': 'OrangeRed'})
    ])
    # Change the bar mode
    fig.update_layout(barmode='group')
    st.write("#### ",state.upper())
    st.plotly_chart(fig, use_container_width=True, height=200)
    st.info(
        """
        Details of BarGraph:
        - The X Axis shows both Registered users and App openings 
        - The Y Axis shows the Percentage of Registered users and App openings
        - User can observe the increasing rate of App openings and Registered users in state
        """
        
        
    
        )
# ==================================================U DISTRICT ANALYSIS ====================================================
with tab2:
    col1, col2, col3= st.columns(3)
    with col1:
        Year = st.selectbox(
            'Please select the Year',
            ('2022', '2021','2020','2019','2018'),key='y12')
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
        'uttarakhand', 'west-bengal'),key='dk2')
    with col3:
        Quarter = st.selectbox(
            'Please select the Quarter',
            ('1', '2', '3','4'),key='qwe2')
    districts=Map_User_Table.loc[(Map_User_Table['State'] == state ) & (Map_User_Table['Year']==int(Year))
                                          & (Map_User_Table['Quarter']==int(Quarter))]
    l=len(districts)    
    fig = px.bar(districts, x='Place_Name', y='App_Openings',color="App_Openings",
                 color_continuous_scale="deep")   

    if l:
            st.write('#### '+state.upper()+' WITH '+str(l)+' DISTRICTS')
            st.plotly_chart(fig,use_container_width=True)
    else:
            st.write('#### NO DISTRICTS DATA AVAILABLE FOR '+state.upper())

    
    if l:
            st.info(
        """
        Details of BarGraph:
        - X Axis represents the districts of selected state
        - Y Axis represents App Openings   
        -From this we can observe the leading districts of App opening.   
        """
            )
        
# ==================================================U YEAR ANALYSIS ========================================================
with tab3:
    st.write(st.write('<p style="color:#006400;font-size:40px;font:bold;text-align:center">Brand Shares </p>',unsafe_allow_html=True))
    col1, col2= st.columns(2)
    with col1:
        state = st.selectbox(
        'Please select the State',
        ('india','andaman-&-nicobar-islands', 'andhra-pradesh', 'arunachal-pradesh',
        'assam', 'bihar', 'chandigarh', 'chhattisgarh',
        'dadra-&-nagar-haveli-&-daman-&-diu', 'delhi', 'goa', 'gujarat',
        'haryana', 'himachal-pradesh', 'jammu-&-kashmir',
        'jharkhand', 'karnataka', 'kerala', 'ladakh', 'lakshadweep',
        'madhya-pradesh', 'maharashtra', 'manipur', 'meghalaya', 'mizoram',
        'nagaland', 'odisha', 'puducherry', 'punjab', 'rajasthan',
        'sikkim', 'tamil-nadu', 'telangana', 'tripura', 'uttar-pradesh',
        'uttarakhand', 'west-bengal'),key='Z')
    with col2:
        Y = st.selectbox(
        'Please select the Year',
        ('2018', '2019', '2020','2021','2022'),key='X')
    y=int(Y)
    s=state
    brand=Aggregated_User_df[Aggregated_User_df['Year']==y] 
    brand=Aggregated_User_df.loc[(Aggregated_User_df['Year'] == y) & (Aggregated_User_df['State'] ==s)]
    myb= brand['Brand_Name'].unique()
    x = sorted(myb).copy()
    b=brand.groupby('Brand_Name').sum()
    b['brand']=x
    br=b['Registered_Users_Count'].sum()
    labels = b['brand']
    values = b['Registered_Users_Count'] # customdata=labels,
    fig3 = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.4,textinfo='label+percent',texttemplate='%{label}<br>%{percent:1%f}',insidetextorientation='horizontal',textfont=dict(color='#000000'),marker_colors=px.colors.qualitative.Dark24)])
    st.write("#### ",state.upper()+' IN '+Y)
    st.plotly_chart(fig3, use_container_width=True)        
    st.info(
        """
        Details of Map:        
        - Initially we select data by means of State and Year
        - Percentage of registered users is represented with dounut chat through Device Brand
         - User can observe the top leading brands and brands with less users in a particular state

        """
        )
    b = b.sort_values(by=['Registered_Users_Count'])
    fig4= px.bar(b, x='brand', y='Registered_Users_Count',color="Registered_Users_Count",
                title='In '+state+'in '+str(y),
                color_continuous_scale="rainbow",)
    with st.expander("See Bar graph for the same data"):
        st.plotly_chart(fig4,use_container_width=True)
    with tab4:
        years=Aggregated_User_Summary_df.groupby('Year')
        years_List=Aggregated_User_Summary_df['Year'].unique()
        years_Table=years.sum()
        del years_Table['Quarter']
        years_Table['year']=years_List
        total_trans=years_Table['Registered_Users'].sum() # this data is used in sidebar    
        fig1 = px.pie(years_Table, values='Registered_Users', names='year',color_discrete_sequence=px.colors.sequential.Jet, title='TOTAL REGISTERED USERS (2018 TO 2022)')

        labels = ["US", "China", "European Union", "Russian Federation", "Brazil", "India",
                "Rest of World"]

        # Create subplots: use 'domain' type for Pie subplot
        fig = make_subplots(rows=1, cols=2, specs=[[{'type':'domain'}, {'type':'domain'}]])
        fig.add_trace(go.Pie(labels=years_Table['year'], values=years_Table['Registered_Users'], name="REGISTERED USERS"),
                        1, 1)
        fig.add_trace(go.Pie(labels=years_Table['year'], values=years_Table['AppOpenings'], name="APP OPENINGS"),
                        1, 2)

        # Use `hole` to create a donut-like pie chart
        fig.update_traces(hole=.6, hoverinfo="label+percent+name")

        fig.update_layout(
        title_text="USERS DATA (2018 TO 2022)",
        # Add annotations in the center of the donut pies.
        annotations=[dict(text='USERS', x=0.18, y=0.5, font_size=20, showarrow=False),
                            dict(text='APP', x=0.82, y=0.5, font_size=20, showarrow=False)])
        # st.plotly_chart(fig1)
        st.plotly_chart(fig)
          
        # st.write('#### :green[Year Wise Transaction Analysis in INDIA]')      
        st.markdown(years_Table.style.hide(axis="index").to_html(), unsafe_allow_html=True)
        st.info(
            """
            Important Observation:
            -  We can see that the Registered Users and App openings are increasing year by year
            
            """
            )
