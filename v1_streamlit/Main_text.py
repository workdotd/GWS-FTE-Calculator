# -*- coding: utf-8 -*-
"""
Created on Thu May  9 11:32:09 2024

@author: SKureley
"""


import streamlit as st
import FMUI
import AMS_calculator,EMEA_calculator,APAC_calculator
from PIL import Image
import base64


    
image = Image.open("Cbre_logo.jpg")

st.set_page_config(page_title="Finance FTE Calculator",page_icon=image,layout="centered")



sidebar_text = """ Info
1) This finance FTE calculator is not a substitute for actual solutioning.
                The best practice is still to solution and put forward a finance team based on 
                a detailed understanding of client requirements and performance expectation.
                
2) This calculator provides 2 key advantages: 

   (1) It calculates a data-driven “base model” for finance team, that the solution
       team can refine further or build on according to client requirements; 
   
   (2) It provides an intelligent benchmark against which a solution or 
       price can be measured and evaluated.
                
3) Artificial intelligence or machine learning used in this tool does not 
replace valuable human critical thinking and solutioning. AI used in this
tool is meant to augment human intelligence and productivity by increasing
efficiency and accuracy in the solutioning process."""
                
st.sidebar.markdown(sidebar_text)

st.markdown(
   """
<style>
html, body{
    height: 100%;
    margin: 0;
    padding: 0;
    overflow: hidden;
}
[data-testid="stAppViewBlockContainer"] {
   background-color: #CAD1D3;
   display: flex;
   flex-direction: column;
   align-items: center;
   justify-content: flex-start;
   width: auto;
   height: auto;
   padding: 20px; /* Adjust as necessary */
   margin: auto;
   box-sizing: border-box;
   max-width: 100%; /* Ensure it doesn't exceed the viewport */
   max-height: 100%; /* Ensure it doesn't exceed the viewport */
   overflow-y: auto;
   font-family: Financier Display;
}

[data-testid="stExpander"]{
    background-color: white;
    width: 100%;
    box-sizing: border-box;
    font-family: calibre !important;
        }
[data-testid="stVerticalBlockBorderWrapper"]{
    font-family: calibre !important;
    
        }

[data-testid="stSidebarContent"]{
    background-color: #7F8480;
    font-family: calibre;
    color: white;
        }
h3
    {
    color: #012A2D;
    font-family: calibre;
    font-weight: 300;
    }
.st-bp{
    font-family: calibre !important;
    color: #012A2D;
           }
.mord.textbf.sizing.reset-size6.size5{
    font-family: calibre !important;
    color: #012A2D;
    }
</style>
   """,
   unsafe_allow_html=True
)


st.markdown("""<style>footer {visibility: hidden;}</style>""", unsafe_allow_html=True)
st.markdown("""<style>header {visibility: hidden;}</style>""", unsafe_allow_html=True)

def add_bg_from_local(image_file):
        with open(image_file, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read())
        st.markdown(
        f"""
<style>
        .stApp {{
            background-image: url(data:Image/{"jpeg"};base64,{encoded_string.decode()});
            background-size: cover
            }}
</style>
        """,
        unsafe_allow_html=True
        )
        
add_bg_from_local('Image_background.jpeg')



st.markdown(
   """
<style>
   /* Button text color */
   .stButton>button {
       color: white; /* Change to desired text color */
   }
   /* Button text color when clicked */
   .stButton>button:active {
       color: #ffffff; /* Change to desired text color when clicked */
   }
   /* Button background color */
   .stButton>button {
       background-color: #003F2D; /* Change to desired background color */
   }
</style>
   """,unsafe_allow_html=True
)

col1,col2 = st.columns([1,4])


with col1:
    st.image("Cbre_logo.jpg",width=130)
with col2:
    st.markdown(
   """
<div>
    <span id="gws-enterprise">
    GWS Enterprise </span><br>
    <span id="fte-enterprise">
    Finance FTE Calculator </span><br>
</div>
   """,
   unsafe_allow_html=True
)
# Custom CSS to change the font and style
st.markdown(
   """
<style>

   #gws-enterprise {
       font-family: calibre;
       font-size: 25px;
       color: #012A2D;
       margin:20px 0 0 0;
       line-height: 1;
       }
    
    #fte-enterprise {
        font-family: Financier Display;
        font-size: 50px;
        color: #012A2D;
        margin:0;
        line-height:1;
        
    }
</style>
   """,
   unsafe_allow_html=True
)
    


st.subheader("1. Finance Management")
with st.expander("Finance Management"):
      FMUI.run_1()

st.subheader("2. Finance Delivery")
 
with st.expander("2a. AMS"):
              AMS_calculator.run_2()  

with st.expander("2b. EMEA"):
             EMEA_calculator.run_3()
    
with st.expander("2c. APAC"):
           APAC_calculator.run_4()
          
          
         