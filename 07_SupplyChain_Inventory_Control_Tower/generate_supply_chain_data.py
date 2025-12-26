import pandas as pd
import numpy as np
import random

# Configurações
NUM_SKUS = 5000 # Número de produtos diferentes
random.seed(42)
np.random.seed(42)

print(">>> Generating Supply Chain Data (Inventory & Sales)...")

# 1. Identificação do Produto (SKU)
skus = [f"SKU_{i:04d}" for i in range(1, NUM_SKUS + 1)]
categories = np.random.choice(['Electronics', 'Home & Garden', 'Apparel', 'Sports', 'Toys'], NUM_SKUS)

# 2. Dados de Vendas (Simulando Pareto / Curva ABC)
# 20% dos produtos vendem muito (Head), 80% vendem pouco (Tail)
# Usando distribuição Log-Normal para simular vendas reais
daily_sales_avg = np.random.lognormal(2, 1.2, NUM_SKUS) 
daily_sales_std = daily_sales_avg * np.random.uniform(0.1, 0.5, NUM_SKUS) # Volatilidade da demanda

# Preço Unitário
unit_prices = np.random.uniform(10, 500, NUM_SKUS)
unit_costs = unit_prices * 0.6 # Margem de 40%

# 3. Dados de Fornecimento (Lead Time)
# Quanto tempo demora para chegar o produto? (Variabilidade é o inimigo)
lead_time_avg = np.random.randint(5, 45, NUM_SKUS) # 5 a 45 dias
lead_time_std = lead_time_avg * 0.2 # Desvio padrão do fornecedor

# 4. Cálculo de Métricas de Inventário (Engenharia de Dados)
safety_stocks = []
reorder_points = []
abc_class = []
revenue_annual = []

z_score_95 = 1.65 # Nível de Serviço desejado de 95%

for i in range(NUM_SKUS):
    # Receita Anual Estimada
    rev = daily_sales_avg[i] * 365 * unit_prices[i]
    revenue_annual.append(rev)
    
    # Cálculo de Estoque de Segurança (Safety Stock)
    # Fórmula: Z * sqrt((Avg Lead Time * Std Demand^2) + (Avg Demand^2 * Std Lead Time^2))
    # Simplificada: Z * StdDev_Demand_During_LeadTime
    demand_during_lead_std = np.sqrt(lead_time_avg[i]) * daily_sales_std[i]
    ss = z_score_95 * demand_during_lead_std
    safety_stocks.append(round(ss, 0))
    
    # Ponto de Reabastecimento (Reorder Point) = (Avg Daily Sales * Avg Lead Time) + Safety Stock
    rop = (daily_sales_avg[i] * lead_time_avg[i]) + ss
    reorder_points.append(round(rop, 0))

# Classificação ABC (Baseada na Receita)
# Ordenar para calcular acumulado
temp_df = pd.DataFrame({'Revenue': revenue_annual})
temp_df = temp_df.sort_values('Revenue', ascending=False)
temp_df['Cumulative'] = temp_df['Revenue'].cumsum() / temp_df['Revenue'].sum()

def get_abc(cum_pct):
    if cum_pct <= 0.80: return 'A' # Top 80% da receita (Ouro)
    elif cum_pct <= 0.95: return 'B' # Próximos 15% (Prata)
    return 'C' # Últimos 5% (Cauda longa)

abc_map = {idx: get_abc(row['Cumulative']) for idx, row in temp_df.iterrows()}

# 5. Estoque Atual (Snapshot)
# Alguns SKUs terão estoque baixo (Risco de Stockout), outros excesso (Overstock)
current_inventory = []
stock_status = []

for i in range(NUM_SKUS):
    abc = abc_map[i]
    rop = reorder_points[i]
    
    # Simular status aleatório
    rand = np.random.random()
    if rand < 0.10: # 10% de chance de Stockout (Crítico para Classe A)
        inv = np.random.uniform(0, rop * 0.2)
        status = "Critical Low"
    elif rand < 0.30: # Excesso
        inv = rop * np.random.uniform(2, 3)
        status = "Overstock"
    else: # Normal
        inv = np.random.uniform(rop * 0.5, rop * 1.5)
        status = "Healthy"
        
    current_inventory.append(round(inv, 0))
    stock_status.append(status)
    abc_class.append(abc)

# DataFrame Final
df = pd.DataFrame({
    'SKU_ID': skus,
    'Category': categories,
    'ABC_Class': abc_class,
    'Unit_Price': [round(x, 2) for x in unit_prices],
    'Annual_Revenue': [round(x, 2) for x in revenue_annual],
    'Avg_Daily_Sales': [round(x, 1) for x in daily_sales_avg],
    'Lead_Time_Days': lead_time_avg,
    'Safety_Stock_Qty': safety_stocks,
    'Reorder_Point_Qty': reorder_points,
    'Current_Inventory_Qty': current_inventory,
    'Stock_Status': stock_status
})

# Cálculo Financeiro: Valor do Estoque
df['Inventory_Value'] = df['Current_Inventory_Qty'] * df['Unit_Price'] * 0.6 # Custo

# Salvar
df.to_csv('supply_chain_data.csv', index=False)
print("✅ Supply Chain Data Generated!")
print(f"📦 Total SKUs: {NUM_SKUS}")
print(f"💰 Total Inventory Value: ${df['Inventory_Value'].sum():,.2f}")
print(f"🚨 Critical Low Items: {df[df['Stock_Status'] == 'Critical Low'].shape[0]}")