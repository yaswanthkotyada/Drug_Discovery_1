import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import ast
from rdkit import Chem
from rdkit.Chem import Draw

# Load the dataset
st.title("🔬 Quantum Molecular Simulation for Drug Discovery")

def load_data():
    uploaded_file = st.file_uploader("Upload your quantum molecular results CSV", type=["csv"])
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        return df
    return None

df = load_data()

if df is not None:
    st.subheader("📊 Data Overview")
    st.write(df.head())  # Show first few rows
    
    # Display available columns
    st.write("### Available Columns:")
    st.write(df.columns.tolist())
    
    # Check if 'Quantum Measurement Counts' exists
    if 'Quantum Measurement Counts' in df.columns:
        df['Quantum Measurement Counts'] = df['Quantum Measurement Counts'].apply(lambda x: ast.literal_eval(str(x)))
    else:
        st.warning("Quantum Measurement Counts column is missing! Please check the uploaded CSV file.")
    
    # Molecular Structure Visualization
    st.subheader("🧪 Molecular Structures")
    mol_col = "SMILES"  # Ensure the column name matches your dataset
    if mol_col in df.columns:
        df["Molecule"] = df[mol_col].apply(lambda x: Chem.MolFromSmiles(x) if pd.notna(x) else None)
        for _, row in df.iterrows():
            if row["Molecule"]:
                st.image(Draw.MolToImage(row["Molecule"]), caption=f"Molecule: {row[mol_col]}")
    
    # Energy Convergence Plot
    st.subheader("📉 Energy Convergence")
    if "Optimized Molecular Configuration" in df.columns:
        energy_values = [sum(ast.literal_eval(str(x))**2) for x in df["Optimized Molecular Configuration"] if pd.notna(x)]
        plt.figure(figsize=(8, 4))
        plt.plot(range(len(energy_values)), energy_values, marker='o', linestyle='-', color='blue')
        plt.xlabel("Iteration")
        plt.ylabel("Energy Value")
        plt.title("Energy Convergence Plot")
        st.pyplot(plt)
    else:
        st.warning("Optimized Molecular Configuration column is missing!")
    
    # Quantum Measurement Counts Distribution
    st.subheader("🔢 Quantum Measurement Counts")
    if 'Quantum Measurement Counts' in df.columns:
        for index, row in df.iterrows():
            plt.figure(figsize=(6, 4))
            plt.bar(row['Quantum Measurement Counts'].keys(), row['Quantum Measurement Counts'].values(), color='purple')
            plt.xlabel("Measurement Outcome")
            plt.ylabel("Frequency")
            plt.title(f"Quantum Measurement for Molecule {index+1}")
            st.pyplot(plt)

else:
    st.info("Please upload a valid CSV file to continue.")


