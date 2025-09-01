import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from io import StringIO

# Set page config
st.set_page_config(
    page_title="Sustainable Supplier Selection",
    page_icon="🌱",
    layout="wide"
)

# Load default data
@st.cache_data
def load_default_data():
    data = """supplier_id,name,carbon_footprint,recycling_rate,energy_efficiency,water_usage,waste_production,ISO_14001,Fair_Trade,Organic,B_Corp,Rainforest_Alliance,location,industry,lead_time_days,onboarding_cost_usd,switching_cost_usd
1,Supplier 1,714.1166769233291,29.57677421693583,75.16623547101494,251.4031719548862,390.9132356645378,0,0,0,0,0,Asia,Food,23.6,23269,12387
2,Supplier 2,148.4389169220004,39.31718786821429,69.29628140084088,3556.8194827979046,122.4677443100453,1,0,0,0,0,Africa,Food,5.9,25541,12181
3,Supplier 3,298.3238854953502,20.23858319699837,88.63688397017094,6627.169186980986,216.6788549204162,0,0,1,0,0,Africa,Electronics,44.7,57849,47465
4,Supplier 4,265.9346296288027,48.58008108618643,57.23741189880475,2725.639708714191,234.48690213737729,1,0,0,0,1,North America,Textiles,37.6,33733,17716
5,Supplier 5,258.3153109765273,63.19048130277249,66.21591647263133,6554.986500565352,161.74613614825734,0,0,0,1,0,North America,Chemicals,16.9,42903,28571
6,Supplier 6,830.8850559901963,52.04740784622126,78.82294715746612,9282.053946572889,96.73534230988996,0,0,1,1,1,Africa,Manufacturing,31.9,56393,37869
7,Supplier 7,931.0104982243508,82.63267604814271,91.8985707325292,4714.773709985899,141.33508581450604,1,0,0,1,1,South America,Electronics,40.9,69042,46754
8,Supplier 8,348.9169580173956,66.23684385576423,61.78104599406949,2150.3846505887764,427.6536467978239,0,1,0,1,1,Africa,Textiles,31.5,34836,19801
9,Supplier 9,837.7791054337018,39.95629340084561,80.96442861118311,9234.8710219338,497.0954146097067,1,0,1,1,1,North America,Electronics,43.9,80192,59400
10,Supplier 10,900.9034238000672,80.82665834885623,56.70736935599132,9463.980448331726,191.63038022845015,1,1,1,1,0,Europe,Food,21.5,36257,18017
11,Supplier 11,561.6734097065787,57.4615062727263,83.30697380394844,1435.565973797956,236.2579452941466,1,0,0,1,1,Africa,Electronics,49.6,72019,50878
12,Supplier 12,320.4681409619168,76.91077407529008,63.19315773594768,9006.421484304012,174.1443912947202,0,1,0,0,1,Africa,Chemicals,18.0,47285,29009
13,Supplier 13,841.8174364876702,62.45668147450391,60.96852970566833,2992.2767517002662,189.06496544999757,0,0,0,0,0,South America,Food,27.8,24204,12643
14,Supplier 14,292.38666703758594,52.80802711679443,60.34196470302127,1368.936887880434,346.71501229266994,0,0,0,1,0,Europe,Chemicals,26.4,40626,26535
15,Supplier 15,767.3203470112387,49.71158333130676,66.67930243254042,1268.9592333091648,370.30989388002325,0,1,1,1,0,South America,Electronics,38.9,70979,50001
16,Supplier 16,666.9461841307127,21.667646593990916,64.78497893665164,7618.555763143286,165.34841876203237,0,0,0,0,0,North America,Food,27.4,23300,12817
17,Supplier 17,934.6665326726504,55.2013091125972,77.56887523181679,975.580892746518,81.05984209372605,0,1,0,1,1,South America,Chemicals,24.6,48380,31783
18,Supplier 18,308.717369745777,66.76688016185793,74.51219300862363,7655.202261702742,356.6877412840242,1,1,0,0,0,Asia,Textiles,26.8,34266,17521
19,Supplier 19,819.2126157580745,90.95850657580564,83.73393972009089,2472.223684463265,225.30158870928847,1,1,1,0,1,Africa,Textiles,17.7,39849,21397
20,Supplier 20,566.3485331674428,52.64945601241151,63.27294284417181,4245.959520236914,458.98468503206175,0,0,1,1,1,Africa,Chemicals,37.0,51613,31836
21,Supplier 21,308.4000623353608,56.42310523099979,93.22491777687635,1515.8752865296751,210.5737134707338,1,0,0,0,1,Asia,Chemicals,15.4,44012,32651
22,Supplier 22,249.3135939166701,58.93363579846216,74.45672413700476,6561.430991512163,23.58035342353998,0,0,0,1,0,North America,Electronics,31.0,60520,43094
23,Supplier 23,548.0100716480144,50.64432349940869,80.57408667842829,4632.080675857905,365.80793351432186,0,0,0,0,0,Africa,Textiles,18.0,27898,16830
24,Supplier 24,624.4521765537879,63.40967891384354,80.97166618217085,3998.918498243481,493.033126237438,1,1,1,1,0,South America,Chemicals,24.9,56849,36253
25,Supplier 25,265.90418868563177,25.2763004956794,56.85340067372008,8066.264061430327,238.51729516545035,0,1,0,0,0,Europe,Manufacturing,22.6,47119,34624
26,Supplier 26,113.405425084209,56.62878734024179,56.52610031981015,4644.249593096447,476.7982005220777,1,0,0,0,1,North America,Chemicals,36.2,46899,30288
27,Supplier 27,524.0199060014147,65.76086212262993,70.7919719922401,6946.526539422575,89.66895710211355,0,0,1,0,0,Europe,Food,15.6,26406,13194
28,Supplier 28,755.4189953649355,75.79093304897424,73.48700900364693,7841.691863223069,114.30124714336708,0,1,0,0,1,South America,Chemicals,21.6,45527,29940
29,Supplier 29,926.7404425961888,52.2372740325685,62.24201389225348,6187.324456591461,177.3409004717472,1,1,1,1,0,Europe,Electronics,47.4,78828,55119
30,Supplier 30,662.9806051619177,42.71015995417882,58.10544261248254,9617.76985822728,208.9135576621187,0,0,1,0,1,North America,Textiles,26.2,33120,18271
31,Supplier 31,925.410315292842,20.44175249881023,72.67644892365037,5553.692669474443,450.734512300703,1,1,1,0,0,Europe,Food,18.4,32656,16236
32,Supplier 32,878.2212259843974,76.73592276094679,79.68372567839128,2268.224019982993,486.5297872793633,0,0,0,0,0,Africa,Textiles,42.6,26688,14143
33,Supplier 33,296.3285859249892,25.81819776489323,60.29395040400203,5464.610445043458,260.00399249184954,0,0,1,1,1,Europe,Electronics,34.8,74463,48176
34,Supplier 34,879.5146876644186,56.74910282441853,59.82882038886803,2521.1141102487613,351.4046959037132,0,1,1,0,0,Africa,Textiles,31.2,31230,17349
35,Supplier 35,757.6767427341284,42.82708225868422,92.97045765333569,924.9374703843562,317.53329755001096,0,0,0,0,0,Asia,Electronics,37.5,52317,43281
36,Supplier 36,350.078761269035,83.06166216322707,82.62018203739076,7587.984708260179,431.6610496474103,0,0,0,1,0,Africa,Chemicals,27.3,44396,28780
37,Supplier 37,817.3391978651181,91.2856896687563,51.54515817163916,2718.5257301610304,62.81294885633013,0,0,0,0,1,Africa,Food,38.0,26840,13150
38,Supplier 38,878.6995415593628,43.91559340507873,94.17276653862346,3205.040326715688,285.22066611502163,0,1,0,0,1,Africa,Chemicals,14.3,44542,32188
39,Supplier 39,369.4941060737115,87.3326216694693,50.382327483134986,9884.594295356706,406.0814093483304,1,1,1,1,1,North America,Food,23.0,41318,18001
40,Supplier 40,574.3378756272673,45.31467879577566,61.92328467430809,4065.5225327923354,389.3712873175893,1,1,1,1,1,Europe,Chemicals,27.4,63365,38832
41,Supplier 41,164.33812596105722,80.90840828851823,91.27958681905712,4468.989748684143,386.0563568919587,0,0,0,1,0,Africa,Food,14.5,26921,13795
42,Supplier 42,624.9145691359522,79.91326985443355,53.617447237541136,9213.927426384133,490.7880170413485,1,1,0,1,1,Asia,Manufacturing,47.7,66673,42187
43,Supplier 43,314.1157596666558,69.14638827583093,88.46220668991475,7921.657144977087,23.868869772681727,1,1,0,1,0,South America,Textiles,43.3,36459,19589
44,Supplier 44,788.4672814932836,37.1527591081704,56.51048288171135,8608.872667801174,61.987891372188976,1,0,1,1,1,Europe,Manufacturing,30.7,65900,41299
45,Supplier 45,256.2684725578623,30.32558485567013,58.06584849781253,4736.731467934748,85.13132272613105,1,0,0,1,1,South America,Electronics,41.8,70109,50169
46,Supplier 46,381.46803062569023,51.82783541952585,85.3103062984651,2203.785379907467,294.6320887741575,0,0,0,1,0,Asia,Food,15.1,23853,13419
47,Supplier 47,113.02702911106029,31.365406476448012,90.29408254754424,749.8242833590889,221.11026857832988,0,0,0,1,0,Africa,Manufacturing,42.0,47197,34061
48,Supplier 48,129.29672944593042,85.49547115910387,70.73304467325339,890.1587888538393,41.423410856838544,1,0,1,1,0,Europe,Chemicals,28.1,49443,32983
49,Supplier 49,547.0316576158065,33.43450681158511,51.73176569909992,1456.1965749246167,146.7997303223048,0,0,1,0,1,North America,Food,18.2,28692,13830
50,Supplier 50,521.4812809839186,22.27209962092454,64.18873670956421,2766.554349275768,201.4725246292858,0,0,1,1,0,Africa,Chemicals,31.5,44779,28092"""
    return pd.read_csv(StringIO(data))

