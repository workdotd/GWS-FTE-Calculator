FTE calculator is a resource recommender system that uses various contract variables, and activity estimated country hours as input and calculates the total number of monthly hours that would be spent for the activities under contract. It also considers if the activities would be performed at the client site or not, or if partially at the client site.

The estimated hours are the used to calculate the number of resources to be employed for the contract. The seniority level of the resources is decided based on the complexity of the activities under the contract. Using the calculated number of the resources, we also can calculate the number of managers/team leads required.

We get 2 outputs (number of hours)

Calculations Based Output

Machine Learning Model based output.

 

Calculation Based Output: For calculation-based output we use multipliers assigned to each contract variable and the delivery model.

Machine learning Based Output: Here we calculate the total activity hours and based on activity hours and other features we use ML model to estimate the final hours.

 

Calculation Based Output:

 

Calculations:

Average spend Per site = Total Managed Spend/Total Number of Sites

Based on Avg site size classification, site size multiplier is multiplied with nof sites for each country and finally we get adjusted number of sites.

All the selected activities with any frequency are first converted to monthly frequency, country wrt each activity is multiplied with a frequency multiplier as shown below:

a.      Weekly = 4

b.      Bi-Weekly = 2

c.       Monthly = 1

d.      Quarterly = 1/3

e.      Yearly = 1/12

The adjusted number of sites is multiplied with billing country hours

a.      If adjusted number of sites is <= 1 then the billing hours are multiplied by 2

b.      Else billing hours are simply multiplied by adjusted number of sites.

Rest of the activities are multiplied by selective multipliers successively as shown below

Activities

Contract Variables

Billing

Contract Structure

 Fixed/Var. Spend Ratio

 Automation Adjustments

 Client Reporting Level

 Principal/MA

 

Fund Reconciliations

Bank Account

 Principal/MA

 

 

 

 

Payment

Bank Account

 Principal/MA

 

 

 

 

Monthly JDE period close and Open PO review

Tech Stack

 Automation Adjustments

 Principal/MA

 

 

 

Monhtly JDE Balance Sheet Reconciliation

Tech Stack

 Automation Adjustments

 Principal/MA

 

 

 

Corporate Month End Revenue/Costs Adjustments

Tech Stack

 Automation Adjustments

 Principal/MA

 

 

 

Corporate Pass Through Reconciliation

Tech Stack

 Automation Adjustments

 Principal/MA

 

 

 

Corporate Payment Entries Submission

 

 

 

 

 

 

Internal & External Audit Sampling Requests (SOC1 & SOX)

Tech Stack

 Automation Adjustments

 Principal/MA

 

 

 

Client JDE Month End Accruals - Open PO, Rental, Utilities etc. - Manual Journal Entries Posting

Contract Structure

 Client Reporting Level

 

 

 

 

Client Reporting Pack - Standard Report Generation & Distribution

Contract Structure

 Automation Adjustments

 Client Reporting Level

 

 

 

Monthly Operational Call for Client Month End Close (Queries from FM - Finance Related)

 

 

 

 

 

 

Client Specific reporting (Customised)

Contract Structure

 Automation Adjustments

 Client Reporting Level

 

 

 

Corporate P&L Month End Review, Analysis & Queries

Tech Stack

 Automation Adjustments

 Principal/MA

 

 

 

Corporate Yearly Budget - Preparation, Review & Approval

Tech Stack

 Automation Adjustments

 Principal/MA

 

 

 

Corporate Monthly Forecast - Preparation, Review & Approval

Tech Stack

 Automation Adjustments

 Principal/MA

 

 

 

Corporate Operation Merit & Bonus Review

Tech Stack

Automation Adjustments

 

 

 

 

Client Budget - Management Fee & Payroll Calculation; Vendor Spend Data

Contract Structure

 Automation Adjustments

 Client Reporting Level

 

 

 

Client Forecast - Vendor Spend

Contract Structure

 Automation Adjustments

 Client Reporting Level

 

 

 

Client Savings Report

Contract Structure

 Automation Adjustments

 Client Reporting Level

 

 

 

Client Finance Audit Supporting

Contract Structure

 Automation Adjustments

 Client Reporting Level

 

 

 

Client Billing to Actuals Reconciliation

Contract Structure

 Automation Adjustments

 Client Reporting Level

 

 

 

 

After activities are multiplied with multipliers, all the activities are added together.

20% of the total of activities is added to the activity total.

Classify the activities as per complexity (As shown below)

Activity

Complexity

Billing_Monthly

Low

Fund Reconciliations_Monthly

Low

Payment_Monthly

Low

Monthly JDE period close and Open PO review_Monthly

Low

Monhtly JDE Balance Sheet Reconciliation_Monthly

Low

Corporate Month End Revenue/Costs Adjustments_Monthly

Low

Corporate Pass Through Reconciliation_Monthly

Low

Corporate Payment Entries Submission_Monthly

Low

Internal & External Audit Sampling Requests (SOC1 & SOX)_Monthly

Low

Client JDE Month End Accruals - Open PO, Rental, Utilities etc. - Manual Journal Entries Posting_Monthly

Mid

Client Reporting Pack - Standard Report Generation & Distribution_Monthly

Mid

Monthly Operational Call for Client Month End Close (Queries from FM - Finance Related)_Monthly

Mid

Client Specific reporting (Customised)_Monthly

High

Corporate P&L Month End Review, Analysis & Queries_Monthly

Low

Corporate Yearly Budget - Preparation, Review & Approval_Monthly

High

Corporate Monthly Forecast - Preparation, Review & Approval_Monthly

Low

Corporate Operation Merit & Bonus Review_Monthly

High

Client Budget - Management Fee & Payroll Calculation; Vendor Spend Data_Monthly

Mid

Client Forecast - Vendor Spend_Monthly

Low

Client Savings Report_Monthly

Mid

Client Finance Audit Supporting_Monthly

Low

Client Billing to Actuals Reconciliation_Monthly

High

Check the delivery model;

a.      Shared Service: The total activity hours after overlay are final estimated hours.

b.      Mixed: The total of mid and high complexity hours after overlay is added with a 30% in-efficiency factor. The final estimated          hours = Low complexity Hours + (Mid + High Complexity Hours)*1.3

c.       On-Site: The total activity hours after overlay are multiplied with 30% in-efficiency factor. The final estimated hours = (Total activity Hours after overlay)*1.3

d.      After adding the in-efficiency factor as per delivery model, we get Total hours (After DM Adjustment)

9.  Total required FTE = Total hours(After DM Adjustment)/150

10.  Recommended Roles:

a.      Financia Analyst = Total low complexity hours (After DM Adjustment)/150

b.      Sr. Financial Analyst = Total mid+high complexity hours (After DM Adjustment)/150

c.       Manager/Team Leads = (Financial Analyst + Sr. Financial Analyst)/5

