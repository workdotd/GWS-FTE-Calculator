import pandas as pd
import numpy as np
import joblib
import math as mt
import uuid
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import logging
import dbconn
import os


app = FastAPI()
#-----------------------------------------------------------------------------------------------------------------------

sma, ema, pma = None, None, None

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
role = None

cv = ["None", cv1, cv2, cv3]
pr = ["None", pr1, pr2, pr3]
go = ["None", go1, go2, go3]
apcv = ["None", apcv1, apcv2, apcv3]
appr = ["None", appr1, appr2, appr3]
apgo = ["None", apgo1, apgo2, apgo3]
cams, cemea, capac = 0,0,0

activities = ['1.Billing', '2.Fund Reconciliations', '3.Payment',
                '4.Monthly JDE period close and Open PO review',
                '5.Monthly JDE Balance Sheet Reconciliation',
                '6.Corporate Month End Revenue/Costs Adjustments',
                '7.Corporate Pass Through Reconciliation',
                '8.Corporate Payment Entries Submission',
                '9.Internal & External Audit Sampling Requests (SOC1 & SOX)',
                '10.Corporate P&L Month End Review, Analysis & Queries',
                '11.Corporate Yearly Budget - Preparation, Review & Approval',
                '12.Corporate Monthly Forecast - Preparation, Review & Approval',
                '13.Corporate Operation Merit & Bonus Review',
                '14.Client Month End Accruals - Open PO, Rental, Utilities etc. - Manual Journal Entries Posting',
                '15.Monthly Operational Call for Client Month End Close (Queries from FM - Finance Related)',
                '16.Client Budget - Management Fee & Payroll Calculation; Vendor Spend Data',
                '17.Client Forecast - Vendor Spend',
                '18.Client Savings Report',
                '19.Client Finance Audit Support',
                '20.Client Billing to Actuals Reconciliation',
                'Standard Report',
                'Customised Report']

cvs = ["Contract Structure","Spend Ratio","Principal/MA","Client Reporting Level","Tech Stack","Automation Adjustment","Bank Account"]
contract_vars = {
              "Contract Structure": {"GMP": 0.90, "Cost Plus": 1.00, "Fixed Price": 0.90, "Other": 1.20},
              "Spend Ratio": {"25% fixed; 75% variable": 1.20, "50% fixed; 50% variable": 1.00, "75% fixed; 25% variable": 0.90},
              "Principal/MA": {"Full Principal (immaterial agency spend)": 1.00, "Full Managing Agent (immaterial principal spend)": 0.10, "50% Principal; 50% MA": 0.60, "25% Principal; 75% MA":0.40, "75% Principal; 25% MA": 0.90 },
              "Client Reporting Level": {"Country-level": 0.90, "Site-level": 1.00, "Cost-center level": 1.20},
              "Tech Stack": {"Standard - Mybuy/JDE/PS": 1.00, "Full Iscala": 0.90, "Full PS": 1.10, "Non-standard": 1.20},
              "Automation Adjustment": {"High": 0.75, "Mid": 0.85, "Low": 0.90, "None": 1.00},
              "Bank Account": {"Dedicated": 1.00, "Shared/Ded": 1.10, "Corporate": 1.20}
          }

frequency_options = { 'Monthly': 1,'None': 0, 'Weekly': 4, 'Bi-Weekly': 2, 'Quarterly': 0.333333333333333, 'Yearly': 0.083}

LCA = ['1.Billing','2.Fund Reconciliations','3.Payment','4.Monthly JDE period close and Open PO review',
       '5.Monthly JDE Balance Sheet Reconciliation','6.Corporate Month End Revenue/Costs Adjustments',
       '7.Corporate Pass Through Reconciliation','8.Corporate Payment Entries Submission','9.Internal & External Audit Sampling Requests (SOC1 & SOX)',
       '10.Corporate P&L Month End Review, Analysis & Queries','12.Corporate Monthly Forecast - Preparation, Review & Approval',
       '17.Client Forecast - Vendor Spend','19.Client Finance Audit Support']
MCA = ['14.Client Month End Accruals - Open PO, Rental, Utilities etc. - Manual Journal Entries Posting',
       '15.Monthly Operational Call for Client Month End Close (Queries from FM - Finance Related)',
       '16.Client Budget - Management Fee & Payroll Calculation; Vendor Spend Data',
       '18.Client Savings Report''Standard Report']
HCA = ['11.Corporate Yearly Budget - Preparation, Review & Approval','13.Corporate Operation Merit & Bonus Review',
       '20.Client Billing to Actuals Reconciliation','Customised Report']
inputs = pd.read_excel("Inputs.xlsx", 'Sheet2')

#-------------------------------------------Finance Management Functions---------------------------------------------------------------------------------------------------
radf = pd.DataFrame(columns = ['RA Region', "Selected Role", "Contract Value", "Performance Risk", "Growth Opportunity", "GA Region_count", "Global Role Req", "Global Managed Spend","location"])
def fmanagement(radf: pd.DataFrame):

    if radf['RA Region'].eq("APAC").any():
        if (radf["Contract Value"].eq(apcv1).any() and radf["Performance Risk"].eq(appr1).any() and radf["Growth Opportunity"].eq(apgo1).any()) or (radf["Contract Value"].eq(apcv1).any() and radf["Performance Risk"].eq(appr1).any() and radf["Growth Opportunity"].ne(apgo1).any()) or (radf["Contract Value"].eq(apcv1).any() and radf["Performance Risk"].ne(appr1).any() and radf["Growth Opportunity"].eq(apgo1).any()) or (radf["Contract Value"].ne(apcv1).any() and radf["Performance Risk"].eq(appr1).any() and radf["Growth Opportunity"].eq(apgo1).any()):
            role = "Finance Director"
        elif (radf["Contract Value"].eq(apcv2).any() and radf["Performance Risk"].eq(appr2).any() and radf["Growth Opportunity"].eq(apgo2).any()) or (radf["Contract Value"].eq(apcv2).any() and radf["Performance Risk"].eq(appr2).any() and radf["Growth Opportunity"].ne(apgo2).any()) or (radf["Contract Value"].eq(apcv2).any() and radf["Performance Risk"].ne(appr2).any() and radf["Growth Opportunity"].eq(apgo2).any()) or (radf["Contract Value"].ne(apcv2).any() and radf["Performance Risk"].eq(appr2).any() and radf["Growth Opportunity"].eq(apgo2).any()):
            role = "Sr Finance Manager"
        elif (radf["Contract Value"].eq(apcv3).any() and radf["Performance Risk"].eq(appr3).any() and radf["Growth Opportunity"].eq(apgo3).any()) or (radf["Contract Value"].eq(apcv3).any() and radf["Performance Risk"].eq(appr3).any() and radf["Growth Opportunity"].ne(apgo3).any()) or (radf["Contract Value"].eq(apcv3).any() and radf["Performance Risk"].ne(appr3).any() and radf["Growth Opportunity"].eq(apgo3).any()) or (radf["Contract Value"].ne(apcv3).any() and radf["Performance Risk"].eq(appr3).any() and radf["Growth Opportunity"].eq(apgo3).any()):
            role = "Finance Manager"
        elif (radf["Contract Value"].eq("None").any() and radf["Performance Risk"].eq("None").any() and radf["Growth Opportunity"].eq("None").any()) or (radf["Contract Value"].isin(apcv).any() and radf["Performance Risk"].eq("None").any() and radf["Growth Opportunity"].eq("None").any()) or (radf["Contract Value"].eq("None").any() and radf["Performance Risk"].isin(appr).any() and radf["Growth Opportunity"].eq("None").any()) or (radf["Contract Value"].eq("None").any() and radf["Performance Risk"].eq("None").any() and radf["Growth Opportunity"].isin(apgo).any()):
            role = "None"
        else:
            role = "Finance Director"
    else:
        if (radf["Contract Value"].eq(cv1).any() and radf["Performance Risk"].eq(pr1).any() and radf["Growth Opportunity"].eq(go1).any()) or (radf["Contract Value"].eq(cv1).any() and radf["Performance Risk"].eq(pr1).any() and radf["Growth Opportunity"].ne(go1).any()) or (radf["Contract Value"].eq(cv1).any() and radf["Performance Risk"].ne(pr1).any() and radf["Growth Opportunity"].eq(go1).any()) or (radf["Contract Value"].ne(cv1).any() and radf["Performance Risk"].eq(pr1).any() and radf["Growth Opportunity"].eq(go1).any()):
            role = "Finance Director"
        elif (radf["Contract Value"].eq(cv2).any() and radf["Performance Risk"].eq(pr2).any() and radf["Growth Opportunity"].eq(go2).any()) or (radf["Contract Value"].eq(cv2).any() and radf["Performance Risk"].eq(pr2).any() and radf["Growth Opportunity"].ne(go2).any()) or (radf["Contract Value"].eq(cv2).any() and radf["Performance Risk"].ne(pr2).any() and radf["Growth Opportunity"].eq(go2).any()) or (radf["Contract Value"].ne(cv2).any() and radf["Performance Risk"].eq(pr2).any() and radf["Growth Opportunity"].eq(go2).any()):
            role = "Sr Finance Manager"
        elif (radf["Contract Value"].eq(cv3).any() and radf["Performance Risk"].eq(pr3).any() and radf["Growth Opportunity"].eq(go3).any()) or (radf["Contract Value"].eq(cv3).any() and radf["Performance Risk"].eq(pr3).any() and radf["Growth Opportunity"].ne(go3).any()) or (radf["Contract Value"].eq(cv3).any() and radf["Performance Risk"].ne(pr3).any() and radf["Growth Opportunity"].eq(go3).any()) or (radf["Contract Value"].ne(cv3).any() and radf["Performance Risk"].eq(pr3).any() and radf["Growth Opportunity"].eq(go3).any()):
            role = "Finance Manager"
        elif (radf["Contract Value"].eq("None").any() and radf["Performance Risk"].eq("None").any() and radf["Growth Opportunity"].eq("None").any()) or (radf["Contract Value"].isin(cv).any() and radf["Performance Risk"].eq("None").any() and radf["Growth Opportunity"].eq("None").any()) or (radf["Contract Value"].eq("None").any() and radf["Performance Risk"].isin(pr).any() and radf["Growth Opportunity"].eq("None").any()) or (radf["Contract Value"].eq("None").any() and radf["Performance Risk"].eq("None").any() and radf["Growth Opportunity"].isin(go).any()):
            role = "None"
        else:
            role = "Finance Director"

    radf["RA Calc Role"] = radf["Selected Role"].where(radf["Selected Role"] != "None", role)
    fmdf = radf.reindex(columns = ['RA Region', 'Selected Role', 'Contract Value', 'Performance Risk',
        'Growth Opportunity','RA Calc Role','RA FTE Count','RA Location','GA Region_count', 'Global Role Req',
        'Global Managed Spend', 'Location'])
    fmdf['RA FTE Count'] = 1
    fmdf['RA Location'] = "TBC"

    roleams = fmdf['RA Calc Role'][0]
    roleemea = fmdf['RA Calc Role'][1]
    roleapac = fmdf['RA Calc Role'][2]
    globalloc = fmdf['Location'][0]

    count_r = radf["GA Region_count"]
    gflr = radf["Global Role Req"]
    managed_spend = radf["Global Managed Spend"]

    if gflr.eq("No").any():
        if count_r.gt(1).any() and managed_spend.eq("Above 50M Managed Spend").any():
            garr = "Global Finance Director"
            
        elif count_r.le(1).any() and managed_spend.eq("Above 50M Managed Spend").any():
            garr = "No Role Recommended"

        else: 
            garr = "Finance Director"

    else:
        garr = "Global Finance Director"

    fmsumm = pd.DataFrame({"Role": [garr,"-----",roleams,roleemea,roleapac], "FTE":[1,"-----",1,1,1],"location":[globalloc,"-----", "TBC", "TBC", "TBC"]},index=["Global Role","Regional Roles","AMERICAS","EMEA","APAC"])
    

    return fmsumm