# Load data function
@st.cache_data
def load_data(file_path=None):
    if file_path is not None:
        try:
            return pd.read_csv(file_path)
        except:
            st.error("Error loading the uploaded file. Using default dataset.")
            return load_default_data()
    else:
        return load_default_data()

# Scoring function
def calculate_sustainability_score(row):
    try:
        carbon_score = max(0, 100 - (row['carbon_footprint'] / 10))
        recycling_score = row['recycling_rate']
        energy_score = row['energy_efficiency']
        water_score = max(0, 100 - (row['water_usage'] / 100))
        waste_score = max(0, 100 - (row['waste_production'] / 5))
        certifications = sum([
            row.get('ISO_14001', 0),
            row.get('Fair_Trade', 0),
            row.get('Organic', 0),
            row.get('B_Corp', 0),
            row.get('Rainforest_Alliance', 0)
        ]) * 5
        return (carbon_score + recycling_score + energy_score +
                water_score + waste_score + certifications) / 6
    except Exception:
        return 0

# Normalize function for ranking
def normalize_column(column, ascending=True):
    if ascending:
        return (column - column.min()) / (column.max() - column.min())
    else:
        return 1 - ((column - column.min()) / (column.max() - column.min()))

# Calculate weighted score for buyer requirements
def calculate_weighted_score(row, weights):
    try:
        # Normalize all metrics to 0-1 scale (higher is better)
        sustainability_norm = row['sustainability_score'] / 100
        lead_time_norm = 1 - normalize_column(pd.Series([row['lead_time_days']]), ascending=True).iloc[0]
        onboarding_cost_norm = 1 - normalize_column(pd.Series([row['onboarding_cost_usd']]), ascending=True).iloc[0]
        switching_cost_norm = 1 - normalize_column(pd.Series([row['switching_cost_usd']]), ascending=True).iloc[0]
        
        # Calculate weighted score
        weighted_score = (
            weights['sustainability'] * sustainability_norm +
            weights['lead_time'] * lead_time_norm +
            weights['onboarding_cost'] * onboarding_cost_norm +
            weights['switching_cost'] * switching_cost_norm
        )
        
        return weighted_score
    except Exception:
        return 0

