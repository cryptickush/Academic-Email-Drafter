import streamlit as st
# Import the Gemini library
import google.generativeai as genai

# Page config
st.set_page_config(page_title="Academic Email Generator", page_icon="✉️") # Updated title slightly

# Initialize Gemini client
try:
    # Get the Gemini API key from Streamlit secrets
    gemini_api_key = st.secrets["gemini"]["GEMINI_API_KEY"]
    if not gemini_api_key:
        st.error("Gemini API key not found in Streamlit secrets.")
        st.stop()

    # Configure the genai library with the API key
    genai.configure(api_key=gemini_api_key)

    # Initialize the Gemini model
    model = genai.GenerativeModel('gemini-1.5-flash-latest') # Using a suitable Gemini model

except KeyError:
    st.error("""Please set up your Gemini API key in Streamlit secrets with this format:
    [gemini]
    GEMINI_API_KEY = "your_gemini_api_key_here"
    """)
    st.stop()
except Exception as e:
    st.error("Error initializing Gemini client. Please check your API key in Streamlit secrets.")
    st.error(str(e))
    st.stop()

# Title
st.title("✉️ Academic Email Generator (powered by Gemini)") # Updated title

# Input fields
recipient = st.text_input("To:", placeholder="e.g., Dr. Jane Smith")
sender = st.text_input("From:", placeholder="Your name")
subject = st.text_input("Subject:", placeholder="e.g., Research Collaboration Opportunity")
purpose = st.text_area("What's the purpose of your email?",
                      placeholder="e.g., I want to inquire about research opportunities")

# Tone selection
tone = st.select_slider(
    "Email Tone",
    options=["Very Formal", "Formal", "Semi-Formal", "Friendly"],
    value="Formal"
)

def generate_email_with_gemini(recipient, sender, subject, purpose, tone):
    try:
        # Create the prompt for the Gemini model
        prompt = f"""Write a professional academic email:
        To: {recipient}
        From: {sender}
        Subject: {subject}
        Purpose: {purpose}
        Tone: {tone}

        Make it concise and professional, suitable for an academic context."""

        # Generate content using the Gemini model
        response = model.generate_content(prompt)

        # Access the generated text
        return response.text
    except Exception as e:
        st.error(f"An error occurred during email generation: {e}")
        return None # Return None or an empty string in case of error

# Button to generate email and display the result
if st.button("Generate Email"):
    if not purpose:
        st.warning("Please enter the purpose of the email.")
    else:
        # Call the Gemini email generation function
        generated_email = generate_email_with_gemini(recipient, sender, subject, purpose, tone)
        if generated_email:
            st.subheader("Generated Email:")
            st.text_area("Email Content", generated_email, height=300)