def fmsumdnld(radf: pd.DataFrame):
    
    if radf['RA Region'].eq("APAC").any():
        if (radf["Contract Value"].eq(apcv1).any() and radf["Performance Risk"].eq(appr1).any() and radf["Growth Opportunity"].eq(apgo1).any()) or (radf["Contract Value"].eq(apcv1).any() and radf["Performance Risk"].eq(appr1).any() and radf["Growth Opportunity"].ne(apgo1).any()) or (radf["Contract Value"].eq(apcv1).any() and radf["Performance Risk"].ne(appr1).any() and radf["Growth Opportunity"].eq(apgo1).any()) or (radf["Contract Value"].ne(apcv1).any() and radf["Performance Risk"].eq(appr1).any() and radf["Growth Opportunity"].eq(apgo1).any()):
            role = "Finance Director"
        elif (radf["Contract Value"].eq(apcv2).any() and radf["Performance Risk"].eq(appr2).any() and radf["Growth Opportunity"].eq(apgo2).any()) or (radf["Contract Value"].eq(apcv2).any() and radf["Performance Risk"].eq(appr2).any() and radf["Growth Opportunity"].ne(apgo2).any()) or (radf["Contract Value"].eq(apcv2).any() and radf["Performance Risk"].ne(appr2).any() and radf["Growth Opportunity"].eq(apgo2).any()) or (radf["Contract Value"].ne(apcv2).any() and radf["Performance Risk"].eq(appr2).any() and radf["Growth Opportunity"].eq(apgo2).any()):
            role = "Sr Finance Manager"
        elif (radf["Contract Value"].eq(apcv3).any() and radf["Performance Risk"].eq(appr3).any() and radf["Growth Opportunity"].eq(apgo3).any()) or (radf["Contract Value"].eq(apcv3).any() and radf["Performance Risk"].eq(appr3).any() and radf["Growth Opportunity"].ne(apgo3).any()) or (radf["Contract Value"].eq(apcv3).any() and radf["Performance Risk"].ne(appr3).any() and radf["Growth Opportunity"].eq(apgo3).any()) or (radf["Contract Value"].ne(apcv3).any() and radf["Performance Risk"].eq(appr3).any() and radf["Growth Opportunity"].eq(apgo3).any()):
            role = "Finance Manager"
        elif (radf["Contract Value"].eq("None").any() and radf["Performance Risk"].eq("None").any() and radf["Growth Opportunity"].eq("None").any()) or (radf["Contract Value"].isin(apcv).any() and radf["Performance Risk"].eq("None").any() and radf["Growth Opportunity"].eq("None").any()) or (radf["Contract Value"].eq("None").any() and radf["Performance Risk"].isin(appr).any() and radf["Growth Opportunity"].eq("None").any()) or (radf["Contract Value"].eq("None").any() and radf["Performance Risk"].eq("None").any() and radf["Growth Opportunity"].isin(apgo).any()):
            role = "None"
        else:
            role = "Finance Director"
    else:
        if (radf["Contract Value"].eq(cv1).any() and radf["Performance Risk"].eq(pr1).any() and radf["Growth Opportunity"].eq(go1).any()) or (radf["Contract Value"].eq(cv1).any() and radf["Performance Risk"].eq(pr1).any() and radf["Growth Opportunity"].ne(go1).any()) or (radf["Contract Value"].eq(cv1).any() and radf["Performance Risk"].ne(pr1).any() and radf["Growth Opportunity"].eq(go1).any()) or (radf["Contract Value"].ne(cv1).any() and radf["Performance Risk"].eq(pr1).any() and radf["Growth Opportunity"].eq(go1).any()):
            role = "Finance Director"
        elif (radf["Contract Value"].eq(cv2).any() and radf["Performance Risk"].eq(pr2).any() and radf["Growth Opportunity"].eq(go2).any()) or (radf["Contract Value"].eq(cv2).any() and radf["Performance Risk"].eq(pr2).any() and radf["Growth Opportunity"].ne(go2).any()) or (radf["Contract Value"].eq(cv2).any() and radf["Performance Risk"].ne(pr2).any() and radf["Growth Opportunity"].eq(go2).any()) or (radf["Contract Value"].ne(cv2).any() and radf["Performance Risk"].eq(pr2).any() and radf["Growth Opportunity"].eq(go2).any()):
            role = "Sr Finance Manager"
        elif (radf["Contract Value"].eq(cv3).any() and radf["Performance Risk"].eq(pr3).any() and radf["Growth Opportunity"].eq(go3).any()) or (radf["Contract Value"].eq(cv3).any() and radf["Performance Risk"].eq(pr3).any() and radf["Growth Opportunity"].ne(go3).any()) or (radf["Contract Value"].eq(cv3).any() and radf["Performance Risk"].ne(pr3).any() and radf["Growth Opportunity"].eq(go3).any()) or (radf["Contract Value"].ne(cv3).any() and radf["Performance Risk"].eq(pr3).any() and radf["Growth Opportunity"].eq(go3).any()):
            role = "Finance Manager"
        elif (radf["Contract Value"].eq("None").any() and radf["Performance Risk"].eq("None").any() and radf["Growth Opportunity"].eq("None").any()) or (radf["Contract Value"].isin(cv).any() and radf["Performance Risk"].eq("None").any() and radf["Growth Opportunity"].eq("None").any()) or (radf["Contract Value"].eq("None").any() and radf["Performance Risk"].isin(pr).any() and radf["Growth Opportunity"].eq("None").any()) or (radf["Contract Value"].eq("None").any() and radf["Performance Risk"].eq("None").any() and radf["Growth Opportunity"].isin(go).any()):
            role = "None"
        else:
            role = "Finance Director"

    radf["RA Calc Role"] = radf["Selected Role"].where(radf["Selected Role"] != "None", role)
    fmdf = radf.reindex(columns = ['RA Region', 'Selected Role', 'Contract Value', 'Performance Risk',
        'Growth Opportunity','RA Calc Role','RA FTE Count','RA Location','GA Region_count', 'Global Role Req',
        'Global Managed Spend', 'Location'])
    fmdf['RA FTE Count'] = 1
    fmdf['RA Location'] = "TBC"

    roleams = fmdf['RA Calc Role'][0]
    roleemea = fmdf['RA Calc Role'][1]
    roleapac = fmdf['RA Calc Role'][2]
    globalloc = fmdf['Location'][0]

    count_r = radf["GA Region_count"]
    gflr = radf["Global Role Req"]
    managed_spend = radf["Global Managed Spend"]

    if gflr.eq("No").any():
        if count_r.gt(1).any() and managed_spend.eq("Above 50M Managed Spend").any():
            garr = "Global Finance Director"
            
        elif count_r.eq(1).any():
            garr = "No Role Recommended"

        else: 
            garr = "Finance Director"

    else:
        garr = "Recommended Global Finance Management Role"

    fmsumm = pd.DataFrame({"Role": [garr,"-----",roleams,roleemea,roleapac], "FTE":[1,"-----",1,1,1],"location":[globalloc,"-----", "TBC", "TBC", "TBC"]},index=["Global Role","Regional Roles","AMERICAS","EMEA","APAC"])

    fmsumm.to_csv("fte_fm_sum.csv")

