import streamlit as st
import sqlite3
import pandas as pd

# Connexion à la base SQLite
conn = sqlite3.connect("joueurs.db", check_same_thread=False)
cursor = conn.cursor()

# Création de la table si elle n'existe pas
cursor.execute("CREATE TABLE IF NOT EXISTS joueurs (nom TEXT UNIQUE)")
conn.commit()

# Affichage de l'image en bandeau
st.markdown("""
    <style>
        .title {
            background-image: url('https://laurafoot.fff.fr/wp-content/uploads/sites/10/2021/01/Bandeau_SiteWeb-Futsal.png');
            background-size: cover;
            background-position: center;
            color: white;
            padding: 50px;
            font-size: 40px;
            text-align: center;
            font-weight: bold;
            border-radius: 10px;
        }
        .blue-title {
            color: blue;
            font-size: 24px;
            font-weight: bold;
        }
    </style>
    <div class="title"></div>
""", unsafe_allow_html=True)

st.title("⚽ Les Footix du Mercredi - Inscription Futsal 20h15")

# Vérification du nombre de joueurs inscrits
cursor.execute("SELECT nom FROM joueurs")
joueurs = [row[0] for row in cursor.fetchall()]
nombre_max = 10
places_restantes = nombre_max - len(joueurs)

# Affichage du nombre de places restantes
st.markdown(f"## 🏆 Places restantes : {places_restantes} / {nombre_max}")

# Formulaire d'inscription
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

# Affichage des joueurs inscrits avec indexation à partir de 1
st.markdown("<div class='blue-title'>Joueurs inscrits :</div>", unsafe_allow_html=True)

df_joueurs = pd.DataFrame({'#': range(1, len(joueurs) + 1), 'Nom': joueurs})
st.dataframe(df_joueurs.style.set_properties(**{'color': 'blue'}))

# Insérer 10 lignes vides
for _ in range(10):
    st.text("")

# Suppression d'un joueur (réservé à l'organisateur avec mot de passe)
st.write("### Supprimer un joueur (Organisateur uniquement)")
joueur_a_supprimer = st.selectbox("Sélectionner un joueur", [""] + joueurs)
password = st.text_input("Mot de passe", type="password")
if st.button("Supprimer"):
    if password == "Jules2014" and joueur_a_supprimer:
        cursor.execute("DELETE FROM joueurs WHERE nom = ?", (joueur_a_supprimer,))
        conn.commit()
        st.success(f"{joueur_a_supprimer} a été supprimé !")
    elif password != "Jules2014":
        st.error("Mot de passe incorrect")

# Réinitialisation de la session avec mot de passe
password_reset = st.text_input("Mot de passe pour réinitialiser", type="password")
if st.button("Réinitialiser la session"):
    if password_reset == "Jules2014":
        cursor.execute("DELETE FROM joueurs")
        conn.commit()
        st.success("Nouvelle session démarrée, toutes les inscriptions ont été réinitialisées.")
    else:
        st.error("Mot de passe incorrect")

# Fermeture de la connexion
conn.close()

#  streamlit run futsal.py
