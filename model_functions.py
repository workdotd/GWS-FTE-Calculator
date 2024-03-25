# Contract variable Assumptions:
contact_structure_mul = {"GMP":0.90, "Cost Plus":1.00, "Fixed Price":0.90, "Other":1.20}
spend_ratio_mul = {f"25% fixed; 75% variable":1.20, f"50% fixed; 50% variable":1.00, f"75% fixed; 25% variable":0.90}
principal_mul = {"Full Principal (immaterial agency spend)":1.00, "Full Managing Agent (immaterial principal spend)":0.10, 
                 "50% Principal; 50% MA":0.60, "25% Principal; 75% MA":0.40 ,"75% Principal; 25% MA":0.90}
client_reporting_level_mul = {"Country-level":0.90, "Site-level":1.00, "Cost-center level":1.20}
tech_stack_mul = {"Standard - Mybuy/JDE/PS":1.00, "Full Iscala":0.90, "Full PS":1.10, "Non-standard":1.20}
automation_adjustment_mul = {"High":0.75, "Mid":0.85, "Low":0.90, "None":1.00}
bank_account_use_mul = {"Dedicated":1.00,"Shared/Ded":1.10,"Corporate":1.20}


# Functions:

# calssification (Average Site Size Multiplier): 
def avg_site_size_multiplier(region, avg_spend_per_site):
    if region == "APAC":
        if avg_spend_per_site < 40000:
            result = 0.6
        elif avg_spend_per_site < 80000:
            result = 0.8
        elif avg_spend_per_site < 300000:
            result = 1
        elif avg_spend_per_site < 750000:
            result = 1
        elif avg_spend_per_site >= 750000:
            result = 1.1
    else:
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


# Contract variable Multiplier Function:
def contract_varibale_mul(contract_variable, key):
    if contract_variable == "Contract Structure":
        return contact_structure_mul[key]
    elif contract_variable == "Spend Ratio":
        return spend_ratio_mul[key]
    elif contract_variable == "Principal/MA":
        return principal_mul[key]
    elif contract_variable == "Client Reporting Level":
        return client_reporting_level_mul[key]
    elif contract_variable == "Technology Stack":
        return tech_stack_mul[key]
    elif contract_variable == "Automation Adjustment":
        return automation_adjustment_mul[key]
    elif contract_variable == "Bank Account Use":
        return bank_account_use_mul[key]

# Delivery Model 
def delivery_model(dm, ah, p):
    if dm == "Shared Services":
        result = ah * 1
    elif dm == "On-site":
        result = ah * 1.3
    elif dm == "Mixed":
        result = ah * p + (1 - p) * ah * 1.3
    return result

# Low Complexities:
