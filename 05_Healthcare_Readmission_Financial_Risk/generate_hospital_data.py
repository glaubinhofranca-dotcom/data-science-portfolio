import pandas as pd
import numpy as np
import random

# Configurações
NUM_PATIENTS = 15000
random.seed(42)
np.random.seed(42)

print(">>> Generating Synthetic Hospital Data (HIPAA Compliant)...")

# 1. Dados Demográficos
ids = [f"PT_{i:05d}" for i in range(1, NUM_PATIENTS + 1)]
ages = np.random.randint(18, 95, NUM_PATIENTS)
genders = np.random.choice(['Male', 'Female'], NUM_PATIENTS)

# 2. Dados Clínicos e de Admissão
# Tipos de admissão impactam o custo e risco
admission_types = np.random.choice(['Emergency', 'Elective', 'Urgent', 'Trauma'], NUM_PATIENTS, p=[0.5, 0.3, 0.15, 0.05])
diagnoses = np.random.choice(['Heart Failure', 'Diabetes', 'Pneumonia', 'COPD', 'Hip/Knee Replacement', 'Sepsis'], NUM_PATIENTS)

# Tempo de internação (Length of Stay - LOS) depende um pouco do diagnóstico
los = []
for diag in diagnoses:
    if diag == 'Sepsis': los.append(np.random.randint(5, 20))
    elif diag == 'Heart Failure': los.append(np.random.randint(3, 12))
    elif diag == 'Diabetes': los.append(np.random.randint(2, 8))
    else: los.append(np.random.randint(1, 10))
los = np.array(los)

# Comorbidades (Fatores de Risco)
has_diabetes = np.random.choice([0, 1], NUM_PATIENTS, p=[0.7, 0.3])
has_hypertension = np.random.choice([0, 1], NUM_PATIENTS, p=[0.6, 0.4])
num_prior_visits = np.random.poisson(0.5, NUM_PATIENTS) # Média de visitas anteriores

# 3. Engenharia do "Risco de Readmissão" (A Lógica do Modelo)
# Vamos criar uma probabilidade baseada na saúde do paciente para não ser totalmente aleatório
readmission_prob = (
    (ages / 100) * 0.3 +            # Mais velhos = mais risco
    (has_diabetes * 0.2) +          # Diabetes = mais risco
    (has_hypertension * 0.1) +      # Hipertensão = mais risco
    (num_prior_visits * 0.1) +      # Quem vai muito ao hospital tende a voltar
    np.random.normal(0, 0.1, NUM_PATIENTS) # Ruído aleatório
)

# Normalizar probabilidade entre 0 e 1
readmission_prob = (readmission_prob - readmission_prob.min()) / (readmission_prob.max() - readmission_prob.min())
readmitted = [1 if p > 0.65 else 0 for p in readmission_prob] # Threshold de corte

# 4. Dados Financeiros (A parte "Asset Allocation")
# Quanto custou a internação inicial?
base_costs = {'Heart Failure': 12000, 'Diabetes': 8000, 'Pneumonia': 9000, 'COPD': 7500, 'Sepsis': 25000, 'Hip/Knee Replacement': 35000}
billing_amount = []
potential_penalty = []

for i in range(NUM_PATIENTS):
    # Custo base + Custo por dia ($1500/dia) + Variação aleatória
    cost = base_costs[diagnoses[i]] + (los[i] * 1500) + np.random.randint(-1000, 2000)
    billing_amount.append(round(cost, 2))
    
    # Penalidade Estimada (Se readmitido, hospital perde ~20% do valor ou tem custo não reembolsado)
    # Asset Managers gostam de ver "Risco Exposto"
    penalty = cost * 0.25 if readmitted[i] == 1 else 0
    potential_penalty.append(round(penalty, 2))

# 5. Consolidar DataFrame
df = pd.DataFrame({
    'Patient_ID': ids,
    'Age': ages,
    'Gender': genders,
    'Admission_Type': admission_types,
    'Primary_Diagnosis': diagnoses,
    'Length_of_Stay_Days': los,
    'Has_Diabetes': has_diabetes,
    'Has_Hypertension': has_hypertension,
    'Prior_Emergency_Visits': num_prior_visits,
    'Billing_Amount': billing_amount,       # Receita
    'Readmitted_30d': readmitted,           # Target (0 ou 1)
    'Financial_Risk_Penalty': potential_penalty # Risco ($)
})

# Inserir alguns valores nulos para mostrar que sabe tratar dados (Data Cleaning)
df.loc[df.sample(frac=0.02).index, 'Age'] = np.nan

# Salvar
df.to_csv('hospital_readmission_data.csv', index=False)
print(f"✅ Success! Generated {NUM_PATIENTS} patient records.")
print(f"📊 Readmission Rate: {df['Readmitted_30d'].mean():.2%}")
print(f"💰 Total Financial Exposure: ${df['Financial_Risk_Penalty'].sum():,.2f}")