#-------------------------------------------Finance Delivery Functions---------------------------------------------------------------------------------------------------
def calculate_fte_requirement(df: pd.DataFrame):

    df['Contract Structure Multiplier'] = df['Contract Structure Option'].map(contract_vars['Contract Structure'])
    df['Spend Ratio Multiplier'] = df['Spend Ratio Option'].map(contract_vars['Spend Ratio'])
    df['Principal/MA Multiplier'] = df['Principal/MA Option'].map(contract_vars['Principal/MA'])
    df['Client Reporting Level Multiplier'] = df['Client Reporting Level Option'].map(contract_vars['Client Reporting Level'])
    df['Tech Stack Multiplier'] = df['Tech Stack Option'].map(contract_vars['Tech Stack'])
    df['Automation Adjustment Multiplier'] = df['Automation Adjustment Option'].map(contract_vars['Automation Adjustment'])
    df['Bank Account Multiplier'] = df['Bank Account Option'].map(contract_vars['Bank Account'])

    for index, row in inputs.iterrows():
        country = row['Country']
        activity = row['activity']
        time_spent = row['Time Spend/Country']
        
        # Check if the activity is in df columns
        if f'{activity}_freq' in df.columns:
            # Find the corresponding frequency option
            frequency_values = df.loc[df['Country'] == country, f'{activity}_freq'].values
            if len(frequency_values) > 0:
                frequency = frequency_values[0]
                multiplier = frequency_options.get(frequency, 1)
                
                # Update the df with the calculated value
                df.loc[df['Country'] == country, f'{activity}'] = time_spent * multiplier


    df['Total No of Sites'] = df['Number of Sites'].sum()
    df['Average Spend per Site'] = df['Total Managed Spend']/df['Total No of Sites']
    df['Spend per Country'] = df['Average Spend per Site'] * df['Number of Sites']

    if df['Region'].eq("APAC").any():
        df.loc[df['Average Spend per Site'] < 40000, 'Average Site Multiplier value'] = 0.6
        df.loc[(df['Average Spend per Site'] >= 40000) & (df['Average Spend per Site'] < 80000), 'Average Site Multiplier value'] = 0.8
        df.loc[(df['Average Spend per Site'] >= 80000) & (df['Average Spend per Site'] < 300000), 'Average Site Multiplier value'] = 1
        df.loc[(df['Average Spend per Site'] >= 300000) & (df['Average Spend per Site'] < 750000), 'Average Site Multiplier value'] = 1
        df.loc[df['Average Spend per Site'] >= 750000, 'Average Site Multiplier value'] = 1.1
        
    else:
        df.loc[df['Average Spend per Site'] < 80000, 'Average Site Multiplier value'] = 0.6
        df.loc[(df['Average Spend per Site'] >= 80000) & (df['Average Spend per Site'] < 150000), 'Average Site Multiplier value'] = 0.8
        df.loc[(df['Average Spend per Site'] >= 150000) & (df['Average Spend per Site'] < 500000), 'Average Site Multiplier value'] = 1
        df.loc[(df['Average Spend per Site'] >= 500000) & (df['Average Spend per Site'] < 1200000), 'Average Site Multiplier value'] = 1
        df.loc[df['Average Spend per Site'] >= 1200000, 'Average Site Multiplier value'] = 1.1

    df['Adjusted No of Sites/Country'] = df['Number of Sites']*df['Average Site Multiplier value']
    df['Adjusted No of Sites'] = df['Adjusted No of Sites/Country'].sum()

    df['1.Billing_adj'] = np.where(df['Adjusted No of Sites/Country'] <= 1,df['1.Billing'] * 2 ,df['1.Billing']*df['Adjusted No of Sites/Country'])

    df['Contrct_Spend_Auto_CRL_PMA'] = df['Contract Structure Multiplier']*df['Spend Ratio Multiplier']*df['Automation Adjustment Multiplier']*df['Client Reporting Level Multiplier']*df['Principal/MA Multiplier']
    df['Bank_PMA'] = df['Bank Account Multiplier']*df['Principal/MA Multiplier']
    df['tech_auto_pma'] = df['Tech Stack Multiplier']*df['Automation Adjustment Multiplier']*df['Principal/MA Multiplier']
    df['Contrct_crl'] = df['Contract Structure Multiplier']*df['Client Reporting Level Multiplier']
    df['Contrct_crl_auto'] = df['Contract Structure Multiplier']*df['Client Reporting Level Multiplier']*df['Automation Adjustment Multiplier']
    df['tech_auto'] = df['Tech Stack Multiplier']*df['Automation Adjustment Multiplier']

    df['adj_time_CSACP'] = df['1.Billing_adj']*df['Contrct_Spend_Auto_CRL_PMA']
    df['adj_time_BP'] = df['2.Fund Reconciliations']*df['Bank_PMA'] + df['3.Payment']*df['Bank_PMA']
    df['adj_time_TAP'] = (df['4.Monthly JDE period close and Open PO review'] + df['5.Monthly JDE Balance Sheet Reconciliation'] + df['6.Corporate Month End Revenue/Costs Adjustments'] +df['7.Corporate Pass Through Reconciliation']+df['8.Corporate Payment Entries Submission']+df['9.Internal & External Audit Sampling Requests (SOC1 & SOX)'] + df['10.Corporate P&L Month End Review, Analysis & Queries'] +df['11.Corporate Yearly Budget - Preparation, Review & Approval']+df['12.Corporate Monthly Forecast - Preparation, Review & Approval']) * df['tech_auto_pma']
    df['adj_time_CC'] = df['14.Client Month End Accruals - Open PO, Rental, Utilities etc. - Manual Journal Entries Posting'] * df['Contrct_crl']
    df['adj_time_CCA'] = (df['Customised Report']+ df['Standard Report'] + df['16.Client Budget - Management Fee & Payroll Calculation; Vendor Spend Data']+df['17.Client Forecast - Vendor Spend']+df['18.Client Savings Report']+df['19.Client Finance Audit Support']+df['20.Client Billing to Actuals Reconciliation']) * df['Contrct_crl_auto']
    df['adj_time_None'] = df['15.Monthly Operational Call for Client Month End Close (Queries from FM - Finance Related)']
    df['adj_time_TA'] = df['13.Corporate Operation Merit & Bonus Review'] * df['tech_auto']

    df['Adj_Activity_Hours'] = df['adj_time_CSACP'] + df['adj_time_BP'] + df['adj_time_TAP'] + df['adj_time_CC'] + df['adj_time_None'] + df['adj_time_TA'] + df['adj_time_CCA']
    df['after_add_overlay'] = df['Adj_Activity_Hours']*1.2

    df['adj_time_CSACP_low'] = df['adj_time_CSACP']
    df['adj_time_BP_low'] = df['adj_time_BP']
    df['adj_time_TAP_low'] = (df['4.Monthly JDE period close and Open PO review'] + df['5.Monthly JDE Balance Sheet Reconciliation'] + df['6.Corporate Month End Revenue/Costs Adjustments'] +df['7.Corporate Pass Through Reconciliation']+df['8.Corporate Payment Entries Submission']+df['9.Internal & External Audit Sampling Requests (SOC1 & SOX)'] + df['10.Corporate P&L Month End Review, Analysis & Queries'] + df['12.Corporate Monthly Forecast - Preparation, Review & Approval']) * df['tech_auto_pma']
    df['adj_time_CCA_low'] = (df['17.Client Forecast - Vendor Spend'] + df['19.Client Finance Audit Support']) * df['Contrct_crl_auto']
    df['p'] = (df['adj_time_CSACP_low'] + df['adj_time_BP_low'] + df['adj_time_TAP_low'] + df['adj_time_CCA_low'])/df['Adj_Activity_Hours']

    df.loc[df['Delivery Model'] == "Shared Services", 'adj_time_after_dm'] = df['after_add_overlay'] * 1
    df.loc[df['Delivery Model'] == "On-site", 'adj_time_after_dm'] = df['after_add_overlay'] * 1.3
    df.loc[df['Delivery Model'] == "Mixed", 'adj_time_after_dm'] = df['after_add_overlay'] * df['p'] + (1 - df['p']) * df['after_add_overlay'] * 1.3

    df['Activities Subscribed'] = df.apply(lambda row:sum(row[col]>0 for col in activities if col in row.index),axis=1)
    df['Total Activity Hours'] = df['1.Billing_adj'].astype(float)+df['2.Fund Reconciliations'].astype(float)+df['3.Payment'].astype(float)+df['4.Monthly JDE period close and Open PO review'].astype(float) + df['5.Monthly JDE Balance Sheet Reconciliation'].astype(float) + df['6.Corporate Month End Revenue/Costs Adjustments'].astype(float) + df['7.Corporate Pass Through Reconciliation'].astype(float) + df['8.Corporate Payment Entries Submission'].astype(float) + df['9.Internal & External Audit Sampling Requests (SOC1 & SOX)'].astype(float) + df['10.Corporate P&L Month End Review, Analysis & Queries'].astype(float) + df['11.Corporate Yearly Budget - Preparation, Review & Approval'].astype(float) + df['12.Corporate Monthly Forecast - Preparation, Review & Approval'].astype(float) + df['13.Corporate Operation Merit & Bonus Review'].astype(float) + df['14.Client Month End Accruals - Open PO, Rental, Utilities etc. - Manual Journal Entries Posting'].astype(float) + df['15.Monthly Operational Call for Client Month End Close (Queries from FM - Finance Related)'].astype(float) + df['16.Client Budget - Management Fee & Payroll Calculation; Vendor Spend Data'].astype(float) + df['17.Client Forecast - Vendor Spend'].astype(float) + df['18.Client Savings Report'].astype(float) + df['19.Client Finance Audit Support'].astype(float) + df['20.Client Billing to Actuals Reconciliation'].astype(float) + df['Customised Report']+df['Standard Report']

    df['bin_billing'] = (pd.qcut(df['1.Billing_adj'], 10, labels=False, duplicates = 'drop') + 1) if df['1.Billing_adj'].sum() >1 else 1
    df['bin_funds'] = (pd.qcut(df['2.Fund Reconciliations'], 5, labels=False, duplicates = 'drop') + 1) if df['2.Fund Reconciliations'].sum() >1 else 1
    df['bin_payments'] = (pd.qcut(df['3.Payment'], 5, labels=False, duplicates = 'drop') + 1) if df['3.Payment'].sum() >1 else 1
    df['bin_accruals'] = (pd.qcut(df['14.Client Month End Accruals - Open PO, Rental, Utilities etc. - Manual Journal Entries Posting'], 5, labels=False, duplicates = 'drop') + 1) if df['14.Client Month End Accruals - Open PO, Rental, Utilities etc. - Manual Journal Entries Posting'].sum() >1 else 1
    df['bin_Operation'] = (pd.qcut(df['15.Monthly Operational Call for Client Month End Close (Queries from FM - Finance Related)'], 5, labels=False, duplicates = 'drop') + 1) if df['15.Monthly Operational Call for Client Month End Close (Queries from FM - Finance Related)'].sum() >1 else 1
    df['bin_Savings Report'] = (pd.qcut(df['18.Client Savings Report'], 5, labels=False, duplicates = 'drop') + 1) if df['18.Client Savings Report'].sum() >1 else 1
    df['Bins Total'] = df['bin_billing'].sum()+df['bin_funds'].sum()+df['bin_payments'].sum()+df['bin_accruals'].sum()+df['bin_Operation'].sum()+df['Activities Subscribed'].sum() + df['18.Client Savings Report'].sum() - 6

    dml = pd.DataFrame(columns = ['Region','Country','Spend/Country','Total Activity Hours','bins_total'])
    dml['Region'] = df['Region']
    dml['Country'] = df['Country']
    dml['Spend/Country'] = df['Total Managed Spend']
    dml["Contract Structure"] = df['Contract Structure Multiplier']
    dml["Fixed/Var. Spend Ratio"] = df['Spend Ratio Multiplier']
    dml["Principal/MA"] = df['Principal/MA Multiplier']
    dml["Client Reporting Level"] = df['Client Reporting Level Multiplier']
    dml["Tech Stack"] = df['Contract Structure Multiplier']
    dml["Automation Adjustments"] = df['Tech Stack Multiplier']
    dml["Bank Account"] = df['Bank Account Multiplier']
    dml['LC Count'] = df.apply(lambda row:sum(row[col]>0 for col in LCA if col in row.index),axis=1)
    dml['MC Count'] = df.apply(lambda row:sum(row[col]>0 for col in MCA if col in row.index),axis=1)
    dml['HC Count'] = df.apply(lambda row:sum(row[col]>0 for col in HCA if col in row.index),axis=1)
    dml['LC Hours'] = df['adj_time_CSACP_low'] + df['adj_time_BP_low'] + df['adj_time_TAP_low'] + df['adj_time_CCA_low']
    dml['MC Hours'] = df['14.Client Month End Accruals - Open PO, Rental, Utilities etc. - Manual Journal Entries Posting'] + df['Standard Report'] + df['15.Monthly Operational Call for Client Month End Close (Queries from FM - Finance Related)'] + df['16.Client Budget - Management Fee & Payroll Calculation; Vendor Spend Data'] + df['18.Client Savings Report']
    dml['HC Hours'] = df['Customised Report'] + df['11.Corporate Yearly Budget - Preparation, Review & Approval'] + df['13.Corporate Operation Merit & Bonus Review'] + df['20.Client Billing to Actuals Reconciliation']
    dml['bins_total'] = df['Bins Total']
    
    model = joblib.load("FTE_Calc_wc.pkl")
    prediction = model.predict(dml)


    data_len= len(df)
    pred_len=len(prediction)

    if data_len==pred_len:
        df['ML Prediction'] = prediction
    else:
        pass
    if data_len < pred_len:
        df['ML Prediction'] = prediction[:data_len]
    else:
        df=df.iloc[:pred_len]
        
    df["ML Prediction"] = prediction

    chrs = (df['after_add_overlay'].sum()).__round__(0)
    mlhrs = (df["ML Prediction"].sum()).__round__(0)
    lowpct = (df['adj_time_CSACP_low'].sum() + df['adj_time_BP_low'].sum() + df['adj_time_TAP_low'].sum() + df['adj_time_CCA_low'].sum())/df['Adj_Activity_Hours'].sum()
    hmpct = (1- lowpct)

    fte_count_xl_ss = mt.ceil((df['after_add_overlay'].sum()/150)*2)/2
    fte_count_xl_os = mt.ceil(((1.3)*df['after_add_overlay'].sum()/150)*2)/2
    fte_count_xl_m = mt.ceil(fte_count_xl_ss*lowpct*2)/2 + mt.ceil(fte_count_xl_os*hmpct*2)/2

    fte_count_ml_ss = mt.ceil((df["ML Prediction"].sum()/150)*2)/2
    fte_count_ml_os = mt.ceil(((1.3)*df["ML Prediction"].sum()/150)*2)/2
    fte_count_ml_m = mt.ceil(fte_count_ml_ss*lowpct*2)/2 + mt.ceil(fte_count_ml_os*hmpct*2)/2

    # Shared Services
    shared_services_mask = df['Delivery Model'] == "Shared Services"
    df.loc[shared_services_mask, 'SFAE'] = mt.ceil(fte_count_xl_ss * hmpct * 2) / 2
    df.loc[shared_services_mask, 'SFAML'] = mt.ceil(fte_count_ml_ss * hmpct * 2) / 2
    df.loc[shared_services_mask, 'tle'] = mt.floor(fte_count_xl_ss / 6)
    df.loc[shared_services_mask, 'tlml'] = mt.floor(fte_count_ml_ss / 6)
    df.loc[shared_services_mask, 'FAE'] = fte_count_xl_ss - df.loc[shared_services_mask, 'SFAE'] - df.loc[shared_services_mask, 'tle']
    df.loc[shared_services_mask, 'FAML'] = fte_count_ml_ss - df.loc[shared_services_mask, 'SFAML'] - df.loc[shared_services_mask, 'tlml']
    df.loc[shared_services_mask, 'tftec'] = fte_count_xl_ss
    df.loc[shared_services_mask, 'tfteml'] = fte_count_ml_ss

    # On-site
    on_site_mask = df['Delivery Model'] == "On-site"
    df.loc[on_site_mask, 'SFAE'] = mt.ceil(fte_count_xl_os * hmpct * 2) / 2
    df.loc[on_site_mask, 'SFAML'] = mt.ceil(fte_count_ml_os * hmpct * 2) / 2
    df.loc[on_site_mask, 'tle'] = mt.floor(fte_count_xl_os / 6)
    df.loc[on_site_mask, 'tlml'] = mt.floor(fte_count_ml_os / 6)
    df.loc[on_site_mask, 'FAE'] = fte_count_xl_os - df.loc[on_site_mask, 'SFAE'] - df.loc[on_site_mask, 'tle']
    df.loc[on_site_mask, 'FAML'] = fte_count_ml_os - df.loc[on_site_mask, 'SFAML'] - df.loc[on_site_mask, 'tlml']
    df.loc[on_site_mask, 'tftec'] = fte_count_xl_os
    df.loc[on_site_mask, 'tfteml'] = fte_count_ml_os

    # Mixed
    mixed_mask = df['Delivery Model'] == "Mixed"
    df.loc[mixed_mask, 'SFAE'] = mt.ceil(fte_count_xl_os * hmpct * 2) / 2
    df.loc[mixed_mask, 'SFAML'] = mt.ceil(fte_count_ml_os * hmpct * 2) / 2
    df.loc[mixed_mask, 'tle'] = mt.floor(fte_count_xl_m / 6)
    df.loc[mixed_mask, 'tlml'] = mt.floor(fte_count_ml_m / 6)
    df.loc[mixed_mask, 'FAE'] = fte_count_xl_m - df.loc[mixed_mask, 'SFAE'] - df.loc[mixed_mask, 'tle']
    df.loc[mixed_mask, 'FAML'] = fte_count_ml_m - df.loc[mixed_mask, 'SFAML'] - df.loc[mixed_mask, 'tlml']
    df.loc[mixed_mask, 'tftec'] = fte_count_xl_m
    df.loc[mixed_mask, 'tfteml'] = fte_count_ml_m
    

    
    # Shared Services
    if df['Delivery Model'].eq("Shared Services").any():
        tftec = df.loc[shared_services_mask, 'tftec'].values[0]
        FAE = df.loc[shared_services_mask, 'FAE'].values[0]
        SFAE = df.loc[shared_services_mask, 'SFAE'].values[0]
        tle = df.loc[shared_services_mask, 'tle'].values[0]
        tfteml = df.loc[shared_services_mask, 'tfteml'].values[0]
        FAML = df.loc[shared_services_mask, 'FAML'].values[0]
        SFAML = df.loc[shared_services_mask, 'SFAML'].values[0]
        tlml = df.loc[shared_services_mask, 'tlml'].values[0]
    # On-site
    elif df['Delivery Model'].eq("On-site").any():
        tftec = df.loc[on_site_mask, 'tftec'].values[0]
        FAE = df.loc[on_site_mask, 'FAE'].values[0]
        SFAE = df.loc[on_site_mask, 'SFAE'].values[0]
        tle = df.loc[on_site_mask, 'tle'].values[0]
        tfteml = df.loc[on_site_mask, 'tfteml'].values[0]
        FAML = df.loc[on_site_mask, 'FAML'].values[0]
        SFAML = df.loc[on_site_mask, 'SFAML'].values[0]
        tlml = df.loc[on_site_mask, 'tlml'].values[0]
    # Mixed
    elif df['Delivery Model'].eq("Mixed").any():
        tftec = df.loc[mixed_mask, 'tftec'].values[0]
        FAE = df.loc[mixed_mask, 'FAE'].values[0]
        SFAE = df.loc[mixed_mask, 'SFAE'].values[0]
        tle = df.loc[mixed_mask, 'tle'].values[0]
        tfteml = df.loc[mixed_mask, 'tfteml'].values[0]
        FAML = df.loc[mixed_mask, 'FAML'].values[0]
        SFAML = df.loc[mixed_mask, 'SFAML'].values[0]
        tlml = df.loc[mixed_mask, 'tlml'].values[0]
    
    dfdb = df.iloc[:,:71]
    dfdb.drop(dfdb.columns[[64,65,67,69]],axis=1,inplace = True)   
    dfdb['Final_Est_Hours'] = df.iloc[:,85]
    dfdb['Total_Est_FTE'] = tftec
    dfdb['FA'] = FAE
    dfdb['SFA'] = SFAE
    dfdb['FM'] = tle
    dfdb['Final_Est_Hours_ML'] = df.iloc[:,101]
    dfdb['Total_Est_FTE_ML'] = tfteml
    dfdb['FA_ML'] = FAML
    dfdb['SFA_ML'] = SFAML
    dfdb['FM_ML'] = tlml
    dfdb['instance_key'] = str(uuid.uuid4())[:12]
    
    dbdf = dfdb.rename(columns = {'Average Spend per Site':'Avg_Spend_Site',
                                'Client Name': 'Client_Name',
                                'Average Site Multiplier value':'Classification',
                                'Adjusted No of Sites':'Adj_Nof_Sites',
                                'Total Managed Spend': 'Total_Managed_Spend',
                                'Number of Sites':'Number_of_Sites',
                                'Contract Structure Option':'Contract_Structure',
                                'Contract Structure Multiplier':'Contract_Structure_Multiplier',
                                'Spend Ratio Option':'Fixed_Var_Spend_Ratio',
                                'Spend Ratio Multiplier':'Fixed_Var_Spend_Ratio_Multiplier',
                                'Principal/MA Option':'Principal_MA',
                                'Principal/MA Multiplier':'Principal_MA_Multiplier',
                                'Client Reporting Level Option':'Client_Reporting_Level',
                                'Client Reporting Level Multiplier':'Client_Reporting_Level_Multiplier',
                                'Tech Stack Option':'Tech_Stack','Tech Stack Multiplier':'Tech_Stack_Multiplier',
                                'Automation Adjustment Option':'Automation_Adjustments',
                                'Automation Adjustment Multiplier':'Automation_Adjustments_Multiplier',
                                'Bank Account Option':'Bank_Account','Bank Account Multiplier':'Bank_Account_Multiplier',
                                'Delivery Model':'Delivery_Model','1.Billing_freq':'Billing_Frequency',
                                '1.Billing_adj':'Billing_Value','2.Fund Reconciliations_freq':'Fund_Reconciliations_Frequency',
                                '2.Fund Reconciliations':'Fund_Reconciliations_Value','3.Payment_freq':'Payment_Frequency',
                                '3.Payment':'Payment_Value',
                                '4.Monthly JDE period close and Open PO review_freq':'Period_close_and_Open_PO_review_Frequency',
                                '4.Monthly JDE period close and Open PO review':'Period_close_and_Open_PO_review_Value',
                                '5.Monthly JDE Balance Sheet Reconciliation_freq':'Balance_Sheet_Reconciliation_Frequency',
                                '5.Monthly JDE Balance Sheet Reconciliation':'Balance_Sheet_Reconciliation_Value',
                                '6.Corporate Month End Revenue/Costs Adjustments_freq':'Revenue_Costs_Adjustments_Frequency',
                                '6.Corporate Month End Revenue/Costs Adjustments':'Revenue_Costs_Adjustments_Value',
                                '7.Corporate Pass Through Reconciliation_freq':'Pass_Through_Reconciliation_Frequency',
                                '7.Corporate Pass Through Reconciliation':'Pass_Through_Reconciliation_Value',
                                '8.Corporate Payment Entries Submission_freq':'Payment_Entries_Submission_Frequency',
                                '8.Corporate Payment Entries Submission':'Payment_Entries_Submission_Value',
                                '9.Internal & External Audit Sampling Requests (SOC1 & SOX)_freq':'Internal_External_Audit_Frequency',
                                '9.Internal & External Audit Sampling Requests (SOC1 & SOX)':'Internal_External_Audit_Value',
                                '10.Corporate P&L Month End Review, Analysis & Queries_freq':'PL_review_Frequency',
                                '10.Corporate P&L Month End Review, Analysis & Queries':'PL_review_Value',
                                '11.Corporate Yearly Budget - Preparation, Review & Approval_freq':'Yearly_budget_prepration_Frequency',
                                '11.Corporate Yearly Budget - Preparation, Review & Approval':'Yearly_budget_prepration_Value',
                                '12.Corporate Monthly Forecast - Preparation, Review & Approval_freq':'Monthly_forcast_prepration_Frequency',
                                '12.Corporate Monthly Forecast - Preparation, Review & Approval':'Monthly_forcast_prepration_Value',
                                '13.Corporate Operation Merit & Bonus Review_freq':'Operation_Merit_Bonus_Review_Frequency',
                                '13.Corporate Operation Merit & Bonus Review':'Operation_Merit_Bonus_Review_Value',
                                '14.Client Month End Accruals - Open PO, Rental, Utilities etc. - Manual Journal Entries Posting_freq':'Manual_Journal_Entries_Posting_Frequency',
                                '14.Client Month End Accruals - Open PO, Rental, Utilities etc. - Manual Journal Entries Posting':'Manual_Journal_Entries_Posting_Value',
                                '15.Monthly Operational Call for Client Month End Close (Queries from FM - Finance Related)_freq':'Monthly_Operational_Call_Frequency',
                                '15.Monthly Operational Call for Client Month End Close (Queries from FM - Finance Related)':'Monthly_Operational_Call_Value',
                                '16.Client Budget - Management Fee & Payroll Calculation; Vendor Spend Data_freq':'Budget_Management_Fee_Payroll_Calculation_Frequency',
                                '16.Client Budget - Management Fee & Payroll Calculation; Vendor Spend Data':'Budget_Management_Fee_Payroll_Calculation_Value',
                                '17.Client Forecast - Vendor Spend_freq':'Client_Forecast_Vendor_Spend_Value',
                                '17.Client Forecast - Vendor Spend':'Client_Forecast_Vendor_Spend_Frequency',
                                '18.Client Savings Report_freq':'Client_Savings_Report_Value',
                                '18.Client Savings Report':'Client_Savings_Report_Frequency',
                                '19.Client Finance Audit Support_freq':'Client_Finance_Audit_Supporting_Value',
                                '19.Client Finance Audit Support':'Client_Finance_Audit_Supporting_Frequency',
                                '20.Client Billing to Actuals Reconciliation_freq':'Client_Billing_to_Actuals_Reconciliation_Frequency',
                                '20.Client Billing to Actuals Reconciliation':'Client_Billing_to_Actuals_Reconciliation_Value',
                                'Standard Report_freq':'Standard_Report_Frequency','Standard Report':'Standard_Report_Value','Customised Report_freq':'Customized_Reporting_Frequency','Customised Report':'Customized_Reporting_Value'})

    dft = dbdf.reindex(columns = ['instance_key','Client_Name','Country','Region','Total_Managed_Spend',
                    'Number_of_Sites','Contract_Structure','Contract_Structure_Multiplier',
                    'Fixed_Var_Spend_Ratio','Fixed_Var_Spend_Ratio_Multiplier','Principal_MA',
                    'Principal_MA_Multiplier','Client_Reporting_Level','Client_Reporting_Level_Multiplier',
                    'Tech_Stack','Tech_Stack_Multiplier','Automation_Adjustments','Automation_Adjustments_Multiplier',
                    'Bank_Account','Bank_Account_Multiplier','Delivery_Model','Avg_Spend_Site','Classification','Adj_Nof_Sites',
                    'Billing_Frequency','Billing_Value',
                    'Fund_Reconciliations_Frequency','Fund_Reconciliations_Value',
                    'Payment_Frequency','Payment_Value','Period_close_and_Open_PO_review_Frequency',
                    'Period_close_and_Open_PO_review_Value',
                    'Balance_Sheet_Reconciliation_Frequency',
                    'Balance_Sheet_Reconciliation_Value',
                    'Revenue_Costs_Adjustments_Frequency',
                    'Revenue_Costs_Adjustments_Value',
                    'Pass_Through_Reconciliation_Frequency',
                    'Pass_Through_Reconciliation_Value',
                    'Payment_Entries_Submission_Frequency',
                    'Payment_Entries_Submission_Value',
                    'Internal_External_Audit_Frequency',
                    'Internal_External_Audit_Value',
                    'PL_review_Frequency',
                    'PL_review_Value',
                    'Yearly_budget_prepration_Frequency',
                    'Yearly_budget_prepration_Value',
                    'Monthly_forcast_prepration_Frequency',
                    'Monthly_forcast_prepration_Value',
                    'Operation_Merit_Bonus_Review_Frequency',
                    'Operation_Merit_Bonus_Review_Value',
                    'Manual_Journal_Entries_Posting_Frequency',
                    'Manual_Journal_Entries_Posting_Value',
                    'Monthly_Operational_Call_Frequency',
                    'Monthly_Operational_Call_Value',
                    'Budget_Management_Fee_Payroll_Calculation_Frequency',
                    'Budget_Management_Fee_Payroll_Calculation_Value',
                    'Client_Forecast_Vendor_Spend_Value',
                    'Client_Forecast_Vendor_Spend_Frequency',
                    'Client_Savings_Report_Value',
                    'Client_Savings_Report_Frequency',
                    'Client_Finance_Audit_Supporting_Value',
                    'Client_Finance_Audit_Supporting_Frequency',
                    'Client_Billing_to_Actuals_Reconciliation_Frequency',
                    'Client_Billing_to_Actuals_Reconciliation_Value',
                    'Standard_Report_Frequency',
                    'Standard_Report_Value',
                    'Customized_Reporting_Frequency',
                    'Customized_Reporting_Value','Final_Est_Hours','Total_Est_FTE',
                    'FA','SFA','FM','Final_Est_Hours_ML','Total_Est_FTE_ML','FA_ML',
                    'SFA_ML','FM_ML'])

    conn, cur = dbconn.connection()
    insert_query = f"INSERT INTO ftecalc_data.fin_data ({', '.join(dft.columns)}) VALUES ({', '.join(['%s'] * len(dft.columns))})"
    try:
        cur.executemany(insert_query, dft.values.tolist())
        success = True
    except Exception as e:
        success = False
        print(f"Error occurred during data upload: {e}")
    if success:
        conn.commit()

    cur.close()
    conn.close()

    dfam = pd.DataFrame({"Rule Based":[chrs,tftec,"------------------------",FAE,SFAE,tle], "ML Predicted":[mlhrs,tfteml,"------------------------",FAML,SFAML,tlml]},index=["Total Hours", "Total FTE Count","Recommended Role", "Financial Analyst","Sr. Financial Analyst", "Manager/Team-Lead"])
    return dfam

