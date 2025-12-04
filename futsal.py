import streamlit as st
import sqlite3
import pandas as pd
import streamlit.components.v1 as components

# Connexion à la base SQLite
conn = sqlite3.connect("joueurs.db", check_same_thread=False)
cursor = conn.cursor()

# Création de la table si elle n'existe pas
cursor.execute("CREATE TABLE IF NOT EXISTS joueurs (nom TEXT UNIQUE)")
conn.commit()

# Affichage de l'image en bandeau et en arrière-plan
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
        body {
            background: url('https://img.freepik.com/vecteurs-libre/fond-football-abstrait-realiste_52683-67579.jpg') no-repeat center center fixed;
            background-size: cover;         
        }
    </style>
    <div class="title"></div>
""", unsafe_allow_html=True)

st.title("⚽ Les Footix ⚽")
st.title("RDV=20H      KickOff=20h15")


# Vérification du nombre de joueurs inscrits
cursor.execute("SELECT nom FROM joueurs")
joueurs = [row[0] for row in cursor.fetchall()]
nombre_max = 10
places_restantes = nombre_max - len(joueurs)

# Affichage du nombre de places restantes
st.markdown(f"## 🏆 Places : {places_restantes} / {nombre_max}")

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
df = df_joueurs[['#', 'Nom']]
st.dataframe(df.style.set_properties(**{'color': 'blue'}))

# Insérer 10 lignes vides
for _ in range(10):
    st.text("")

st.title("***ARCHIVES***")
st.write("     *****      ")
st.write("**MERCREDI 03/12/25**")
st.write("18    --> Mano, Dodo, Romain, Nico, Guillaume")
st.write("à")
st.write("13    --> Gianni, Alex, Charles, Yann, Adrien")
st.write("La vidéo du match :")
st.write("a charger")
st.write("     *****      ")
st.write("**MERCREDI 26/11/25**")
st.write("XXX Foot annulé XXX  - 4 inscrits")
st.write("Mano, Romain, Dodo, Raphaël")
st.write("     *****      ")
st.write("**MERCREDI 19/11/25**")
st.write("26    --> Mano, Nico, Romain, Yann, Stéphane")
st.write("à")
st.write("16    --> Madjid, Alex, Fabien, Charles, Cyril")
st.write("La vidéo du match :")
st.write("PAS DE VIDEO")
st.write("     *****      ")
st.write("**MERCREDI 12/11/25**")
st.write("18    --> Mano, Dodo, Romain, Charles, Coco")
st.write("à")
st.write("20    --> Madjid, Sylvain, Fabien, Yann, Cyril")
st.write("La vidéo du match :")
st.write("https://drive.google.com/file/d/1v7vyhCAKfQnqoDtWZLNI-5EZvkZfwhFc/view?usp=drive_link")
st.write("     *****      ")
st.write("**MERCREDI 05/11/25**")
st.write("30    --> Mano, Stef, Yann, Charles, Carlos")
st.write("à")
st.write("18    --> Romain, Dodo, Nico, Zak, Alex")
st.write("La vidéo du match :")
st.write("https://drive.google.com/file/d/1j7aeRAz9jBo7EgzVZV0x8yDjF-Z_jxab/view?usp=drive_link")
st.write("     *****      ")
st.write("**MERCREDI 29/10/25**")
st.write("14    --> Zak, Stef, Dodo, Madjid, Guillaume")
st.write("à")
st.write("20    --> Vince, Mano, Nico, Yann, Halim")
st.write("La vidéo du match :")
st.write("https://drive.google.com/file/d/1kiYVeHeHcM9f9APMmckF2wcND8qOtQx8/view?usp=sharing")
st.write("     *****      ")
st.write(" ")


# Affichage de l'adresse
adresse = "8 Rue du Frenelet, 59650 Villeneuve-d'Ascq"
st.markdown(f"### Adresse : {adresse}")

# Affichage de la carte Google Maps via iframe (avec l'adresse exacte)
map_iframe = """
<iframe src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d2520.4335253054123!2d3.1225587763705196!3d50.63979287371289!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x47c329dfdbd2b16b%3A0xd255ea458f438532!2s8%20Rue%20du%20Frenelet%2C%2059650%20Villeneuve-d'Ascq!5e1!3m2!1sfr!2sfr!4v1742461795759!5m2!1sfr!2sfr" width="600" height="450" style="border:0;" allowfullscreen="" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe>
"""

# Affichage de la carte dans Streamlit
components.html(map_iframe, height=500)

# Insérer 3 lignes vides
for _ in range(3):
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






































