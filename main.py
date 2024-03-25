# Imports
from model_functions import avg_site_size_multiplier, count_activities_subscribed, total_activity_hrs, contract_varibale_mul
import pandas as pd
from IPython.display import display

# Inputs [6]:
"""
1. Financial Activities:-> Avg Time Spent per Activity per country. [1]
2. Volumetric Criteria:
    i. Frequency of activity [2]
   ii. Country [3]
  iii. Sites [4]
   iv. Total Managed Spend [5]
3. Contract Variables: [6]
    i. Contract Structure
    ii. Spend ratio
    iii. Automation Adjustment
    iv. Client Reporting Level
    v. Principal/MA
    vi. Technology Stack
    vii. Bank Account Use
"""
client = "Dragon"
region = "AMS"

country = "Argentina"
no_sites_per_country = 142
contract_structure = "Cost Plus"
spend_ratio = f"75% fixed; 25% variable"
principal_ma = "Full Principal (immaterial agency spend)"
client_reporting_level = "Country-level"
tech_stack = "Standard - Mybuy/JDE/PS"
automation_adjustment = "High"
bank_account= "Dedicated"
total_managed_spend = 47901198   # across countries
deliver_model = "On-site"


# Calculations:

# Total Number of Sites:
total_no_sites = 1176   # perform cal from data sheet

avg_spend_per_site = total_managed_spend / total_no_sites
print("Avg Spend/Site:->",round(avg_spend_per_site))

spend_per_country = avg_spend_per_site * no_sites_per_country
print("Spend/Country:->",round(spend_per_country))

avg_site_size_multiplier_value = avg_site_size_multiplier(region,avg_spend_per_site)
print("Average Site Size Multiplier:->",avg_site_size_multiplier_value)

adj_no_sites = no_sites_per_country * avg_site_size_multiplier_value
print("Adjusted No of Sites:->",adj_no_sites)

Finance_Activity_items = [
    "Billing_monthly",
    "Fund_Reconciliations_monthly",
    "Payment_monthly",
    "Monthly_JDE_period_close_and_Open_PO_review_monthly",
    "Monthly_JDE_Balance_Sheet_Reconciliation_monthly",
    "Corporate_Month_End_Revenue/Costs_Adjustments_monthly",
    "Corporate_Pass_Through_Reconciliation_monthly",
    "Corporate_Payment_Entries_Submission_monthly",
    "Internal_&External_Audit_Sampling_Requests(SOC1_&_SOX)monthly",
    "Client_Month_End_Accruals-_Open_PO,Rental,Utilities_etc.-Manual_Journal_Entries_Posting_monthly",
    "Client_Reporting_Pack-Standard_Report_Generation&Distribution_monthly",
    "Monthly_Operational_Call_for_Client_Month_End_Close(Queries_from_FM-_Finance_Related)monthly",
    "Client_Specific_reporting(Customised)_monthly",
    "Corporate_P&L_Month_End_Review,Analysis&Queries_monthly",
    "Corporate_Yearly_Budget-_Preparation,Review&Approval_monthly",
    "Corporate_Monthly_Forecast-_Preparation,Review&Approval_monthly",
    "Corporate_Operation_Merit&Bonus_Review_monthly",
    "Client_Budget-Management_Fee&_Payroll_Calculation;Vendor_Spend_Data_monthly",
    "Client_Forecast-_Vendor_Spend_monthly",
    "Client_Savings_Report_monthly",
    "Client_Finance_Audit_Supporting_monthly",
    "Client_Billing_to_Actuals_Reconciliation_monthly"
]

fa_values = [94.95, 0.0, 0.0, 0.5, 1.0, 1.57, 1.43, 0.0, 0.0, 0.5, 0.0, 2.29, 4.72, 4.0, 0.78, 2.0, 0.25, 0.42, 3.0, 1.78, 0.17, 0.0]

Activities = dict(zip(Finance_Activity_items,fa_values))
# print(Activities)

df_activities = pd.DataFrame([],columns=Finance_Activity_items)
df_activities.loc[len(df_activities.index)] = fa_values
# display(df_activities)

activities_subscribed = count_activities_subscribed(Activities)
print("Activities Subscribed",activities_subscribed)

total_activity_hours = total_activity_hrs(Activities)
print("Total Activity Hours",total_activity_hours)

