# 🏨 Hotel Booking Cancellation Prediction

## 📌 Project Overview
High cancellation rates are a major revenue leak in the hospitality industry. This project utilizes machine learning to predict which bookings are likely to be canceled *before* the arrival date. By identifying high-risk bookings, hotel managers can implement overbooking strategies or offer incentives to secure revenue.

## 💼 Business Problem
- **Issue:** Last-minute cancellations lead to empty rooms and lost revenue.
- **Goal:** Predict cancellation probability for every new booking.
- **Impact:** Optimize inventory management and reduce "Revenue at Risk".

## 🛠️ Tech Stack
- **Language:** Python
- **Libraries:** Pandas, Scikit-Learn (Random Forest), NumPy.
- **Visualization:** Power BI (Interactive Dashboard).

## 📊 Methodology
1. **Data Generation:** Simulated 5,000 realistic booking records including Lead Time, ADR, Market Segment, and Deposit Type.
2. **Feature Engineering:** Created flags for "High Lead Time" and "History of Cancellations".
3. **Modeling:** Trained a **Random Forest Classifier** to predict the `Is_Canceled` target.
4. **Risk Scoring:** Calculated `Revenue_at_Risk` (Probability * Total Booking Value).

## 📈 Key Results
- **Model Performance:** Achieved robust ROC-AUC scores, effectively distinguishing between reliable and risky guests.
- **Dashboard:** Visualizes the monetary impact of potential cancellations, allowing for data-driven Revenue Management decisions.

## 🚀 How to Run
1. Run the script: `python project_booking_cancellation.py`
2. The script will generate `hotel_bookings_powerbi.csv`.
3. Import the CSV into Power BI to view the risk analysis dashboard.
