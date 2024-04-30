import streamlit as st
import pandas as pd
import hashlib

st.markdown("""
    <style>
    body {
        font-family: 'Arial', sans-serif; /* Modern font */
    }
    .stApp {
        background-color: #FFFFFF;
        background-image: linear-gradient(180deg, #f8fbfd, #FFFFFF 90%);
    }
    h1, h2, h3, h4, h5, h6, .stMarkdown, .stLabel, .stSelectbox label, .stNumberInput label {
        color: #0055A2; /* UNISA theme */
        font-weight: bold; /* Makes text bold */
    }
    .stAlert-success {
        background-color: #D4EDDA; /* Light green background for success messages */
        color: black; /* Black text for visibility */
        border-color: #C3E6CB; /* Slightly lighter green border */
    }
    .stAlert-error {
        background-color: #F8D7DA; /* Light red background for error messages */
        color: black; /* Black text for visibility */
        border-color: #F5C6CB; /* Slightly lighter red border */
    }
    .st-cb, .st-ci, .st-ck, .st-cl, .stMarkdown, h1, h2 {
        flex-direction: column;
        align-items: center;
        justify-content: center;
        text-align: center;
    }
    .stSelectbox, .stNumberInput, .stButton {
        margin: auto;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1); /* Adds shadow for depth */
        transition: box-shadow 0.2s ease-in-out; /* Smooth transition for hover effects */
    }
    .stSelectbox > div > div, .stNumberInput > input {
        color: #013369; /* Dark blue text */
        border: 1px solid #ced4da; /* Light grey border */
        background-color: white; /* White background */
    }
    .stSelectbox > label, .stNumberInput > label, .stTextInput label {
        display: block;
        text-align: center;
        width: 100%;
        color: #0055A2; /* Dark blue text to match UNISA theme */
    }
    .stButton > button {
        width: 100%;
        border-radius: 20px;
        background-color: #00529B; /* Dark blue background */
        color: white; /* White text */
        padding: 10px 24px; /* Padding for size */
        border: none; /* No border */
        font-size: 16px; /* Large font size */
    }
    .stButton > button:hover {
        background-color: #003366; /* Darker blue on hover */
        box-shadow: 0 6px 12px rgba(0,0,0,0.2); /* Shadow effect on hover */
    }
    #title, #about-header {
        border: 2px solid #013369; /* Dark blue border */
        padding: 10px;
        border-radius: 10px;
        background-color: #0055A2; /* Dark blue background */
        color: #FFFFFF; /* White text */
    }
    #how-it-works-header {
        display: inline-block;
        padding: 5px 10px;
        border: 2px solid #013369; /* Dark blue border */
        border-radius: 10px;
        background-color: #E6E6FA; /* Lavender background */
        color: #0055A2; /* Dark blue text */
    }
    .stDataFrame {
        width: 100%; /* Full-width data frames */
        margin: auto; /* Centered data frames */
    }
    .stTextInput > div {
        flex-direction: column; /* Column direction for text input */
    }
    .stTextInput label {
        color: #0055A2; /* Dark blue text for labels */
    }
    </style>
    """, unsafe_allow_html=True)




def send_to_aws_and_fetch_link(data):
    """
    Placeholder function to simulate sending data to AWS S3 and getting a dataset link.
    """
    # Placeholder link, assuming the dataset is identified by some unique ID or parameters
    return "https://aws.s3/download/dataset_link_based_on_criteria"

def generate_fake_dataset(size):
    """
    Generate a fake dataset for preview purposes. This can be replaced with actual dataset fetching logic.
    """
    import numpy as np
    np.random.seed(0)
    data = np.random.rand(size, 5)  # Assume 5 columns for simplicity
    return pd.DataFrame(data, columns=['Feature1', 'Feature2', 'Feature3', 'Feature4', 'Feature5'])



def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def check_username(username, df):
    return username in df['username'].values

def verify_login(username, password, df):
    user = df[df['username'] == username]
    if not user.empty:
        return user.iloc[0]['password'] == hash_password(password)
    return False

def register_user(username, password, df):
    new_user = pd.DataFrame({'username': [username], 'password': [hash_password(password)]})
    df = pd.concat([df, new_user], ignore_index=True)
    df.to_csv('user_credentials.csv', index=False)

try:
    user_credentials = pd.read_csv('user_credentials.csv')
except FileNotFoundError:
    user_credentials = pd.DataFrame(columns=['username', 'password'])