def activity_summary(df: pd.DataFrame):
    df['Contract Structure Multiplier'] = df['Contract Structure Option'].map(contract_vars['Contract Structure'])
    df['Spend Ratio Multiplier'] = df['Spend Ratio Option'].map(contract_vars['Spend Ratio'])
    df['Principal/MA Multiplier'] = df['Principal/MA Option'].map(contract_vars['Principal/MA'])
    df['Client Reporting Level Multiplier'] = df['Client Reporting Level Option'].map(contract_vars['Client Reporting Level'])
    df['Tech Stack Multiplier'] = df['Tech Stack Option'].map(contract_vars['Tech Stack'])
    df['Automation Adjustment Multiplier'] = df['Automation Adjustment Option'].map(contract_vars['Automation Adjustment'])
    df['Bank Account Multiplier'] = df['Bank Account Option'].map(contract_vars['Bank Account'])

    for index, row in inputs.iterrows():
        country = row['Country']
        activity = row['activity']
        time_spent = row['Time Spend/Country']
        
        # Check if the activity is in df columns
        if f'{activity}_freq' in df.columns:
            # Find the corresponding frequency option
            frequency_values = df.loc[df['Country'] == country, f'{activity}_freq'].values
            if len(frequency_values) > 0:
                frequency = frequency_values[0]
                multiplier = frequency_options.get(frequency, 1)
                
                # Update the df with the calculated value
                df.loc[df['Country'] == country, f'{activity}'] = time_spent * multiplier


    df['Total No of Sites'] = df['Number of Sites'].sum()
    df['Average Spend per Site'] = df['Total Managed Spend']/df['Total No of Sites']
    df['Spend per Country'] = df['Average Spend per Site'] * df['Number of Sites']

    if df['Region'].eq("APAC").any():
        df.loc[df['Average Spend per Site'] < 40000, 'Average Site Multiplier value'] = 0.6
        df.loc[(df['Average Spend per Site'] >= 40000) & (df['Average Spend per Site'] < 80000), 'Average Site Multiplier value'] = 0.8
        df.loc[(df['Average Spend per Site'] >= 80000) & (df['Average Spend per Site'] < 300000), 'Average Site Multiplier value'] = 1
        df.loc[(df['Average Spend per Site'] >= 300000) & (df['Average Spend per Site'] < 750000), 'Average Site Multiplier value'] = 1
        df.loc[df['Average Spend per Site'] >= 750000, 'Average Site Multiplier value'] = 1.1
        
    else:
        df.loc[df['Average Spend per Site'] < 80000, 'Average Site Multiplier value'] = 0.6
        df.loc[(df['Average Spend per Site'] >= 80000) & (df['Average Spend per Site'] < 150000), 'Average Site Multiplier value'] = 0.8
        df.loc[(df['Average Spend per Site'] >= 150000) & (df['Average Spend per Site'] < 500000), 'Average Site Multiplier value'] = 1
        df.loc[(df['Average Spend per Site'] >= 500000) & (df['Average Spend per Site'] < 1200000), 'Average Site Multiplier value'] = 1
        df.loc[df['Average Spend per Site'] >= 1200000, 'Average Site Multiplier value'] = 1.1

    df['Adjusted No of Sites/Country'] = df['Number of Sites']*df['Average Site Multiplier value']
    df['Adjusted No of Sites'] = df['Adjusted No of Sites/Country'].sum()

    df['1.Billing_adj'] = np.where(df['Adjusted No of Sites/Country'] <= 1,df['1.Billing'] * 2 ,df['1.Billing']*df['Adjusted No of Sites/Country'])
 
    actable = pd.DataFrame({"Activities": ['Billing','Fund Reconciliations','Payment','Monthly JDE period close and Open PO review',
                                                    'Monthly JDE Balance Sheet Reconciliation','Corporate Month End Revenue/Costs Adjustments',
                                                    'Corporate Pass Through Reconciliation','Corporate Payment Entries Submission','Internal & External Audit Sampling Requests (SOC1 & SOX)',
                                                    'Corporate P&L Month End Review, Analysis & Queries','Corporate Yearly Budget - Preparation, Review & Approval','Corporate Monthly Forecast - Preparation, Review & Approval',
                                                    'Corporate Operation Merit & Bonus Review','Client Month End Accruals - Open PO, Rental, Utilities etc. - Manual Journal Entries Posting','Monthly Operational Call for Client Month End Close (Queries from FM - Finance Related)',
                                                    'Client Budget - Management Fee & Payroll Calculation; Vendor Spend Data','Client Forecast - Vendor Spend','Client Savings Report','Client Finance Audit Support',
                                                    'Client Billing to Actuals Reconciliation','Standard Report','Customised Report'],
                                "Hours":[df['1.Billing_adj'].sum().round(1),df['2.Fund Reconciliations'].sum().round(1),df['3.Payment'].sum().round(1),df['4.Monthly JDE period close and Open PO review'].sum().round(1),df['5.Monthly JDE Balance Sheet Reconciliation'].sum().round(1),
                                            df['6.Corporate Month End Revenue/Costs Adjustments'].sum().round(1),df['7.Corporate Pass Through Reconciliation'].sum().round(1),df['8.Corporate Payment Entries Submission'].sum().round(1),df['9.Internal & External Audit Sampling Requests (SOC1 & SOX)'].sum().round(1),df['10.Corporate P&L Month End Review, Analysis & Queries'].sum().round(1),
                                            df['11.Corporate Yearly Budget - Preparation, Review & Approval'].sum().round(1),df['12.Corporate Monthly Forecast - Preparation, Review & Approval'].sum().round(1),df['13.Corporate Operation Merit & Bonus Review'].sum().round(1),df['14.Client Month End Accruals - Open PO, Rental, Utilities etc. - Manual Journal Entries Posting'].sum().round(1),df['15.Monthly Operational Call for Client Month End Close (Queries from FM - Finance Related)'].sum().round(1),
                                            df['16.Client Budget - Management Fee & Payroll Calculation; Vendor Spend Data'].sum().round(1),df['17.Client Forecast - Vendor Spend'].sum().round(1),df['18.Client Savings Report'].sum().round(1),df['19.Client Finance Audit Support'].sum().round(1),df['20.Client Billing to Actuals Reconciliation'].sum().round(1),
                                            df['Standard Report'].sum().round(1),df['Customised Report'].sum().round(1)]},index = (1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22))
    return actable



