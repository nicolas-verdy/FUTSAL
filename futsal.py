import streamlit as st
import sqlite3
import pandas as pd

# Config page
st.set_page_config(layout="wide")

# Connexion à la base SQLite
conn = sqlite3.connect("joueurs.db", check_same_thread=False)
cursor = conn.cursor()

# Création de la table si elle n'existe pas
cursor.execute("CREATE TABLE IF NOT EXISTS joueurs (nom TEXT UNIQUE)")
conn.commit()

# ------------------ BANDEAU ------------------
st.markdown("""
<style>
.banner {
    background-image: url("https://laurafoot.fff.fr/wp-content/uploads/sites/10/2021/01/Bandeau_SiteWeb-Futsal.png");
    background-size: cover;
    background-position: center;
    height: 220px;
    width: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
    color: white;
    font-size: 40px;
    font-weight: bold;
    border-radius: 10px;
}
.blue-title {
    color: blue;
    font-weight: bold;
    font-size: 20px;
}
</style>

<div class="banner">
⚽ FUTSAL DU MERCREDI ⚽
</div>
""", unsafe_allow_html=True)

st.title("⚽ Les Footix ⚽")
st.title("RDV=20H      KickOff=20h15")

# ------------------ FONCTIONS ------------------
def get_joueurs():
    cursor.execute("SELECT nom FROM joueurs")
    return [row[0] for row in cursor.fetchall()]

def afficher_joueurs(joueurs):
    df_joueurs = pd.DataFrame({'#': range(1, len(joueurs) + 1), 'Nom': joueurs})
    st.dataframe(df_joueurs.style.set_properties(**{'color': 'blue'}))

# ------------------ INSCRIPTION ------------------
nombre_max = 10
joueurs = get_joueurs()
places_restantes = nombre_max - len(joueurs)
st.markdown(f"## 🏆 Places : {places_restantes} / {nombre_max}")

nom = st.text_input("Votre nom")
if st.button("S'inscrire"):
    if nom:
        if len(joueurs) < nombre_max:
            try:
                cursor.execute("INSERT INTO joueurs (nom) VALUES (?)", (nom,))
                conn.commit()
                st.success(f"{nom} inscrit avec succès !")
            except sqlite3.IntegrityError:
                st.warning("Ce joueur est déjà inscrit !")
        else:
            st.error("Le nombre maximum de joueurs est atteint !")
    # Rafraîchir la liste après inscription
    joueurs = get_joueurs()

st.markdown("<div class='blue-title'>Joueurs inscrits :</div>", unsafe_allow_html=True)
afficher_joueurs(joueurs)

# ------------------ ARCHIVES ------------------
st.title("***ARCHIVES***")
st.write("*****")
st.write("**MARDI 30/12/25**")
st.write("20    --> Tanguy, Stef, Madjid, Mehdy, Yann")
st.write("à")
st.write("11    --> Mano, Charles, Guillaume, Cyril, Adrien")
st.write("La vidéo du match : https://drive.google.com/file/d/1OtOEvUW2MweI7F1t8iNcMm62n2ucxLC5/view?usp=sharing")
st.write("*****")
# (tu peux garder toutes tes archives ici)

# ------------------ CARTE ------------------
adresse = "8 Rue du Frenelet, 59650 Villeneuve-d'Ascq"
st.markdown(f"### Adresse : {adresse}")

map_iframe = """
<iframe src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d2520.4335253054123!2d3.1225587763705196!3d50.63979287371289!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x47c329dfdbd2b16b%3A0xd255ea458f438532!2s8%20Rue%20du%20Frenelet%2C%2059650%20Villeneuve-d'Ascq!5e1!3m2!1sfr!2sfr!4v1742461795759!5m2!1sfr!2sfr" width="600" height="450" style="border:0;" allowfullscreen="" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe>
"""
st.components.v1.html(map_iframe, height=500)

# ------------------ SUPPRESSION ------------------
st.write("### Supprimer un joueur (Organisateur uniquement)")
joueur_a_supprimer = st.selectbox("Sélectionner un joueur", [""] + joueurs)
password = st.text_input("Mot de passe", type="password")
if st.button("Supprimer"):
    if password == "Jules2014" and joueur_a_supprimer:
        cursor.execute("DELETE FROM joueurs WHERE nom = ?", (joueur_a_supprimer,))
        conn.commit()
        st.success(f"{joueur_a_supprimer} a été supprimé !")
        joueurs = get_joueurs()  # Rafraîchir la liste
    elif password != "Jules2014":
        st.error("Mot de passe incorrect")

# ------------------ RÉINITIALISATION ------------------
password_reset = st.text_input("Mot de passe pour réinitialiser", type="password")
if st.button("Réinitialiser la session"):
    if password_reset == "Jules2014":
        cursor.execute("DELETE FROM joueurs")
        conn.commit()
        st.success("Nouvelle session démarrée, toutes les inscriptions ont été réinitialisées.")
        joueurs = get_joueurs()  # Rafraîchir la liste
    else:
        st.error("Mot de passe incorrect")

# Fermeture de la connexion
conn.close()