# Main app
def main():
    st.title("🌱 Sustainable Supplier Selection Tool")
    st.markdown("An AI-powered tool for evaluating and comparing suppliers based on sustainability metrics.")

    # File upload
    uploaded_file = st.sidebar.file_uploader("Upload your supplier data (CSV)", type="csv")
    
    if uploaded_file is not None:
        df = load_data(uploaded_file)
    else:
        df = load_data()
    
    # Clean column names
    df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')
    
    # Rename back to expected
    df.rename(columns={
        'supplier_id': 'supplier_id',
        'supplier_name': 'name'
    }, inplace=True, errors='ignore')
    
    # Fill missing certifications with 0
    for col in ['iso_14001', 'fair_trade', 'organic', 'b_corp', 'rainforest_alliance']:
        if col not in df.columns:
            df[col] = 0
    
    # Calculate sustainability score
    df['sustainability_score'] = df.apply(calculate_sustainability_score, axis=1)
    
    # Sidebar filters
    st.sidebar.header("Filters")
    
    # Industry filter
    industry_filter = st.sidebar.multiselect(
        "Select Industry",
        options=sorted(df['industry'].unique()),
        default=sorted(df['industry'].unique())
    )
    
    # Location filter
    location_filter = st.sidebar.multiselect(
        "Select Location",
        options=sorted(df['location'].unique()),
        default=sorted(df['location'].unique())
    )
    
    # Certification filters
    st.sidebar.header("Certifications")
    iso_filter = st.sidebar.checkbox("ISO 14001", value=True)
    fair_trade_filter = st.sidebar.checkbox("Fair Trade", value=True)
    organic_filter = st.sidebar.checkbox("Organic", value=True)
    b_corp_filter = st.sidebar.checkbox("B Corp", value=True)
    rainforest_filter = st.sidebar.checkbox("Rainforest Alliance", value=True)
    
    # New: Buyer Requirements Filter Section
    st.sidebar.header("Buyer Requirements")
    
    st.sidebar.markdown("**Set your priorities (0-100%):**")
    sustainability_weight = st.sidebar.slider("Sustainability Importance", 0, 100, 50) / 100
    lead_time_weight = st.sidebar.slider("Lead Time Importance", 0, 100, 25) / 100
    onboarding_cost_weight = st.sidebar.slider("Onboarding Cost Importance", 0, 100, 15) / 100
    switching_cost_weight = st.sidebar.slider("Switching Cost Importance", 0, 100, 10) / 100
    
    # Ensure weights sum to 1
    total_weight = sustainability_weight + lead_time_weight + onboarding_cost_weight + switching_cost_weight
    if total_weight != 1:
        # Normalize weights to sum to 1
        sustainability_weight /= total_weight
        lead_time_weight /= total_weight
        onboarding_cost_weight /= total_weight
        switching_cost_weight /= total_weight
    
    weights = {
        'sustainability': sustainability_weight,
        'lead_time': lead_time_weight,
        'onboarding_cost': onboarding_cost_weight,
        'switching_cost': switching_cost_weight
    }
    
    # Additional cost and lead time filters
    st.sidebar.header("Cost & Lead Time Filters")
    max_lead_time = st.sidebar.slider("Maximum Lead Time (days)", 
                                     min_value=int(df['lead_time_days'].min()), 
                                     max_value=int(df['lead_time_days'].max()),
                                     value=int(df['lead_time_days'].max()))
    
    max_onboarding_cost = st.sidebar.slider("Maximum Onboarding Cost (USD)", 
                                           min_value=int(df['onboarding_cost_usd'].min()), 
                                           max_value=int(df['onboarding_cost_usd'].max()),
                                           value=int(df['onboarding_cost_usd'].max()))
    
    max_switching_cost = st.sidebar.slider("Maximum Switching Cost (USD)", 
                                          min_value=int(df['switching_cost_usd'].min()), 
                                          max_value=int(df['switching_cost_usd'].max()),
                                          value=int(df['switching_cost_usd'].max()))
    
    # Apply filters
    filtered_df = df[
        (df['industry'].isin(industry_filter)) &
        (df['location'].isin(location_filter)) &
        (df['lead_time_days'] <= max_lead_time) &
        (df['onboarding_cost_usd'] <= max_onboarding_cost) &
        (df['switching_cost_usd'] <= max_switching_cost)
    ].copy()
    
    # Apply certification filters
    cert_conditions = []
    if iso_filter:
        cert_conditions.append(filtered_df['iso_14001'] == 1)
    if fair_trade_filter:
        cert_conditions.append(filtered_df['fair_trade'] == 1)
    if organic_filter:
        cert_conditions.append(filtered_df['organic'] == 1)
    if b_corp_filter:
        cert_conditions.append(filtered_df['b_corp'] == 1)
    if rainforest_filter:
        cert_conditions.append(filtered_df['rainforest_alliance'] == 1)
    
    if cert_conditions:
        cert_mask = pd.concat(cert_conditions, axis=1).any(axis=1)
        filtered_df = filtered_df[cert_mask]
    
    # Calculate weighted score based on buyer requirements
    if not filtered_df.empty:
        filtered_df['weighted_score'] = filtered_df.apply(
            lambda row: calculate_weighted_score(row, weights), axis=1
        )
    
    # Ranking options
    st.sidebar.header("Ranking Options")
    ranking_criteria = st.sidebar.selectbox(
        "Rank suppliers by:",
        options=[
            "Weighted Score (Buyer Requirements)", 
            "Sustainability Score", 
            "Carbon Footprint (Low to High)",
            "Recycling Rate (High to Low)",
            "Energy Efficiency (High to Low)",
            "Water Usage (Low to High)",
            "Waste Production (Low to High)",
            "Lead Time (Low to High)",
            "Onboarding Cost (Low to High)",
            "Switching Cost (Low to High)"
        ]
    )
    
    # Apply ranking
    if ranking_criteria == "Weighted Score (Buyer Requirements)":
        filtered_df = filtered_df.sort_values('weighted_score', ascending=False)
    elif ranking_criteria == "Sustainability Score":
        filtered_df = filtered_df.sort_values('sustainability_score', ascending=False)
    elif ranking_criteria == "Carbon Footprint (Low to High)":
        filtered_df = filtered_df.sort_values('carbon_footprint', ascending=True)
    elif ranking_criteria == "Recycling Rate (High to Low)":
        filtered_df = filtered_df.sort_values('recycling_rate', ascending=False)
    elif ranking_criteria == "Energy Efficiency (High to Low)":
        filtered_df = filtered_df.sort_values('energy_efficiency', ascending=False)
    elif ranking_criteria == "Water Usage (Low to High)":
        filtered_df = filtered_df.sort_values('water_usage', ascending=True)
    elif ranking_criteria == "Waste Production (Low to High)":
        filtered_df = filtered_df.sort_values('waste_production', ascending=True)
    elif ranking_criteria == "Lead Time (Low to High)":
        filtered_df = filtered_df.sort_values('lead_time_days', ascending=True)
    elif ranking_criteria == "Onboarding Cost (Low to High)":
        filtered_df = filtered_df.sort_values('onboarding_cost_usd', ascending=True)
    elif ranking_criteria == "Switching Cost (Low to High)":
        filtered_df = filtered_df.sort_values('switching_cost_usd', ascending=True)
    
    # Tabs
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "📊 Dashboard", "🏆 Rankings", "📈 Trends", "🔮 Scenario Simulation", "📋 Supplier Details", "💰 Buyer Analysis"
    ])
    
    # Dashboard
    with tab1:
        st.header("Supplier Sustainability Dashboard")
        
        # Key metrics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            avg_score = filtered_df['sustainability_score'].mean()
            st.metric("Average Sustainability Score", f"{avg_score:.2f}")
        with col2:
            avg_carbon = filtered_df['carbon_footprint'].mean()
            st.metric("Average Carbon Footprint", f"{avg_carbon:.2f}")
        with col3:
            avg_recycling = filtered_df['recycling_rate'].mean()
            st.metric("Average Recycling Rate", f"{avg_recycling:.2f}%")
        with col4:
            avg_energy = filtered_df['energy_efficiency'].mean()
            st.metric("Average Energy Efficiency", f"{avg_energy:.2f}%")
        
        # Charts
        col1, col2 = st.columns(2)
        with col1:
            fig1 = px.histogram(filtered_df, x="sustainability_score", nbins=20, 
                               title="Distribution of Sustainability Scores")
            st.plotly_chart(fig1, use_container_width=True)
        with col2:
            fig2 = px.box(filtered_df, x="industry", y="sustainability_score", 
                         title="Sustainability Scores by Industry")
            st.plotly_chart(fig2, use_container_width=True)
        
        fig3 = px.scatter(filtered_df, x="carbon_footprint", y="energy_efficiency",
                         size="sustainability_score", color="industry",
                         hover_name="name", title="Carbon Footprint vs Energy Efficiency")
        st.plotly_chart(fig3, use_container_width=True)
    
    # Rankings
    with tab2:
        st.header("Supplier Rankings")
        st.write(f"Ranked by: {ranking_criteria}")
        
        top_n = st.slider("Select number of suppliers to display", 5, 50, 10)
        ranked_suppliers = filtered_df.head(top_n)
        
        # Display ranking table
        display_cols = ['name', 'industry', 'location', 'sustainability_score', 
                       'carbon_footprint', 'recycling_rate', 'energy_efficiency',
                       'water_usage', 'waste_production', 'lead_time_days',
                       'onboarding_cost_usd', 'switching_cost_usd']
        
        # Add weighted score if it's the ranking criteria
        if ranking_criteria == "Weighted Score (Buyer Requirements)":
            display_cols.insert(3, 'weighted_score')
        
        # Add certification columns that exist
        cert_cols = ['iso_14001', 'fair_trade', 'organic', 'b_corp', 'rainforest_alliance']
        for col in cert_cols:
            if col in filtered_df.columns:
                display_cols.append(col)
        
        st.dataframe(ranked_suppliers[display_cols])
        
        # Visualize top suppliers
        if ranking_criteria == "Weighted Score (Buyer Requirements)":
            fig4 = px.bar(ranked_suppliers, x="name", y="weighted_score", color="industry",
                         title=f"Top {top_n} Suppliers by Weighted Score")
        else:
            fig4 = px.bar(ranked_suppliers, x="name", y="sustainability_score", color="industry",
                         title=f"Top {top_n} Suppliers by Sustainability Score")
        st.plotly_chart(fig4, use_container_width=True)
    
    # Trends
    with tab3:
        st.header("Sustainability Trends")
        
        col1, col2 = st.columns(2)
        with col1:
            industry_trends = filtered_df.groupby("industry")["sustainability_score"].mean().reset_index()
            fig5 = px.bar(industry_trends, x="industry", y="sustainability_score",
                         title="Average Sustainability Score by Industry")
            st.plotly_chart(fig5, use_container_width=True)
        
        with col2:
            location_trends = filtered_df.groupby("location")["sustainability_score"].mean().reset_index()
            fig6 = px.bar(location_trends, x="location", y="sustainability_score",
                         title="Average Sustainability Score by Location")
            st.plotly_chart(fig6, use_container_width=True)
        
        # Certification analysis
        cert_data = []
        for cert in cert_cols:
            if cert in filtered_df.columns:
                cert_mean = filtered_df[filtered_df[cert] == 1]['sustainability_score'].mean()
                cert_data.append({'certification': cert.replace('_', ' ').title(), 'score': cert_mean})
        
        if cert_data:
            cert_df = pd.DataFrame(cert_data)
            fig7 = px.bar(cert_df, x='certification', y='score', 
                         title='Average Sustainability Score by Certification')
            st.plotly_chart(fig7, use_container_width=True)
    
    # Scenario Simulation
    with tab4:
        st.header("Scenario Simulation")
        st.markdown("Compare different supplier choices and their environmental impacts.")
        
        suppliers = filtered_df['name'].unique()
        col1, col2 = st.columns(2)
        with col1:
            current_supplier = st.selectbox("Current Supplier", suppliers, key="current_supplier")
        with col2:
            alternative_supplier = st.selectbox("Alternative Supplier", suppliers, key="alt_supplier")
        
        if current_supplier and alternative_supplier:
            current = filtered_df[filtered_df['name'] == current_supplier].iloc[0]
            alternative = filtered_df[filtered_df['name'] == alternative_supplier].iloc[0]
            
            # Calculate impact differences
            impact_diff = {
                'Carbon Footprint': alternative['carbon_footprint'] - current['carbon_footprint'],
                'Water Usage': alternative['water_usage'] - current['water_usage'],
                'Waste Production': alternative['waste_production'] - current['waste_production'],
                'Recycling Rate': alternative['recycling_rate'] - current['recycling_rate'],
                'Energy Efficiency': alternative['energy_efficiency'] - current['energy_efficiency']
            }
            
            # Display comparison
            st.subheader("Environmental Impact Comparison")
            fig = go.Figure()
            
            fig.add_trace(go.Bar(
                name='Current',
                x=list(impact_diff.keys()),
                y=[
                    current['carbon_footprint'],
                    current['water_usage'],
                    current['waste_production'],
                    current['recycling_rate'],
                    current['energy_efficiency']
                ],
                marker_color='blue'
            ))
            
            fig.add_trace(go.Bar(
                name='Alternative',
                x=list(impact_diff.keys()),
                y=[
                    alternative['carbon_footprint'],
                    alternative['water_usage'],
                    alternative['waste_production'],
                    alternative['recycling_rate'],
                    alternative['energy_efficiency']
                ],
                marker_color='green'
            ))
            
            fig.update_layout(barmode='group', title_text="Environmental Impact Comparison")
            st.plotly_chart(fig, use_container_width=True)
            
            # Improvements / declines
            improvements = []
            declines = []
            
            for metric, diff in impact_diff.items():
                if metric in ['Recycling Rate', 'Energy Efficiency']:
                    if diff > 0:
                        improvements.append(f"{metric}: {diff:.2f} increase")
                    else:
                        declines.append(f"{metric}: {abs(diff):.2f} decrease")
                else:
                    if diff < 0:
                        improvements.append(f"{metric}: {abs(diff):.2f} reduction")
                    else:
                        declines.append(f"{metric}: {diff:.2f} increase")
            
            col1, col2 = st.columns(2)
            with col1:
                st.success("Improvements")
                for imp in improvements:
                    st.write("✅ " + imp)
            with col2:
                st.error("Potential Declines")
                for dec in declines:
                    st.write("⚠️ " + dec)
    
    # Supplier Details
    with tab5:
        st.header("Supplier Details")
        
        selected_supplier = st.selectbox("Select a supplier to view details", filtered_df['name'].unique())
        
        if selected_supplier:
            supplier_data = filtered_df[filtered_df['name'] == selected_supplier].iloc[0]
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("Basic Information")
                st.write(f"**Industry:** {supplier_data['industry']}")
                st.write(f"**Location:** {supplier_data['location']}")
                st.write(f"**Lead Time:** {supplier_data['lead_time_days']} days")
                st.write(f"**Onboarding Cost:** ${supplier_data['onboarding_cost_usd']:,.2f}")
                st.write(f"**Switching Cost:** ${supplier_data['switching_cost_usd']:,.2f}")
                
                st.subheader("Certifications")
                certs = []
                for cert in cert_cols:
                    if cert in supplier_data and supplier_data[cert] == 1:
                        certs.append(cert.replace('_', ' ').title())
                
                if certs:
                    for cert in certs:
                        st.write(f"✅ {cert}")
                else:
                    st.write("No certifications")
            
            with col2:
                st.subheader("Sustainability Metrics")
                st.write(f"**Sustainability Score:** {supplier_data['sustainability_score']:.2f}")
                st.write(f"**Carbon Footprint:** {supplier_data['carbon_footprint']:.2f}")
                st.write(f"**Recycling Rate:** {supplier_data['recycling_rate']:.2f}%")
                st.write(f"**Energy Efficiency:** {supplier_data['energy_efficiency']:.2f}%")
                st.write(f"**Water Usage:** {supplier_data['water_usage']:.2f}")
                st.write(f"**Waste Production:** {supplier_data['waste_production']:.2f}")
            
            # Radar chart for sustainability metrics
            metrics = ['Carbon Footprint', 'Recycling Rate', 'Energy Efficiency', 'Water Usage', 'Waste Production']
            values = [
                max(0, 100 - (supplier_data['carbon_footprint'] / 10)),
                supplier_data['recycling_rate'],
                supplier_data['energy_efficiency'],
                max(0, 100 - (supplier_data['water_usage'] / 100)),
                max(0, 100 - (supplier_data['waste_production'] / 5))
            ]
            
            fig = go.Figure(data=go.Scatterpolar(
                r=values,
                theta=metrics,
                fill='toself'
            ))
            
            fig.update_layout(
                polar=dict(
                    radialaxis=dict(
                        visible=True,
                        range=[0, 100]
                    )),
                showlegend=False,
                title="Sustainability Metrics Radar Chart"
            )
            
            st.plotly_chart(fig, use_container_width=True)
    
    # New: Buyer Analysis Tab
    with tab6:
        st.header("Supplier Analysis Based on Buyer Requirements")
        st.markdown(f"""
        This analysis ranks suppliers based on your specific requirements:
        - **Sustainability Importance:** {weights['sustainability']*100:.0f}%
        - **Lead Time Importance:** {weights['lead_time']*100:.0f}%
        - **Onboarding Cost Importance:** {weights['onboarding_cost']*100:.0f}%
        - **Switching Cost Importance:** {weights['switching_cost']*100:.0f}%
        """)
        
        if filtered_df.empty:
            st.warning("No suppliers match your current filters. Please adjust your filters to see results.")
            return
        
        # Show top suppliers based on weighted score
        top_buyer_suppliers = filtered_df.sort_values('weighted_score', ascending=False).head(10)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Top Suppliers Based on Your Requirements")
            st.dataframe(top_buyer_suppliers[[
                'name', 'industry', 'location', 'weighted_score', 
                'sustainability_score', 'lead_time_days', 
                'onboarding_cost_usd', 'switching_cost_usd'
            ]].round(3))
        
        with col2:
            # Create a radar chart to compare top suppliers
            metrics = ['Sustainability', 'Lead Time', 'Onboarding Cost', 'Switching Cost']
            
            fig = go.Figure()
            
            for _, supplier in top_buyer_suppliers.head(3).iterrows():
                # Normalize values for radar chart (0-1 scale)
                sustainability_norm = supplier['sustainability_score'] / 100
                lead_time_norm = 1 - ((supplier['lead_time_days'] - filtered_df['lead_time_days'].min()) / 
                                     (filtered_df['lead_time_days'].max() - filtered_df['lead_time_days'].min()))
                onboarding_cost_norm = 1 - ((supplier['onboarding_cost_usd'] - filtered_df['onboarding_cost_usd'].min()) / 
                                           (filtered_df['onboarding_cost_usd'].max() - filtered_df['onboarding_cost_usd'].min()))
                switching_cost_norm = 1 - ((supplier['switching_cost_usd'] - filtered_df['switching_cost_usd'].min()) / 
                                          (filtered_df['switching_cost_usd'].max() - filtered_df['switching_cost_usd'].min()))
                
                values = [
                    sustainability_norm,
                    lead_time_norm,
                    onboarding_cost_norm,
                    switching_cost_norm
                ]
                
                fig.add_trace(go.Scatterpolar(
                    r=values,
                    theta=metrics,
                    fill='toself',
                    name=supplier['name']
                ))
            
            fig.update_layout(
                polar=dict(
                    radialaxis=dict(
                        visible=True,
                        range=[0, 1]
                    )),
                showlegend=True,
                title="Comparison of Top 3 Suppliers"
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        # Cost vs Sustainability analysis - FIXED: Remove size parameter
        st.subheader("Cost vs Sustainability Analysis")
        
        fig = px.scatter(filtered_df, 
                        x="sustainability_score", 
                        y="onboarding_cost_usd",
                        color="industry",
                        hover_name="name",
                        title="Sustainability vs Onboarding Cost",
                        labels={
                            "sustainability_score": "Sustainability Score",
                            "onboarding_cost_usd": "Onboarding Cost (USD)"
                        })
        st.plotly_chart(fig, use_container_width=True)
        
        # Lead Time vs Sustainability analysis - FIXED: Remove size parameter
        fig = px.scatter(filtered_df, 
                        x="sustainability_score", 
                        y="lead_time_days",
                        color="industry",
                        hover_name="name",
                        title="Sustainability vs Lead Time",
                        labels={
                            "sustainability_score": "Sustainability Score",
                            "lead_time_days": "Lead Time (Days)"
                        })
        st.plotly_chart(fig, use_container_width=True)
        
        # Show trade-off analysis
        st.subheader("Trade-off Analysis")
        
        # Calculate normalized scores for visualization
        filtered_df['sustainability_norm'] = filtered_df['sustainability_score'] / 100
        filtered_df['lead_time_norm'] = 1 - ((filtered_df['lead_time_days'] - filtered_df['lead_time_days'].min()) / 
                                           (filtered_df['lead_time_days'].max() - filtered_df['lead_time_days'].min()))
        filtered_df['cost_norm'] = 1 - ((filtered_df['onboarding_cost_usd'] - filtered_df['onboarding_cost_usd'].min()) / 
                                      (filtered_df['onboarding_cost_usd'].max() - filtered_df['onboarding_cost_usd'].min()))
        
        # Create a trade-off scatter plot
        fig = px.scatter(filtered_df, 
                        x="sustainability_norm", 
                        y="cost_norm",
                        color="industry",
                        hover_name="name",
                        title="Trade-off: Sustainability vs Cost Efficiency (Normalized)",
                        labels={
                            "sustainability_norm": "Sustainability (Higher is better)",
                            "cost_norm": "Cost Efficiency (Higher is better)"
                        })
        st.plotly_chart(fig, use_container_width=True)

if __name__ == "__main__":
    main()