#----------------------------------------------------------------------------------------------
def download_summary(df: pd.DataFrame):
    df['Contract Structure Multiplier'] = df['Contract Structure Option'].map(contract_vars['Contract Structure'])
    df['Spend Ratio Multiplier'] = df['Spend Ratio Option'].map(contract_vars['Spend Ratio'])
    df['Principal/MA Multiplier'] = df['Principal/MA Option'].map(contract_vars['Principal/MA'])
    df['Client Reporting Level Multiplier'] = df['Client Reporting Level Option'].map(contract_vars['Client Reporting Level'])
    df['Tech Stack Multiplier'] = df['Tech Stack Option'].map(contract_vars['Tech Stack'])
    df['Automation Adjustment Multiplier'] = df['Automation Adjustment Option'].map(contract_vars['Automation Adjustment'])
    df['Bank Account Multiplier'] = df['Bank Account Option'].map(contract_vars['Bank Account'])

    for index, row in inputs.iterrows():
        country = row['Country']
        activity = row['activity']
        time_spent = row['Time Spend/Country']
        
        # Check if the activity is in df columns
        if f'{activity}_freq' in df.columns:
            # Find the corresponding frequency option
            frequency_values = df.loc[df['Country'] == country, f'{activity}_freq'].values
            if len(frequency_values) > 0:
                frequency = frequency_values[0]
                multiplier = frequency_options.get(frequency, 1)
                
                # Update the df with the calculated value
                df.loc[df['Country'] == country, f'{activity}'] = time_spent * multiplier


    df['Total No of Sites'] = df['Number of Sites'].sum()
    df['Average Spend per Site'] = df['Total Managed Spend']/df['Total No of Sites']
    df['Spend per Country'] = df['Average Spend per Site'] * df['Number of Sites']

    
    if df['Region'].eq("APAC").any():
        df.loc[df['Average Spend per Site'] < 40000, 'Average Site Multiplier value'] = 0.6
        df.loc[(df['Average Spend per Site'] >= 40000) & (df['Average Spend per Site'] < 80000), 'Average Site Multiplier value'] = 0.8
        df.loc[(df['Average Spend per Site'] >= 80000) & (df['Average Spend per Site'] < 300000), 'Average Site Multiplier value'] = 1
        df.loc[(df['Average Spend per Site'] >= 300000) & (df['Average Spend per Site'] < 750000), 'Average Site Multiplier value'] = 1
        df.loc[df['Average Spend per Site'] >= 750000, 'Average Site Multiplier value'] = 1.1
        
    else:
        df.loc[df['Average Spend per Site'] < 80000, 'Average Site Multiplier value'] = 0.6
        df.loc[(df['Average Spend per Site'] >= 80000) & (df['Average Spend per Site'] < 150000), 'Average Site Multiplier value'] = 0.8
        df.loc[(df['Average Spend per Site'] >= 150000) & (df['Average Spend per Site'] < 500000), 'Average Site Multiplier value'] = 1
        df.loc[(df['Average Spend per Site'] >= 500000) & (df['Average Spend per Site'] < 1200000), 'Average Site Multiplier value'] = 1
        df.loc[df['Average Spend per Site'] >= 1200000, 'Average Site Multiplier value'] = 1.1

    df['Adjusted No of Sites/Country'] = df['Number of Sites']*df['Average Site Multiplier value']
    df['Adjusted No of Sites'] = df['Adjusted No of Sites/Country'].sum()

    df['1.Billing_adj'] = np.where(df['Adjusted No of Sites/Country'] <= 1,df['1.Billing'] * 2 ,df['1.Billing']*df['Adjusted No of Sites/Country'])

    df['Contrct_Spend_Auto_CRL_PMA'] = df['Contract Structure Multiplier']*df['Spend Ratio Multiplier']*df['Automation Adjustment Multiplier']*df['Client Reporting Level Multiplier']*df['Principal/MA Multiplier']
    df['Bank_PMA'] = df['Bank Account Multiplier']*df['Principal/MA Multiplier']
    df['tech_auto_pma'] = df['Tech Stack Multiplier']*df['Automation Adjustment Multiplier']*df['Principal/MA Multiplier']
    df['Contrct_crl'] = df['Contract Structure Multiplier']*df['Client Reporting Level Multiplier']
    df['Contrct_crl_auto'] = df['Contract Structure Multiplier']*df['Client Reporting Level Multiplier']*df['Automation Adjustment Multiplier']
    df['tech_auto'] = df['Tech Stack Multiplier']*df['Automation Adjustment Multiplier']

    df['adj_time_CSACP'] = df['1.Billing_adj']*df['Contrct_Spend_Auto_CRL_PMA']
    df['adj_time_BP'] = df['2.Fund Reconciliations']*df['Bank_PMA'] + df['3.Payment']*df['Bank_PMA']
    df['adj_time_TAP'] = (df['4.Monthly JDE period close and Open PO review'] + df['5.Monthly JDE Balance Sheet Reconciliation'] + df['6.Corporate Month End Revenue/Costs Adjustments'] +df['7.Corporate Pass Through Reconciliation']+df['8.Corporate Payment Entries Submission']+df['9.Internal & External Audit Sampling Requests (SOC1 & SOX)'] + df['10.Corporate P&L Month End Review, Analysis & Queries'] +df['11.Corporate Yearly Budget - Preparation, Review & Approval']+df['12.Corporate Monthly Forecast - Preparation, Review & Approval']) * df['tech_auto_pma']
    df['adj_time_CC'] = df['14.Client Month End Accruals - Open PO, Rental, Utilities etc. - Manual Journal Entries Posting'] * df['Contrct_crl']
    df['adj_time_CCA'] = (df['Customised Report']+ df['Standard Report'] + df['16.Client Budget - Management Fee & Payroll Calculation; Vendor Spend Data']+df['17.Client Forecast - Vendor Spend']+df['18.Client Savings Report']+df['19.Client Finance Audit Support']+df['20.Client Billing to Actuals Reconciliation']) * df['Contrct_crl_auto']
    df['adj_time_None'] = df['15.Monthly Operational Call for Client Month End Close (Queries from FM - Finance Related)']
    df['adj_time_TA'] = df['13.Corporate Operation Merit & Bonus Review'] * df['tech_auto']

    df['Adj_Activity_Hours'] = df['adj_time_CSACP'] + df['adj_time_BP'] + df['adj_time_TAP'] + df['adj_time_CC'] + df['adj_time_None'] + df['adj_time_TA'] + df['adj_time_CCA']
    df['after_add_overlay'] = df['Adj_Activity_Hours']*1.2

    df['adj_time_CSACP_low'] = df['adj_time_CSACP']
    df['adj_time_BP_low'] = df['adj_time_BP']
    df['adj_time_TAP_low'] = (df['4.Monthly JDE period close and Open PO review'] + df['5.Monthly JDE Balance Sheet Reconciliation'] + df['6.Corporate Month End Revenue/Costs Adjustments'] +df['7.Corporate Pass Through Reconciliation']+df['8.Corporate Payment Entries Submission']+df['9.Internal & External Audit Sampling Requests (SOC1 & SOX)'] + df['10.Corporate P&L Month End Review, Analysis & Queries'] + df['12.Corporate Monthly Forecast - Preparation, Review & Approval']) * df['tech_auto_pma']
    df['adj_time_CCA_low'] = (df['17.Client Forecast - Vendor Spend'] + df['19.Client Finance Audit Support']) * df['Contrct_crl_auto']
    df['p'] = (df['adj_time_CSACP_low'] + df['adj_time_BP_low'] + df['adj_time_TAP_low'] + df['adj_time_CCA_low'])/df['Adj_Activity_Hours']
    
    df.loc[df['Delivery Model'].eq("Shared Services"), 'adj_time_after_dm'] = df['after_add_overlay'] * 1
    df.loc[df['Delivery Model'].eq("On-site"), 'adj_time_after_dm'] = df['after_add_overlay'] * 1.3
    df.loc[df['Delivery Model'].eq("Mixed"), 'adj_time_after_dm'] = df['after_add_overlay'] * df['p'] + (1 - df['p']) * df['after_add_overlay'] * 1.3

    df['Activities Subscribed'] = df.apply(lambda row:sum(row[col]>0 for col in activities if col in row.index),axis=1)
    df['Total Activity Hours'] = df['1.Billing_adj'].astype(float)+df['2.Fund Reconciliations'].astype(float)+df['3.Payment'].astype(float)+df['4.Monthly JDE period close and Open PO review'].astype(float) + df['5.Monthly JDE Balance Sheet Reconciliation'].astype(float) + df['6.Corporate Month End Revenue/Costs Adjustments'].astype(float) + df['7.Corporate Pass Through Reconciliation'].astype(float) + df['8.Corporate Payment Entries Submission'].astype(float) + df['9.Internal & External Audit Sampling Requests (SOC1 & SOX)'].astype(float) + df['10.Corporate P&L Month End Review, Analysis & Queries'].astype(float) + df['11.Corporate Yearly Budget - Preparation, Review & Approval'].astype(float) + df['12.Corporate Monthly Forecast - Preparation, Review & Approval'].astype(float) + df['13.Corporate Operation Merit & Bonus Review'].astype(float) + df['14.Client Month End Accruals - Open PO, Rental, Utilities etc. - Manual Journal Entries Posting'].astype(float) + df['15.Monthly Operational Call for Client Month End Close (Queries from FM - Finance Related)'].astype(float) + df['16.Client Budget - Management Fee & Payroll Calculation; Vendor Spend Data'].astype(float) + df['17.Client Forecast - Vendor Spend'].astype(float) + df['18.Client Savings Report'].astype(float) + df['19.Client Finance Audit Support'].astype(float) + df['20.Client Billing to Actuals Reconciliation'].astype(float) + df['Customised Report']+df['Standard Report']

    df['bin_billing'] = (pd.qcut(df['1.Billing_adj'], 10, labels=False, duplicates = 'drop') + 1) if df['1.Billing_adj'].sum() >0 else 0
    # df['bin_funds'] = (pd.qcut(df['2.Fund Reconciliations'], 5, labels=False, duplicates = 'drop') + 1) if df['2.Fund Reconciliations']['2.Fund Reconciliations'].sum() >0 else 0
    df['bin_funds'] = 1
    df['bin_payments'] = (pd.qcut(df['3.Payment'], 5, labels=False, duplicates = 'drop') + 1) if df['3.Payment'].sum() >0 else 0
    df['bin_accruals'] = (pd.qcut(df['14.Client Month End Accruals - Open PO, Rental, Utilities etc. - Manual Journal Entries Posting'], 5, labels=False, duplicates = 'drop') + 1) if df['14.Client Month End Accruals - Open PO, Rental, Utilities etc. - Manual Journal Entries Posting'].sum() >0 else 0
    df['bin_Operation'] = (pd.qcut(df['15.Monthly Operational Call for Client Month End Close (Queries from FM - Finance Related)'], 5, labels=False, duplicates = 'drop') + 1) if df['15.Monthly Operational Call for Client Month End Close (Queries from FM - Finance Related)'].sum() >0 else 0
    df['bin_Savings Report'] = (pd.qcut(df['18.Client Savings Report'], 5, labels=False, duplicates = 'drop') + 1) if df['18.Client Savings Report'].sum() >0 else 0
    df['Bins Total'] = df['bin_billing'].sum()+df['bin_funds'].sum()+df['bin_payments'].sum()+df['bin_accruals'].sum()+df['bin_Operation'].sum()+df['Activities Subscribed'].sum() + df['18.Client Savings Report'].sum() - 6

    dml = pd.DataFrame(columns = ['Region','Country','Spend/Country','Total Activity Hours','bins_total'])
    dml['Region'] = df['Region']
    dml['Country'] = df['Country']
    dml['Spend/Country'] = df['Total Managed Spend']
    dml["Contract Structure"] = df['Contract Structure Multiplier']
    dml["Fixed/Var. Spend Ratio"] = df['Spend Ratio Multiplier']
    dml["Principal/MA"] = df['Principal/MA Multiplier']
    dml["Client Reporting Level"] = df['Client Reporting Level Multiplier']
    dml["Tech Stack"] = df['Contract Structure Multiplier']
    dml["Automation Adjustments"] = df['Tech Stack Multiplier']
    dml["Bank Account"] = df['Bank Account Multiplier']
    dml['LC Count'] = df.apply(lambda row:sum(row[col]>0 for col in LCA if col in row.index),axis=1)
    dml['MC Count'] = df.apply(lambda row:sum(row[col]>0 for col in MCA if col in row.index),axis=1)
    dml['HC Count'] = df.apply(lambda row:sum(row[col]>0 for col in HCA if col in row.index),axis=1)
    dml['LC Hours'] = df['adj_time_CSACP_low'] + df['adj_time_BP_low'] + df['adj_time_TAP_low'] + df['adj_time_CCA_low']
    dml['MC Hours'] = df['14.Client Month End Accruals - Open PO, Rental, Utilities etc. - Manual Journal Entries Posting'] + df['Standard Report'] + df['15.Monthly Operational Call for Client Month End Close (Queries from FM - Finance Related)'] + df['16.Client Budget - Management Fee & Payroll Calculation; Vendor Spend Data'] + df['18.Client Savings Report']
    dml['HC Hours'] = df['Customised Report'] + df['11.Corporate Yearly Budget - Preparation, Review & Approval'] + df['13.Corporate Operation Merit & Bonus Review'] + df['20.Client Billing to Actuals Reconciliation']
    dml['bins_total'] = df['Bins Total']

    model = joblib.load("FTE_Calc_wc.pkl")
    prediction = model.predict(dml)


    data_len= len(df)
    pred_len=len(prediction)

    if data_len==pred_len:
        df['ML Prediction'] = prediction
    else:
        pass
    if data_len < pred_len:
        df['ML Prediction'] = prediction[:data_len]
    else:
        df=df.iloc[:pred_len]
        
    df["ML Prediction"] = prediction

    chrs = (df['after_add_overlay'].sum()).__round__(0)
    mlhrs = (df["ML Prediction"].sum()).__round__(0)
    lowpct = (df['adj_time_CSACP_low'].sum() + df['adj_time_BP_low'].sum() + df['adj_time_TAP_low'].sum() + df['adj_time_CCA_low'].sum())/df['Adj_Activity_Hours'].sum()
    hmpct = (1- lowpct)

    fte_count_xl_ss = mt.ceil((df['after_add_overlay'].sum()/150)*2)/2
    fte_count_xl_os = mt.ceil(((1.3)*df['after_add_overlay'].sum()/150)*2)/2
    fte_count_xl_m = mt.ceil(fte_count_xl_ss*lowpct*2)/2 + mt.ceil(fte_count_xl_os*hmpct*2)/2

    fte_count_ml_ss = mt.ceil((df["ML Prediction"].sum()/150)*2)/2
    fte_count_ml_os = mt.ceil(((1.3)*df["ML Prediction"].sum()/150)*2)/2
    fte_count_ml_m = mt.ceil(fte_count_ml_ss*lowpct*2)/2 + mt.ceil(fte_count_ml_os*hmpct*2)/2

    if df['Delivery Model'].eq("Shared Services").any():
        SFAE = mt.ceil(fte_count_xl_ss*hmpct*2)/2
        SFAML = mt.ceil(fte_count_ml_ss*hmpct*2)/2
        tle = mt.floor(fte_count_xl_ss/6)
        tlml = mt.floor(fte_count_ml_ss/6)
        FAE = fte_count_xl_ss - SFAE - tle
        FAML = fte_count_ml_ss - SFAML - tlml
        tftec = fte_count_xl_ss
        tfteml = fte_count_ml_ss
    elif df['Delivery Model'].eq("On-site").any():
        SFAE = mt.ceil(fte_count_xl_os*hmpct*2)/2
        SFAML = mt.ceil(fte_count_ml_os*hmpct*2)/2
        tle = mt.floor(fte_count_xl_os/6)
        tlml = mt.floor(fte_count_ml_os/6)
        FAE = fte_count_xl_os - SFAE - tle
        FAML = fte_count_ml_os - SFAML - tlml
        tftec = fte_count_xl_os
        tfteml = fte_count_ml_os
    elif df['Delivery Model'].eq("Mixed").any():
        SFAE = mt.ceil(fte_count_xl_os*hmpct*2)/2
        SFAML = mt.ceil(fte_count_ml_os*hmpct*2)/2
        tle = mt.floor(fte_count_xl_m/6)
        tlml = mt.floor(fte_count_ml_m/6)
        FAE = fte_count_xl_m - SFAE - tle
        FAML = fte_count_ml_m - SFAML - tlml
        tftec = fte_count_xl_m
        tfteml = fte_count_ml_m
    
    dfdb = df.iloc[:,:71]
    dfdb.drop(dfdb.columns[[64,65,67,69]],axis=1,inplace = True)
    dfdb['Final_Est_Hours'] = df.iloc[:,85]
    dfdb['Total_Est_FTE'] = tftec
    dfdb['FA'] = FAE
    dfdb['SFA'] = SFAE
    dfdb['FM'] = tle
    dfdb['Final_Est_Hours_ML'] = df.iloc[:,101]
    dfdb['Total_Est_FTE_ML'] = tfteml
    dfdb['FA_ML'] = FAML
    dfdb['SFA_ML'] = SFAML
    dfdb['FM_ML'] = tlml
    dfdb['instance_key'] = str(uuid.uuid4())[:12]
    dbdf = dfdb.rename(columns = {'Average Spend per Site':'Avg_Spend_Site',
                                'Client Name': 'Client_Name',
                                'Average Site Multiplier value':'Classification',
                                'Adjusted No of Sites':'Adj_Nof_Sites',
                                'Total Managed Spend': 'Total_Managed_Spend',
                                'Number of Sites':'Number_of_Sites',
                                'Contract Structure Option':'Contract_Structure',
                                'Contract Structure Multiplier':'Contract_Structure_Multiplier',
                                'Spend Ratio Option':'Fixed_Var_Spend_Ratio',
                                'Spend Ratio Multiplier':'Fixed_Var_Spend_Ratio_Multiplier',
                                'Principal/MA Option':'Principal_MA',
                                'Principal/MA Multiplier':'Principal_MA_Multiplier',
                                'Client Reporting Level Option':'Client_Reporting_Level',
                                'Client Reporting Level Multiplier':'Client_Reporting_Level_Multiplier',
                                'Tech Stack Option':'Tech_Stack','Tech Stack Multiplier':'Tech_Stack_Multiplier',
                                'Automation Adjustment Option':'Automation_Adjustments',
                                'Automation Adjustment Multiplier':'Automation_Adjustments_Multiplier',
                                'Bank Account Option':'Bank_Account','Bank Account Multiplier':'Bank_Account_Multiplier',
                                'Delivery Model':'Delivery_Model','1.Billing_freq':'Billing_Frequency',
                                '1.Billing_adj':'Billing_Value','2.Fund Reconciliations_freq':'Fund_Reconciliations_Frequency',
                                '2.Fund Reconciliations':'Fund_Reconciliations_Value','3.Payment_freq':'Payment_Frequency',
                                '3.Payment':'Payment_Value',
                                '4.Monthly JDE period close and Open PO review_freq':'Period_close_and_Open_PO_review_Frequency',
                                '4.Monthly JDE period close and Open PO review':'Period_close_and_Open_PO_review_Value',
                                '5.Monthly JDE Balance Sheet Reconciliation_freq':'Balance_Sheet_Reconciliation_Frequency',
                                '5.Monthly JDE Balance Sheet Reconciliation':'Balance_Sheet_Reconciliation_Value',
                                '6.Corporate Month End Revenue/Costs Adjustments_freq':'Revenue_Costs_Adjustments_Frequency',
                                '6.Corporate Month End Revenue/Costs Adjustments':'Revenue_Costs_Adjustments_Value',
                                '7.Corporate Pass Through Reconciliation_freq':'Pass_Through_Reconciliation_Frequency',
                                '7.Corporate Pass Through Reconciliation':'Pass_Through_Reconciliation_Value',
                                '8.Corporate Payment Entries Submission_freq':'Payment_Entries_Submission_Frequency',
                                '8.Corporate Payment Entries Submission':'Payment_Entries_Submission_Value',
                                '9.Internal & External Audit Sampling Requests (SOC1 & SOX)_freq':'Internal_External_Audit_Frequency',
                                '9.Internal & External Audit Sampling Requests (SOC1 & SOX)':'Internal_External_Audit_Value',
                                '10.Corporate P&L Month End Review, Analysis & Queries_freq':'PL_review_Frequency',
                                '10.Corporate P&L Month End Review, Analysis & Queries':'PL_review_Value',
                                '11.Corporate Yearly Budget - Preparation, Review & Approval_freq':'Yearly_budget_prepration_Frequency',
                                '11.Corporate Yearly Budget - Preparation, Review & Approval':'Yearly_budget_prepration_Value',
                                '12.Corporate Monthly Forecast - Preparation, Review & Approval_freq':'Monthly_forcast_prepration_Frequency',
                                '12.Corporate Monthly Forecast - Preparation, Review & Approval':'Monthly_forcast_prepration_Value',
                                '13.Corporate Operation Merit & Bonus Review_freq':'Operation_Merit_Bonus_Review_Frequency',
                                '13.Corporate Operation Merit & Bonus Review':'Operation_Merit_Bonus_Review_Value',
                                '14.Client Month End Accruals - Open PO, Rental, Utilities etc. - Manual Journal Entries Posting_freq':'Manual_Journal_Entries_Posting_Frequency',
                                '14.Client Month End Accruals - Open PO, Rental, Utilities etc. - Manual Journal Entries Posting':'Manual_Journal_Entries_Posting_Value',
                                '15.Monthly Operational Call for Client Month End Close (Queries from FM - Finance Related)_freq':'Monthly_Operational_Call_Frequency',
                                '15.Monthly Operational Call for Client Month End Close (Queries from FM - Finance Related)':'Monthly_Operational_Call_Value',
                                '16.Client Budget - Management Fee & Payroll Calculation; Vendor Spend Data_freq':'Budget_Management_Fee_Payroll_Calculation_Frequency',
                                '16.Client Budget - Management Fee & Payroll Calculation; Vendor Spend Data':'Budget_Management_Fee_Payroll_Calculation_Value',
                                '17.Client Forecast - Vendor Spend_freq':'Client_Forecast_Vendor_Spend_Value',
                                '17.Client Forecast - Vendor Spend':'Client_Forecast_Vendor_Spend_Frequency',
                                '18.Client Savings Report_freq':'Client_Savings_Report_Value',
                                '18.Client Savings Report':'Client_Savings_Report_Frequency',
                                '19.Client Finance Audit Support_freq':'Client_Finance_Audit_Supporting_Value',
                                '19.Client Finance Audit Support':'Client_Finance_Audit_Supporting_Frequency',
                                '20.Client Billing to Actuals Reconciliation_freq':'Client_Billing_to_Actuals_Reconciliation_Frequency',
                                '20.Client Billing to Actuals Reconciliation':'Client_Billing_to_Actuals_Reconciliation_Value',
                                'Standard Report_freq':'Standard_Report_Frequency','Standard Report':'Standard_Report_Value','Customised Report_freq':'Customized_Reporting_Frequency','Customised Report':'Customized_Reporting_Value'})

    dft = dbdf.reindex(columns = ['instance_key','Client_Name','Country','Region','Total_Managed_Spend',
                    'Number_of_Sites','Contract_Structure','Contract_Structure_Multiplier',
                    'Fixed_Var_Spend_Ratio','Fixed_Var_Spend_Ratio_Multiplier','Principal_MA',
                    'Principal_MA_Multiplier','Client_Reporting_Level','Client_Reporting_Level_Multiplier',
                    'Tech_Stack','Tech_Stack_Multiplier','Automation_Adjustments','Automation_Adjustments_Multiplier',
                    'Bank_Account','Bank_Account_Multiplier','Delivery_Model','Avg_Spend_Site','Classification','Adj_Nof_Sites',
                    'Billing_Frequency','Billing_Value',
                    'Fund_Reconciliations_Frequency','Fund_Reconciliations_Value',
                    'Payment_Frequency','Payment_Value','Period_close_and_Open_PO_review_Frequency',
                    'Period_close_and_Open_PO_review_Value',
                    'Balance_Sheet_Reconciliation_Frequency',
                    'Balance_Sheet_Reconciliation_Value',
                    'Revenue_Costs_Adjustments_Frequency',
                    'Revenue_Costs_Adjustments_Value',
                    'Pass_Through_Reconciliation_Frequency',
                    'Pass_Through_Reconciliation_Value',
                    'Payment_Entries_Submission_Frequency',
                    'Payment_Entries_Submission_Value',
                    'Internal_External_Audit_Frequency',
                    'Internal_External_Audit_Value',
                    'PL_review_Frequency',
                    'PL_review_Value',
                    'Yearly_budget_prepration_Frequency',
                    'Yearly_budget_prepration_Value',
                    'Monthly_forcast_prepration_Frequency',
                    'Monthly_forcast_prepration_Value',
                    'Operation_Merit_Bonus_Review_Frequency',
                    'Operation_Merit_Bonus_Review_Value',
                    'Manual_Journal_Entries_Posting_Frequency',
                    'Manual_Journal_Entries_Posting_Value',
                    'Monthly_Operational_Call_Frequency',
                    'Monthly_Operational_Call_Value',
                    'Budget_Management_Fee_Payroll_Calculation_Frequency',
                    'Budget_Management_Fee_Payroll_Calculation_Value',
                    'Client_Forecast_Vendor_Spend_Value',
                    'Client_Forecast_Vendor_Spend_Frequency',
                    'Client_Savings_Report_Value',
                    'Client_Savings_Report_Frequency',
                    'Client_Finance_Audit_Supporting_Value',
                    'Client_Finance_Audit_Supporting_Frequency',
                    'Client_Billing_to_Actuals_Reconciliation_Frequency',
                    'Client_Billing_to_Actuals_Reconciliation_Value',
                    'Standard_Report_Frequency',
                    'Standard_Report_Value',
                    'Customized_Reporting_Frequency',
                    'Customized_Reporting_Value','Final_Est_Hours','Total_Est_FTE',
                    'FA','SFA','FM','Final_Est_Hours_ML','Total_Est_FTE_ML','FA_ML',
                    'SFA_ML','FM_ML'])

    dfam = pd.DataFrame({"Rule Based":[chrs,tftec,"------------------------",FAE,SFAE,tle], "ML Predicted":[mlhrs,tfteml,"------------------------",FAML,SFAML,tlml]},index=["Total Hours", "Total FTE Count","Recommended Role", "Financial Analyst","Sr. Financial Analyst", "Manager/Team-Lead"])
    actable = pd.DataFrame({"Activities": ['Billing','Fund Reconciliations','Payment','Monthly JDE period close and Open PO review',
                                                    'Monthly JDE Balance Sheet Reconciliation','Corporate Month End Revenue/Costs Adjustments',
                                                    'Corporate Pass Through Reconciliation','Corporate Payment Entries Submission','Internal & External Audit Sampling Requests (SOC1 & SOX)',
                                                    'Corporate P&L Month End Review, Analysis & Queries','Corporate Yearly Budget - Preparation, Review & Approval','Corporate Monthly Forecast - Preparation, Review & Approval',
                                                    'Corporate Operation Merit & Bonus Review','Client Month End Accruals - Open PO, Rental, Utilities etc. - Manual Journal Entries Posting','Monthly Operational Call for Client Month End Close (Queries from FM - Finance Related)',
                                                    'Client Budget - Management Fee & Payroll Calculation; Vendor Spend Data','Client Forecast - Vendor Spend','Client Savings Report','Client Finance Audit Support',
                                                    'Client Billing to Actuals Reconciliation','Standard Report','Customised Report'],
                                "Hours":[df['1.Billing_adj'].sum().round(1),df['2.Fund Reconciliations'].sum().round(1),df['3.Payment'].sum().round(1),df['4.Monthly JDE period close and Open PO review'].sum().round(1),df['5.Monthly JDE Balance Sheet Reconciliation'].sum().round(1),
                                            df['6.Corporate Month End Revenue/Costs Adjustments'].sum().round(1),df['7.Corporate Pass Through Reconciliation'].sum().round(1),df['8.Corporate Payment Entries Submission'].sum().round(1),df['9.Internal & External Audit Sampling Requests (SOC1 & SOX)'].sum().round(1),df['10.Corporate P&L Month End Review, Analysis & Queries'].sum().round(1),
                                            df['11.Corporate Yearly Budget - Preparation, Review & Approval'].sum().round(1),df['12.Corporate Monthly Forecast - Preparation, Review & Approval'].sum().round(1),df['13.Corporate Operation Merit & Bonus Review'].sum().round(1),df['14.Client Month End Accruals - Open PO, Rental, Utilities etc. - Manual Journal Entries Posting'].sum().round(1),df['15.Monthly Operational Call for Client Month End Close (Queries from FM - Finance Related)'].sum().round(1),
                                            df['16.Client Budget - Management Fee & Payroll Calculation; Vendor Spend Data'].sum().round(1),df['17.Client Forecast - Vendor Spend'].sum().round(1),df['18.Client Savings Report'].sum().round(1),df['19.Client Finance Audit Support'].sum().round(1),df['20.Client Billing to Actuals Reconciliation'].sum().round(1),
                                            df['Standard Report'].sum().round(1),df['Customised Report'].sum().round(1)]},index = (1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22))
    
    with pd.ExcelWriter('Summary_File.xlsx', engine='openpyxl') as writer:
                dfam.to_excel(writer, sheet_name='Summary')
                actable.to_excel(writer, sheet_name='Activity Summary')
                dft.to_excel(writer, sheet_name='Inputs')    
