import pandas as pd
import random
import uuid
from datetime import datetime, timedelta

# --- Configuration ---
NUM_USERS = 200
NUM_TRANSACTIONS = 1500
FRAUD_RINGS = 5  # Number of criminal groups to inject

def generate_data():
    """
    Generates synthetic banking transactions with injected fraud patterns.
    """
    users = [f"User_{i}" for i in range(NUM_USERS)]
    transactions = []

    # 1. Generate Legitimate Traffic (Random Noise)
    print("🎲 Generating legitimate transactions...")
    for _ in range(NUM_TRANSACTIONS):
        sender = random.choice(users)
        receiver = random.choice(users)
        while receiver == sender:
            receiver = random.choice(users)
            
        amount = round(random.uniform(10.0, 5000.0), 2)
        timestamp = datetime.now() - timedelta(days=random.randint(0, 30))
        
        transactions.append({
            "sender": sender,
            "receiver": receiver,
            "amount": amount,
            "timestamp": timestamp,
            "is_fraud": 0
        })

    # 2. Inject Fraud Rings (Smurfing/Structuring Cycles)
    # Pattern: A -> B -> C -> A (Money laundering loop)
    print(f"⚠️ Injecting {FRAUD_RINGS} fraud rings...")
    
    for i in range(FRAUD_RINGS):
        # Create a dedicated ring of 3-5 mules
        ring_size = random.randint(3, 5)
        mules = random.sample(users, ring_size)
        
        base_amount = random.uniform(10000, 50000) # High value
        
        for j in range(len(mules)):
            sender = mules[j]
            receiver = mules[(j + 1) % len(mules)] # Points to next, last points to first
            
            # Add jitter to amount to evade basic rules
            amount = base_amount * random.uniform(0.95, 1.05)
            
            transactions.append({
                "sender": sender,
                "receiver": receiver,
                "amount": round(amount, 2),
                "timestamp": datetime.now(), # Recent activity
                "is_fraud": 1 # Label for validation later
            })

    # 3. Create DataFrame
    df = pd.DataFrame(transactions)
    df = df.sort_values(by="timestamp").reset_index(drop=True)
    
    # Save to CSV
    df.to_csv("transactions.csv", index=False)
    print(f"✅ Data generated: {len(df)} transactions saved to 'transactions.csv'")
    return df

if __name__ == "__main__":
    generate_data()