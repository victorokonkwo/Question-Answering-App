import streamlit as st
from transformers import pipeline
import pdfplumber

st.sidebar.header("""
© Harvinder Power
""")

st.title('Q&A')
nlp = pipeline("question-answering")


## Helper function to extract words from the PDF ##
def extract_data(feed):
    data = ""
    with pdfplumber.load(feed) as pdf:
        pages = pdf.pages
        for p in pages:
            data = data + p.extract_text()
    return data # build more code to return a dataframe 

uploaded_file = st.file_uploader('Choose your .pdf file', type="pdf")

if uploaded_file is not None:
    df = extract_data(uploaded_file)
    context = df

# dummy_text = r"""
# Extractive Question Answering is the task of extracting an answer from a text given a question. An example of a
# question answering dataset is the SQuAD dataset, which is entirely based on that task. If you would like to fine-tune
# a model on a SQuAD task, you may leverage the `run_squad.py`.
# """
# context = st.text_area("Text:", value=dummy_text)

question = st.text_input("Question:")

if st.button("Summarise"):
    answer = nlp(question=question, context=context)
    st.header("Answer")
    st.write(answer['answer'])