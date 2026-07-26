def evaluate_rules(row):
    score=0
    signals=[]
    def add(cond,pts,msg):
        nonlocal score
        if cond:
            score+=pts
            signals.append(msg)
    add(row.avg_amount>10000,20,"High average transaction value")
    add(row.high_risk_country_transactions>3,25,"Frequent high-risk country transfers")
    add(row.crypto_transactions>5,15,"Heavy crypto activity")
    add(row.failed_transactions>5,20,"Multiple failed transactions")
    add(row.unique_devices>4,15,"Multiple devices used")
    add(row.sanction_alert==1,50,"Sanctions match")
    add(str(row.PEP)=="Yes",20,"Politically Exposed Person")
    add(row.dormant_alert==1,30,"Dormant account reactivated")
    add(row.aml_alert==1,40,"AML investigation alert")
    add(getattr(row,"structuring_count",0)>=15,35,"Possible structuring pattern")
    return score,signals