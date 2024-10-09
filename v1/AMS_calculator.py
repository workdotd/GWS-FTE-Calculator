
# -*- coding: utf-8 -*-
"""
Created on Wed Jun  5 10:30:06 2024

@author: SKureley
"""

import streamlit as st
import pandas as pd
import numpy as np
import joblib
import math as mt
import psycopg2
import dbconn


def run_2():
          
          xls = pd.ExcelFile("Copy of FTE_calc_input.xlsx")
          df_rf= pd.read_excel(xls, 'Sheet2')

          #getting all the labels from the sheet 
          contract = pd.read_excel(xls, 'Sheet1',usecols=['contract']).dropna(how='any',axis=0)
          spend_ratio = pd.read_excel(xls, 'Sheet1',usecols=['spend_ratio']).dropna(how='any',axis=0)
          principal_MA = pd.read_excel(xls, 'Sheet1',usecols=['principal_MA']).dropna(how='any',axis=0)
          client_reporting_level = pd.read_excel(xls, 'Sheet1',usecols=['client_reporting_level']).dropna(how='any',axis=0)
          tech_stack = pd.read_excel(xls, 'Sheet1',usecols=['tech_stack']).dropna(how='any',axis=0)
          automation_adjustment = pd.read_excel(xls, 'Sheet1',usecols=['automation_adjustment']).dropna(how='any',axis=0)
          bank_account = pd.read_excel(xls, 'Sheet1',usecols=['bank_account']).dropna(how='any',axis=0)
          delivery_model = pd.read_excel(xls, 'Sheet1',usecols=['delivery_model']).dropna(how='any',axis=0)
          #AR_activities = pd.read_excel(xls, 'Sheet1',usecols=['AR/AP Activities']).dropna(how='any',axis=0)
          #Reporting_activities = pd.read_excel(xls, 'Sheet1',usecols=['CBRE Reporting Activities']).dropna(how='any',axis=0)
          Countries = pd.read_excel(xls, 'Sheet1',usecols=['Countries']).dropna(how='any',axis=0)
          APAC_countries = pd.read_excel(xls, 'Sheet1',usecols=['APAC_countries']).dropna(how='any',axis=0)
          AMS_countries = pd.read_excel(xls, 'Sheet1',usecols=['AMS_countries']).dropna(how='any',axis=0)
          EMEA_countries = pd.read_excel(xls, 'Sheet1',usecols=['EMEA_countries']).dropna(how='any',axis=0)
          #Client_Reporting_Activities = pd.read_excel(xls, 'Sheet1',usecols=['Client Reporting Activities']).dropna(how='any',axis=0)
          Special_client_activity = pd.read_excel(xls, 'Sheet1',usecols=['Special_client_activity']).dropna(how='any',axis=0)
          All_activities = pd.read_excel(xls, 'Sheet1',usecols=['All_activities']).dropna(how='any',axis=0)
          LCA = pd.read_excel(xls, 'Sheet1',usecols=['LCA']).dropna(how='any',axis=0)
          MCA = pd.read_excel(xls, 'Sheet1',usecols=['MCA']).dropna(how='any',axis=0)
          HCA = pd.read_excel(xls, 'Sheet1',usecols=['HCA']).dropna(how='any',axis=0)

          contract = contract['contract'].unique().tolist()
          spend_ratio = spend_ratio['spend_ratio'].unique().tolist()
          principal_MA = principal_MA['principal_MA'].unique().tolist()
          client_reporting_level = client_reporting_level['client_reporting_level'].unique().tolist()
          tech_stack = tech_stack['tech_stack'].unique().tolist()
          automation_adjustment = automation_adjustment['automation_adjustment'].unique().tolist()
          bank_account = bank_account['bank_account'].unique().tolist()
          delivery_model = delivery_model['delivery_model'].unique().tolist()
          #AR_activities = AR_activities['AR/AP Activities'].unique().tolist()
          #Reporting_activities = Reporting_activities['CBRE Reporting Activities'].unique().tolist()
          Countries = Countries['Countries'].unique().tolist()
          APAC_countries = APAC_countries['APAC_countries'].unique().tolist()
          AMS_countries = AMS_countries['AMS_countries'].unique().tolist()
          EMEA_countries = EMEA_countries['EMEA_countries'].unique().tolist()
          #Client_Reporting_Activities = Client_Reporting_Activities['Client Reporting Activities'].unique().tolist()
          Special_client_activity = Special_client_activity['Special_client_activity'].unique().tolist()
          All_activities = All_activities['All_activities'].unique().tolist()
          LCA = LCA['LCA'].unique().tolist()
          MCA = MCA['MCA'].unique().tolist()
          HCA = HCA['HCA'].unique().tolist()
          
          colaa, colbb = st.columns([1,4])
          colaa.write("")
          colaa.write("")
          colaa = colaa.write("Client Name")
          client_name = colbb.text_input("", key="client_name_ams")
          
          def handle_input():
                     
           if client_name:  # Check if something is entered
                     st.session_state.input_filled = True
                     #st.write("Thanks for entering the text!")
           else:
                     st.session_state.input_filled = False
                     st.error("This field is required.")  # Show error if input is empty
          # Proceed with other operations if input is filled
           if st.session_state.input_filled:
                     st.write("You entered:", client_name)
          # Initialize or reset the session state for input_filled
           if 'input_filled' not in st.session_state:
                     st.session_state.input_filled = False
          # Call the function to display the input form and handle logic
          handle_input()

          data = {
          "AR/AP Activities": {"1.Billing": None, "2.Fund Reconciliations": None, "3.Payment": None},
          "CBRE Reporting Activities": {
          "4.Monthly JDE period close and Open PO review": None,
          "5.Monhtly JDE Balance Sheet Reconciliation": None,
          "6.Corporate Month End Revenue/Costs Adjustments": None,
          "7.Corporate Pass Through Reconciliation": None,
          "8.Corporate Payment Entries Submission": None,
          "9.Internal & External Audit Sampling Requests (SOC1 & SOX)": None,
          "10.Corporate P&L Month End Review, Analysis & Queries": None,
          "11.Corporate Yearly Budget - Preparation, Review & Approval": None,
          "12.Corporate Monthly Forecast - Preparation, Review & Approval": None,
          "13.Corporate Operation Merit & Bonus Review": None,
          },
          "Client Reporting Activities":{"14.Client Month End Accruals - Open PO, Rental, Utilities etc. - Manual Journal Entries Posting": None,
            "15.Monthly Operational Call for Client Month End Close (Queries from FM - Finance Related)": None,
            "16.Client Budget - Management Fee & Payroll Calculation; Vendor Spend Data": None,
            "17.Client Forecast - Vendor Spend": None,
            "18.Client Savings Report": None,
            "19.Client Finance Audit Support": None,
            "20.Client Billing to Actuals Reconciliation": None
            }
           }
          
          AR_activities = list(data["AR/AP Activities"].keys())
          Reporting_activities = list(data["CBRE Reporting Activities"].keys())
          Client_Reporting_Activities = list(data["Client Reporting Activities"].keys())
          
          # Initialize session state for data entries as a DataFrame
          if 'data_entries' not in st.session_state:
              st.session_state['data_entries'] = pd.DataFrame()

          
          managed_spend = st.number_input("Total Managed Spend (USD)",min_value=0,key="managed_spend_ams",placeholder="Type a number...")
          
          try:
               spend_value=int(managed_spend)
               formatted_number=f"{spend_value:,}"
               st.write(f"{formatted_number}")
          except ValueError:
               st.write("Enter a valid number")
          
          # Selection of the region and displaying country selections based on the region
          
          countries = AMS_countries
          selected_countries = st.multiselect("Select countries:", countries)

          # For each selected country, provide an input for the number of sites
          sites_input = {}
          for country in selected_countries:
              num_sites = st.number_input(f"Number of Sites for {country}:", min_value=0, key=f"sites_{country}")
              sites_input[country] = num_sites

          st.header("Contract Variables")
          # Dropdowns for contract variables
          contract_vars = {
              "Contract Structure": {"GMP": 0.90, "Cost Plus": 1.00, "Fixed Price": 0.90, "Other": 1.20},
              "Spend Ratio": {"25% fixed; 75% variable": 1.20, "50% fixed; 50% variable": 1.00, "75% fixed; 25% variable": 0.90},
              "Principal/MA": {"Full Principal (immaterial agency spend)": 1.00, "Full Managing Agent (immaterial principal spend)": 0.10, "50% Principal; 50% MA": 0.60, "25% Principal; 75% MA":0.40, "75% Principal; 25% MA": 0.90 },
              "Client Reporting Level": {"Country-level": 0.90, "Site-level": 1.00, "Cost-center level": 1.20},
              "Tech Stack": {"Standard - Mybuy/JDE/PS": 1.00, "Full Iscala": 0.90, "Full PS": 1.10, "Non-standard": 1.20},
              "Automation Adjustment": {"High": 0.75, "Mid": 0.85, "Low": 0.90, "None": 1.00},
              "Bank Account": {"Dedicated": 1.00, "Shared/Ded": 1.10, "Corporate": 1.20}
          }

          contract_selections = {}
          # Arrange dropdowns in two rows using Streamlit columns
          keys = list(contract_vars.keys())
          #first_row_vars = keys[:4]  # First four contract variables
          #second_row_vars = keys[4:]  # Remaining three contract variables

          # First row of contract variables
          #cols = st.columns(4)
          for i, var_name in enumerate(keys):
            options = contract_vars[var_name]
            selected_option = st.selectbox(f"{i+1}.{var_name}", list(options.keys()), key=f"{var_name}_ams")
            contract_selections[var_name] = {'Option': selected_option, 'Multiplier': options[selected_option]}
                  
          frequency_options = { 'Monthly': 1,'None': 0, 'Weekly': 4, 'Bi-Weekly': 2, 'Quarterly': 0.333333333333333, 'Yearly': 0.083}
         
          if st.session_state.get('reset_triggered',False):
              for activity in AR_activities + Reporting_activities + Client_Reporting_Activities + Special_client_activity:
                    st.session_state[f"{activity}_ams"] = 'Monthly'
                    st.session_state['reset_triggered'] = False
                
          def reset_frequencies():
                 for activity in AR_activities + Reporting_activities + Client_Reporting_Activities + Special_client_activity:
                                st.session_state[f"{activity}_ams"] = 'None'
         
            
          st.header("AR/AP Activities")
          # Frequency selection for activities
          AR_activities = AR_activities  # Example activities
          activity_frequencies1 = {}
          # frequency_options1 = { 'Monthly': 1,'None': 0, 'Weekly': 4, 'Bi-Weekly': 2, 'Quarterly': 0.333333333333333, 'Yearly': 0.083}
          for activity in AR_activities: 
              selected_frequency = st.selectbox(f"{activity}", list(frequency_options.keys()), key=f"{activity}_ams")
              activity_frequencies1[activity] = frequency_options[selected_frequency]
        
          st.header("CBRE Reporting Activities")
          # Frequency selection for activities
          Reporting_activities = Reporting_activities  # Example activities
          activity_frequencies2 = {}
          # frequency_options2 = {'Monthly': 1,'None': 0, 'Weekly': 4, 'Bi-Weekly': 2, 'Quarterly': 0.333333333333333, 'Yearly': 0.083}
          for activity in Reporting_activities: 
              selected_frequency = st.selectbox(f"{activity}", list(frequency_options.keys()), key=f"{activity}_ams")
              activity_frequencies2[activity] = frequency_options[selected_frequency]
         
          st.header("Client Reporting Activities")
          # Frequency selection for activities
          Client_Reporting_Activities = Client_Reporting_Activities  # Example activities
          activity_frequencies3 = {}
          #frequency_options3 = { 'Monthly': 1,'None': 0, 'Weekly': 4, 'Bi-Weekly': 2, 'Quarterly': 0.333333333333333, 'Yearly': 0.083}
          for activity in Client_Reporting_Activities: 
              selected_frequency = st.selectbox(f"{activity}", list(frequency_options.keys()), key=f"{activity}_ams")
              activity_frequencies3[activity] = frequency_options[selected_frequency]
              
             
          #st.text("21.Client Reporting")
          # Frequency selection for activities
          Special_client_activity = Special_client_activity  
          selected_activities = st.radio("21.Client Reporting - select one of the below :",Special_client_activity,key="activity_selection_ams")
          # frequency_options4 = {'Monthly': 1,'None': 0, 'Weekly': 4, 'Bi-Weekly': 2, 'Quarterly': 0.333333333333333, 'Yearly': 0.083}
          selected_frequency1 = st.selectbox(f"{selected_activities}", list(frequency_options.keys()), key=f"{selected_activities}_ams")
          #selected_frequency1 = st.selectbox(f"{selected_activities}", list(frequency_options1.keys()), key=f"{selected_activities}")
          activity_frequencies4={activity:0 for activity in Special_client_activity}
          activity_frequencies4[selected_activities] = frequency_options[selected_frequency1]

          # Reset button to trigger reset logic
          if st.button('Reset Frequencies to Monthly', key="reset_ams"):
              st.session_state['reset_triggered'] = True
              st.experimental_rerun()  # Rerun the app to update the UI with the reset values
              
              
          # calssification (Average Site Size Multiplier): 
          def avg_site_size_multiplier(avg_spend_per_site):
              result = 0 
              if avg_spend_per_site < 80000:
                      result = 0.6
              elif avg_spend_per_site < 150000:
                      result = 0.8
              elif avg_spend_per_site < 500000:
                      result = 1
              elif avg_spend_per_site < 1200000:
                      result = 1
              elif avg_spend_per_site >= 1200000:
                      result = 1.1
              return result

          # Count Activities Subscribed:
          def count_activities_subscribed(activities):
              count = 0
              for k,v in activities.items():
                  if v>0:
                      count += 1
              return count

          # Total Activity Hours:
          def total_activity_hrs(activities):
              return sum(activities.values())    
          

          st.header("Delivery Model")
          selected_delivery_model=st.selectbox("Select Delivery Model",delivery_model,key="delivery_ams")

          # Delivery Model 
          def delivery_model_multiplier(dm, ah, p):
              if dm == "Shared Services":
                  result = ah * 1
              elif dm == "On-site":
                  result = ah * 1.3
              elif dm == "Mixed":
                  result = ah * p + (1 - p) * ah * 1.3
              return result      
                     
              
          # Button to calculate and update DataFrame
          col1, col2, col3 , col4, col5 = st.columns(5)
          with col1:
              pass
          with col2:
              pass
          with col4:
              pass
          with col5:
              pass
          with col3 :
              center_button = st.button('Calculate FTE Requirement',key="Calc_Ams")
          if center_button:
              st.session_state['data_entries']=pd.DataFrame()
              entries = []
              for country, num_sites in sites_input.items():
                  entry = {
                      'Client Name' : client_name,
                      'Country': country,
                      'Region': "AMS",
                      'Total Managed Spend': managed_spend,
                      'Number of Sites': num_sites,
                      'Delivery Model' : selected_delivery_model
                  }

                  # Add contract selections to the entry
                  for var, details in contract_selections.items():
                      entry[f'{var} Option'] = details['Option']
                      entry[f'{var} Multiplier'] = details['Multiplier']
                 
                  # Add activities and their selected frequencies
                  freq1,freq2,freq3,freq4 = None,None,None,None
                  for activity, frequency_value in activity_frequencies1.items():
                      filtered_df = df_rf[(df_rf['L2 Process'] == activity) | (df_rf['L3 Process'] == activity)]
                      filtered_df = filtered_df[filtered_df['Country'] == country]
                      if not filtered_df.empty:
                          base_value = filtered_df.iloc[0]['Time Spend/Country']
                          calculated_value = base_value * frequency_value
                          if frequency_value == 4:
                               freq1 = "Weekly"
                          elif frequency_value == 2:
                               freq1 = "Bi-Weekly"
                          elif frequency_value == 1:
                               freq1 = "Monthly"
                          elif frequency_value == 0.333333333333333:
                               freq1 = "Quarterly"
                          elif frequency_value == 0.083:
                               freq1 = "Yearly"
                          elif frequency_value == 0:
                               freq1 = "None"

                          entry[f'{activity}_freq'] = freq1
                          entry[f'{activity}'] = calculated_value
                      else:
                          entry[f'{activity}'] = 0
                  
                  for activity, frequency_value in activity_frequencies2.items():
                      print(f"processing: {activity}")
                      filtered_df = df_rf[(df_rf['L2 Process'] == activity) | (df_rf['L3 Process'] == activity)]
                      filtered_df = filtered_df[filtered_df['Country'] == country]
                      
                      if not filtered_df.empty:
                          base_value = filtered_df.iloc[0]['Time Spend/Country']
                          calculated_value = base_value * frequency_value
                          if frequency_value == 4:
                               freq2 = "Weekly"
                          elif frequency_value == 2:
                               freq2 = "Bi-Weekly"
                          elif frequency_value == 1:
                               freq2 = "Monthly"
                          elif frequency_value == 0.333333333333333:
                               freq2 = "Quarterly"
                          elif frequency_value == 0.083:
                               freq2 = "Yearly"
                          elif frequency_value == 0:
                               freq2 = "None"

                          entry[f'{activity}_freq'] = freq2
                          entry[f'{activity}'] = calculated_value
                      else:
                          entry[f'{activity}'] = 0
                  
                  for activity, frequency_value in activity_frequencies3.items():
                      filtered_df = df_rf[(df_rf['L2 Process'] == activity) | (df_rf['L3 Process'] == activity)]
                      filtered_df = filtered_df[filtered_df['Country'] == country]
                      if not filtered_df.empty:
                          base_value = filtered_df.iloc[0]['Time Spend/Country']
                          calculated_value = base_value * frequency_value
                          if frequency_value == 4:
                               freq3 = "Weekly"
                          elif frequency_value == 2:
                               freq3 = "Bi-Weekly"
                          elif frequency_value == 1:
                               freq3 = "Monthly"
                          elif frequency_value == 0.333333333333333:
                               freq3 = "Quarterly"
                          elif frequency_value == 0.083:
                               freq3 = "Yearly"
                          elif frequency_value == 0:
                               freq3 = "None"

                          entry[f'{activity}_freq'] = freq3
                          entry[f'{activity}'] = calculated_value
                      else:
                          entry[f'{activity}'] = 0
                          
                  # Add activities and their selected frequencies
                  calculated_value1 = 0
                  for special_activity, frequency_value1 in activity_frequencies4.items():
                      #entry[f'{activity}'] = frequency_value
                      filtered_df = df_rf[(df_rf['L2 Process'] == special_activity) | (df_rf['L3 Process'] == special_activity)] 
                      filtered_df = filtered_df[filtered_df['Country'] == country] 
                      if not filtered_df.empty: 
                          base_value1 = filtered_df.iloc[0]['Time Spend/Country'] 
                          calculated_value1 = base_value1 * frequency_value1
                          if frequency_value1 == 4:
                               freq4 = "Weekly"
                          elif frequency_value1 == 2:
                               freq4 = "Bi-Weekly"
                          elif frequency_value1 == 1:
                               freq4 = "Monthly"
                          elif frequency_value1 == 0.333333333333333:
                               freq4 = "Quarterly"
                          elif frequency_value1 == 0.083:
                               freq4 = "Yearly"
                          elif frequency_value1 == 0:
                               freq4 = "None"

                          entry[f'{special_activity}_freq'] = freq4
                          entry[f'{special_activity}'] = calculated_value1
                      else: 
                          entry[f'{special_activity}'] = 0
                          
                  entries.append(entry) 
              new_df = pd.DataFrame(entries) 
              st.session_state['data_entries'] = new_df
              
              # Ensure all necessary columns exist in st.session_state['data_entries']
              required_columns = ['1.Billing', '2.Fund Reconciliations', '3.Payment',
                                  '4.Monthly JDE period close and Open PO review',
                                  '5.Monhtly JDE Balance Sheet Reconciliation',
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
                                  'Customised Report'
                                 ]
              for col in required_columns:
                 if col not in st.session_state['data_entries'].columns:
                     st.session_state['data_entries'][col] = 0
    
          # Check if the session state DataFrame is empty
              if 'data_entries' not in st.session_state or st.session_state['data_entries'].empty:
                  st.session_state['data_entries'] = new_df
              else:
                  # Check for duplicates
                  st.session_state['data_entries'] = pd.concat([st.session_state['data_entries'], new_df], ignore_index=True).drop_duplicates(keep='first')
              
              st.session_state['data_entries']['Sites/Country'] = st.session_state['data_entries']['Number of Sites']
              st.session_state['data_entries']['Total No of Sites'] = st.session_state['data_entries']['Sites/Country'].sum()
              
              # Calculate Average Spend per Site
              st.session_state['data_entries']['Average Spend per Site'] = st.session_state['data_entries']['Total Managed Spend'] / st.session_state['data_entries']['Total No of Sites']
              
              # Calculate Spend per Country
              st.session_state['data_entries']['Spend per Country'] = st.session_state['data_entries']['Average Spend per Site'] * st.session_state['data_entries']['Total No of Sites']

              # Apply custom function for site size multiplier
              st.session_state['data_entries']['Average Site Multiplier value'] = st.session_state['data_entries'].apply(lambda row: avg_site_size_multiplier(row['Average Spend per Site']), axis=1)

              # Calculate Adjusted Number of Sites
              st.session_state['data_entries']['Adjusted No of Sites/Country'] = np.where(st.session_state['data_entries']['Sites/Country'] * st.session_state['data_entries']['Average Site Multiplier value'] >=1,st.session_state['data_entries']['Sites/Country'] * st.session_state['data_entries']['Average Site Multiplier value'],1)
              st.session_state['data_entries']['Adjusted No of Sites'] = st.session_state['data_entries']['Adjusted No of Sites/Country'].sum()
              
              # Calculate Adj Billing
              st.session_state['data_entries']['1.Billing'] = np.where(st.session_state['data_entries']['Adjusted No of Sites/Country'] <= 1,st.session_state['data_entries']['1.Billing'] * 2 ,st.session_state['data_entries']['1.Billing']*st.session_state['data_entries']['Adjusted No of Sites/Country'])
              
              # Multipliers Combo:
              st.session_state['data_entries']['Contrct_Spend_Auto_CRL_PMA'] = st.session_state['data_entries']['Contract Structure Multiplier'] * st.session_state['data_entries']['Spend Ratio Multiplier'] * st.session_state['data_entries']['Principal/MA Multiplier'] * st.session_state['data_entries']['Client Reporting Level Multiplier'] * st.session_state['data_entries']['Automation Adjustment Multiplier']
              st.session_state['data_entries']['Bank_PMA'] = st.session_state['data_entries']['Bank Account Multiplier'] * st.session_state['data_entries']['Principal/MA Multiplier']
              st.session_state['data_entries']['tech_auto_pma'] = st.session_state['data_entries']['Principal/MA Multiplier'] * st.session_state['data_entries']['Tech Stack Multiplier'] * st.session_state['data_entries']['Automation Adjustment Multiplier']
              st.session_state['data_entries']['Contrct_crl'] = st.session_state['data_entries']['Contract Structure Multiplier'] * st.session_state['data_entries']['Client Reporting Level Multiplier']
              st.session_state['data_entries']['Contrct_crl_auto'] = st.session_state['data_entries']['Contract Structure Multiplier'] * st.session_state['data_entries']['Client Reporting Level Multiplier'] * st.session_state['data_entries']['Automation Adjustment Multiplier']
              st.session_state['data_entries']['tech_auto'] = st.session_state['data_entries']['Tech Stack Multiplier'] * st.session_state['data_entries']['Automation Adjustment Multiplier']
              
              st.session_state['data_entries']['adj_time_CSACP'] = st.session_state['data_entries']['1.Billing'] * st.session_state['data_entries']['Contrct_Spend_Auto_CRL_PMA']
              st.session_state['data_entries']['adj_time_BP'] = (st.session_state['data_entries']['2.Fund Reconciliations'] + st.session_state['data_entries']['3.Payment']) * st.session_state['data_entries']['Bank_PMA']
              st.session_state['data_entries']['adj_time_TAP'] = (st.session_state['data_entries']['4.Monthly JDE period close and Open PO review'] + st.session_state['data_entries']['5.Monhtly JDE Balance Sheet Reconciliation'] + st.session_state['data_entries']['6.Corporate Month End Revenue/Costs Adjustments'] +st.session_state['data_entries']['7.Corporate Pass Through Reconciliation']+st.session_state['data_entries']['8.Corporate Payment Entries Submission']+st.session_state['data_entries']['9.Internal & External Audit Sampling Requests (SOC1 & SOX)'] +st.session_state['data_entries']['10.Corporate P&L Month End Review, Analysis & Queries'] +st.session_state['data_entries']['11.Corporate Yearly Budget - Preparation, Review & Approval']+st.session_state['data_entries']['12.Corporate Monthly Forecast - Preparation, Review & Approval']) * st.session_state['data_entries']['tech_auto_pma']
              st.session_state['data_entries']['adj_time_CC'] = st.session_state['data_entries']['14.Client Month End Accruals - Open PO, Rental, Utilities etc. - Manual Journal Entries Posting'] * st.session_state['data_entries']['Contrct_crl']
              st.session_state['data_entries']['adj_time_CCA'] = (st.session_state['data_entries']['Customised Report']+st.session_state['data_entries']['Standard Report']+st.session_state['data_entries']['16.Client Budget - Management Fee & Payroll Calculation; Vendor Spend Data']+st.session_state['data_entries']['17.Client Forecast - Vendor Spend']+st.session_state['data_entries']['18.Client Savings Report']+st.session_state['data_entries']['19.Client Finance Audit Support']+st.session_state['data_entries']['20.Client Billing to Actuals Reconciliation']) * st.session_state['data_entries']['Contrct_crl_auto']
              st.session_state['data_entries']['adj_time_None'] = st.session_state['data_entries']['15.Monthly Operational Call for Client Month End Close (Queries from FM - Finance Related)']
              st.session_state['data_entries']['adj_time_TA'] = st.session_state['data_entries']['13.Corporate Operation Merit & Bonus Review'] * st.session_state['data_entries']['tech_auto']
              st.session_state['data_entries']['Adj_Activity_Hours'] = st.session_state['data_entries']['adj_time_CSACP'] + st.session_state['data_entries']['adj_time_BP'] + st.session_state['data_entries']['adj_time_TAP'] + st.session_state['data_entries']['adj_time_CC']+ st.session_state['data_entries']['adj_time_None'] + st.session_state['data_entries']['adj_time_TA'] + st.session_state['data_entries']['adj_time_CCA'] 
              
              # Add +20% Ad hoc Overlay:
              st.session_state['data_entries']['after_add_overlay'] = st.session_state['data_entries']['Adj_Activity_Hours'] * 1.2
              st.session_state['data_entries']['adj_time_CSACP_low'] = st.session_state['data_entries']['adj_time_CSACP']
              st.session_state['data_entries']['adj_time_BP_low'] = st.session_state['data_entries']['adj_time_BP']
              st.session_state['data_entries']['adj_time_TAP_low'] = (st.session_state['data_entries']['4.Monthly JDE period close and Open PO review'] + st.session_state['data_entries']['5.Monhtly JDE Balance Sheet Reconciliation'] + st.session_state['data_entries']['6.Corporate Month End Revenue/Costs Adjustments'] +st.session_state['data_entries']['7.Corporate Pass Through Reconciliation']+st.session_state['data_entries']['8.Corporate Payment Entries Submission'] +st.session_state['data_entries']['9.Internal & External Audit Sampling Requests (SOC1 & SOX)'] +st.session_state['data_entries']['10.Corporate P&L Month End Review, Analysis & Queries'] +st.session_state['data_entries']['12.Corporate Monthly Forecast - Preparation, Review & Approval']) * st.session_state['data_entries']['tech_auto_pma'] + st.session_state['data_entries']['8.Corporate Payment Entries Submission']
              st.session_state['data_entries']['adj_time_CCA_low'] = (st.session_state['data_entries']['17.Client Forecast - Vendor Spend']+st.session_state['data_entries']['19.Client Finance Audit Support']) * st.session_state['data_entries']['Contrct_crl_auto']
              st.session_state['data_entries']['p'] = (st.session_state['data_entries']['adj_time_CSACP_low'] + st.session_state['data_entries']['adj_time_BP_low'] + st.session_state['data_entries']['adj_time_TAP_low'] + st.session_state['data_entries']['adj_time_CCA_low']) / st.session_state['data_entries']['Adj_Activity_Hours']
              st.session_state['data_entries']['adj_time_after_dm'] = st.session_state['data_entries'].apply(lambda row: delivery_model_multiplier(row['Delivery Model'],row['after_add_overlay'],row['p']),axis=1)
              st.session_state['data_entries']['adj_time_after_dm'].sum()
              st.session_state['data_entries']['Standard Report'].astype(float)
              
              #st.session_state['data_entries']['All_activities'] = activities
              st.session_state['data_entries']['Activities Subscribed'] = st.session_state['data_entries'].apply(lambda row:sum(row[col]>0 for col in All_activities if col in row.index),axis=1)
              st.session_state['data_entries']['Total Activity Hours']= st.session_state['data_entries']['Customised Report']+st.session_state['data_entries']['Standard Report']+st.session_state['data_entries']['3.Payment'].astype(float)+st.session_state['data_entries']['4.Monthly JDE period close and Open PO review'].astype(float) +st.session_state['data_entries']['5.Monhtly JDE Balance Sheet Reconciliation'].astype(float)+st.session_state['data_entries']['6.Corporate Month End Revenue/Costs Adjustments'].astype(float)+st.session_state['data_entries']['7.Corporate Pass Through Reconciliation'].astype(float)+st.session_state['data_entries']['8.Corporate Payment Entries Submission'].astype(float)+st.session_state['data_entries']['9.Internal & External Audit Sampling Requests (SOC1 & SOX)'].astype(float)+st.session_state['data_entries']['14.Client Month End Accruals - Open PO, Rental, Utilities etc. - Manual Journal Entries Posting'].astype(float)+st.session_state['data_entries']['15.Monthly Operational Call for Client Month End Close (Queries from FM - Finance Related)'].astype(float)+st.session_state['data_entries']['8.Corporate Payment Entries Submission'].astype(float)+st.session_state['data_entries']['10.Corporate P&L Month End Review, Analysis & Queries'].astype(float)+st.session_state['data_entries']['11.Corporate Yearly Budget - Preparation, Review & Approval'].astype(float)+st.session_state['data_entries']['12.Corporate Monthly Forecast - Preparation, Review & Approval'].astype(float)+st.session_state['data_entries']['13.Corporate Operation Merit & Bonus Review'].astype(float)+st.session_state['data_entries']['16.Client Budget - Management Fee & Payroll Calculation; Vendor Spend Data'].astype(float)+st.session_state['data_entries']['17.Client Forecast - Vendor Spend'].astype(float)+st.session_state['data_entries']['1.Billing'].astype(float)+st.session_state['data_entries']['2.Fund Reconciliations'].astype(float)+st.session_state['data_entries']['20.Client Billing to Actuals Reconciliation'].astype(float)+st.session_state['data_entries']['19.Client Finance Audit Support'].astype(float)+st.session_state['data_entries']['18.Client Savings Report'].astype(float)
              
              st.session_state['data_entries']=st.session_state['data_entries'].drop_duplicates(keep='first')
              
              st.session_state['data_entries']['bin_billing'] = (pd.qcut(st.session_state['data_entries']['1.Billing'], 10, labels=False, duplicates = 'drop') + 1) if st.session_state['data_entries']['1.Billing'].sum() >0 else 0
              st.session_state['data_entries']['bin_funds'] = (pd.qcut(st.session_state['data_entries']['2.Fund Reconciliations'], 5, labels=False, duplicates = 'drop') + 1) if st.session_state['data_entries']['2.Fund Reconciliations'].sum() >0 else 0
              st.session_state['data_entries']['bin_payments'] = (pd.qcut(st.session_state['data_entries']['3.Payment'], 5, labels=False, duplicates = 'drop') + 1) if st.session_state['data_entries']['3.Payment'].sum() >0 else 0
              st.session_state['data_entries']['bin_accruals'] = (pd.qcut(st.session_state['data_entries']['14.Client Month End Accruals - Open PO, Rental, Utilities etc. - Manual Journal Entries Posting'], 5, labels=False, duplicates = 'drop') + 1) if st.session_state['data_entries']['14.Client Month End Accruals - Open PO, Rental, Utilities etc. - Manual Journal Entries Posting'].sum() >0 else 0
              st.session_state['data_entries']['bin_Operation'] = (pd.qcut(st.session_state['data_entries']['15.Monthly Operational Call for Client Month End Close (Queries from FM - Finance Related)'], 5, labels=False, duplicates = 'drop') + 1) if st.session_state['data_entries']['15.Monthly Operational Call for Client Month End Close (Queries from FM - Finance Related)'].sum() >0 else 0
              st.session_state['data_entries']['bin_Savings Report'] = (pd.qcut(st.session_state['data_entries']['18.Client Savings Report'], 5, labels=False, duplicates = 'drop') + 1) if st.session_state['data_entries']['18.Client Savings Report'].sum() >0 else 0
              st.session_state['data_entries']['Bins Total'] = st.session_state['data_entries']['bin_billing'].sum()+st.session_state['data_entries']['bin_funds'].sum()+st.session_state['data_entries']['bin_payments'].sum()+st.session_state['data_entries']['bin_accruals'].sum()+st.session_state['data_entries']['bin_Operation'].sum()+st.session_state['data_entries']['Activities Subscribed'].sum() + st.session_state['data_entries']['18.Client Savings Report'].sum() - 6
              #st.success('df update')

             
              dml = pd.DataFrame(columns = ['Region','Country','Spend/Country','Total Activity Hours','bins_total'])
              dml['Region'] = "AMS"
              dml['Country'] = st.session_state['data_entries']['Country']
              dml['Spend/Country'] = st.session_state['data_entries']['Total Managed Spend']
              dml["Contract Structure"] = st.session_state['data_entries']['Contract Structure Multiplier']
              dml["Fixed/Var. Spend Ratio"] = st.session_state['data_entries']['Spend Ratio Multiplier']
              dml["Principal/MA"] = st.session_state['data_entries']['Principal/MA Multiplier']
              dml["Client Reporting Level"] = st.session_state['data_entries']['Client Reporting Level Multiplier']
              dml["Tech Stack"] = st.session_state['data_entries']['Contract Structure Multiplier']
              dml["Automation Adjustments"] = st.session_state['data_entries']['Tech Stack Multiplier']
              dml["Bank Account"] = st.session_state['data_entries']['Bank Account Multiplier']
              dml['LC Count'] = st.session_state['data_entries'].apply(lambda row:sum(row[col]>0 for col in LCA if col in row.index),axis=1)
              dml['MC Count'] = st.session_state['data_entries'].apply(lambda row:sum(row[col]>0 for col in MCA if col in row.index),axis=1)
              dml['HC Count'] = st.session_state['data_entries'].apply(lambda row:sum(row[col]>0 for col in HCA if col in row.index),axis=1)
              dml['LC Hours'] = st.session_state['data_entries']['adj_time_CSACP_low'] + st.session_state['data_entries']['adj_time_BP_low'] + st.session_state['data_entries']['adj_time_TAP_low'] + st.session_state['data_entries']['adj_time_CCA_low']
              dml['MC Hours'] = st.session_state['data_entries']['14.Client Month End Accruals - Open PO, Rental, Utilities etc. - Manual Journal Entries Posting']+st.session_state['data_entries']['Standard Report']+st.session_state['data_entries']['15.Monthly Operational Call for Client Month End Close (Queries from FM - Finance Related)']+st.session_state['data_entries']['16.Client Budget - Management Fee & Payroll Calculation; Vendor Spend Data']+st.session_state['data_entries']['18.Client Savings Report']
              dml['HC Hours'] = st.session_state['data_entries']['Customised Report']+st.session_state['data_entries']['11.Corporate Yearly Budget - Preparation, Review & Approval']+st.session_state['data_entries']['13.Corporate Operation Merit & Bonus Review']+st.session_state['data_entries']['20.Client Billing to Actuals Reconciliation']
              dml['bins_total'] = st.session_state['data_entries']['Bins Total']
             
              model = joblib.load("FTE_Calc_wc.pkl")
              prediction = model.predict(dml)
              
              
              data_len= len(st.session_state['data_entries'])
              pred_len=len(prediction)
              
              if data_len==pred_len:
                  st.session_state['data_entries']['ML Prediction'] = prediction
              else:
                  pass
              if data_len < pred_len:
                  st.session_state['data_entries']['ML Prediction'] = prediction[:data_len]
              else:
                  st.session_state['data_entries']=st.session_state['data_entries'].iloc[:pred_len]
                  
              st.session_state['data_entries']["ML Prediction"] = prediction
 
              col00, colaa, colbb = st.columns(3)
              colxx, colcc, coldd = st.columns(3)
             
              col00 = col00.write("__")
              colxx = colxx.write("Total Hours")
 
              colaa.subheader("Rules-based Model Output")
              chrs = sum(st.session_state['data_entries']['after_add_overlay']).__round__(0)
              colcc = colcc.write(chrs)
              
              mlhrs = (st.session_state['data_entries']["ML Prediction"].sum()).__round__(0)
              
              colbb.subheader("ML Model Output \n (In Development)")
              coldd = coldd.write(mlhrs)
              olay = st.session_state['data_entries']['after_add_overlay'].sum()
              low = st.session_state['data_entries']['adj_time_CSACP_low'].sum()+st.session_state['data_entries']['adj_time_BP_low'].sum()+st.session_state['data_entries']['adj_time_TAP_low'].sum()+st.session_state['data_entries']['adj_time_CCA_low'].sum()
              lowpct = low/(st.session_state['data_entries']['Adj_Activity_Hours'].sum())
              hmpct = (1- lowpct)
              
              fte_count_xl_ss = mt.ceil((st.session_state['data_entries']['after_add_overlay'].sum()/150)*2)/2
              fte_count_xl_os = mt.ceil(((1.3)*st.session_state['data_entries']['after_add_overlay'].sum()/150)*2)/2
              fte_count_xl_m = mt.ceil(fte_count_xl_ss*lowpct*2)/2 + mt.ceil(fte_count_xl_os*hmpct*2)/2
              
              fte_count_ml_ss = mt.ceil((st.session_state['data_entries']["ML Prediction"].sum()/150)*2)/2
              fte_count_ml_os = mt.ceil(((1.3)*st.session_state['data_entries']["ML Prediction"].sum()/150)*2)/2
              fte_count_ml_m = mt.ceil(fte_count_ml_ss*lowpct*2)/2 + mt.ceil(fte_count_ml_os*hmpct*2)/2

              if selected_delivery_model == "Shared Services":
                   SFAE = mt.ceil(fte_count_xl_ss*hmpct*2)/2
                   SFAML = mt.ceil(fte_count_ml_ss*hmpct*2)/2
                   tle = mt.floor(fte_count_xl_ss/6)
                   tlml = mt.floor(fte_count_ml_ss/6)
                   FAE = fte_count_xl_ss - SFAE - tle
                   FAML = fte_count_ml_ss - SFAML - tlml
                   tftec = fte_count_xl_ss
                   tfteml = fte_count_ml_ss
              elif selected_delivery_model == "On-site":
                   SFAE = mt.ceil(fte_count_xl_os*hmpct*2)/2
                   SFAML = mt.ceil(fte_count_ml_os*hmpct*2)/2
                   tle = mt.floor(fte_count_xl_os/6)
                   tlml = mt.floor(fte_count_ml_os/6)
                   FAE = fte_count_xl_os - SFAE - tle
                   FAML = fte_count_ml_os - SFAML - tlml
                   tftec = fte_count_xl_os
                   tfteml = fte_count_ml_os
              elif selected_delivery_model == "Mixed":
                   SFAE = mt.ceil(fte_count_xl_os*hmpct*2)/2
                   SFAML = mt.ceil(fte_count_ml_os*hmpct*2)/2
                   tle = mt.floor(fte_count_xl_m/6)
                   tlml = mt.floor(fte_count_ml_m/6)
                   FAE = fte_count_xl_m - SFAE - tle
                   FAML = fte_count_ml_m - SFAML - tlml
                   tftec = fte_count_xl_m
                   tfteml = fte_count_ml_m
              
              colee, colff, colgg = st.columns(3)
              colee = colee.write("Recommended FTE Count")
              colff = colff.write(tftec)
              colgg = colgg.write(tfteml)

              st.subheader("Recommended Roles")
              colhh, colii, coljj = st.columns(3)
              colhh = colhh.write("Financial Analysts")
              colii = colii.write(FAE)
              coljj = coljj.write(FAML)
              
              colkk, colll, colmm = st.columns(3)
              colkk = colkk.write("Sr. Financial Analysts")
              colll = colll.write(SFAE)
              colmm = colmm.write(SFAML)

              colnn, coloo, colpp = st.columns(3)
              colnn = colnn.write("Finance Manager/Team Lead")
              coloo = coloo.write(tle)
              colpp = colpp.write(tlml)

              st.write("")
              st.write("")
              st.write("")
              st.write("")              
              
              dfdb = st.session_state['data_entries'].iloc[:,:71]
              dfdb.drop(dfdb.columns[[64,65,67,69]],axis=1,inplace = True)
              dfdb['Final_Est._Hours'] = st.session_state['data_entries'].iloc[:,85]
              dfdb['Total_Est._FTE'] = tftec
              dfdb['FA'] = FAE
              dfdb['SFA'] = SFAE
              dfdb['FM'] = tle
              dfdb['Final_Est._Hours_ML'] = st.session_state['data_entries'].iloc[:,101]
              dfdb['Total_Est._FTE_ML'] = tfteml
              dfdb['FA_ML'] = FAML
              dfdb['SFA_ML'] = SFAML
              dfdb['FM_ML'] = tlml
              dbdf = dfdb.rename(columns = {'Average Spend per Site':'Avg_Spend_Site',
                                            'Client Name': 'Client_Name',
                                            'Average Site Multiplier value':'Classification',
                                            'Adjusted No of Sites':'Adj_Nof_Sites',
                                            'Total Managed Spend': 'Total_Managed_Spend',
                                            'Number of Sites':'Number_of_Sites','Contract_Structure':'Contract_Structure',
                                            'Contract Structure Multiplier':'Contract_Structure_Multiplier',
                                            'Spend Ratio Option':'fixed_Var_Spend_Ratio',
                                            'Spend Ratio Multiplier':'fixed_Var_spend_ratio_multiplier',
                                            'Principal/MA Option':'principal_ma',
                                            'Principal/MA Multiplier':'principal_ma_multiplier',
                                            'Client Reporting Level Option':'Client_Reporting_Level',
                                            'Client Reporting Level Multiplier':'Client_Reporting_Level_Multiplier',
                                            'Tech Stack Option':'Tech_Stack','Tech Stack Multiplier':'Tech_Stack_Multiplier',
                                            'Automation Adjustment Option':'Automation_Adjustments',
                                            'Automation Adjustment Multiplier':'Automation_Adjustments_Multiplier',
                                            'Bank Account Option':'Bank_Account','Bank Account Multiplier':'Bank_Account_Multiplier',
                                            'Delivery_Model':'Delivery_Model','1.Billing_freq':'Billing_Frequency',
                                            '1.Billing':'Billing_Value','2.Fund Reconciliations_freq':'Fund_Reconciliations_Frequency',
                                            '2.Fund Reconciliations':'Fund_Reconciliations_Value','3.Payment_freq':'Payment_Frequency',
                                            '3.Payment':'Payment_Value',
                                            '4.Monthly JDE period close and Open PO review_freq':'Period_close_and_Open_PO_review_Frequency',
                                            '4.Monthly JDE period close and Open PO review':'Period_close_and_Open_PO_review_Value',
                                            '5.Monhtly JDE Balance Sheet Reconciliation_freq':'Balance_Sheet_Reconciliation_Frequency',
                                            '5.Monhtly JDE Balance Sheet Reconciliation':'Balance_Sheet_Reconciliation_Value',
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
              
              dft = dbdf.reindex(columns = ['Client_Name','Country','Region','Total_Managed_Spend',
                                    'Number_of_Sites','Contract_Structure','Contract_Structure_Multiplier',
                                    'fixed_var_spend_ratio','fixed_var_spend_ratio_multiplier','principal_ma',
                                    'principal_ma_multiplier','Client_Reporting_Level','Client_Reporting_Level_Multiplier',
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
                                    'SFA_ML','FM_ML'
])
              #st.write(dft)
              #st.write(st.session_state['data_entries'])
              st.subheader("AMS Summary")
              
              st.write("")
              st.write("")
              st.write("")
              st.write("")

              conn, cur = dbconn.connection()
              insert_query = f"INSERT INTO ftecalc_data.fin_data (finance_data_skey,{', '.join(dft.columns)}) VALUES (nextval('finance_data_seq'),{', '.join(['%s'] * len(dft.columns))})"
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

              if success:
                st.write("Data uploaded to the database successfully.")
              else:
                st.write("Data upload failed.")



              dfam = pd.DataFrame({"Rule Based":[chrs,tftec,"------------------------",FAE,SFAE,tle], "ML Predicted":[mlhrs,tfteml,"------------------------",FAML,SFAML,tlml]},index=["Total Hours", "Total FTE Count","Recommended Role", "Financial Analyst","Sr. Financial Analyst", "Manager/Team-Lead"])
              st.write(dfam)

              st.subheader("AMS Activities Summary")
              actable = pd.DataFrame({"Activities": ['Billing','Fund Reconciliations','Payment','Monthly JDE period close and Open PO review',
                                                     'Monhtly JDE Balance Sheet Reconciliation','Corporate Month End Revenue/Costs Adjustments',
                                                     'Corporate Pass Through Reconciliation','Corporate Payment Entries Submission','Internal & External Audit Sampling Requests (SOC1 & SOX)',
                                                     'Corporate P&L Month End Review, Analysis & Queries','Corporate Yearly Budget - Preparation, Review & Approval','Corporate Monthly Forecast - Preparation, Review & Approval',
                                                     'Corporate Operation Merit & Bonus Review','Client Month End Accruals - Open PO, Rental, Utilities etc. - Manual Journal Entries Posting','Monthly Operational Call for Client Month End Close (Queries from FM - Finance Related)',
                                                     'Client Budget - Management Fee & Payroll Calculation; Vendor Spend Data','Client Forecast - Vendor Spend','Client Savings Report','Client Finance Audit Support',
                                                     'Client Billing to Actuals Reconciliation','Standard Report','Customised Report'],
                                    "Hours":[st.session_state['data_entries'][All_activities[0]].sum().round(1),st.session_state['data_entries'][All_activities[1]].sum().round(1),st.session_state['data_entries'][All_activities[2]].sum().round(1),st.session_state['data_entries'][All_activities[3]].sum().round(1),st.session_state['data_entries'][All_activities[4]].sum().round(1),
                                               st.session_state['data_entries'][All_activities[5]].sum().round(1),st.session_state['data_entries'][All_activities[6]].sum().round(1),st.session_state['data_entries'][All_activities[7]].sum().round(1),st.session_state['data_entries'][All_activities[8]].sum().round(1),st.session_state['data_entries'][All_activities[9]].sum().round(1),
                                               st.session_state['data_entries'][All_activities[10]].sum().round(1),st.session_state['data_entries'][All_activities[11]].sum().round(1),st.session_state['data_entries'][All_activities[12]].sum().round(1),st.session_state['data_entries'][All_activities[13]].sum().round(1),st.session_state['data_entries'][All_activities[14]].sum().round(1),
                                               st.session_state['data_entries'][All_activities[15]].sum().round(1),st.session_state['data_entries'][All_activities[16]].sum().round(1),st.session_state['data_entries'][All_activities[17]].sum().round(1),st.session_state['data_entries'][All_activities[18]].sum().round(1),st.session_state['data_entries'][All_activities[19]].sum().round(1),
                                               st.session_state['data_entries'][All_activities[20]].sum().round(1),st.session_state['data_entries'][All_activities[21]].sum().round(1)]},index = (1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22))
              
              st.write(actable)
 
              if not st.session_state['data_entries'].empty:
                  st.write("Data Loaded Successfully")
              else:
                  st.write("No data collected yet.")              

                  
if __name__ == "__main__":
    run_2()