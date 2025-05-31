import streamlit as st
import google.generativeai as genai

# Configure Gemini API
genai.configure(api_key="AIzaSyBZirLRrzpyDlOyqrqcBIWLNkXfAs07PLg")

# Safety settings - adjust these to be more permissive
safety_settings = [
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_NONE",
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_NONE",
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_NONE",
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_NONE",
    },
]

# Initialize model with safety settings
model = genai.GenerativeModel('gemini-pro', safety_settings=safety_settings)

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
                prompt = f"""Write a professional email with these details:
To: {recipient_name}
Title: {recipient_title}
Institution: {recipient_institution}

From: {sender_name}
Sender Title: {sender_title}
Sender Institution: {sender_institution}

Purpose: {email_purpose}
Additional Context: {additional_context}

Tone: {tone}

Requirements:
1. Use appropriate academic language
2. Be clear and concise
3. Follow proper email etiquette
4. Match the specified tone
5. Include greeting and sign-off"""
                
                response = model.generate_content(prompt)
                
                if response.text:
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
                else:
                    st.error("The AI model returned an empty response. Please try again with different input.")
                
            except Exception as e:
                st.error(f"Error: {str(e)}")
                st.info("If you're seeing this error, please try with a simpler request or different wording.")

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
