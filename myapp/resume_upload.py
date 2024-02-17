import streamlit as st
from docx import Document
import textract
import PyPDF2


def process_pdf(file_buffer):
    pdf_reader = PyPDF2.PdfFileReader(file_buffer)
    resume_text = ""
    for page_num in range(pdf_reader.numPages):
        page = pdf_reader.getPage(page_num)
        resume_text += page.extractText()
    return resume_text


def process_docx(file_buffer):
    doc = Document(file_buffer)
    resume_text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
    return resume_text


def process_txt(file_buffer):
    return file_buffer.getvalue().decode("utf-8")


def display_upload_resume():
    st.header("Upload Resume")
    upload_option = st.radio("Choose upload method:", ("Upload file", "Paste text"))

    resume_text = ""

    if upload_option == "Upload file":
        uploaded_file = st.file_uploader(
            "Upload your resume", type=["txt", "docx", "pdf"]
        )

        if uploaded_file is not None:
            file_extension = uploaded_file.name.split(".")[-1]

            if file_extension.lower() == "txt":
                resume_text = process_txt(uploaded_file)
            elif file_extension.lower() == "docx":
                resume_text = process_docx(uploaded_file)
            elif file_extension.lower() == "pdf":
                resume_text = process_pdf(uploaded_file)

    else:  # Paste text option
        resume_text = st.text_area("Paste your resume here:", "")

    # Save the resume text in the app's state variable
    st.session_state.resume_text = resume_text

    return resume_text


def process_file(uploaded_file):
    file_extension = uploaded_file.name.split(".")[-1]
    if file_extension.lower() == "txt":
        text = process_txt(uploaded_file)
    elif file_extension.lower() == "docx":
        text = process_docx(uploaded_file)
    elif file_extension.lower() == "pdf":
        text = process_pdf(uploaded_file)
    return text


# Example usage:
# resume_text = display_upload_resume()
# st.write("Resume text:", resume_text)
