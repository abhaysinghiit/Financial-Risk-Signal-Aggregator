
import pandas as pd
from .rules import evaluate_rules

def level(score):
    if score<=25:return "Low"
    if score<=50:return "Medium"
    if score<=75:return "High"
    return "Critical"

def score_customers(features_df):
    rows=[]
    for _,r in features_df.iterrows():
        s,signals=evaluate_rules(r)
        s=min(s,100)
        rows.append({
            "CustomerID":r.CustomerID,
            "RiskScore":s,
            "RiskLevel":level(s),
            "Signals":"; ".join(signals)
        })
    out=pd.DataFrame(rows).sort_values("RiskScore",ascending=False)
    return out