# Contract variable Multiplier:
contract_structure_mul = contract_varibale_mul("Contract Structure",contract_structure)
spend_ratio_mul = contract_varibale_mul("Spend Ratio",spend_ratio)
principal_mul = contract_varibale_mul("Principal/MA",principal_ma)
client_reporting_level_mul = contract_varibale_mul("Client Reporting Level",client_reporting_level)
tech_stack_mul = contract_varibale_mul("Technology Stack",tech_stack)
automation_adjustment_mul = contract_varibale_mul("Automation Adjustment",automation_adjustment)
bank_account_mul = contract_varibale_mul("Bank Account Use",bank_account)

# print(contract_structure_mul)
# print(spend_ratio_mul)
# print(principal_mul)
# print(client_reporting_level_mul)
# print(tech_stack_mul)
# print(automation_adjustment_mul)
# print(bank_account_mul)

# Multipliers Combo:
Contrct_Spend_Auto_CRL_PMA = contract_structure_mul * spend_ratio_mul * principal_mul * client_reporting_level_mul * automation_adjustment_mul
Bank_PMA = bank_account_mul * principal_mul
tech_auto_pma = principal_mul * tech_stack_mul * automation_adjustment_mul
Contrct_crl = contract_structure_mul * client_reporting_level_mul
Contrct_crl_auto = contract_structure_mul * client_reporting_level_mul * automation_adjustment_mul
tech_auto = tech_stack_mul * automation_adjustment_mul


adj_time_CSACP = Activities['Billing_monthly'] * Contrct_Spend_Auto_CRL_PMA
# print(adj_time_CSACP)

adj_time_BP = (Activities['Fund_Reconciliations_monthly'] + Activities['Payment_monthly']) * Bank_PMA
# print(adj_time_BP)

adj_time_TAP = (Activities['Monthly_JDE_period_close_and_Open_PO_review_monthly'] + Activities['Monthly_JDE_Balance_Sheet_Reconciliation_monthly'] + Activities['Corporate_Month_End_Revenue/Costs_Adjustments_monthly'] +Activities['Corporate_Pass_Through_Reconciliation_monthly'] + Activities['Corporate_Payment_Entries_Submission_monthly'] +Activities['Internal_&External_Audit_Sampling_Requests(SOC1_&_SOX)monthly'] +Activities['Corporate_P&L_Month_End_Review,Analysis&Queries_monthly'] +Activities['Corporate_Yearly_Budget-_Preparation,Review&Approval_monthly']+Activities['Corporate_Monthly_Forecast-_Preparation,Review&Approval_monthly']) * tech_auto_pma
# print(adj_time_TAP)

adj_time_CC = Activities['Client_Month_End_Accruals-_Open_PO,Rental,Utilities_etc.-Manual_Journal_Entries_Posting_monthly'] * Contrct_crl
# print(adj_time_CC)

adj_time_CCA = (Activities['Client_Reporting_Pack-Standard_Report_Generation&Distribution_monthly']+Activities['Client_Specific_reporting(Customised)_monthly']+Activities['Client_Budget-Management_Fee&_Payroll_Calculation;Vendor_Spend_Data_monthly']+Activities['Client_Forecast-_Vendor_Spend_monthly']+Activities['Client_Savings_Report_monthly']+Activities['Client_Finance_Audit_Supporting_monthly']+Activities['Client_Billing_to_Actuals_Reconciliation_monthly']) * Contrct_crl_auto
# print(adj_time_CCA)

adj_time_None = Activities['Monthly_Operational_Call_for_Client_Month_End_Close(Queries_from_FM-_Finance_Related)monthly']
# print(adj_time_None)

adj_time_TA = Activities['Corporate_Operation_Merit&Bonus_Review_monthly'] * tech_auto
# print(adj_time_TA)

# Adjusted Total Activity hours (After Multipliers)
Adj_Activity_Hours = adj_time_CSACP + adj_time_BP + adj_time_TAP + adj_time_CC + adj_time_CCA + adj_time_None + adj_time_TA
print("Adjusted Total Activity hours (After Multipliers):->",Adj_Activity_Hours)

# Add +20% Ad hoc Overlay:
after_add_overlay = Adj_Activity_Hours * 1.2
print("After 20% Overlay:->",after_add_overlay)

# After DM Adjustment
