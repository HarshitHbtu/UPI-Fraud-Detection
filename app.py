import streamlit as st
import pandas as pd
import pickle

# ---------------- Load Model & Scaler ----------------

with open("fraud_model.pkl", "rb") as f:
    model = pickle.load(f)

with open("scaler.pkl", "rb") as f:
    scaler = pickle.load(f)

# ---------------- Page Configuration ----------------

st.set_page_config(
    page_title="UPI Fraud Detection",
    page_icon="💳",
    layout="centered"
)

st.title("💳 UPI Fraud Detection System")
st.write("Predict whether a UPI transaction is Genuine, Suspicious, or Fraudulent")

# ---------------- Inputs Section ----------------

step = st.number_input("Step", min_value=0, value=1)

amount = st.number_input(
    "Transaction Amount",
    min_value=0.0,
    format="%.2f"
)

oldbalanceOrg = st.number_input(
    "Old Balance (Sender)",
    min_value=0.0,
    format="%.2f"
)

newbalanceOrig = st.number_input(
    "New Balance (Sender)",
    min_value=0.0,
    format="%.2f"
)

oldbalanceDest = st.number_input(
    "Old Balance (Receiver)",
    min_value=0.0,
    format="%.2f"
)

newbalanceDest = st.number_input(
    "New Balance (Receiver)",
    min_value=0.0,
    format="%.2f"
)

transaction_type = st.selectbox(
    "Transaction Type",
    [
        "PAYMENT",
        "TRANSFER",
        "CASH_OUT",
        "DEBIT"
    ]
)

# ---------------- Prediction & Validation Logic ----------------

if st.button("Predict"):

    # 1. Rule Based Validation (Capturing Mismatches)
    
    st.subheader("System Alerts & Validation")
    has_warnings = False

    # Check 1: Sender balance insufficient
    if amount > oldbalanceOrg:
        st.warning("⚠️ Rule Alert: Insufficient Balance detected for this transaction.")
        st.write(f"- **Available Balance:** ₹{oldbalanceOrg:,.2f}")
        st.write(f"- **Requested Amount:** ₹{amount:,.2f}")
        has_warnings = True

    # Check 2: Sender balance mismatch
    expected_sender = max(oldbalanceOrg - amount, 0)
    if abs(expected_sender - newbalanceOrig) > 1:
        st.warning("⚠️ Rule Alert: Sender balance is mathematically inconsistent.")
        st.write(f"- **Expected New Sender Balance:** ₹{expected_sender:,.2f}")
        st.write(f"- **Entered New Sender Balance:** ₹{newbalanceOrig:,.2f}")
        has_warnings = True

    # Check 3: Receiver balance mismatch
    expected_receiver = oldbalanceDest + amount
    if abs(expected_receiver - newbalanceDest) > 1:
        st.warning("⚠️ Rule Alert: Receiver balance is mathematically inconsistent.")
        st.write(f"- **Expected Receiver Balance:** ₹{expected_receiver:,.2f}")
        st.write(f"- **Entered Receiver Balance:** ₹{newbalanceDest:,.2f}")
        has_warnings = True

    if not has_warnings:
        st.success("✅ All basic accounting rules passed successfully!")

    # 2. One Hot Encoding

    type_CASH_OUT = 0
    type_DEBIT = 0
    type_PAYMENT = 0
    type_TRANSFER = 0

    if transaction_type == "CASH_OUT":
        type_CASH_OUT = 1
    elif transaction_type == "DEBIT":
        type_DEBIT = 1
    elif transaction_type == "PAYMENT":
        type_PAYMENT = 1
    elif transaction_type == "TRANSFER":
        type_TRANSFER = 1

    # 3. Create Input DataFrame

    input_data = pd.DataFrame([[
        step,
        amount,
        oldbalanceOrg,
        newbalanceOrig,
        oldbalanceDest,
        newbalanceDest,
        type_CASH_OUT,
        type_DEBIT,
        type_PAYMENT,
        type_TRANSFER
    ]], columns=[
        "step",
        "amount",
        "oldbalanceOrg",
        "newbalanceOrig",
        "oldbalanceDest",
        "newbalanceDest",
        "type_CASH_OUT",
        "type_DEBIT",
        "type_PAYMENT",
        "type_TRANSFER"
    ])

    # 4. Scaling & ML Model Prediction

    input_scaled = scaler.transform(input_data)
    fraud_probability = model.predict_proba(input_scaled)[0][1]

    st.divider()

    
    st.subheader("Final Prediction Result")

    if fraud_probability >= 0.20:
        st.error("🚨 Fraudulent Transaction Detected")
        st.write("**System Status:** TRANSACTION BLOCKED. High ML risk model trigger.")
        
    elif has_warnings:
        st.warning("🟡 Suspicious Transaction")
        st.write("**System Status:** TRANSACTION FLAGGED. Accounting data discrepancies found.")
        
    else:
        st.success("✅ Genuine Transaction")
        st.write("**System Status:** TRANSACTION APPROVED. Passed all safety layers.")

    # Metric Display
    st.metric(
        "Model Confidence (Fraud Probability)",
        f"{fraud_probability*100:.2f}%"
    )

    # Debug Section
    with st.expander("Transaction Details (Debug View)"):
        st.write("### Raw Dataframe Input:")
        st.dataframe(input_data, use_container_width=True)