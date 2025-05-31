import streamlit as st
import google.generativeai as genai

# Configure Google Gemini API
GOOGLE_API_KEY = "AIzaSyBZirLRrzpyDlOyqrqcBIWLNkXfAs07PLg"
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-pro')

# Set page configuration
st.set_page_config(
    page_title="Academic Email Generator",
    page_icon="✉️",
    layout="wide"
)

# Add custom CSS
st.markdown("""
    <style>
    .stTextArea textarea {
        height: 200px;
    }
    .main {
        padding: 2rem;
    }
    </style>
""", unsafe_allow_html=True)

# Title and description
st.title("✉️ Academic Email Generator")
st.markdown("""
This tool helps you generate professional academic emails using AI. Simply fill in the details
below, and the AI will help craft a well-structured email for you.
""")

# Input fields
col1, col2 = st.columns(2)

with col1:
    recipient_name = st.text_input("Recipient's Name", placeholder="e.g., Dr. Jane Smith")
    recipient_title = st.text_input("Recipient's Title/Position", placeholder="e.g., Professor of Computer Science")
    recipient_institution = st.text_input("Recipient's Institution", placeholder="e.g., Stanford University")

with col2:
    sender_name = st.text_input("Your Name", placeholder="e.g., John Doe")
    sender_title = st.text_input("Your Title/Position", placeholder="e.g., PhD Student")
    sender_institution = st.text_input("Your Institution", placeholder="e.g., MIT")

email_purpose = st.text_area("Email Purpose", placeholder="e.g., Inquiring about research opportunities in your lab")
additional_context = st.text_area("Additional Context", placeholder="Add any specific points, requirements, or context you'd like to include in the email")

# Email tone selection
tone = st.select_slider(
    "Email Tone",
    options=["Very Formal", "Formal", "Semi-Formal", "Professional Friendly"],
    value="Formal"
)

if st.button("Generate Email", type="primary"):
    if not all([recipient_name, email_purpose]):
        st.error("Please fill in at least the recipient's name and email purpose.")
    else:
        with st.spinner("Generating your email..."):
            try:
                prompt = f"""
                Generate a professional academic email with the following details:
                
                To: {recipient_name}
                Title: {recipient_title}
                Institution: {recipient_institution}
                
                From: {sender_name}
                Sender Title: {sender_title}
                Sender Institution: {sender_institution}
                
                Purpose: {email_purpose}
                Additional Context: {additional_context}
                
                Tone: {tone}
                
                Please generate a well-structured email that:
                1. Uses appropriate academic language and formality
                2. Is clear and concise
                3. Follows proper email etiquette
                4. Maintains the specified tone ({tone})
                5. Includes a proper greeting and sign-off
                
                Format the email with proper spacing and structure.
                """
                
                response = model.generate_content(prompt)
                
                # Display the generated email in a nice format
                st.markdown("### Generated Email:")
                st.markdown("---")
                email_container = st.container()
                with email_container:
                    st.markdown(f"```text\n{response.text}\n```")
                
                # Add copy button
                st.markdown("---")
                if st.button("📋 Copy to Clipboard"):
                    st.write(response.text)
                
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")

# Add helpful tips in the sidebar
with st.sidebar:
    st.markdown("### 📝 Tips for Better Results")
    st.markdown("""
    1. Be specific about your purpose
    2. Provide relevant context
    3. Include any specific requirements
    4. Choose the appropriate tone
    5. Review and edit the generated email
    """)
    
    st.markdown("### 🎯 Common Use Cases")
    st.markdown("""
    - Research collaboration inquiries
    - Graduate program applications
    - Conference submissions
    - Recommendation letter requests
    - Meeting scheduling
    - Research guidance
    """) 
