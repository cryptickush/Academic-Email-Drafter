%%writefile app.py
import streamlit as st
import google.generativeai as genai

# --- Configure Gemini API (using Streamlit Secrets) ---
# Make sure you have configured a secret named "GEMINI_API_KEY" in your Streamlit Cloud settings
try:
    genai.configure(api_key=st.secrets["AIzaSyBZirLRrzpyDlOyqrqcBIWLNkXfAs07PLg"])
    model = genai.GenerativeModel('gemini-pro') # Or other suitable Gemini model
except Exception as e:
    st.error(f"Failed to configure Gemini API. Make sure 'AIzaSyBZirLRrzpyDlOyqrqcBIWLNkXfAs07PLg' is set in Streamlit Secrets. Error: {e}")
    model = None # Set model to None if configuration fails

# --- Email Generation Logic (Using Gemini) ---
def generate_email_with_gemini(prompt, intent, recipient_name="", paper_details="", other_info=""):
    """
    Generates an email draft using the Gemini API based on intent and user inputs.
    """
    if model is None:
        return "Gemini API is not configured. Cannot generate email."

    # Construct a detailed prompt for Gemini
    full_prompt = f"""
    Generate a professional academic email draft with the following details:

    Intent: {intent}
    Recipient Name: {recipient_name if recipient_name else 'Colleague'}
    Core Message/Prompt: {prompt}
    Relevant Paper/Manuscript Details: {paper_details if paper_details else 'None provided'}
    Other Specific Information: {other_info if other_info else 'None provided'}

    Please ensure the email is polite, clear, and appropriate for an academic context.
    Start with a suitable salutation and end with a professional closing.
    Do not include sender contact information, just placeholders.
    """

    try:
        response = model.generate_content(full_prompt)
        # Access the generated text
        if response and response.candidates:
            return response.candidates[0].content.parts[0].text
        else:
            return "Gemini did not generate a valid response."
    except Exception as e:
        return f"An error occurred during Gemini generation: {e}"


# --- Streamlit App UI Configuration ---
st.set_page_config(layout="wide", page_title="Academic Email Drafter AI")

# --- Main Application ---
st.title("🎓 Academic Email Drafter AI (Powered by Gemini)")
st.markdown("""
Welcome to the Academic Email Drafter AI assistant. This tool helps you craft professional emails for various academic purposes using the Gemini model.
Please provide a core prompt, select the email's intent, and fill in any optional details to generate a draft.
""")

# Initialize session state for the draft if it doesn't exist
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
    else:
        paper_details_label = "Relevant Paper/Manuscript Title:" # Default

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
    else:
         other_specific_info_label = "Other Specific Information:" # Default


    other_info = st.text_area(
        other_specific_info_label,
        height=80,
        placeholder="Provide context relevant to the selected intent."
    )
    st.markdown("---")
    generate_button = st.button("✨ Generate Email Draft (with Gemini)", use_container_width=True, type="primary")

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
            # Use the Gemini-powered function
            draft = generate_email_with_gemini(
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
        st.info("Please fill in the details in the sidebar and click 'Generate Email Draft (with Gemini)'.")

# --- Footer ---
st.markdown("---")
st.markdown("<p style='text-align: center; color: grey;'>Academic Email Drafter AI (Powered by Gemini) - Demo</p>", unsafe_allow_html=True)