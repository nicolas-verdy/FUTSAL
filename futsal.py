import streamlit as st
import pandas as pd  # Pour afficher les joueurs en tableau


# Affichage de l'image en bandeau sans titre
st.markdown("""
    <style>
        .bandeau {
            background-image: url('https://laurafoot.fff.fr/wp-content/uploads/sites/10/2021/01/Bandeau_SiteWeb-Futsal.png');
            background-size: cover;
            background-position: center;
            height: 200px;  /* Ajuste la hauteur du bandeau */
            border-radius: 10px;
        }
    </style>
    <div class="bandeau"></div>
""", unsafe_allow_html=True)

# Configuration de la session
st.title("⚽ Les Footix du Mercredi - Inscription Futsal 20h15")

# Initialisation des joueurs inscrits
if "joueurs" not in st.session_state:
    st.session_state.joueurs = []

# Définition du nombre maximum de joueurs
MAX_JOUEURS = 10

# Formulaire d'inscription
st.subheader("📝 Inscris-toi pour mercredi soir !")
nom = st.text_input("Ton nom", key="nom")

if st.button("S'inscrire"):
    if nom:
        if nom in st.session_state.joueurs:
            st.warning("❌ Tu es déjà inscrit !")
        elif len(st.session_state.joueurs) >= MAX_JOUEURS:
            st.error("⚠️ La session est complète !")
        else:
            st.session_state.joueurs.append(nom)
            st.success(f"✅ {nom}, tu es inscrit !")
    else:
        st.warning("⚠️ Merci d'entrer un nom.")

# Affichage des joueurs inscrits sous forme de tableau
st.subheader("👥 Joueurs inscrits")
if st.session_state.joueurs:
    df_joueurs = pd.DataFrame({"Joueurs": st.session_state.joueurs})
    st.table(df_joueurs)
    st.write(f"📊 **Total inscrits : {len(st.session_state.joueurs)} / {MAX_JOUEURS}**")
else:
    st.info("Aucun joueur inscrit pour le moment.")

# Génération du lien WhatsApp personnalisé
lien = "https://les-footix-du-mercredi.streamlit.app"
whatsapp_message = f"Les Footix du Mercredi - Futsal 20h15 ! Inscris-toi ici : {lien}"
whatsapp_link = f"https://api.whatsapp.com/send?text={whatsapp_message}"

st.markdown(f"[📲 Partager sur WhatsApp]({whatsapp_link})", unsafe_allow_html=True)

# 🔒 Gestion organisateur (Seul toi peux désinscrire quelqu'un)
st.subheader("🔒 Gestion des inscriptions (organisateur uniquement)")
mdp_admin = st.text_input("Mot de passe organisateur", type="password")

if mdp_admin == "Jules2014":  # Remplace "footix2024" par ton propre mot de passe
    st.success("👑 Bienvenue, organisateur ! Voici ton tableau de bord.")  
    st.write("🔧 Actions disponibles :")
    
    # Affichage de la liste des joueurs sous forme de tableau interactif
    if st.session_state.joueurs:
        st.table(df_joueurs)

        # Suppression d'un joueur spécifique (seul l'admin peut le faire)
        nom_remove = st.selectbox("Sélectionne un joueur à supprimer", [""] + st.session_state.joueurs)
        if st.button("❌ Supprimer un joueur") and nom_remove:
            st.session_state.joueurs.remove(nom_remove)
            st.success(f"✅ {nom_remove} a été supprimé !")
    
    # Bouton de réinitialisation
    if st.button("🔄 Réinitialiser la session"):
        st.session_state.joueurs = []
        st.success("✅ Session réinitialisée !")
else:
    st.warning("⚠️ Mot de passe requis pour gérer les inscriptions.")


#  streamlit run futsal.py
