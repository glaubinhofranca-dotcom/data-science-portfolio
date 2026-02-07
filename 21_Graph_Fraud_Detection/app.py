import streamlit as st
import pandas as pd
import networkx as nx
import numpy as np
from sklearn.ensemble import IsolationForest
from pyvis.network import Network
import streamlit.components.v1 as components
import os

# --- Page Config ---
st.set_page_config(layout="wide", page_title="AML Graph Detector", page_icon="🕸️")

st.title("🕸️ Anti-Money Laundering (AML) Graph Detector")
st.markdown("""
**Advanced Data Science:** Using Graph Topology + Unsupervised Learning (IsolationForest) 
to detect money laundering rings and circular transactions.
""")

# --- 1. Load Data ---
@st.cache_data
def load_data():
    if not os.path.exists("transactions.csv"):
        st.error("❌ 'transactions.csv' not found. Please run 'data_gen.py' first.")
        return pd.DataFrame()
    
    df = pd.read_csv("transactions.csv")
    return df

df = load_data()

if not df.empty:
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.dataframe(df.head(), use_container_width=True)
    with col2:
        st.metric("Total Transactions", len(df))
        st.metric("Total Volume ($)", f"{df['amount'].sum():,.2f}")

    # --- 2. Build Graph (The Core Logic) ---
    st.divider()
    st.subheader("1. Graph Topology Analysis")
    
    # Initialize Directed Graph
    G = nx.from_pandas_edgelist(
        df, 
        source='sender', 
        target='receiver', 
        edge_attr='amount', 
        create_using=nx.DiGraph()
    )

    # --- 3. Feature Engineering (Graph Metrics) ---
    with st.spinner("Extracting topological features..."):
        # Degree Centrality: How many connections?
        degree_dict = dict(G.degree(weight='amount'))
        
        # In-Degree vs Out-Degree (Imbalance suggests layering)
        in_degree = dict(G.in_degree(weight='amount'))
        out_degree = dict(G.out_degree(weight='amount'))
        
        # PageRank: Identifying 'hub' nodes (important movers)
        pagerank = nx.pagerank(G, weight='amount')
        
        # Create a Features DataFrame for ML
        features = pd.DataFrame({
            'node': list(G.nodes()),
            'degree_centrality': [degree_dict[n] for n in G.nodes()],
            'in_degree': [in_degree[n] for n in G.nodes()],
            'out_degree': [out_degree[n] for n in G.nodes()],
            'pagerank': [pagerank[n] for n in G.nodes()]
        })
        
        # Feature: Ratio of In/Out (Suspicious if exactly 1.0 in high volume loops)
        # Added small epsilon (1e-5) to avoid division by zero
        features['flow_ratio'] = features['in_degree'] / (features['out_degree'] + 0.00001)
        
    st.success("✅ Graph Features Extracted successfully.")

    # --- 4. Unsupervised Anomaly Detection ---
    st.subheader("2. AI Anomaly Detection (Isolation Forest)")
    
    # Model parameters
    contamination = st.slider("Expected Fraud Rate (Contamination)", 0.01, 0.10, 0.05)
    
    model = IsolationForest(contamination=contamination, random_state=42)
    
    # Select features for training
    X = features[['degree_centrality', 'pagerank', 'flow_ratio']]
    
    # Train and Predict
    features['anomaly_score'] = model.fit_predict(X)
    # Isolation Forest returns -1 for anomalies, 1 for normal
    features['is_anomaly'] = features['anomaly_score'].apply(lambda x: 1 if x == -1 else 0)
    
    # Filter Anomalies
    anomalies = features[features['is_anomaly'] == 1]
    
    st.warning(f"🚨 Detected {len(anomalies)} Suspicious Accounts out of {len(features)} users.")
    st.dataframe(anomalies.sort_values(by="pagerank", ascending=False).head(10))

    # --- 5. Interactive Visualization ---
    st.subheader("3. Visual Investigation")
    
    # Filter graph to show only anomalies and their direct neighbors (Subgraph)
    suspicious_nodes = anomalies['node'].tolist()
    
    if suspicious_nodes:
        # Create subgraph for visualization (Full graph is too heavy for browser)
        subgraph_nodes = set(suspicious_nodes)
        for node in suspicious_nodes:
            if node in G:
                # Add neighbors to context
                neighbors = list(G.neighbors(node)) + list(G.predecessors(node))
                subgraph_nodes.update(neighbors)
                
        H = G.subgraph(subgraph_nodes)
        
        # Visualize using PyVis
        net = Network(height='600px', width='100%', bgcolor='#222222', font_color='white', directed=True)
        
        for node in H.nodes():
            # Color code: Red = Anomaly, Blue = Normal
            color = 'red' if node in suspicious_nodes else '#00BFFF'
            
            # Safe access to pagerank
            pr_val = pagerank.get(node, 0)
            
            title = f"User: {node}\nPageRank: {pr_val:.4f}"
            size = 15 + (pr_val * 500) # Size based on importance
            net.add_node(node, label=node, color=color, title=title, size=size)
            
        for edge in H.edges(data=True):
            sender, receiver, attr = edge
            # Ensure value is convertible to float/int for PyVis
            try:
                val = float(attr.get('amount', 1.0))
            except:
                val = 1.0
            
            net.add_edge(sender, receiver, value=val, title=f"${val:.2f}", color='#555555')

        # Physics options for better layout
        net.force_atlas_2based()
        
        # Save locally and read
        net.save_graph('pyvis_graph.html')
        
        # Read the file and display
        with open('pyvis_graph.html', 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        components.html(html_content, height=610)
    else:
        st.info("No anomalies detected with current threshold.")

else:
    st.info("Waiting for data. Please run 'data_gen.py' first.")