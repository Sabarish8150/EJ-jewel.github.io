import streamlit as st
import cv2
import pytesseract
from PIL import Image
import numpy as np
import re
from calculation import *

# Custom CSS to style the app
st.markdown("""
    <style>
        .main-title {
            text-align: center;
            font-size: 40px;
            font-weight: bold;
            color: #ff6347;
        }
        .sidebar .sidebar-content {
            background-color: #f0f2f6;
        }
        .header-text {
            color: #007acc;
            font-size: 24px;
            font-weight: bold;
            margin-top: 20px;
        }
        .uploaded-image {
            border: 3px solid #007acc;
            border-radius: 10px;
            margin-bottom: 10px;
        }
        .output-card {
            background-color: #f7f7f7;
            border-radius: 10px;
            padding: 20px;
            margin-top: 20px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        }
        .grade-output {
            color: #28a745;
            font-size: 22px;
            font-weight: bold;
        }
    </style>
""", unsafe_allow_html=True)

def isdigit(num):
    for i in str(num):
        if i not in {'0','1','2','3','4','5','6','7','8','9'}:
            return 1
    return 0
def preprocess_image(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)
    return thresh

def extract_table_data(image):
    # Convert the uploaded image to a NumPy array if it's not already one
    if isinstance(image, np.ndarray):
        img = image
    else:
        img = np.array(Image.open(image))

    # Process the image as before
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    extracted_text = pytesseract.image_to_string(gray)

    # Clean up the text
    extracted_text = extracted_text.replace("|", " ").strip()
    extracted_text = extracted_text.replace(";", " ").strip()
    extracted_text = extracted_text.replace("[", " ").strip()
    extracted_text = extracted_text.replace("]", " ").strip()

    total, gold_wt = None, None
    lines = extracted_text.split('\n')
    S_area = 0
    for line in lines:
        # st.write(line)
        # try:
            # Check for 'TOTAL' in the line and extract its value
        total=0
        if 'TOTAL' in line.upper():
            parts = line.split()
                # If the next word or value exists after 'TOTAL', assign it as the total
            if len(parts) > 1:
                total = parts[1]
        

            # Check for 'GOLD WT' and extract its numeric value
        gold_wt=0
        if 'GOLD WT' in line.upper():
            
                # Find the numeric part using regex
            match = re.search(r'(\d+(\.\d+)?)', line)
            if match:
                gold_wt = match.group(1)
                

        if not isdigit(gold_wt):
            gold_wt = 0
        if 'SURFACE AREA' in line.upper() or 'SURFACE' in line.upper() :
            S_area = line.split()[2]
        # except (IndexError, ValueError) as e:
        #     st.write(f"Error extracting data: {e}")


    return total, gold_wt, extracted_text, S_area


def main():
    # Main title with styled header
    st.markdown("<h1 class='main-title'>Grade Calculation </h1>", unsafe_allow_html=True)

    # Sidebar for file upload and toggle
    st.sidebar.markdown("<h2 class='header-text'>Upload and Options</h2>", unsafe_allow_html=True)
    uploaded_image = st.sidebar.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])

    # Mode selection: Array or Mirror
    mode = st.sidebar.selectbox("Select Type", options=["None","Array", "Mirror"])

    # st.write(mode)

    # Jewelry type selection from the list
    jewelry_type = st.sidebar.selectbox("Select Jewelry Type", [x for x in products])

    # Create two columns: left for image, right for data extraction
    col1, col2 = st.columns(2)

    if uploaded_image is not None:
        # Display image in left column with styling
        with col1:
            image = np.array(Image.open(uploaded_image))
            st.image(image, caption="Uploaded Jewelry Image", use_column_width=True)

        # Extract data and display in right column
        with col2:
            if mode!="None":
                st.markdown(f"<h2 class='header-text'>Grade for Uploaded {jewelry_type} image in {mode} Type </h2>", unsafe_allow_html=True)
            else:
                st.markdown(f"<h2 class='header-text'>Grade for Uploaded {jewelry_type} image </h2>", unsafe_allow_html=True)
            # Extract data from the image
            total, gold_wt, extracted_text, S_area = extract_table_data(image)

            if total or gold_wt:
                total = int(total)
                gold_wt = float(gold_wt)
                
                # Only process surface area if in 'Mirror' mode
                # if mode == "Mirror":
                S_area = float(S_area) if S_area else 0
                # st.write(total,gold_wt,S_area,jewelry_type,mode)
                
                total,gold_wt = jewel_type(total,gold_wt,jewelry_type, mode) 

                st.markdown(f"""
                    <div class='output-card'>
                        <p><strong>Total:</strong> {total} PCS</p>
                        <p><strong>Gold Weight:</strong> {gold_wt:.2f} g</p>
                        {f"<p><strong>Surface Area:</strong> {S_area} mm³</p>"} 
                    </div>
                """, unsafe_allow_html=True)#if mode == "Mirror" else ""
        
                try:
                    count = 1  
                    total_sum = 0
                    if mode == "Array":
                        total_sum += total_pieces(total)
                        total_sum += gold_weight(gold_wt)
                        count = 2
                    
                    elif mode == "Mirror":
                        total_sum += total_pieces(total)
                        total_sum += gold_weight(gold_wt)
                        total_sum += Sur(S_area)
                        count = 3

                    else:
                        total_sum += total_pieces(total)
                        total_sum += gold_weight(gold_wt)
                        total_sum += Sur(S_area)
                        count=3

                    if total==0:
                        count-=1
                    if gold_wt==0:
                        count-=1

                    # st.write(total_sum )

                    st.markdown(f"<div class='grade-output'>Grade: {round((total_sum / count), 1)}</div>", unsafe_allow_html=True)

                except ValueError:
                    st.write("Error: Unable to convert 'Total' or 'Gold Weight' to a number.")
            else:
                st.write("Could not find 'Total' or 'Gold Weight' in the image.")
    else:
        st.write("Please upload an image to begin.")

if __name__ == "__main__":
    main()
