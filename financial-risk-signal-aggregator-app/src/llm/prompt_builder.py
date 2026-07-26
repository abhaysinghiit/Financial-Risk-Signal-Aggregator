def build_prompt(customer,score,alerts,news):
    cust_alerts=[a for a in alerts if a['CustomerID']==customer['CustomerID']]
    alert_text='\n'.join(f"- {a['AlertType']}: {a['Description']}" for a in cust_alerts) or 'None'
    return f'''You are a Senior Financial Crime Investigator.

Customer: {customer['CustomerID']}
Country: {customer['Country']}
Risk Category: {customer['RiskCategory']}
PEP: {customer['PEP']}

Risk Score: {score['RiskScore']}
Risk Level: {score['RiskLevel']}

Signals:
{score['Signals']}

Alerts:
{alert_text}

Relevant News:
{"".join(news)}

Return sections:
Executive Summary
Risk Factors
Supporting Evidence
Potential Impact
Recommended Action
Confidence Level
'''
