import streamlit as st
import sqlite3

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
    </style>
    <div class="title"></div>
""", unsafe_allow_html=True)

st.title("⚽ Les Footix du Mercredi - Inscription Futsal 20h15")

# Formulaire d'inscription
nom = st.text_input("Votre nom")
if st.button("S'inscrire"):
    if nom:
        try:
            cursor.execute("INSERT INTO joueurs (nom) VALUES (?)", (nom,))
            conn.commit()
            st.success(f"{nom} inscrit avec succès !")
        except sqlite3.IntegrityError:
            st.warning("Ce joueur est déjà inscrit !")

# Suppression d'un joueur (réservé à l'organisateur avec mot de passe)
st.write("### Supprimer un joueur (Organisateur uniquement)")
joueur_a_supprimer = st.selectbox("Sélectionner un joueur", [""] + [row[0] for row in cursor.execute("SELECT nom FROM joueurs").fetchall()])
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

# Affichage des joueurs inscrits
cursor.execute("SELECT nom FROM joueurs")
joueurs = [row[0] for row in cursor.fetchall()]
st.write("### Joueurs inscrits :")
st.write(joueurs)

# Fermeture de la connexion
conn.close()


#  streamlit run futsal.py
