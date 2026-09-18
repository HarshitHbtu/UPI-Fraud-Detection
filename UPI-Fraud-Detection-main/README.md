# 💳 UPI Fraud Detection System

A Machine Learning based web application that predicts whether a UPI transaction is **Genuine**, **Suspicious**, or **Fraudulent** using a **Random Forest Classifier** and a simple **rule-based validation system**.

The application is built with **Streamlit** and provides an easy-to-use interface for testing transaction details.

---

## 🚀 Features

- Predicts Genuine, Suspicious, or Fraudulent transactions
- Random Forest based fraud detection
- Rule-based validation for:
  - Insufficient sender balance
  - Sender balance mismatch
  - Receiver balance mismatch
- Displays fraud probability
- Interactive Streamlit web interface<img width="770" height="1324" alt="Screenshot 2026-07-09 171641" src="https://github.com/user-attachments/assets/700f677d-c6be-4404-a0e3-1afecf33d2ba" />
<img width="1196" height="1282" alt="Screenshot 2026-07-09 173831" src="https://github.com/user-attachments/assets/006b998d-4982-4e76-bc3b-4ca2e26c48a1" />

---

## 🛠 Tech Stack

- Python
- Pandas
- NumPy
- Scikit-learn
- Streamlit
- Matplotlib

---

## 📂 Project Structure

```
UPI-Fraud-Detection/
│
├── app.py
├── UpiFraudDetection.ipynb
├── fraud_model.pkl
├── scaler.pkl
└── README.md
```

---

## ▶️ How to Run

Clone the repository

```bash
git clone https://github.com/HarshitHbtu/UPI-Fraud-Detection.git
```

Move into the project folder

```bash
cd UPI-Fraud-Detection
```

Install the required libraries

```bash
pip install streamlit pandas numpy scikit-learn matplotlib
```

Run the application

```bash
streamlit run app.py
```

---

## 📊 Model

- Algorithm: **Random Forest Classifier**
- Feature Scaling: **StandardScaler**
- One-Hot Encoding for transaction types
- Fraud prediction based on probability threshold

---

## 📈 Future Improvements

- Train using larger datasets
- Experiment with XGBoost and LightGBM
- Deploy the application online
- Add explainable AI (SHAP)

---

## 👨‍💻 Author

**Harshit Gangwar**

B.Tech (Information Technology)  
Harcourt Butler Technical University, Kanpur

GitHub: https://github.com/HarshitHbtu