#-------------------------------------------Enable CORS---------------------------------------------------------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)
#-------------------------------------------Finance Management endpoint---------------------------------------------------------------------------------------------------
@app.post("/finance_management")
async def finance_management(request: Request):
    try:
        input_fm = await request.json()
        logging.info(f"Received input data: {input_fm}")
        radf_1 = pd.DataFrame.from_records(input_fm)
        logging.info(f"Converted input data to DataFrame: {radf_1}")
        fm_summary = fmanagement(radf_1)
        logging.info(f"Generated summary data: {fm_summary}")
        # Convert DataFrame to dictionary
        fm_summary.fillna("None", inplace=True)
        fm_summary_dict = fm_summary.reset_index().to_dict(orient='records')#orient='records'
        return fm_summary_dict
    except Exception as err:
        logging.error(f"Error processing input data: {err}")
        raise HTTPException(status_code=400, detail=f"bad data: {err}")

@app.post("/finance_management/fm_summary_download")
async def fm_sum_dnld(request:Request):
    try:
        input_fmsum = await request.json()
        radf_2 = pd.DataFrame.from_records(input_fmsum)
        fmsumdnld(radf_2)
        # return summary_download
    except Exception as err:
        raise HTTPException(status_code=400, detail=f"bad data: {err}")

#-------------------------------------------Finance Delivery endpoint---------------------------------------------------------------------------------------------------
@app.post("/calculate_fte")
async def calculate_fte(request:Request):
     try:
        body = await request.body()

        if not body:
            raise HTTPException(status_code=400, detail="Request body is empty")

        input_1 = await request.json()
        if not isinstance(input_1, list):
            raise HTTPException(status_code=400, detail="JSON body must be a list of dictionaries")

        df_1 = pd.DataFrame.from_records(input_1)
        fte_summ = calculate_fte_requirement(df_1)
        fte_summary_dict = fte_summ.reset_index().to_dict(orient='records')#orient='records'
        return fte_summary_dict

     except ValueError as ve:
        raise HTTPException(status_code=400, detail=f"bad data: {ve}")
     except Exception as err:
        raise HTTPException(status_code=400, detail=f"bad data: {err}")