def main():
    st.sidebar.title("Navigation")
    menu = ["Home", "Login", "Signup"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Home":
        st.title('Dataset Generator', anchor='title')
        st.markdown("""<br>""", unsafe_allow_html=True)
        st.subheader('How it Works', anchor='how-it-works-header')
        col1, col2, col3 = st.columns(3)
        with col1:
            st.header('Fill Out the Form')
            st.write('Fill out a short form with five questions to tell us what you need in your dataset.')
        with col2:
            st.header('Search the Dataset')
            st.write('Our program takes over to find an existing dataset or craft a synthetic dataset tailored to your inputs.')
        with col3:
            st.header('Download Dataset')
            st.write('Receive and download your custom dataset. It shall create a downloadable file.')

        with st.form(key='dataset_form'):
            algorithm = st.selectbox(
                'What type of machine learning algorithm do you want to use the dataset for?',
                ['', 'Linear Regression', 'Random Forest', 'K-nearest Neighbours']
            )
            size = st.selectbox(
                'What size is the dataset do you require?',
                ['', '≤ 1000 rows', '≤ 5000 rows']
            )
            features = st.selectbox(
                'How many features do you want for your dataset?',
                ['', '3', '5', '10+']
            )
            topic = st.selectbox(
                'What topic do you want your dataset to be about?',
                ['', 'Health', 'Finance', 'Environment', 'Technology']
            )
            cleanliness = st.selectbox(
                'Do you want the dataset to be clean or unclean?',
                ['', 'Clean', 'Unclean']
            )

            submit_button = st.form_submit_button(label='Generate Dataset')

            st.markdown("""<br>""", unsafe_allow_html=True)

        if submit_button:
            data = {
                'algorithm': algorithm,
                'size': size,
                'features': features,
                'topic': topic,
                'cleanliness': cleanliness
            }
            link = send_to_aws_and_fetch_link(data)
            st.markdown(f"Your dataset has been successfully generated! Download [here]({link})")

            # Generating and displaying a fake dataset for preview
            st.write('### Dataset Preview', anchor='preview')
            preview_size = 10  # Number of rows to display
            dataset_preview = generate_fake_dataset(preview_size)
            
            # Centering the DataFrame
            col1, col2, col3 = st.columns([1, 6, 1])  # Keeps the structure but may adjust the column ratios
            with col2:
                st.markdown("""
                <div style="display: flex; justify-content: center;">
                    <div style="width: 100%;">
                        """, unsafe_allow_html=True)
                st.dataframe(dataset_preview)
                st.markdown("""
                    </div>
                </div>
                """, unsafe_allow_html=True)

        st.subheader('About', anchor='about-header')
        st.markdown("""<br>""", unsafe_allow_html=True)
        st.write('Our platform is designed to assist students and researchers in finding the perfect datasets for their machine learning experiments. With the exponential growth of data in various domains, choosing the right dataset for a specific machine learning task is crucial for achieving accurate and meaningful results. Our platform aims to streamline this process by providing a curated collection of diverse datasets and powerful search functionalities.')
            

    elif choice == "Login":
        st.subheader("Login")
        username = st.text_input("Username")
        password = st.text_input("Password", type='password')
        if st.button("Login"):
            if verify_login(username, password, user_credentials):
                st.markdown(f'<div style="color: green; text-align: center;">Welcome {username}!</div>', unsafe_allow_html=True)
            else:
                st.markdown('<div style="color: red; text-align: center;">Invalid username or password</div>', unsafe_allow_html=True)

    elif choice == "Signup":
        st.subheader("Create New Account")
        new_username = st.text_input("Choose Username", key="new_username")
        new_password = st.text_input("Choose Password", type='password', key="new_password")
        confirm_password = st.text_input("Confirm Password", type='password', key="confirm_password")

        if st.button("Signup"):
            if new_password != confirm_password:
                st.markdown('<div style="color: red; text-align: center;">Passwords do not match</div>', unsafe_allow_html=True)
            elif check_username(new_username, user_credentials):
                st.markdown('<div style="color: red; text-align: center;">Username already exists</div>', unsafe_allow_html=True)
            else:
                register_user(new_username, new_password, user_credentials)
                st.markdown(f'<div style="color: green; text-align: center;">Account created successfully for {new_username}</div>', unsafe_allow_html=True)

if __name__ == '__main__':
    main()
