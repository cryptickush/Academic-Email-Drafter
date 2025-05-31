%%writefile app.py
import streamlit as st
import google.generativeai as genai
import os

# --- Configure the Gemini API ---
# IMPORTANT: In a real application, use environment variables or Streamlit Secrets
# for your API key, NOT directly embedding it in the code like this.
# For Colab demo purposes, we'll put it here.
API_KEY = "AIzaSyBZirLRrzpyDlOyqrqcBIWLNkXfAs07PLg" # <-- Your API key here
genai.configure(api_key=API_KEY)

# Choose the Gemini model
# You can explore other models offered by the API if needed
GEMINI_MODEL = 'gemini-pro'

# --- Email Generation Logic (Using Gemini) ---
def generate_email_draft_with_gemini(prompt, intent, recipient_name="", paper_details="", other_info=""):
    """
    Generates a draft email using the Gemini model based on intent and user inputs.
    """
    # Construct a detailed prompt for the Gemini model
    # This prompt guides Gemini on the desired content and format
    gemini_prompt = f"""
    Draft a professional academic email based on the following information:

    Email Purpose/Intent: {intent}
    Core message or key points to include: {prompt}
    Recipient's Name (if available): {recipient_name if recipient_name else 'a colleague'}
    Relevant Paper/Manuscript Title or Details (if applicable): {paper_details if paper_details else 'N/A'}
    Other specific context or information: {other_info if other_info else 'N/A'}

    Please structure the email professionally with a clear subject line, a polite salutation (addressing the recipient by name if provided), a body incorporating the core message and relevant details, and a standard closing.

    Example structure:
    Subject: [Relevant Subject]

    Dear [Recipient Name],

    [Opening]
    [Body incorporating core message, intent, paper/other details]
    [Closing remarks]

    Sincerely,
    [Your Name]
    [Your Title/Affiliation]
    [Your Contact Information (Optional)]

    Generate only the email text. Do not include any introductory or concluding remarks outside of the email content itself.
    """

    try:
        # Initialize the Gemini model
        model = genai.GenerativeModel(GEMINI_MODEL)

        # Generate content using the prompt
        response = model.generate_content(gemini_prompt)

        # Extract the generated text from the response
        if response and response.text:
            generated_text = response.text
            return generated_text
        else:
            return "Gemini did not return a valid response."

    except Exception as e:
        st.error(f"An error occurred while generating the email draft with Gemini: {e}")
        return "Error generating email draft. Please check the API key and try again."


# --- Streamlit App UI Configuration ---
st.set_page_config(layout="wide", page_title="Academic Email Drafter AI (Gemini)")

# --- Main Application ---
st.title("🎓 Academic Email Drafter AI (Powered by Gemini)")
st.markdown("""
Welcome to the Academic Email Drafter AI assistant. This tool uses the Gemini model to help you craft professional emails for various academic purposes.
Please provide a core prompt, select the email's intent, and fill in any optional details to generate a draft.

**Note:** This application uses the Gemini API for email generation.
Ensure your API key is configured correctly (in a real application, use secure methods like Streamlit Secrets).
""")

# Initialize session state for the draft and error message
if 'draft' not in st.session_state:
    st.session_state.draft = ""
if 'error_message' not in st.session_state:
    st.session_state.error_message = ""

# --- Sidebar for User Inputs ---
with st.sidebar:
    st.header("📬 Compose Your Email")

    user_prompt = st.text_area(
        "Your Core Prompt / Key Message:",
        height=120,
        placeholder="e.g., Inquire about Prof. Smith's recent paper on neuroplasticity and its implications for learning."
    )

    email_intent_options = ["Inquiry", "Submission", "Thank You", "Collaboration Request", "Follow-up", "General"]
    selected_intent = st.selectbox(
        "Select Email Intent:",
        email_intent_options,
        help="Choose the primary purpose of your email."
    )

    st.markdown("---")
    st.subheader("📄 Optional Details")
    recipient_name = st.text_input(
        "Recipient's Full Name (e.g., Dr. Eleanor Vance):",
        placeholder="Dr. Eleanor Vance"
    )

    # Dynamic label for paper_details based on intent
    paper_details_label = "Relevant Paper/Manuscript Title:"
    if selected_intent == "Submission":
        paper_details_label = "Your Manuscript Title:"
    elif selected_intent == "Follow-up":
        paper_details_label = "Date of Previous Email (e.g., 2024-05-15):"
    elif selected_intent == "Thank You":
         paper_details_label = "Relevant Paper/Work Title (if applicable):"
    elif selected_intent == "Collaboration Request":
         paper_details_label = "Your Relevant Paper/Work Title (if applicable):"

    paper_info = st.text_input(
        paper_details_label,
        placeholder="e.g., 'The Impact of X on Y' or '2024-05-15'"
    )

    other_specific_info_label = "Other Specific Information:"
    if selected_intent == "Inquiry":
        other_specific_info_label = "Specific topic of inquiry:"
    elif selected_intent == "Submission":
        other_specific_info_label = "Name of Journal/Conference:"
    elif selected_intent == "Thank You":
        other_specific_info_label = "Reason for thanks (e.g., their helpful advice):"
    elif selected_intent == "Collaboration Request":
        other_specific_info_label = "Specific area/topic of collaboration:"
    elif selected_intent == "Follow-up":
        other_specific_info_label = "Subject of previous email:"


    other_info = st.text_area(
        other_specific_info_label,
        height=80,
        placeholder="Provide context relevant to the selected intent."
    )
    st.markdown("---")
    generate_button = st.button("✨ Generate Email Draft with Gemini", use_container_width=True, type="primary")

# --- Main Area for Displaying Output and Errors ---
st.header("📝 Generated Email Draft")

if st.session_state.error_message:
    st.error(st.session_state.error_message)

if generate_button:
    if not user_prompt:
        st.session_state.error_message = "⚠️ Please enter a core prompt for your email in the sidebar."
        st.session_state.draft = "" # Clear previous draft if error
    else:
        st.session_state.error_message = "" # Clear error message
        with st.spinner("🤖 Drafting your email with Gemini..."):
            # Call the new Gemini-powered function
            draft = generate_email_draft_with_gemini(
                prompt=user_prompt,
                intent=selected_intent,
                recipient_name=recipient_name,
                paper_details=paper_info,
                other_info=other_info
            )
            st.session_state.draft = draft

if st.session_state.draft:
    st.text_area(
        "Review and Edit Your Draft:",
        st.session_state.draft,
        height=500,
        help="You can copy this draft to your email client."
    )

    # Placeholder for email sending functionality
    st.markdown("---")
    st.subheader("✉️ Sending the Email (Conceptual)")
    st.info("""
    **How to Send:** Copy the generated draft above and paste it into your preferred email client.

    **Note on Direct Sending:** Actual email sending functionality (e.g., using `smtplib` in Python) is not implemented in this web demo.
    """)
else:
    if not st.session_state.error_message: # Only show this if no error is displayed
        st.info("Please fill in the details in the sidebar and click 'Generate Email Draft with Gemini'.")


# --- Footer ---
st.markdown("---")
st.markdown("<p style='text-align: center; color: grey;'>Academic Email Drafter AI (Powered by Gemini) - Demo</p>", unsafe_allow_html=True)