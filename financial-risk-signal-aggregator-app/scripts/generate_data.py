
"""
generate_data.py
Synthetic data generator for Financial Risk Signal Aggregator.

Generates:
- customers.csv
- transactions.csv
- alerts.json
- news.txt

Usage:
    python generate_data.py
    python generate_data.py --customers 100 --transactions 1000
"""
import argparse
import json
import logging
import random
from datetime import datetime, timedelta
from pathlib import Path
from uuid import uuid4

import numpy as np
import pandas as pd
from faker import Faker

fake = Faker()
random.seed(42)
np.random.seed(42)
Faker.seed(42)

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

BASE_DIR = Path(__file__).resolve().parent.parent
OUTPUT_DIR = BASE_DIR / "data" / "sample"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

COUNTRIES = [
    "United States","Canada","United Kingdom","Germany",
    "Singapore","India","Nigeria","Russia","United Arab Emirates"
]
HIGH_RISK_COUNTRIES = ["Nigeria","Russia"]

MERCHANT_CATEGORY = {
    "Amazon":"Retail",
    "Walmart":"Retail",
    "Apple":"Electronics",
    "Shell":"Fuel",
    "Starbucks":"Food",
    "Alpha Crypto Exchange":"Crypto",
    "Lucky Spin Casino":"Casino",
    "Global Electronics":"Electronics",
    "Travel Hub":"Travel",
    "Quick Transfer":"Money Transfer"
}
MERCHANTS=list(MERCHANT_CATEGORY.keys())
PAYMENT_METHODS=["Card","Bank Transfer","Wallet"]
DEVICE_PREFIX=["IPH","AND","WEB"]
OCCUPATIONS=[
    "Engineer","Doctor","Teacher","Consultant","Business Owner",
    "Student","Government Officer","Lawyer","Accountant","Software Developer"
]
SPECIAL={
    "SANCTIONED":"C005",
    "CRYPTO":"C018",
    "CARD_FRAUD":"C031",
    "STRUCTURING":"C052",
    "DORMANT":"C070"
}

def random_timestamp(days=180):
    start=datetime.now()-timedelta(days=days)
    return start+timedelta(seconds=random.randint(0,days*24*3600))

def random_device():
    return f"{random.choice(DEVICE_PREFIX)}-{random.randint(10000,99999)}"

def generate_customers(n=100):
    rows=[]
    for i in range(1,n+1):
        rows.append({
            "CustomerID":f"C{i:03}",
            "Name":fake.name(),
            "Age":random.randint(21,75),
            "Occupation":random.choice(OCCUPATIONS),
            "AnnualIncome":random.randint(30000,200000),
            "RiskCategory":random.choices(["Low","Medium","High"],weights=[70,25,5])[0],
            "KYCStatus":random.choices(["Verified","Pending"],weights=[90,10])[0],
            "PEP":random.choices(["Yes","No"],weights=[5,95])[0],
            "AccountAgeMonths":random.randint(1,120),
            "Country":random.choice(COUNTRIES)
        })
    df=pd.DataFrame(rows)
    if SPECIAL["SANCTIONED"] in df.CustomerID.values:
        df.loc[df.CustomerID==SPECIAL["SANCTIONED"],["PEP","RiskCategory"]]=["Yes","High"]
    if SPECIAL["CRYPTO"] in df.CustomerID.values:
        df.loc[df.CustomerID==SPECIAL["CRYPTO"],"RiskCategory"]="Medium"
    if SPECIAL["DORMANT"] in df.CustomerID.values:
        df.loc[df.CustomerID==SPECIAL["DORMANT"],"AccountAgeMonths"]=84
    return df

def generate_normal_transactions(customers,n):
    tx=[]
    ids=customers.CustomerID.tolist()
    for _ in range(n):
        m=random.choice(MERCHANTS)
        tx.append({
            "TransactionID":str(uuid4()),
            "CustomerID":random.choice(ids),
            "Timestamp":random_timestamp().isoformat(),
            "Amount":round(np.random.lognormal(4.3,0.9),2),
            "Currency":"USD",
            "Merchant":m,
            "MerchantCategory":MERCHANT_CATEGORY[m],
            "Country":random.choice(COUNTRIES),
            "DeviceID":random_device(),
            "PaymentMethod":random.choice(PAYMENT_METHODS),
            "Status":random.choices(["Success","Failed"],weights=[95,5])[0]
        })
    return tx

def inject_crypto(tx):
    base=datetime.now()-timedelta(days=5)
    for i in range(15):
        tx.append({
            "TransactionID":str(uuid4()),"CustomerID":SPECIAL["CRYPTO"],
            "Timestamp":(base+timedelta(minutes=i*3)).isoformat(),
            "Amount":random.randint(12000,25000),"Currency":"USD",
            "Merchant":"Alpha Crypto Exchange","MerchantCategory":"Crypto",
            "Country":"Nigeria","DeviceID":random_device(),
            "PaymentMethod":"Bank Transfer","Status":"Success"
        })

def inject_structuring(tx):
    base=datetime.now()-timedelta(days=2)
    for i in range(20):
        tx.append({
            "TransactionID":str(uuid4()),"CustomerID":SPECIAL["STRUCTURING"],
            "Timestamp":(base+timedelta(minutes=i)).isoformat(),
            "Amount":random.randint(9600,9900),"Currency":"USD",
            "Merchant":"Quick Transfer","MerchantCategory":"Money Transfer",
            "Country":"United States","DeviceID":random_device(),
            "PaymentMethod":"Bank Transfer","Status":"Success"
        })

