# 👥 Hotel Customer Segmentation (Clustering)

## 📌 Project Overview
Understanding guest behavior is key to personalized marketing. This project uses Unsupervised Learning to group guests into distinct personas based on their spending habits, lead time, and stay duration, enabling targeted CRM campaigns.

## 💼 Business Problem
- **Issue:** "One-size-fits-all" marketing wastes budget and creates low engagement.
- **Goal:** Identify distinct guest profiles automatically.
- **Impact:** Higher conversion rates on email campaigns and upsell offers.

## 🛠️ Tech Stack
- **Language:** Python
- **Libraries:** Pandas, Scikit-Learn (K-Means Clustering, StandardScaler).
- **Visualization:** Power BI (Scatter Plots & Persona Profiles).

## 📊 Methodology
1. **Data Preprocessing:** Standardized features (ADR, Lead Time, Total Stays) to ensure equal weighting.
2. **Clustering:** Applied **K-Means algorithm** to find natural groupings in the data.
3. **Persona Naming:** Analyzed cluster centers to label groups (e.g., "VIP/Luxury", "Budget Traveler", "Corporate").

## 📈 Key Results
- **Segments Identified:** Successfully isolated high-value VIPs (high ADR) from advance-planning Families.
- **Actionable Insights:** Marketing teams can now send exclusive spa offers to the VIP cluster and discount codes to the Budget cluster.

## 🚀 How to Run
1. Run the script: `python project_segmentation.py`
2. The script will generate `guest_segmentation_powerbi.csv`.
3. Import into Power BI to visualize the clusters using Scatter Charts.
