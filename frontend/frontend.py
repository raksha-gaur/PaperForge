import streamlit as st
from pipeline import generate_question_paper

# Page configuration
st.set_page_config(page_title="PaperForge",
                   page_icon='📄',
                   layout='centered',
                   initial_sidebar_state='collapsed')

st.header("PaperForge:Exam Paper Generator")

title = st.text_input('Enter the title for your document:')
# PDF Upload
st.markdown("### Book upload")
pdf_file = st.file_uploader("Upload a PDF file", type="pdf")

st.markdown("### Question Configuration")

# Creating the table-like structure with columns
col1, col2, col3 = st.columns(3)

with col1:
    st.write("**Question Type**")
    st.write("MCQs")
    st.write("")
    st.write("Short Answer Questions")
    st.write("")
    st.write("Long Answer Questions")


with col2:
    st.write("**Number of Questions**")
    num_mcqs = st.number_input("Number of MCQs", min_value=1, value=5, label_visibility="collapsed")
    num_short_answers = st.number_input("Number of Short Answer Questions", min_value=1, value=3,
                                        label_visibility="collapsed")
    num_long_answers = st.number_input("Number of Long Answer Questions", min_value=1, value=2,
                                       label_visibility="collapsed")

with col3:
    st.write("**Number of Marks**")
    marks_per_mcq = st.number_input("Marks per MCQ", min_value=1, value=1, label_visibility="collapsed")
    marks_per_short_answer = st.number_input("Marks of short answer", min_value=1, value=5, label_visibility="collapsed"
                                             )
    marks_per_long_answer = st.number_input("Marks of long answer", min_value=1, value=10, label_visibility="collapsed")


st.markdown("### Page Range to Process")
start_page = st.number_input("Start Page", min_value=1, value=1)
end_page = st.number_input("End Page", min_value=1, value=1)

# Button to start processing
submit = st.button("Generate Question Paper")

# Handle button click
if submit:
    if pdf_file is not None:
        with st.spinner('Generating question paper...'):
            # Call to the backend function to generate the question paper
            download_pdf = generate_question_paper(pdf_file, title, num_mcqs, marks_per_mcq, num_short_answers,
                                                   marks_per_short_answer, num_long_answers, marks_per_long_answer,
                                                   start_page, end_page)
                                                    
            st.success("Question paper generated successfully!")

            # Provide a download button for the generated paper
            st.download_button(
                label="Download Question Paper",
                data=download_pdf,
                file_name="question_paper.pdf",
                mime="application/pdf"
            )
    else:
        st.error("Please upload a PDF file.")
