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

# Joueurs affichés par défaut au démarrage
joueurs_defaut = [
    
]

# Initialisation automatique si la table est vide
cursor.execute("SELECT COUNT(*) FROM joueurs")
nb_joueurs = cursor.fetchone()[0]

if nb_joueurs == 0:
    cursor.executemany(
        "INSERT OR IGNORE INTO joueurs (nom) VALUES (?)",
        [(joueur,) for joueur in joueurs_defaut]
    )
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

st.title("⚽ Les Footix du Mercredi")
st.write("RDV = 20H      KickOff = 20H15")

st.balloons()

st.subheader("😭⚽💔 C'est la dernière à Futsal Frenelet 💔⚽😭")
st.subheader("😢❤️ Venez soutenir notre Juju ❤️😢")
st.subheader("🍖🔥 et profiter du Barbecue d'Adieu 🔥🍖")

# Lecture des joueurs
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
                cursor.execute(
                    "INSERT INTO joueurs (nom) VALUES (?)",
                    (nom,)
                )
                conn.commit()
                st.success(f"{nom} inscrit avec succès !")
                st.rerun()
            except sqlite3.IntegrityError:
                st.warning("Ce joueur est déjà inscrit !")
        else:
            st.error("Trop tard ! Prochaine fois, tu iras plus vite !")

# Relecture des joueurs après éventuelle inscription
cursor.execute("SELECT nom FROM joueurs")
joueurs = [row[0] for row in cursor.fetchall()]

# Affichage des joueurs inscrits
st.markdown(
    "<div class='blue-title'>Joueurs inscrits :</div>",
    unsafe_allow_html=True
)

df_joueurs = pd.DataFrame({
    '#': range(1, len(joueurs) + 1),
    'Nom': joueurs
})

st.dataframe(
    df_joueurs.style.set_properties(**{'color': 'blue'}),
    use_container_width=True
)

# Adresse
adresse = "8 Rue du Frenelet, 59650 Villeneuve-d'Ascq"
st.markdown(f"### Adresse : {adresse}")

# Carte Google Maps
map_iframe = """
<iframe src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d2520.4335253054123!2d3.1225587763705196!3d50.63979287371289!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x47c329dfdbd2b16b%3A0xd255ea458f438532!2s8%20Rue%20du%20Frenelet%2C%2059650%20Villeneuve-d'Ascq!5e1!3m2!1sfr!2sfr!4v1742461795759!5m2!1sfr!2sfr"
width="600"
height="450"
style="border:0;"
allowfullscreen=""
loading="lazy"
referrerpolicy="no-referrer-when-downgrade">
</iframe>
"""

components.html(map_iframe, height=500)

# Espacement
for _ in range(10):
    st.text("")

# Suppression d'un joueur
st.write("### Supprimer un joueur (Organisateur uniquement)")

joueur_a_supprimer = st.selectbox(
    "Sélectionner un joueur",
    [""] + joueurs
)

password = st.text_input(
    "Mot de passe",
    type="password"
)

if st.button("Supprimer"):
    if password == "Jules2014" and joueur_a_supprimer:
        cursor.execute(
            "DELETE FROM joueurs WHERE nom = ?",
            (joueur_a_supprimer,)
        )
        conn.commit()
        st.success(f"{joueur_a_supprimer} a été supprimé !")
        st.rerun()
    elif password != "Jules2014":
        st.error("Mot de passe incorrect")

# Réinitialisation complète
st.write("### Réinitialisation administrateur")

password_reset = st.text_input(
    "Mot de passe pour réinitialiser",
    type="password"
)

if st.button("Réinitialiser la session"):
    if password_reset == "Jules2014":
        cursor.execute("DELETE FROM joueurs")
        conn.commit()
        st.success(
            "Session réinitialisée : les 10 places sont maintenant disponibles."
        )
        st.rerun()
    else:
        st.error("Mot de passe incorrect")

st.markdown(
    """
    🎁 **Accéder aux avantages du CSE :**

    👉 [Cliquez ici pour vous connecter au CSE](https://www.csearssup.fr/com/login?back_url=%2Fcom%2Fhomepage)
    """
)

# Fermeture de la connexion
conn.close()

# Lancement :
# streamlit run futsal.py
