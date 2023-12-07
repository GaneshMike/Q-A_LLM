import streamlit as st
from pprint import pprint
from lmqg import TransformersQG

def main():
    model_path = r'C:\Users\Yoga\Desktop\EDA\hackathan\Models\t5-base-squad-qag'
    model = TransformersQG(model_path)
    key1 = "key1" 
    key2 = "key2" 
    key3 = "key3" 
    st.title('Automatic Question & Answer Generation with AI')
    
    if 'text_input' not in st.session_state:
        st.session_state['text_input'] = ""
    text_input = st.text_area("Enter your text here", key="textarea", value=st.session_state['text_input'], height=200)
    st.session_state['text_input'] = text_input


    col1, col2, col3 = st.columns(3)

    if 'option_1' not in st.session_state:
        st.session_state['option_1'] = 'T5 SMALL'
    with col1:
        option_1 = st.selectbox('QAG Model :', ['T5 SMALL', 'T5 BASE', 'Flan-T5 SMALL', 'Flan-T5 BASE'], key=key1)

    if 'option_2' not in st.session_state:
        st.session_state['option_2'] = 'End2End'
    with col2:
        option_2 = st.selectbox('QAG Type :', ['End2End', 'Multitask', 'Pipeline'], key=key2)

    if 'option_3' not in st.session_state:
        st.session_state['option_3'] = 'Paragraph'
    with col3:
        option_3 = st.selectbox('Split :', ['Paragraph', 'Sentence'], key=key3)

    beam_size = st.slider('Please select the Beam size', 0, 130, 25)
    st.session_state['beam_size'] = beam_size
    Top_P = st.slider('Please select the Top-P', 0, 130, 25)
    st.session_state['Top_P'] = Top_P

    col4, col5, col6 = st.columns(3)
    with col4:
        if st.button('Reset'):
            st.write('Button 1 was clicked!')

    # Button 2
    with col5:
        if st.button('Example'):
            st.write('Button 2 was clicked!')

    # Button 3
    generated_qa = []
    with col6:
        if st.button('Generate Q&A'):
            data = model.generate_qa(text_input)
            question_answer_pairs = [(item[0], item[1]) for item in data]
            generated_qa.extend(question_answer_pairs)


    for question, answer in generated_qa:
        st.write(f"Question: {question}")
        st.write(f"Answer: {answer}\n")

if __name__ == "__main__":
    main()


import fitz
import pandas as pd

def extract_paragraphs(pdf_path, chunk_size):
    doc = fitz.open(pdf_path)
    paragraphs = []
 
    for page_num in range(doc.page_count):
        page = doc[page_num]
        text = page.get_text()
        
        # Split text into paragraphs based on your criteria
        current_position = 0
        while current_position < len(text):
            end_position = min(current_position + chunk_size, len(text))
            paragraph = text[current_position:end_position]
            
            # Ensure the paragraph ends with a meaningful delimiter (e.g., period)
            while end_position < len(text) and not paragraph.endswith(('.', '!', '?')):
                end_position += 1
                paragraph = text[current_position:end_position]
 
            paragraphs.append(paragraph.strip())
            current_position = end_position
 
    doc.close()
    return paragraphs


# Example usage
pdf_path = r"C:\Users\1590530\Downloads\banking-approach-2012.pdf"
chunk_size = 500  # Adjust the chunk size as needed
excel_path = 'output.xlsx'
 
paragraphs = extract_paragraphs(pdf_path, chunk_size)

paragraphs[5]






