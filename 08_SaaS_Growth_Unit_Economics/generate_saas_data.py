import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

# Configurações
NUM_CUSTOMERS = 8000
START_DATE = datetime(2023, 1, 1)
END_DATE = datetime(2025, 1, 1)
random.seed(42)
np.random.seed(42)

print(">>> Generating SaaS Subscription Data (LTV & Churn)...")

# 1. Dados do Cliente
ids = [f"CUST_{i:04d}" for i in range(1, NUM_CUSTOMERS + 1)]
segments = np.random.choice(['SMB', 'Mid-Market', 'Enterprise'], NUM_CUSTOMERS, p=[0.6, 0.3, 0.1])
acquisition_channel = np.random.choice(['Organic', 'Paid Ads', 'Referral', 'Sales Outbound'], NUM_CUSTOMERS)

# 2. Dados de Assinatura
# Enterprise paga muito mais e fica mais tempo
prices = {'SMB': 99, 'Mid-Market': 499, 'Enterprise': 2500}
churn_rates_base = {'SMB': 0.05, 'Mid-Market': 0.02, 'Enterprise': 0.005} # Churn mensal

signup_dates = []
churn_dates = []
status_list = []
mrr_list = [] # Monthly Recurring Revenue
ltv_list = []

for i in range(NUM_CUSTOMERS):
    seg = segments[i]
    
    # Data de Início aleatória nos últimos 2 anos
    days_range = (END_DATE - START_DATE).days
    start_day = START_DATE + timedelta(days=np.random.randint(0, days_range))
    signup_dates.append(start_day)
    
    mrr = prices[seg]
    mrr_list.append(mrr)
    
    # Simular Churn (Sobrevivência)
    # Probabilidade de cancelar a cada mês
    months_active = 0
    is_active = True
    current_date = start_day
    churn_date = None
    
    while current_date < END_DATE:
        months_active += 1
        current_date += timedelta(days=30)
        
        # Teste de Churn
        if np.random.random() < churn_rates_base[seg]:
            is_active = False
            churn_date = current_date
            break
    
    if is_active:
        status_list.append('Active')
        churn_dates.append(None)
    else:
        status_list.append('Churned')
        churn_dates.append(churn_date)
        
    # Cálculo do LTV (Lifetime Value) Realizado
    # Quanto dinheiro ele deixou até agora?
    ltv = months_active * mrr
    ltv_list.append(ltv)

# 3. Métricas Derivadas
df = pd.DataFrame({
    'Customer_ID': ids,
    'Segment': segments,
    'Acquisition_Channel': acquisition_channel,
    'Signup_Date': signup_dates,
    'Churn_Date': churn_dates,
    'Status': status_list,
    'MRR': mrr_list,
    'Lifetime_Value': ltv_list
})

# Preencher datas nulas de churn (para Power BI não reclamar)
df['Churn_Date'] = df['Churn_Date'].fillna(pd.NaT)

# Salvar
df.to_csv('saas_growth_data.csv', index=False)
print("✅ SaaS Data Generated!")
print(f"💰 Total ARR (Annual Run Rate): ${(df[df['Status']=='Active']['MRR'].sum() * 12):,.2f}")
print(f"📉 Churned Customers: {df[df['Status']=='Churned'].shape[0]}")