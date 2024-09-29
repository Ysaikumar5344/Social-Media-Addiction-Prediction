import streamlit as st
import pandas as pd
import pickle

# Load the trained model from the pickle file
model_path = r"Addict.pkl"
with open(model_path, 'rb') as file:
    model = pickle.load(file)

st.image(r"innomatics-footer-logo.webp")
# Set up the background image with reduced brightness using an overlay
page_bg_img = f"""
<style>
.stApp {{
    background-image: url("https://cdn.memiah.co.uk/uploads/counselling-directory.org.uk/image_gallery/social-media-use-1694010755-hero.jpg");
    background-size: cover;
    background-position: top center;
    background-blend-mode: darken;
}}

.stApp:before {{
    content: "";
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0.5);  /* Adjust this value to control brightness */
    z-index: -1;
}}

/* Increase font size of labels and add shading */
.stSelectbox > label, .stSlider > label, .stNumberInput > label {{
    font-size: 18px;
    background-color: rgba(0, 0, 0, 0.1);  /* Light shading effect */
    padding: 5px;
    border-radius: 5px;
    color: black;
}}

/* Style for the precautions text */
.precautions {{
    font-size: 20px;  /* Increase font size for the tips */
    line-height: 1.6;  /* Adjust line spacing for readability */
    color: white;
    background-color: rgba(0, 0, 0, 0.5);  /* Add a background for better readability */
    padding: 10px;
    border-radius: 10px;
    margin-top: 20px;
}}
</style>
"""
st.markdown(page_bg_img, unsafe_allow_html=True)

# Define precautions for users predicted to be addicted
precautions = """
<div class="precautions">
    <strong>Tips to reduce social media addiction:</strong><br>
    1. Set time limits for using social media.<br>
    2. Uninstall social media apps from your phone to minimize usage.<br>
    3. Engage in offline hobbies and activities.<br>
    4. Be mindful of the content you consume, and unfollow accounts that lead to negative feelings.<br>
    5. Schedule 'social media detox' periods, like not using it during weekends or at night.<br>
    6. Focus on building in-person connections.<br>
    7. Seek support from friends, family, or a counselor if necessary.
</div>
"""

# Function to get user input
def get_user_input():
    gender = st.selectbox('Gender', ['Male', 'Female', 'Non-binary', 'Unsure', 'Trans', 'Other'])
    age = st.number_input('Age', min_value=10, max_value=70, value=25, step=1)
    occupation_status = st.selectbox('Occupation Status', [
        'University Student', 
        'School Student', 
        'Salaried Worker', 
        'Self-Employed',
        'Unemployed',
        'Freelancer',
        'Homemaker',
        'Retired', 
        'Others'
    ])
    avg_time_on_social_media = st.sidebar.slider('Average Time on Social Media (hours/day)', 0, 24, 2)
    use_without_purpose = st.sidebar.slider('Time spent without purpose on social media (hours/day)', 0, 24, 1)
    distractibility = st.sidebar.slider('Distractibility', 1, 10, 5)
    difficulty_concentrating = st.sidebar.slider('Difficulty Concentrating', 1, 10, 5)
    comparison_with_others = st.sidebar.slider('Comparison with others', 1, 10, 5)
    interest_fluctuation = st.sidebar.slider('Interest Fluctuation', 1, 10, 5)
    
    platform_usage_category = st.selectbox('Platform Usage Category', ['Low', 'Medium', 'High'])
    
    if platform_usage_category == 'Low':
        num_platforms_used = st.number_input('Number of Platforms Used (Low usage)', min_value=1, max_value=3, value=1, step=1)
    elif platform_usage_category == 'Medium':
        num_platforms_used = st.number_input('Number of Platforms Used (Medium usage)', min_value=4, max_value=7, value=4, step=1)
    elif platform_usage_category == 'High':
        num_platforms_used = st.number_input('Number of Platforms Used (High usage)', min_value=8, max_value=15, value=8, step=1)
    
    user_data = {
        'gender': gender,
        'age': age,
        'occupation_status': occupation_status,
        'avg_time_on_social_media': avg_time_on_social_media,
        'use_without_purpose': use_without_purpose,
        'distractibility': distractibility,
        'difficulty_concentrating': difficulty_concentrating,
        'comparison_with_others': comparison_with_others,
        'interest_fluctuation': interest_fluctuation,
        'platform_usage_category': platform_usage_category,
        'num_platforms_used': num_platforms_used
    }

    # Convert the user input into a DataFrame
    features = pd.DataFrame(user_data, index=[0])
    return features

# Main Streamlit app
st.title('The Social Media Detox: Using Machine Learning to Spot Addiction')

# Get user inputs
user_input = get_user_input()

# Display user input
st.write("## Your Input")
st.write(user_input)

# Make predictions using the trained model
if st.button('Predict'):
    prediction = model.predict(user_input)[0]  # Get the prediction result
    
    if prediction == 1:  # If 'addicted'
        st.write("### You might be addicted to social media!")
        st.markdown(precautions, unsafe_allow_html=True)  # Use markdown to display formatted text
    else:
        st.write("### You are not addicted to social media. Keep up the healthy habits!")