def inject_card_fraud(tx):
    base=datetime.now()-timedelta(days=1)
    for i in range(12):
        tx.append({
            "TransactionID":str(uuid4()),"CustomerID":SPECIAL["CARD_FRAUD"],
            "Timestamp":(base+timedelta(minutes=i)).isoformat(),
            "Amount":random.randint(50,400),"Currency":"USD",
            "Merchant":"Amazon","MerchantCategory":"Retail",
            "Country":"Canada","DeviceID":random_device(),
            "PaymentMethod":"Card","Status":"Failed"
        })
    tx.append({
        "TransactionID":str(uuid4()),"CustomerID":SPECIAL["CARD_FRAUD"],
        "Timestamp":(base+timedelta(minutes=20)).isoformat(),
        "Amount":3500,"Currency":"USD",
        "Merchant":"Apple","MerchantCategory":"Electronics",
        "Country":"Canada","DeviceID":random_device(),
        "PaymentMethod":"Card","Status":"Success"
    })

def inject_sanctioned(tx):
    base=datetime.now()-timedelta(days=4)
    for i in range(10):
        tx.append({
            "TransactionID":str(uuid4()),"CustomerID":SPECIAL["SANCTIONED"],
            "Timestamp":(base+timedelta(hours=i)).isoformat(),
            "Amount":random.randint(15000,40000),"Currency":"USD",
            "Merchant":"Alpha Crypto Exchange","MerchantCategory":"Crypto",
            "Country":"Nigeria","DeviceID":random_device(),
            "PaymentMethod":"Bank Transfer","Status":"Success"
        })

def inject_dormant(tx):
    tx.append({
        "TransactionID":str(uuid4()),"CustomerID":SPECIAL["DORMANT"],
        "Timestamp":datetime.now().isoformat(),
        "Amount":90000,"Currency":"USD",
        "Merchant":"Quick Transfer","MerchantCategory":"Money Transfer",
        "Country":"Russia","DeviceID":random_device(),
        "PaymentMethod":"Bank Transfer","Status":"Success"
    })

def generate_transactions(customers,n=1000):
    tx=generate_normal_transactions(customers,n)
    inject_crypto(tx)
    inject_structuring(tx)
    inject_card_fraud(tx)
    inject_sanctioned(tx)
    inject_dormant(tx)
    return pd.DataFrame(tx)

def generate_alerts(customers):
    alerts=[]
    aid=1
    for _ in range(35):
        alerts.append({
            "AlertID":f"A{aid:03}",
            "CustomerID":random.choice(customers.CustomerID.tolist()),
            "AlertType":random.choice([
                "Suspicious Transfers","Device Change","Chargeback Spike",
                "AML Investigation","High Cash Activity"
            ]),
            "Severity":random.choice(["Low","Medium","High"]),
            "Source":random.choice(["Internal AML Engine","Fraud Detection System","Compliance Team"]),
            "Description":"Automatically generated alert.",
            "Timestamp":random_timestamp(90).isoformat()
        })
        aid+=1
    special=[
        (SPECIAL["SANCTIONED"],"Sanction Match","Critical","OFAC","Customer matched sanctions list."),
        (SPECIAL["SANCTIONED"],"PEP Match","High","Compliance Team","Politically exposed person."),
        (SPECIAL["CRYPTO"],"Suspicious Transfers","High","Internal AML Engine","Large transfers to high-risk jurisdiction."),
        (SPECIAL["CARD_FRAUD"],"Multiple Failed Transactions","High","Fraud Detection System","Repeated failed card attempts."),
        (SPECIAL["STRUCTURING"],"High Cash Activity","High","Internal AML Engine","Transactions just below reporting threshold."),
        (SPECIAL["DORMANT"],"Dormant Account Reactivated","High","Compliance Team","Inactive account became active.")
    ]
    for c,a,s,src,d in special:
        alerts.append({
            "AlertID":f"A{aid:03}","CustomerID":c,"AlertType":a,
            "Severity":s,"Source":src,"Description":d,
            "Timestamp":random_timestamp(30).isoformat()
        }); aid+=1
    return alerts

def generate_news():
    articles=[
        "Authorities have launched an investigation into Alpha Crypto Exchange over suspicious cross-border transfers.",
        "Lucky Spin Casino has been linked to anti-money laundering investigations.",
        "Financial institutions have increased monitoring of transfers involving Nigeria.",
        "Banks have strengthened monitoring of Russia-related transactions.",
        "Fraud analysts report increasing device-switching attacks before successful purchases.",
        "Compliance teams are observing more structuring activity below reporting thresholds."
    ]
    while len(articles)<25:
        articles.append(fake.paragraph(nb_sentences=4))
    text=""
    for i,a in enumerate(articles,1):
        text+=f"=== ARTICLE {i} ===\n{a}\n\n"
    return text

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--customers",type=int,default=100)
    parser.add_argument("--transactions",type=int,default=1000)
    args=parser.parse_args()

    customers=generate_customers(args.customers)
    transactions=generate_transactions(customers,args.transactions)
    alerts=generate_alerts(customers)
    news=generate_news()

    customers.to_csv(OUTPUT_DIR/"customers.csv",index=False)
    transactions.to_csv(OUTPUT_DIR/"transactions.csv",index=False)
    with open(OUTPUT_DIR/"alerts.json","w") as f:
        json.dump(alerts,f,indent=2)
    with open(OUTPUT_DIR/"news.txt","w") as f:
        f.write(news)

    logging.info("Customers: %d",len(customers))
    logging.info("Transactions: %d",len(transactions))
    logging.info("Alerts: %d",len(alerts))
    logging.info("News Articles: %d",len(news.split("=== ARTICLE"))-1)
    logging.info("Saved to %s",OUTPUT_DIR)

if __name__=="__main__":
    main()
