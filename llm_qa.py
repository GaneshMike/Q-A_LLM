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

import json

data = [
    {
        "context": "Wealth Management Chief Investment Office16 December 20220utlook 2023Playing itSAFEIN 2023, we expect recessions in",
        "params": {
            "temperature": 0.3,
            "top_k": 50,
            "top_p": 1.0,
            "max_new_tokens": 1000
        },
        "qna": {
            "question": "What is the macroeconomic outlook for 2023?",
            "answer": "In 2023, we expect recessions in the US and Europe, a recovery in China, a slowdown in global inflation, and a pause in Fed rates in 2023."
        },
        "page_no": 1
    },
    {
        "context": "Wealth Management Chief Investment Office16 December 20220utlook 2023Playing itSAFEIN 2023, we expect recessions in",
        "params": {
            "temperature": 0.3,
            "top_k": 50,
            "top_p": 1.0,
            "max_new_tokens": 1000
        },
        "qna": {
            "question": "What is the macroeconomic outlook for 2023?",
            "answer": "In 2023, we expect recessions in the US and Europe, a recovery in China, a slowdown in global inflation, and a pause in Fed rates in 2023."
        },
        "page_no": 2
    }
]

output = {
    "ADP_output": [
        {
            "pdf_file": "file1.pdf",
            "params": {},
            "pdf_info": []
        }
    ]
}

for item in data:
    page_no = item["page_no"]
    context = item["context"]
    question = item["qna"]["question"]
    answer = item["qna"]["answer"]
    params = item["params"]

    page_info = {
        "context": context,
        "Q&A": [
            {
                "question": question,
                "answer": answer
            }
        ]
    }

    # Find existing pdf_info or create a new one
    pdf_info = None
    for pdf in output["ADP_output"][0]["pdf_info"]:
        if pdf["page_no"] == page_no:
            pdf_info = pdf
            break

    if pdf_info:
        pdf_info["page_info"].append(page_info)
    else:
        pdf_info = {
            "page_no": page_no,
            "page_info": [page_info]
        }
        output["ADP_output"][0]["pdf_info"].append(pdf_info)

    # Update params details
    pdf_params = output["ADP_output"][0]["params"]
    pdf_params.update(params)

# Convert the output to JSON
output_json = json.dumps(output, indent=4)
print(output_json)