@app.post("/calculate_fte/activity_summary")
async def calculate_activity_summary(request:Request):
    try:
        body = await request.body()
        logging.info(f'Request body: {body}')

        if body is None or len(body) == 0:
            raise HTTPException(status_code=400, detail="request body is empty")
        input_2 = await request.json()
        df_2 = pd.DataFrame.from_records(input_2)
        activity_smry = activity_summary(df_2)
        activity_summary_dict = activity_smry.to_dict(orient='records')#orient='records'
        return activity_summary_dict

    except Exception as err:
        raise HTTPException(status_code=400, detail=f"bad data: {err}")
    
@app.post("/calculate_fte/activity_summary/download")
async def download_summary_ep(request:Request):
    try:
        body = await request.body()
        logging.info(f'Request body: {body}')

        if not body:
            raise HTTPException(status_code=400, detail="Request body is empty")

        input_3 = await request.json()
        if not isinstance(input_3, list):
            raise HTTPException(status_code=400, detail="JSON body must be a list of dictionaries")
        
        df_3 = pd.DataFrame.from_records(input_3)
        file_path = download_summary(df_3)
        return FileResponse(
            path=file_path,
            filename="fte_summary.xlsx",
            media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            headers={"Content-Disposition": "attachment; filename=fte_summary.xlsx"}
        )
        # return download_sum

    except ValueError as ve:
        raise HTTPException(status_code=400, detail=f"Bad data: {ve}")
    except Exception as err:
        logging.error(f"Error: {err}")
        raise HTTPException(status_code=400, detail=f"Bad data: {err}")

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
