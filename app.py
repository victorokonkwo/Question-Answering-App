import streamlit as st
from transformers import pipeline
import pdfplumber
import bs4 as bs
import urllib.request

st.sidebar.header("""
© Harvinder Power
""")
st.sidebar.markdown("This app allows users to input text of their choice using the tools provided (PDF, Wikipedia article or Textbox), and ask questions with the answer being extracted from the text.")
st.sidebar.markdown("_When running the app the first time, it may take some time to initialise due to the requirements needing to be downloaded._")
tool = st.sidebar.selectbox("Tool", ["PDF Q&A", "Wikipedia Q&A", "Textbox Q&A"])
nlp = pipeline("question-answering")


def generateAnswer(question, context):
    answer = nlp(question=question, context=context)
    return answer['answer']


## ------------------------------ PDF Q&A ------------------------------ ##
## Helper function to extract words from the PDF ##
def extract_data(feed):
    data = ""
    with pdfplumber.load(feed) as pdf:
        pages = pdf.pages
        for p in pages:
            data = data + p.extract_text()
    return data # build more code to return a dataframe 



def pdf_qna():
    heading = """
    # PDF Q&A
    """
    heading
    uploaded_file = st.file_uploader('Choose your .pdf file', type="pdf")
    question = st.text_input("Question:")
    if st.button("Summarise"):
        if uploaded_file is not None:
            context = extract_data(uploaded_file)
            answer = generateAnswer(question, context)
            st.header("Summary")
            st.write(answer)

## ------------------------------ Wikipedia Q&A ------------------------------ ##
def wikipedia_qna():
    heading = """
    # Wikipedia Q&A  
    """
    heading
    user_input = st.text_input("Wikipedia Link:", value="https://en.wikipedia.org/wiki/Machine_learning")
    question = st.text_input("Question:")

    if st.button("Summarise"):
        scraped_data = urllib.request.urlopen(user_input)
        article = scraped_data.read()

        parsed_article = bs.BeautifulSoup(article,'lxml')

        paragraphs = parsed_article.find_all('p')

        article_text = ""
        for p in paragraphs:
            article_text += p.text

        answer = generateAnswer(question, article_text)
        st.header("Answer")
        st.write(answer)



## ------------------------------ Textbox Q&A ------------------------------ ##
def textbox_qna():
    heading = """
    # Textbox Q&A  
    Example text from this article: https://www.bbc.co.uk/news/science-environment-53119686
    """
    heading
    dummy_text = '''
    We've just become a little less ignorant about Planet Earth.
    The initiative that seeks to galvanise the creation of a full map of the ocean floor says one-fifth of this task has now been completed.
    When the Nippon Foundation-GEBCO Seabed 2030 Project was launched in 2017, only 6% of the global ocean bottom had been surveyed to what might be called modern standards.
    That number now stands at 19%, up from 15% in just the last year.
    Some 14.5 million sq km of new bathymetric (depth) data was included in the GEBCO grid in 2019 - an area equivalent to almost twice that of Australia.
    It does, however, still leave a great swathe of the planet in need of mapping to an acceptable degree.
    "Today we stand at the 19% level. That means we've got another 81% of the oceans still to survey, still to map. That's an area about twice the size of Mars that we have to capture in the next decade," project director Jamie McMichael-Phillips told BBC News.

    The map at the top of this page illustrates the challenge faced by GEBCO in the coming years.
    Black represents those areas where we have yet to get direct echosounding measurements of the shape of the ocean floor. Blues correspond to water depth (deeper is purple, shallower is lighter blue).
    It's not true to say we have no idea of what's in the black zones; satellites have actually taught us a great deal. Certain spacecraft carry altimeter instruments that can infer seafloor topography from the way its gravity sculpts the water surface above - but this only gives a best resolution at over a kilometre, and Seabed 2030 has a desire for a resolution of at least 100m everywhere.

    Better seafloor maps are needed for a host of reasons.
    They are essential for navigation, of course, and for laying underwater cables and pipelines.
    They are also important for fisheries management and conservation, because it is around the underwater mountains that wildlife tends to congregate. Each seamount is a biodiversity hotspot.
    In addition, the rugged seafloor influences the behaviour of ocean currents and the vertical mixing of water.
    This is information required to improve the models that forecast future climate change - because it is the oceans that play a critical role in moving heat around the planet. And if you want to understand precisely how sea-levels will rise in different parts of the world, good ocean-floor maps are a must.
    Much of the data that's been imported into the GEBCO grid recently has been in existence for some time but was "sitting on a shelf" out of the public domain. The companies, institutions and governments that were holding this information have now handed it over - and there is probably a lot more of this hidden resource still to be released.

    But new acquisitions will also be required. Some of these will come from a great crowdsourcing effort - from ships, big and small, routinely operating their echo-sounding equipment as they transit the globe. Even small vessels - fishing boats and yachts - can play their part by attaching data-loggers to their sonar and navigation equipment.
    One very effective strategy is evidenced by the British Antarctic Survey (BAS), which operates in the more remote parts of the globe - and that is simply to mix up the routes taken by ships.
    "Very early on we adopted the ethos that data should be collected on passage - on the way to where we were going, not just at the site of interest," explained BAS scientist Dr Rob Larter.
    "A beautiful example of this is the recent bathymetric map of the Drake Passage area (between South America and Antarctica). A lot of that was acquired by different research projects as they fanned out and moved back and forth to the places they were going."

    New technology will be absolutely central to the GEBCO quest.
    
    '''
    user_input = st.text_area("Text:", value=dummy_text)
    question = st.text_input("Question:")

    if st.button("Answer"):
        answer = generateAnswer(question, user_input)
        st.header("Answer")
        st.write(answer)


if tool == "PDF Q&A":
    pdf_qna()


if tool == "Wikipedia Q&A":
    wikipedia_qna()

if tool == "Textbox Q&A":
    textbox_qna()