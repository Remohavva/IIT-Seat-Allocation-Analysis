import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load dataset
df = pd.read_csv('//Users//jaikrishna//Desktop//iits//data.csv')

# Streamlit app title
st.title("Interactive Data Analysis of Institutes and Rankings")

# User prompt for chatbot interaction
st.header("Chat with the Data")
user_input = st.text_input("Ask for specific data insights or visualizations")

# Show Sample Data
if "sample data" in user_input.lower():
    st.subheader("Sample Data")
    st.write(df.sample(10))

# Dataset Overview
if "overview" in user_input.lower():
    st.subheader("Dataset Overview")
    st.write(df.describe())
    buffer = st.empty()
    with buffer:
        st.write("Check console for more details.")
    df.info(buf=buffer)

# Yearly Opening Count
if "yearly opening count" in user_input.lower():
    st.subheader("Yearly Opening Count")
    by_year = df['year'].value_counts()
    st.bar_chart(by_year)

# Institute Count
if "institute count" in user_input.lower():
    st.subheader("Institute Count")
    inst_cnt = df['institute_short'].value_counts()
    st.bar_chart(inst_cnt)

# Quota Distribution
if "quota distribution" in user_input.lower():
    st.subheader("Quota Distribution")
    quota = df['quota'].value_counts()
    fig, ax = plt.subplots()
    quota.plot(kind='pie', startangle=90, colors=['olivedrab', 'rosybrown', 'gray', 'saddlebrown'], autopct='%1.1f%%', pctdistance=1.25, shadow=True, ax=ax)
    plt.title('Quota Distribution')
    st.pyplot(fig)

# Gender Ratios of Each College
if "gender ratios" in user_input.lower():
    st.subheader("Gender Ratios of Each College")
    gender_counts = df.groupby(['institute_short', 'pool']).size().unstack()
    gender_ratios = gender_counts.div(gender_counts.sum(axis=1), axis=0) * 100
    st.write(gender_ratios)

# Program Duration Count
if "program duration" in user_input.lower():
    st.subheader("Program Duration")
    d = df['program_duration'].value_counts()
    fig, ax = plt.subplots()
    ax.pie(d, labels=['4 Years', '5 Years'], autopct='%1.1f%%', startangle=90)
    st.pyplot(fig)

# Programs Offered by Colleges
if "programs offered" in user_input.lower():
    st.subheader("Programs Offered by Colleges")
    qq = {
        'programs': ['B.Tech', 'B.Tech + M.Tech (IDD)', 'BSc', 'B.Arch', 'Btech + M.Tech (IDD)',
                     'BS + MS (IDD)', 'Int M.Tech', 'Int Msc.', 'Int MSc.', 'BSc + MSc (IDD)',
                     'B.Plan', 'B.Pharm', 'B.Pharm + M.Pharm'],
        'cnts': [52086, 6030, 2200, 1343, 868, 660, 594, 523, 298, 204, 144, 4, 4]
    }
    qf = pd.DataFrame(qq)
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(x='cnts', y='programs', data=qf, orient='h', ax=ax)
    plt.title('Number of Colleges Offering Different Programs')
    plt.xlabel("Number of Colleges")
    plt.ylabel('Programs')
    st.pyplot(fig)

# Opening and Closing Ranks Distribution
if "opening and closing ranks distribution" in user_input.lower():
    st.subheader("Opening and Closing Ranks Distribution")
    fig, ax = plt.subplots(figsize=(13, 7))
    sns.histplot(df['opening_rank'], kde=True, bins=50, log_scale=(True, False), ax=ax, color='blue')
    sns.histplot(df['closing_rank'], kde=True, bins=50, log_scale=(True, False), ax=ax, color='red')
    plt.title('Opening and Closing Ranks Trend Over Years')
    st.pyplot(fig)

# Opening Rank Distribution by Category
if "opening rank by category" in user_input.lower():
    st.subheader("Opening Rank Distribution by Category")
    fig, ax = plt.subplots()
    sns.boxplot(x='category', y='opening_rank', data=df, ax=ax)
    plt.title('Opening Rank Distribution by Category')
    st.pyplot(fig)

# Opening vs Closing Rank Scatter Plot
if "opening vs closing rank" in user_input.lower():
    st.subheader("Opening Rank vs Closing Rank")
    fig, ax = plt.subplots()
    sns.scatterplot(x='opening_rank', y='closing_rank', data=df, ax=ax)
    st.pyplot(fig)

# Program Duration vs Opening Rank
if "program duration vs opening rank" in user_input.lower():
    st.subheader("Program Duration vs Opening Rank")
    fig, ax = plt.subplots()
    sns.boxplot(x='program_duration', y='opening_rank', data=df, ax=ax)
    plt.title('Program Duration vs Opening Rank')
    st.pyplot(fig)

# Program Distribution by Quota
if "program distribution by quota" in user_input.lower():
    st.subheader("Program Duration Distribution by Quota")
    fig, ax = plt.subplots()
    sns.countplot(x='program_duration', hue='quota', data=df, ax=ax)
    plt.title('Program Duration Distribution by Quota')
    st.pyplot(fig)

# Opening and Closing Rank Trend Over Time
if "rank trend over time" in user_input.lower():
    st.subheader("Opening and Closing Rank Trend Over Time")
    fig, ax = plt.subplots()
    sns.lineplot(x='year', y='opening_rank', data=df, label='Opening Rank', color='blue', ax=ax)
    sns.lineplot(x='year', y='closing_rank', data=df, label='Closing Rank', color='red', ax=ax)
    plt.title('Opening and Closing Rank Trend Over Time')
    plt.xlabel('Year')
    plt.ylabel('Rank')
    plt.legend()
    st.pyplot(fig)

# Female Presence in Different Colleges
if "female presence" in user_input.lower():
    st.subheader("Female Presence in Different Colleges")
    fdf = df[df['pool'] == "Female-Only"]
    nfdf = df[df['pool'] != "Female-Only"]
    fcnts = fdf.groupby('institute_short').size()
    tcnts = df.groupby('institute_short').size()
    gender_ratio_per_college = (fcnts / tcnts).fillna(0)
    gender_ratio_df = pd.DataFrame({
        'College': gender_ratio_per_college.index,
        'Female_Ratio': gender_ratio_per_college.values
    })
    fig, ax = plt.subplots(figsize=(15, 8))
    sns.barplot(x='College', y='Female_Ratio', data=gender_ratio_df, ax=ax)
    plt.xticks(rotation=90)
    st.pyplot(fig)
