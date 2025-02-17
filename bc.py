import streamlit as st
import pandas as pd
from bs4 import BeautifulSoup
import requests
import base64

# ---- Configuration de la page ----
st.set_page_config(page_title="Scraper Mode", layout="wide")

st.markdown("<h1 style='text-align: center; color: black;'>SCRAPER MODE - COINAFRIQUE</h1>", unsafe_allow_html=True)

st.write("""
Ce programme scrape les vêtements et chaussures pour hommes sur **Coinafrique** et permet de **télécharger les données**.
""")

# ---- FONCTIONS POUR LE SCRAPING ----
def scrap_vetements(nb_pages):
    """Scrape les vêtements pour hommes."""
    data = []
    for page in range(1, nb_pages + 1):
        url = f'https://sn.coinafrique.com/categorie/vetements-homme?page={page}'
        response = requests.get(url)
        if response.status_code != 200:
            continue  

        soup = BeautifulSoup(response.text, 'html.parser')
        containers = soup.find_all('div', class_='col s6 m4 l3')

        for container in containers:
            try:
                prix = container.find('p', class_='ad__card-price').text.strip().replace("F CFA", "").replace("\u202f", "")
                prix = int(prix)  # Conversion en entier
                type_habit = container.find('p', class_='ad__card-description').text.strip()
                img_link = 'https://sn.coinafrique.com/categorie/vetements-homme' + container.find('img', class_='ad__card-img')['src']

                data.append({
                    'Prix': prix,
                    'Type de vêtement': type_habit,
                    'Image': img_link
                })
            except:
                pass  

    return pd.DataFrame(data)

def scrap_chaussures(nb_pages):
    """Scrape les chaussures pour hommes."""
    data = []
    for page in range(1, nb_pages + 1):
        url = f'https://sn.coinafrique.com/categorie/chaussures-homme?page={page}'
        response = requests.get(url)
        if response.status_code != 200:
            continue  

        soup = BeautifulSoup(response.text, 'html.parser')
        containers = soup.find_all('div', class_='col s6 m4 l3')

        for container in containers:
            try:
                prix = container.find('p', class_='ad__card-price').text.strip().replace("F CFA", "").replace("\u202f", "")
                prix = int(prix)  # Conversion en entier
                type_chaussure = container.find('p', class_='ad__card-description').text.strip()
                img_link = 'https://sn.coinafrique.com/categorie/chaussures-homme' + container.find('img', class_='ad__card-img')['src']

                data.append({
                    'Prix': prix,
                    'Type de chaussure': type_chaussure,
                    'Image': img_link
                })
            except:
                pass  

    return pd.DataFrame(data)

# ---- INTERFACE UTILISATEUR STREAMLIT ----
st.sidebar.header("🔍 Paramètres de Scraping")
nb_pages = st.sidebar.slider("Nombre de pages à scraper", min_value=1, max_value=50, value=5)
categorie = st.sidebar.selectbox("Choisissez la catégorie", ["Vêtements Homme", "Chaussures Homme"])

if st.sidebar.button("Scraper les données"):
    st.write("### 📦 Résultats du Scraping")

    if categorie == "Vêtements Homme":
        df = scrap_vetements(nb_pages)
        st.write(f"**{len(df)} articles trouvés** pour **{nb_pages} pages**.")
    else:
        df = scrap_chaussures(nb_pages)
        st.write(f"**{len(df)} articles trouvés** pour **{nb_pages} pages**.")

    st.dataframe(df)

    # Fonction pour convertir en CSV
    def convert_df(df):
        return df.to_csv(index=False).encode('utf-8')

    csv = convert_df(df)

    st.download_button(
        label="📥 Télécharger les données en CSV",
        data=csv,
        file_name="scraping_coinafrique.csv",
        mime="text/csv"
    )

st.write("💡 **Utilisez la barre latérale pour choisir le nombre de pages et la catégorie à scraper.**")
