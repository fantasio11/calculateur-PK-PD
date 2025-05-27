import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="Calculateur Vancomycine PK/PD", layout="centered")

st.title("💉 Calculateur PK/PD - Vancomycine")
st.markdown("Détermine une dose adaptée à ton patient, visualise la courbe concentration/temps, et estime le ratio AUC/MIC.")

# --- Données patient ---
st.header("1. Données patient")
poids = st.number_input("Poids (kg)", min_value=30.0, max_value=200.0, value=70.0)
taille = st.number_input("Taille (cm)", min_value=140, max_value=210, value=175)
age = st.number_input("Âge (ans)", min_value=18, max_value=100, value=50)
cl_cr = st.number_input("Clairance créatinine estimée (ml/min)", min_value=10.0, max_value=150.0, value=80.0)

# --- Données traitement ---
st.header("2. Schéma d'antibiothérapie")
dose = st.number_input("Dose administrée (mg)", min_value=100, max_value=3000, value=1000, step=100)
intervalle = st.number_input("Intervalle entre les doses (heures)", min_value=6, max_value=48, value=12, step=6)
cmi = st.number_input("CMI du germe (mg/L)", min_value=0.1, max_value=64.0, value=1.0, step=0.1)

# --- Calculs PK simplifiés ---
st.header("3. Résultats PK/PD estimés")

# Volume de distribution simplifié (0.7 L/kg)
Vd = 0.7 * poids
# Ke selon Matzke modifié
ke = 0.00083 * cl_cr + 0.0044
demi_vie = np.log(2) / ke

# Temps et concentrations
t = np.linspace(0, intervalle, 200)
concentration = (dose / Vd) * np.exp(-ke * t)

# AUC estimée sur un intervalle donné (approche simplifiée)
AUC = np.trapz(concentration, t)
ratio_auc_mic = AUC / cmi

st.markdown(f"**Volume de distribution estimé :** {Vd:.1f} L")
st.markdown(f"**Demi-vie estimée :** {demi_vie:.1f} h")
st.markdown(f"**AUC estimée sur {intervalle} h :** {AUC:.1f} mg·h/L")
st.markdown(f"**Ratio AUC/CMI :** {ratio_auc_mic:.1f}")

# --- Graphique ---
st.subheader("Courbe de concentration")
fig, ax = plt.subplots()
ax.plot(t, concentration, label="[Vanco]")
ax.axhline(y=cmi, color='r', linestyle='--', label=f"CMI = {cmi} mg/L")
ax.set_xlabel("Temps (heures)")
ax.set_ylabel("Concentration (mg/L)")
ax.set_title("Concentration de vancomycine au cours du temps")
ax.legend()
st.pyplot(fig)

# --- Note ---
st.info("🔬 Ce modèle est une approximation simplifiée. N'utilise pas ce calcul seul pour ajuster une posologie réelle.")

