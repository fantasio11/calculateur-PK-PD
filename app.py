import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="Calculateur PK/PD Antibiotiques", layout="centered")
st.title("💊 Calculateur PK/PD Antibiotiques")
st.markdown("Personnalise la posologie selon le patient, l'antibiotique, l'infection et la CMI.")

# --- Paramètres antibiotiques ---
parametres_ab = {
    "Vancomycine": {"Vd": 0.7, "objectif": "AUC/MIC > 400", "type": "AUC/MIC"},
    "Pipéracilline-Tazobactam": {"Vd": 0.25, "objectif": "Temps > CMI 50%", "type": "Temps>CMI"},
    "Céfépime": {"Vd": 0.25, "objectif": "Temps > CMI 60%", "type": "Temps>CMI"},
    "Méropénème": {"Vd": 0.25, "objectif": "Temps > CMI 40%", "type": "Temps>CMI"},
    "Gentamicine": {"Vd": 0.25, "objectif": "Cmax/CMI > 8-10", "type": "Cmax/CMI"},
    "Amikacine": {"Vd": 0.25, "objectif": "Cmax/CMI > 8-10", "type": "Cmax/CMI"},
    "Ceftazidime": {"Vd": 0.25, "objectif": "Temps > CMI 50%", "type": "Temps>CMI"},
    "Ciprofloxacine": {"Vd": 2.0, "objectif": "AUC/MIC > 125", "type": "AUC/MIC"},
    "Amoxicilline/Acide clavulanique (1g/875)": {"Vd": 0.3, "objectif": "Temps > CMI 50%", "type": "Temps>CMI"},
    "Amoxicilline/Acide clavulanique (2g/875)": {"Vd": 0.3, "objectif": "Temps > CMI 50%", "type": "Temps>CMI"},
    "Amoxicilline seule": {"Vd": 0.3, "objectif": "Temps > CMI 50%", "type": "Temps>CMI"}
}

# --- Sélection antibiotique ---
st.header("1. Sélection de l'antibiotique")
choix_ab = st.selectbox("Choisir un antibiotique :", list(parametres_ab.keys()))
ab = parametres_ab[choix_ab]
Vd_L_kg = ab["Vd"]
type_objectif = ab["type"]
objectif_text = ab["objectif"]

# --- Données patient ---
st.header("2. Données patient")
poids = st.number_input("Poids (kg)", 30.0, 200.0, 70.0)
cl_cr = st.number_input("Clairance créatinine estimée (ml/min)", 10.0, 150.0, 80.0)
age = st.number_input("Âge (ans)", 18, 100, 50)

# --- Données traitement ---
st.header("3. Données thérapeutiques")
intervalle = st.number_input("Intervalle entre les doses (h)", 6, 48, 12, step=6)
cmi = st.number_input("CMI du germe (mg/L)", 0.1, 64.0, 1.0, step=0.1)
dose = st.number_input("Dose administrée (mg)", 100, 3000, 1000, step=100)

# --- Calculs PK ---
Vd = Vd_L_kg * poids
ke = 0.00083 * cl_cr + 0.0044
demi_vie = np.log(2) / ke
t = np.linspace(0, intervalle, 200)
concentration = (dose / Vd) * np.exp(-ke * t)
AUC = np.trapz(concentration, t)
Cmax = concentration[0]
temps_above_cmi = np.sum(concentration > cmi) * (intervalle / len(t))
t_pct = (temps_above_cmi / intervalle) * 100

# --- Affichage des objectifs ---
st.header("4. Objectif PK/PD")
st.success(f"🎯 Objectif pour {choix_ab} : {objectif_text}")

# --- Interprétation des résultats ---
st.header("5. Résultats calculés")
st.markdown(f"**Volume de distribution estimé :** {Vd:.1f} L")
st.markdown(f"**Demi-vie estimée :** {demi_vie:.1f} h")

if type_objectif == "AUC/MIC":
    ratio = AUC / cmi
    st.markdown(f"**AUC estimé :** {AUC:.1f} mg·h/L")
    st.markdown(f"**AUC/MIC :** {ratio:.1f}")
elif type_objectif == "Cmax/CMI":
    ratio = Cmax / cmi
    st.markdown(f"**Cmax estimé :** {Cmax:.1f} mg/L")
    st.markdown(f"**Cmax/CMI :** {ratio:.1f}")
elif type_objectif == "Temps>CMI":
    st.markdown(f"**Temps au-dessus de la CMI :** {temps_above_cmi:.1f} h")
    st.markdown(f"**% Temps > CMI :** {t_pct:.1f} %")

# --- Graphique PK ---
st.header("6. Courbe de concentration")
fig, ax = plt.subplots()
ax.plot(t, concentration, label="Concentration")
ax.axhline(y=cmi, color='r', linestyle='--', label=f"CMI = {cmi} mg/L")
ax.set_xlabel("Temps (heures)")
ax.set_ylabel("Concentration (mg/L)")
ax.set_title(f"Concentration de {choix_ab} sur {intervalle}h")
ax.legend()
st.pyplot(fig)

# --- Note ---
st.info("🧪 Ce simulateur PK/PD est une base de réflexion thérapeutique. À valider par un spécialiste.")




