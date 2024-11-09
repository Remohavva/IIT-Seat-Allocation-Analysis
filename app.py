import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import spacy
from fuzzywuzzy import fuzz

# Load dataset
df = pd.read_csv('//Users//jaikrishna//Desktop//iits//data.csv')

# Load spaCy model


# Define keyword-action mapping
actions = {
    "sample data": ["sample data", "show data", "example data", "display data"],
    "overview": ["overview", "summary", "basic stats", "describe data"],
    "yearly opening count": ["yearly openings", "openings by year", "year count"],
    "institute count": ["institute count", "number of institutes", "college count"],
    "quota distribution": ["quota distribution", "quota breakdown", "quota pie chart"],
    "gender ratios": ["gender ratios", "gender balance", "male female ratio"],
    "program duration": ["program duration", "course duration", "years program"],
    "programs offered": ["programs offered", "course list", "available programs"],
    "opening and closing ranks distribution": ["rank distribution", "opening closing ranks", "rank spread"],
    "opening rank by category": ["rank by category", "category ranks", "category rank distribution"],
    "opening vs closing rank": ["opening vs closing rank", "rank comparison", "rank scatter"],
    "program duration vs opening rank": ["duration vs rank", "course duration rank", "program rank trend"],
    "program distribution by quota": ["program quota", "quota courses", "programs by quota"],
    "rank trend over time": ["rank trend", "rank history", "rank changes"],
    "female presence": ["female presence", "women colleges", "gender diversity"]
}

# Function to match user input to the closest action
def get_action(user_input):
    input_doc = nlp(user_input)
    highest_score = 0
    best_match = None
    for action, keywords in actions.items():
        for keyword in keywords:
            score = fuzz.partial_ratio(user_input.lower(), keyword)
            if score > highest_score:
                highest_score = score
                best_match = action
    return best_match

# Streamlit app title
st.title("Your IIT Analyzer Bot")
st.subheader("Analyze. Arrange. Achieve")
st.subheader("One Stop for All IIT Questions")

# User prompt for chatbot interaction
st.header("Enter your Query")
user_input = st.text_input("Ask your question here...")

# Determine the action based on the input
action = get_action(user_input)

# Display the corresponding data or visualization based on the action
if action == "sample data":
    st.subheader("Sample Data")
    st.write(df.sample(10))

elif action == "overview":
    st.subheader("Dataset Overview")
    st.write(df.describe())
    buffer = st.empty()
    with buffer:
        st.write("Check console for more details.")
    df.info(buf=buffer)

elif action == "yearly opening count":
    st.subheader("Yearly Opening Count")
    by_year = df['year'].value_counts()
    st.bar_chart(by_year)

elif action == "institute count":
    st.subheader("Institute Count")
    inst_cnt = df['institute_short'].value_counts()
    st.bar_chart(inst_cnt)

elif action == "quota distribution":
    st.subheader("Quota Distribution")
    quota = df['quota'].value_counts()
    fig, ax = plt.subplots()
    quota.plot(kind='pie', startangle=90, colors=['olivedrab', 'rosybrown', 'gray', 'saddlebrown'], autopct='%1.1f%%', pctdistance=1.25, shadow=True, ax=ax)
    plt.title('Quota Distribution')
    st.pyplot(fig)

elif action == "gender ratios":
    st.subheader("Gender Ratios of Each College")
    gender_counts = df.groupby(['institute_short', 'pool']).size().unstack()
    gender_ratios = gender_counts.div(gender_counts.sum(axis=1), axis=0) * 100
    st.write(gender_ratios)

elif action == "program duration":
    st.subheader("Program Duration")
    d = df['program_duration'].value_counts()
    fig, ax = plt.subplots()
    ax.pie(d, labels=['4 Years', '5 Years'], autopct='%1.1f%%', startangle=90)
    st.pyplot(fig)

elif action == "programs offered":
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

elif action == "opening and closing ranks distribution":
    st.subheader("Opening and Closing Ranks Distribution")
    fig, ax = plt.subplots(figsize=(13, 7))
    sns.histplot(df['opening_rank'], kde=True, bins=50, log_scale=(True, False), ax=ax, color='blue')
    sns.histplot(df['closing_rank'], kde=True, bins=50, log_scale=(True, False), ax=ax, color='red')
    plt.title('Opening and Closing Ranks Trend Over Years')
    st.pyplot(fig)

elif action == "opening rank by category":
    st.subheader("Opening Rank Distribution by Category")
    fig, ax = plt.subplots()
    sns.boxplot(x='category', y='opening_rank', data=df, ax=ax)
    plt.title('Opening Rank Distribution by Category')
    st.pyplot(fig)

elif action == "opening vs closing rank":
    st.subheader("Opening Rank vs Closing Rank")
    fig, ax = plt.subplots()
    sns.scatterplot(x='opening_rank', y='closing_rank', data=df, ax=ax)
    st.pyplot(fig)

elif action == "program duration vs opening rank":
    st.subheader("Program Duration vs Opening Rank")
    fig, ax = plt.subplots()
    sns.boxplot(x='program_duration', y='opening_rank', data=df, ax=ax)
    plt.title('Program Duration vs Opening Rank')
    st.pyplot(fig)

elif action == "program distribution by quota":
    st.subheader("Program Duration Distribution by Quota")
    fig, ax = plt.subplots()
    sns.countplot(x='program_duration', hue='quota', data=df, ax=ax)
    plt.title('Program Duration Distribution by Quota')
    st.pyplot(fig)

elif action == "rank trend over time":
    st.subheader("Opening and Closing Rank Trend Over Time")
    fig, ax = plt.subplots()
    sns.lineplot(x='year', y='opening_rank', data=df, label='Opening Rank', color='blue', ax=ax)
    sns.lineplot(x='year', y='closing_rank', data=df, label='Closing Rank', color='red', ax=ax)
    plt.title('Opening and Closing Rank Trend Over Time')
    plt.xlabel('Year')
    plt.ylabel('Rank')
    plt.legend()
    st.pyplot(fig)

elif action == "female presence":
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

else:
    st.write("Sorry, I couldn't understand your request. Please try rephrasing.")

