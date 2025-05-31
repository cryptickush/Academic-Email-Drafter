import streamlit as st
from openai import OpenAI

# Set your OpenAI API key here
OPENAI_API_KEY = "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"  # Replace with your actual OpenAI API key

# Initialize OpenAI client
client = OpenAI(api_key=OPENAI_API_KEY)

# Basic page config
st.set_page_config(page_title="Email Generator", page_icon="✉️")

# Test OpenAI connection first
def test_openai_connection():
    try:
        # Simple test completion
        response = client.chat.completions.create(
            model="gpt-4-turbo-preview",
            messages=[{"role": "user", "content": "Say 'API connection successful'"}],
            max_tokens=10
        )
        return True
    except Exception as e:
        st.error(f"OpenAI API Error: {str(e)}")
        return False

# Title
st.title("✉️ Professional Email Generator")
st.write("Generate professional emails with AI assistance")

# Test API connection
if not test_openai_connection():
    st.error("⚠️ Error: Could not connect to OpenAI API. Please check your API key.")
    st.stop()

# Input fields
recipient = st.text_input("To:", placeholder="e.g., Dr. Jane Smith")
sender = st.text_input("From:", placeholder="Your name")
subject = st.text_input("Subject:", placeholder="e.g., Research Collaboration Opportunity")
purpose = st.text_area("What's the purpose of your email?", 
                      placeholder="e.g., I want to inquire about research opportunities in AI")

# Tone selection
tone = st.select_slider(
    "Email Tone",
    options=["Very Formal", "Formal", "Semi-Formal", "Friendly"],
    value="Formal"
)

if st.button("Generate Email"):
    if not all([recipient, sender, subject, purpose]):
        st.error("Please fill in all fields")
    else:
        try:
            with st.spinner("Generating your email..."):
                # Create the prompt
                prompt = f"""Write a professional email:
                To: {recipient}
                From: {sender}
                Subject: {subject}
                Purpose: {purpose}
                Tone: {tone}

                Make it concise, professional, and well-structured."""

                # Get response from OpenAI
                response = client.chat.completions.create(
                    model="gpt-4-turbo-preview",
                    messages=[
                        {"role": "system", "content": "You are a professional email writing assistant."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.7
                )

                # Display the email
                email = response.choices[0].message.content
                st.markdown("### Generated Email")
                st.text_area("", email, height=300)
                
                # Copy button
                if st.button("Copy to Clipboard", type="secondary", key="copy"):
                    st.write(email)

        except Exception as e:
            st.error("OpenAI API Error:")
            st.error(str(e))

# Sidebar tips
with st.sidebar:
    st.markdown("### 💡 Tips")
    st.markdown("""
    - Be clear about your purpose
    - Include relevant details
    - Choose the right tone
    - Review before sending
    """) 
