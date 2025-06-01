import streamlit as st
from openai import OpenAI

# Page config
st.set_page_config(page_title="Email Generator", page_icon="✉️")

# Initialize OpenAI client
try:
    api_key = st.secrets["openai"]["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"]
    if not api_key.startswith("sk-"):
        st.error("Invalid API key format. The key should start with 'sk-'")
        st.stop()
    client = OpenAI(api_key=api_key)
except KeyError:
    st.error("""Please set up your OpenAI API key in Streamlit secrets with this format:
    [openai]
    OPENAI_API_KEY = "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"
    """)
    st.stop()
except Exception as e:
    st.error("Error initializing OpenAI client. Please check your API key in Streamlit secrets.")
    st.error(str(e))
    st.stop()

# Title
st.title("✉️ Professional Email Generator")

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

def generate_email(recipient, sender, subject, purpose, tone):
    try:
        response = client.chat.completions.create(
            model="gpt-4-turbo-preview",
            messages=[
                {"role": "system", "content": "You are a professional email writing assistant."},
                {"role": "user", "content": f"""Write a professional email:
                To: {recipient}
                From: {sender}
                Subject: {subject}
                Purpose: {purpose}
                Tone: {tone}
                
                Make it concise and professional."""}
            ],
            temperature=0.7
        )
        return response.choices[0].message.content
    except Exception as e:
        st.error("Error generating email:")
        st.error(str(e))
        return None

if st.button("Generate Email"):
    if not all([recipient, sender, subject, purpose]):
        st.error("Please fill in all fields")
    else:
        with st.spinner("Generating your email..."):
            email = generate_email(recipient, sender, subject, purpose, tone)
            if email:
                st.markdown("### Generated Email")
                st.text_area("", email, height=300)
                if st.button("Copy to Clipboard"):
                    st.write(email)

# Tips
with st.sidebar:
    st.markdown("### 💡 Tips")
    st.markdown("""
    - Be clear about your purpose
    - Include relevant details
    - Choose the right tone
    - Review before sending
    """) 
