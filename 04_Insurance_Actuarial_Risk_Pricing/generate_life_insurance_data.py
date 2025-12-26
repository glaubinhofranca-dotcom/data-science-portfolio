import pandas as pd
import numpy as np
import random

# Configurações
NUM_POLICIES = 12000
random.seed(42)
np.random.seed(42)

print(">>> Generating Life Insurance Portfolio (Actuarial Data)...")

# 1. Dados do Segurado
ids = [f"POL_{i:05d}" for i in range(1, NUM_POLICIES + 1)]
ages = np.random.randint(25, 75, NUM_POLICIES)
genders = np.random.choice(['Male', 'Female'], NUM_POLICIES)

# Fatores de Saúde (Cruciais para Life Insurance)
# Fumante paga 2x a 3x mais
smoker_status = np.random.choice(['Non-Smoker', 'Smoker'], NUM_POLICIES, p=[0.85, 0.15]) 

# BMI (Índice de Massa Corporal) - Risco de Obesidade
bmi = np.random.normal(26, 4, NUM_POLICIES) # Média 26, Desvio 4
bmi = [round(x, 1) for x in bmi]

# 2. Produto e Apólice
# Term Life (Barato, dura X anos) vs Whole Life (Caro, dura a vida toda + investimento)
product_types = np.random.choice(['Term Life 10Y', 'Term Life 20Y', 'Term Life 30Y', 'Whole Life'], NUM_POLICIES, p=[0.3, 0.3, 0.2, 0.2])

# Valor da Cobertura (Death Benefit)
coverage_amounts = np.random.choice([100000, 250000, 500000, 1000000], NUM_POLICIES, p=[0.4, 0.3, 0.2, 0.1])

# 3. Cálculo do Prêmio (Pricing Engine Simplificado)
annual_premiums = []
risk_scores = []

for i in range(NUM_POLICIES):
    base_rate = 0.5 # Custo por mil dolares de cobertura
    
    # Fator Idade (Exponencial)
    age_factor = (1.05 ** (ages[i] - 25))
    
    # Fator Fumante (Pesado)
    smoker_factor = 2.5 if smoker_status[i] == 'Smoker' else 1.0
    
    # Fator BMI (Saúde)
    bmi_factor = 1.0
    if bmi[i] > 30: bmi_factor = 1.5 # Obesidade
    
    # Fator Produto
    product_factor = 1.0
    if product_types[i] == 'Whole Life': product_factor = 10.0 # Whole Life é muito mais caro (tem Cash Value)
    elif product_types[i] == 'Term Life 30Y': product_factor = 2.0
    
    # Cálculo Final
    premium = (coverage_amounts[i] / 1000) * base_rate * age_factor * smoker_factor * bmi_factor * product_factor
    annual_premiums.append(round(premium, 2))
    
    # Score de Risco para análise
    risk_score = age_factor * smoker_factor * bmi_factor
    risk_scores.append(round(risk_score, 2))

# 4. Status da Apólice (O ciclo de vida)
# Active: Pagando
# Lapsed: Cancelou (Ruim para o negócio se for cedo)
# Death Claim: Morreu (Sinistro pago)
statuses = []

for i in range(NUM_POLICIES):
    r = np.random.random()
    
    # Probabilidade de Morte (Baseada em idade/saúde)
    death_prob = (ages[i] / 1000) * (2 if smoker_status[i] == 'Smoker' else 1)
    
    # Probabilidade de Cancelamento (Lapse) - Mais comum em apólices caras
    lapse_prob = 0.05
    if product_types[i] == 'Whole Life': lapse_prob = 0.08 # Mais caro, mais gente desiste
    
    if r < death_prob:
        statuses.append('Death Claim')
    elif r < (death_prob + lapse_prob):
        statuses.append('Lapsed')
    else:
        statuses.append('Active')

# Criar DataFrame
df = pd.DataFrame({
    'Policy_ID': ids,
    'Product_Type': product_types,
    'Age': ages,
    'Gender': genders,
    'Smoker_Status': smoker_status,
    'BMI': bmi,
    'Coverage_Amount': coverage_amounts,
    'Annual_Premium': annual_premiums,
    'Policy_Status': statuses,
    'Risk_Score': risk_scores
})

# Salvar
df.to_csv('life_insurance_data.csv', index=False)
print("✅ Life Insurance Data Generated!")
print(f"📉 Lapse Rate: {df[df['Policy_Status'] == 'Lapsed'].shape[0] / NUM_POLICIES:.2%}")
print(f"⚰️ Death Claims: {df[df['Policy_Status'] == 'Death Claim'].shape[0]}")
print(f"💰 Total Annual Premium: ${df['Annual_Premium'].sum():,.2f}")