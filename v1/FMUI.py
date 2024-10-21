import streamlit as st
import pandas as pd

def run_1():
    
    RA,GA,Summ = st.tabs(["Regional Assessment", "Global Assessment", "Summary"])
    with RA:
        st.subheader("Is there a clear client requirement to hire a specific finance leader role from at least 1 region?")
        ams = [None,'Argentina','Brazil','Canada','Chile','Colombia','Costa Rica','Dominican Republic','Honduras','Mexico','Panama','Peru','United States','Uruguay']
        emea = [None,'Austria','Belgium','Bulgaria','Croatia','Cyprus','Czech Republic','Denmark','Finland','Germany','Greece','Hungary','Ireland','Israel','Italy','Luxembourg','Netherlands','Norway','Poland','Portugal','Romania','Russia','Saudi Arabia','Serbia','Slovakia','Slovenia','Spain','Sweden','Switzerland','Turkey','Ukraine','United Kingdom']
        apac = [None,'Australia','China','Hong Kong','India','Indonesia','Japan','Malaysia','New Zealand','Philippines','Singapore','South Korea','Taiwan','Thailand','Vietnam']
        all_countries = [None,'Argentina','Brazil','Canada','Chile','Colombia','Costa Rica','Dominican Republic','Honduras','Mexico','Panama','Peru','United States','Uruguay',
                        'Austria','Belgium','Bulgaria','Croatia','Cyprus','Czech Republic','Denmark','Finland','Germany','Greece','Hungary','Ireland','Israel','Italy','Luxembourg','Netherlands','Norway','Poland','Portugal','Romania','Russia','Saudi Arabia','Serbia','Slovakia','Slovenia','Spain','Sweden','Switzerland','Turkey','Ukraine','United Kingdom'
                        ,'Australia','China','Hong Kong','India','Indonesia','Japan','Malaysia','New Zealand','Philippines','Singapore','South Korea','Taiwan','Thailand','Vietnam']
        Role = [None, "Finance Director", "Sr Finance Manager", "Finance Manager"]
        Regions = ['AMERICAS', 'EMEA', 'APAC']

        sma, ema, pma = None, None, None

        ctry_ams = []
        ctry_emea = []
        ctry_apac = []

        cv1 = ">50M of Managed Spend"
        cv2 = ">20<50M of Managed Spend"
        cv3 = "<20M of Managed Spend"
        pr1 = ">2.5M fees at risk"
        pr2 = "1M-2.5M fees at risk"
        pr3 = "<1M fees at risk"
        go1 = ">15M opportunity for growth"
        go2 = "5M-15M opportunity for growth"
        go3 = "<5M opportunity for growth"
        apcv1 = ">40M of Managed Spend"
        apcv2 = ">15<40M of Managed Spend"
        apcv3 = "<15M of Managed Spend"
        appr1 = ">2M fees at risk"
        appr2 = "0.75M-2M fees at risk"
        appr3 = "<0.75M fees at risk"
        apgo1 = ">12M opportunity for growth"
        apgo2 = "3M-12M opportunity for growth"
        apgo3 = "<3M opportunity for growth"

        cv = ["None", cv1, cv2, cv3]
        pr = ["None", pr1, pr2, pr3]
        go = ["None", go1, go2, go3]
        apcv = ["None", apcv1, apcv2, apcv3]
        appr = ["None", appr1, appr2, appr3]
        apgo = ["None", apgo1, apgo2, apgo3]
        cams, cemea, capac = 0,0,0
    
        col1 = st.selectbox(r"$\textbf{\small AMERICAS}$", ["None", "Finance Director", "Sr Finance Manager", "Finance Manager"], key="americas", index=0)
        if col1 in ["None"]:
            colA1, colA2, colA3 = st.columns(3)
            
            colA1 = colA1.selectbox("Contract Value", cv, key = "AMS_contract", index=0 )
            colA2 = colA2.selectbox("Performance Risk", pr, key = "AMS_pr", index=0)
            colA3 = colA3.selectbox("Growth Opportunity", go, key = "AMS_Go", index=0)

            if (colA1 == cv1 and colA2 == pr1 and colA3 ==go1) or (colA1 == cv1 and colA2 == pr1 and colA3 !=go1) or (colA1 == cv1 and colA2 != pr1 and colA3 ==go1) or (colA1 != cv1 and colA2 == pr1 and colA3 ==go1):
                    sma = "Finance Director"
                    st.write(sma)
            elif (colA1 == cv2 and colA2 == pr2 and colA3 ==go2) or (colA1 == cv2 and colA2 == pr2 and colA3 !=go2) or (colA1 == cv2 and colA2 != pr2 and colA3 ==go2) or (colA1 != cv2 and colA2 == pr2 and colA3 ==go2):
                    sma = "Sr Finance Manager"
                    st.write(sma)
            elif (colA1 == cv3 and colA2 == pr3 and colA3 ==go3) or (colA1 == cv3 and colA2 == pr3 and colA3 !=go3) or (colA1 == cv3 and colA2 != pr3 and colA3 ==go3) or (colA1 != cv3 and colA2 == pr3 and colA3 ==go3):
                    sma = "Finance Manager"
                    st.write(sma)
            elif (colA1 == "None" and colA2 == "None" and colA3 == "None") or (colA1 in cv and colA2 == "None" and colA3 == "None") or (colA1 == "None" and colA2 in pr and colA3 == "None") or (colA1 == "None" and colA2 == "None" and colA3 in go):
                    sma = "None"
                    st.write(sma)
            else:
                sma = "Finance Director"
                st.write(sma)
            
            cams = cams + 1 if sma != "None" else 0

        else:
            st.write(col1)
            cams = cams + 1             

        col2 = st.selectbox(r"$\textbf{\small EMEA}$", ["None", "Finance Director", "Sr Finance Manager", "Finance Manager"], key="emea", index=0)
        if col2 in ["None"]:
            colB1, colB2, colB3 = st.columns(3)
            colB1 = colB1.selectbox("Contract Value", cv, key = "EMEA_ca", index=0)
            colB2 = colB2.selectbox("Performance Risk", pr, key = "EMEA_pre", index=0)
            colB3 = colB3.selectbox("Growth Opportunity", go, key = "EMEA_goe", index=0)
            if (colB1 == cv1 and colB2 == pr1 and colB3 ==go1) or (colB1 == cv1 and colB2 == pr1 and colB3 !=go1) or (colB1 == cv1 and colB2 != pr1 and colB3 == go1) or (colB1 != cv1 and colB2 == pr1 and colB3 ==go1):
                    ema = "Finance Director"
                    st.write(ema)
            elif (colB1 == cv2 and colB2 == pr2 and colB3 ==go2) or (colB1 == cv2 and colB2 == pr2 and colB3 !=go2) or (colB1 == cv2 and colB2 != pr2 and colB3 == go2) or (colB1 != cv2 and colB2 == pr2 and colB3 ==go2):
                    ema = "Sr Finance Manager"
                    st.write(ema)
            elif (colB1 == cv3 and colB2 == pr3 and colB3 ==go3) or (colB1 == cv3 and colB2 == pr3 and colB3 !=go3) or (colB1 == cv3 and colB2 != pr3 and colB3 ==go3) or (colB1 != cv3 and colB2 == pr3 and colB3 == go3):
                    ema = "Finance Manager"
                    st.write(ema)
            elif (colB1 == "None" and colB2 == "None" and colB3 == "None") or (colB1 in cv and colB2 == "None" and colB3 == "None") or (colB1 == "None" and colB2 in pr and colB3 == "None") or (colB1 == "None" and colB2 == "None" and colB3 in go):
                    ema = "None"
                    st.write(ema)
            else:
                ema = "Finance Director"
                st.write(ema)
            cemea = cemea + 1 if ema != "None" else 0

        else:
            st.write(col2)
            cemea = cemea + 1

        col3 = st.selectbox(r"$\textbf{\small APAC}$", ["None", "Finance Director", "Sr Finance Manager", "Finance Manager"], key="apac", index=0)
        if col3 in ["None"]:
            colC1, colC2, colC3 = st.columns(3)
            colC1 = colC1.selectbox("Contract Value", apcv, key = "APAC_ca", index=0)
            colC2 = colC2.selectbox("Performance Risk", appr, key = "APAC_pra", index=0)
            colC3 = colC3.selectbox("Growth Opportunity", apgo, key = "APAC_go", index=0)
            if (colC1 == apcv1 and colC2 == appr1 and colC3 ==apgo1) or (colC1 == apcv1 and colC2 == appr1 and colC3 !=apgo1) or (colC1 == apcv1 and colC2 != appr1 and colC3 == apgo1) or (colC1 != apcv1 and colC2 == appr1 and colC3 == apgo1):
                    pma = "Finance Director"
                    st.write(pma)
            elif (colC1 == apcv2 and colC2 == appr2 and colC3 == apgo2) or (colC1 == apcv2 and colC2 == appr2 and colC3 != apgo2) or (colC1 == apcv2 and colC2 != appr2 and colC3 == apgo2) or (colC1 != apcv2 and colC2 == appr2 and colC3 == apgo2):
                    pma = "Sr Finance Manager"
                    st.write(pma)
            elif (colC1 == apcv3 and colC2 == appr3 and colC3 == apgo3) or (colC1 == apcv3 and colC2 == appr3 and colC3 != apgo3) or (colC1 == apcv3 and colC2 != appr3 and colC3 == apgo3) or (colC1 != apcv3 and colC2 == appr3 and colC3 == apgo3):
                    pma = "Finance Manager"
                    st.write(pma)
            elif (colC1 == "None" and colC2 == "None" and colC3 == "None") or (colC1 in apcv and colC2 == "None" and colC3 == "None") or (colC1 == "None" and colC2 in appr and colC3 == "None") or (colC1 == "None" and colC2 == "None" and colC3 in apgo):
                    pma = "None"
                    st.write(pma)
            else:
                pma = "Finance Director"
                st.write(pma)
            capac = capac + 1 if pma != "None" else 0
        
        else:
            st.write(col3)
            capac = capac + 1
        
        st.subheader("Recommended Regional Finance Management Roles")
        colA,colB,colC,colD = st.columns(4)
        colA.write("------")
        colB.write("AMERICAS")
        colC.write("EMEA")
        colD.write("APAC")
        colE,colF,colG,colH = st.columns(4)
        colE.write("Recommended Role:")
        colF.write(col1 if col1 not in ["None"] else sma)
        colG.write(col2 if col2 not in ["None"] else ema)
        colH.write(col3 if col3 not in ["None"] else pma)
        colI,colJ,colK,colL = st.columns(4)
        colI = colI.write("Indicate country-location of role:")
        colJ = colJ.selectbox(label="",options = ams, key = "ams1", index =0)
        colK = colK.selectbox(label="",options = emea, key = "emea1", index=0)
        colL = colL.selectbox(label="",options = apac, key = "apac1", index=0)
        colM,colN,colO,colP = st.columns(4)
        colM = colM.write("FTE")
        
        colN = colN.write(cams)
        colO = colO.write(cemea)
        colP = colP.write(capac)
        
    with GA:
        st.subheader("Global Assessment")

        st.write("Indicate the regions in scope under this deal?")

        selected_regions = []
        for i in range(len(Regions)):
            reg = st.checkbox(Regions[i])
            if reg:
                selected_regions.append(Regions[i])
        count_r = len(selected_regions)

        st.write("")
        st.write("")
        st.subheader("Is there a clear client requirement to hire a global finance leader role?")
        YN = st.radio("", ("Yes", "No"), horizontal=True, key = "global_assessment_yn", index=0)
        if YN == "No":
            location = None
            managed_spend = st.radio("Indicate the total global managed spend under this deal?"  , options = ["Below 50M Managed Spend", "Above 50M Managed Spend"], key = "managed_spend", index= None)

            st.subheader("Recommended Global Finance Management Role")
            col22,col33 = st.columns(2)
            col22.write("Recommended Role:")
            if count_r > 1 and managed_spend == "Above 50M Managed Spend":
                col33 = col33.write("Global Finance Director")
                col44,col55 = st.columns(2)
                col44 = col44.write("Country-location of role:")
                col55 = col55.selectbox(label="",options = all_countries, key= "all_countries")
                location = col55
            elif count_r == 1:
                col33 = col33.write("No Role Recommended")
                col44,col55 = st.columns(2)
                col44 = col44.write("Country-location of role:")
                col55 = col55.write(None)
                location = col55
            else: 
                col33 = col33.write("Finance Director")
                col44,col55 = st.columns(2)
                col44 = col44.write("Country-location of role:")
                col55 = col55.selectbox(label="",options = all_countries, key= "all_countries")
                location = col55

        else:
            st.subheader("Recommended Global Finance Management Role")
            col22,col33 = st.columns(2)
            col22.write("Recommended Role:")
            col33 = col33.write("Global Finance Director")

            col44,col55 = st.columns(2)
            col44 = col44.write("Country-location of role:")
            col55 = col55.selectbox(label="",options = all_countries, key= "all_countries")        

    #------------------------------------------------------------------------------------
    with Summ:
        st.title("Summary")
        if YN == "Yes":
            dfgr = pd.DataFrame({"Regional Role":["Global Finance Director","-----",sma if col1 =="None" else col1,ema if col2 =="None" else col2,pma if col3 =="None" else col3], "FTE":[1,"-----",cams,cemea,capac],"location":[col55,"-----", "TBC", "TBC", "TBC"]},index=["Global Role","Regional Roles","AMERICAS","EMEA","APAC"])
            
        else:
            if count_r > 1 and managed_spend == "Above 50M Managed Spend":
                dfgr = pd.DataFrame({"Regional Role":["Global Finance Director","-----",sma if col1 =="None" else col1,ema if col2 =="None" else col2,pma if col3 =="None" else col3], "FTE":[1,"-----",cams,cemea,capac],"location":[col55,"-----", "TBC", "TBC", "TBC"]},index=["Global Role","Regional Roles","AMERICAS","EMEA","APAC"])
                
            elif count_r == 0 and managed_spend not in ["Below 50M Managed Spend", "Above 50M Managed Spend"]:
                dfgr = pd.DataFrame({"Regional Role":[None, "-----",sma if col1 =="None" else col1,ema if col2 =="None" else col2,pma if col3 =="None" else col3], "FTE":[0,"-----",cams,cemea,capac],"location":[col55,"-----", "TBC", "TBC", "TBC"]},index=["Global Role","Regional Roles","AMERICAS","EMEA","APAC"])

            elif count_r == 1:
                dfgr = pd.DataFrame({"Regional Role":["No Role Recommended", "-----",sma if col1 =="None" else col1,ema if col2 =="None" else col2,pma if col3 =="None" else col3], "FTE":[0,"-----",cams,cemea,capac],"location":[col55,"-----", "TBC", "TBC", "TBC"]},index=["Global Role","Regional Roles","AMERICAS","EMEA","APAC"])
                
            else:
                dfgr = pd.DataFrame({"Regional Role":["Finance Director","-----",sma if col1 =="None" else col1,ema if col2 =="None" else col2,pma if col3 =="None" else col3], "FTE":[1,"-----",cams,cemea,capac],"location":[col55,"-----", "TBC", "TBC", "TBC"]},index=["Global Role","Regional Roles","AMERICAS","EMEA","APAC"])
                
        st.write(dfgr)
if __name__ == "__main__":
    run_1()
