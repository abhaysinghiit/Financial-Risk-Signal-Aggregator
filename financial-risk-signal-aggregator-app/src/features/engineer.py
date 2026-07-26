
import pandas as pd

HIGH_RISK_COUNTRIES={"Nigeria","Russia"}

def engineer_customer_features(transactions_df, customers_df, alerts):
    tx=transactions_df.copy()
    tx["Timestamp"]=pd.to_datetime(tx["Timestamp"])
    tx["IsHighRiskCountry"]=tx["Country"].isin(HIGH_RISK_COUNTRIES)
    tx["IsCrypto"]=tx["MerchantCategory"].eq("Crypto")
    tx["IsCasino"]=tx["MerchantCategory"].eq("Casino")
    agg=tx.groupby("CustomerID").agg(
        total_transactions=("TransactionID","count"),
        total_amount=("Amount","sum"),
        avg_amount=("Amount","mean"),
        max_amount=("Amount","max"),
        failed_transactions=("Status",lambda s:(s=="Failed").sum()),
        unique_devices=("DeviceID","nunique"),
        unique_merchants=("Merchant","nunique"),
        crypto_transactions=("IsCrypto","sum"),
        casino_transactions=("IsCasino","sum"),
        high_risk_country_transactions=("IsHighRiskCountry","sum"),
        unique_countries=("Country","nunique")
    ).reset_index()
    feat=customers_df.merge(agg,on="CustomerID",how="left").fillna(0)
    adf=pd.DataFrame(alerts)
    if not adf.empty:
        cnt=adf.groupby("CustomerID").size().rename("alert_count")
        feat=feat.merge(cnt,left_on="CustomerID",right_index=True,how="left").fillna({"alert_count":0})
        for col,name in [("Sanction Match","sanction_alert"),
                         ("AML Investigation","aml_alert"),
                         ("Dormant Account Reactivated","dormant_alert")]:
            ids=adf.loc[adf.AlertType==col,"CustomerID"].unique()
            feat[name]=feat.CustomerID.isin(ids).astype(int)
    else:
        feat["alert_count"]=0
        feat["sanction_alert"]=0
        feat["aml_alert"]=0
        feat["dormant_alert"]=0
    return feat
