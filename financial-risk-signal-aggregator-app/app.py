import json
import pandas as pd
import plotly.express as px
import streamlit as st

from src.features.engineer import engineer_customer_features
from src.features.scorer import score_customers
from src.llm.summarizer import generate_customer_summary
from src.llm.executive_summary import generate_executive_summary

st.set_page_config(
    page_title="Financial Risk Signal Aggregator",
    page_icon="📊",
    layout="wide"
)

# ---------------------------------------------------------
# SESSION STATE
# ---------------------------------------------------------

if "ai_results" not in st.session_state:
    st.session_state.ai_results = None

if "executive_summary" not in st.session_state:
    st.session_state.executive_summary = None


st.title("📊 Financial Risk Signal Aggregator")
st.write("AI-powered financial risk analysis using structured and unstructured data.")

# ---------------- Sidebar ---------------- #
with st.sidebar:
    st.header("📂 Upload Files")

    transactions_file = st.file_uploader(
        "Transactions CSV",
        type=["csv"],
        key="transactions"
    )

    customers_file = st.file_uploader(
        "Customers CSV",
        type=["csv"],
        key="customers"
    )

    alerts_file = st.file_uploader(
        "Alerts JSON",
        type=["json"],
        key="alerts"
    )

    news_file = st.file_uploader(
        "News TXT",
        type=["txt"],
        key="news"
    )

# ---------------- Load Data ---------------- #
customers_df = None
transactions_df = None
alerts = None
news_text = None

if customers_file:
    customers_df = pd.read_csv(customers_file)

if transactions_file:
    transactions_df = pd.read_csv(transactions_file)

if alerts_file:
    alerts = json.load(alerts_file)

if news_file:
    news_text = news_file.read().decode("utf-8")

# ---------------- Pipeline Status ---------------- #
st.subheader("🚦 Pipeline Status")

status_items = [
    ("Customers", customers_df is not None),
    ("Transactions", transactions_df is not None),
    ("Alerts", alerts is not None),
    ("News", news_text is not None),
]

for name, loaded in status_items:
    icon = "✅" if loaded else "⌛"
    state = "Loaded" if loaded else "Waiting..."
    st.write(f"{icon} **{name}** — {state}")

# ---------------- Preview ---------------- #
if customers_df is not None:
    st.success(f"Loaded {len(customers_df)} customers")

if transactions_df is not None:
    st.success(f"Loaded {len(transactions_df)} transactions")

if alerts is not None:
    st.success(f"Loaded {len(alerts)} alerts")

if news_text is not None:
    articles = news_text.count("=== ARTICLE")
    st.success(f"Loaded news file ({articles if articles else 'multiple'} articles)")

if all(x is not None for x in [customers_df, transactions_df, alerts, news_text]):

    tab1, tab2, tab3, tab4 = st.tabs(
        ["Customers", "Transactions", "Alerts", "News"]
    )

    with tab1:
        st.dataframe(customers_df)

    with tab2:
        st.dataframe(transactions_df)

    with tab3:
        st.json(alerts[:5])

    with tab4:
        st.text(news_text[:1000])

    with st.spinner("Engineering customer features..."):
        features_df = engineer_customer_features(
            transactions_df,
            customers_df,
            alerts
        )

    st.success("✔ Features Engineered")

    with st.spinner("Generating risk scores..."):
        scores_df = score_customers(features_df)

    st.success("✔ Risk Scores Generated")

    st.subheader("🧠 Engineered Features")
    st.dataframe(features_df)

    st.subheader("⚠️ Risk Ranking")
    styled = scores_df.style.background_gradient(
        subset=["RiskScore"],
        cmap="Reds"
    )
    st.dataframe(styled, use_container_width=True)

    st.subheader("📈 Top 10 Highest Risk Customers")

    fig = px.bar(
        scores_df.head(10),
        x="CustomerID",
        y="RiskScore",
        color="RiskLevel",
        title="Top Risk Customers"
    )

    st.plotly_chart(fig, use_container_width=True)

    # ---------------------------------------------------------
    # DOWNLOAD REPORT
    # ---------------------------------------------------------

    csv = scores_df.to_csv(index=False)

    st.download_button(
        label="⬇ Download Risk Report",
        data=csv,
        file_name="risk_report.csv",
        mime="text/csv"
    )

    # ---------------------------------------------------------
    # AI RISK ASSESSMENT
    # ---------------------------------------------------------

    st.divider()

    st.header("🤖 AI Risk Assessment")

    st.write(
        "Generate AI-powered investigations for the Top 5 highest-risk customers."
    )

    top5 = scores_df.head(5)

    # ---------------------------------------------------------
    # GENERATE REPORT (ONLY ONCE)
    # ---------------------------------------------------------

    if st.session_state.ai_results is None:

        if st.button(
            "🚀 Generate AI Risk Report",
            type="primary",
            use_container_width=True,
        ):

            progress = st.progress(0)

            results = []

            total = len(top5)

            for i, (_, score) in enumerate(top5.iterrows()):

                customer = features_df[
                    features_df["CustomerID"] == score["CustomerID"]
                ].iloc[0]

                progress.progress(
                    (i) / (total + 1),
                    text=f"Analyzing {score['CustomerID']}..."
                )

                summary = generate_customer_summary(
                    customer,
                    score,
                    alerts,
                    news_text,
                )

                results.append(
                    {
                        "score": score,
                        "summary": summary,
                    }
                )

            progress.progress(
                total / (total + 1),
                text="Preparing Executive Summary..."
            )

            executive_summary = generate_executive_summary(
                results
            )

            progress.progress(
                1.0,
                text="Completed!"
            )

            progress.empty()

            st.session_state.ai_results = results
            st.session_state.executive_summary = executive_summary

            st.success("✅ AI Risk Report Generated Successfully!")

    # ---------------------------------------------------------
    # REPORT ALREADY EXISTS
    # ---------------------------------------------------------

    else:

        st.success("✅ AI Report already generated.")

        if st.button(
            "🔄 Regenerate AI Report",
            use_container_width=True,
        ):

            st.session_state.ai_results = None
            st.session_state.executive_summary = None

            st.rerun()

    # ---------------------------------------------------------
    # DISPLAY REPORT
    # ---------------------------------------------------------

    if st.session_state.ai_results is not None:

        st.divider()

        st.subheader("📋 Executive Risk Summary")

        st.markdown(
            st.session_state.executive_summary
        )

        st.divider()

        st.subheader("🧾 Individual Customer Assessments")

        for result in st.session_state.ai_results:

            score = result["score"]

            summary = result["summary"]

            with st.expander(
                f"📌 {score['CustomerID']} | "
                f"{score['RiskLevel']} Risk | "
                f"Score: {score['RiskScore']}",
                expanded=False,
            ):

                col1, col2 = st.columns(2)

                with col1:
                    st.metric(
                        "Risk Score",
                        score["RiskScore"],
                    )

                with col2:
                    st.metric(
                        "Risk Level",
                        score["RiskLevel"],
                    )

                st.write("### Triggered Signals")

                st.info(score["Signals"])

                st.write("### AI Assessment")

                st.markdown(summary)

else:
    st.warning("Please upload all four datasets to run the risk analysis pipeline.")