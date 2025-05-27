import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="Calculateur PK/PD - Vancomycine", layout="centered")
st.title("💉 Calculateur PK/PD - Vancomycine")
st.markdown("Détermine la posologie optimale selon le patient, l'infection, le germe et la CMI.")

# --- 1. Données patient ---
st.header("1. Données patient")
poids = st.number_input("Poids (kg)", min_value=30.0, max_value=200.0, value=70.0)
taille = st.number_input("Taille (cm)", min_value=140, max_value=220, value=175)
age = st.number_input("Âge (ans)", min_value=18, max_value=100, value=50)
cl_cr = st.number_input("Clairance créatinine estimée (ml/min)", min_value=10.0, max_value=150.0, value=80.0)

# --- 2. Type d'infection et germe ---
st.header("2. Site infectieux et germe")
site = st.selectbox("Type d'infection", [
    "Pneumonie",
    "Endocardite",
    "Méningite",
    "Infection urinaire",
    "Sepsis",
    "Ostéomyélite",
    "Autre"
])

germe = st.selectbox("Germe suspecté / identifié", [
    "Staphylococcus aureus sensible (MSSA)",
    "Staphylococcus aureus résistant (MRSA)",
    "Streptococcus pneumoniae",
    "Pseudomonas aeruginosa",
    "Escherichia coli",
    "Enterococcus faecalis",
    "Aucun / Empirique"
])

# --- 3. Objectif PK/PD selon site et germe ---
st.header("3. Objectif PK/PD recommandé")
auc_cible = 400  # par défaut
reco = ""

if site == "Pneumonie" and germe == "Staphylococcus aureus résistant (MRSA)":
    auc_cible = 400
    reco = "AUC/MIC ≥ 400 pendant 5 à 7 jours"
elif site == "Endocardite":
    auc_cible = 500
    reco = "AUC/MIC ≥ 500 pendant 4 à 6 semaines"
elif site == "Méningite":
    auc_cible = 0
    reco = "Viser un **pic > 20-25 mg/L**, car diffusion méningée limitée"
elif site == "Ostéomyélite":
    auc_cible = 450
    reco = "AUC/MIC ≥ 450, traitement long (6+ semaines)"
elif site == "Infection urinaire":
    auc_cible = 0
    reco = "Bonne diffusion urinaire, mais Vanco souvent inadaptée"
else:
    auc_cible = 400
    reco = "AUC/MIC ≥ 400 en traitement empirique"

if auc_cible > 0:
    st.success(f"🎯 Objectif : {reco}")
else:
    st.info(f"ℹ️ Objectif : {reco}")

# --- 4. Données traitement ---
st.header("4. Paramètres thérapeutiques")
intervalle = st.number_input("Intervalle d'administration (h)", min_value=6, max_value=48, value=12, step=6)
cmi = st.number_input("CMI du germe (mg/L)", min_value=0.1, max_value=64.0, value=1.0, step=0.1)

# --- 5. Calculs PK ---
Vd = 0.7 * poids
ke = 0.00083 * cl_cr + 0.0044
demi_vie = np.log(2) / ke

# --- Calcul dose recommandée ---
dose_recommandée = auc_cible * ke * Vd if auc_cible > 0 else 0

# --- 6. Visualisation du schéma personnalisé ---
st.header("5. Schéma personnalisé")
if dose_recommandée > 0:
    st.markdown(f"💊 **Dose recommandée :** {dose_recommandée:.0f} mg toutes les {intervalle} h")
else:
    st.info("💡 Dose non calculée. Approche AUC non adaptée ici.")

# Courbe concentration/temps
t = np.linspace(0, intervalle, 200)
concentration = (dose_recommandée / Vd) * np.exp(-ke * t)
AUC = np.trapz(concentration, t)
ratio_auc_mic = AUC / cmi

# --- 7. Résultats PK/PD ---
st.header("6. Résultats PK/PD simulés")
st.markdown(f"**Volume de distribution :** {Vd:.1f} L")
st.markdown(f"**Demi-vie estimée :** {demi_vie:.1f} h")
st.markdown(f"**AUC estimée :** {AUC:.1f} mg·h/L")
st.markdown(f"**Ratio AUC/CMI :** {ratio_auc_mic:.1f}")

# --- 8. Graphique ---
st.subheader("📈 Courbe de concentration")
fig, ax = plt.subplots()
ax.plot(t, concentration, label="Concentration")
ax.axhline(y=cmi, color='r', linestyle='--', label=f"CMI = {cmi} mg/L")
ax.set_xlabel("Temps (heures)")
ax.set_ylabel("Concentration (mg/L)")
ax.set_title("Courbe PK - Vancomycine")
ax.legend()
st.pyplot(fig)

# --- 9. Avertissement ---
st.info("🔬 Ce simulateur est à visée pédagogique. Ne remplace pas une validation pharmacologique ou infectiologique.")



