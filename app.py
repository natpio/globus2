import streamlit as st
import plotly.express as px
import pandas as pd

# --- 1. KONFIGURACJA STRONY ---
st.set_page_config(page_title="Geografia dla Dzieci", layout="wide", initial_sidebar_state="expanded")

# --- 2. CSS: JASNY, CZYTELNY STYL ---
st.markdown("""
<style>
    .stApp {
        background-color: #f4f9f9;
        color: #333333;
    }
    /* Zaokrąglona, przyjazna karta po prawej stronie */
    [data-testid="stVerticalBlock"] > [data-testid="stVerticalBlock"] {
        background: white;
        border-radius: 20px;
        padding: 25px;
        border: 2px solid #d1e8e2;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
    }
    h2 { color: #2c3e50; text-align: center; font-weight: bold; margin-bottom: 20px;}
    h3 { color: #e74c3c; font-weight: bold;}
    
    /* Wygląd lewego panelu */
    [data-testid="stSidebar"] {
        background-color: #ffffff;
        border-right: 2px solid #e0e0e0;
    }
</style>
""", unsafe_allow_html=True)

# --- 3. BAZA DANYCH (Teraz z kodami ISO-3 do rysowania kształtów państw) ---
baza = [
    {"Kraj": "Polska", "Stolica": "Warszawa", "ISO3": "POL", "ISO2": "pl", "Opis": "Nasz piękny kraj! Słynie z pierogów, smoka wawelskiego i pięknych gór."},
    {"Kraj": "Niemcy", "Stolica": "Berlin", "ISO3": "DEU", "ISO2": "de", "Opis": "Nasi sąsiedzi. Znani z pysznych precli i pięknych, baśniowych zamków."},
    {"Kraj": "Francja", "Stolica": "Paryż", "ISO3": "FRA", "ISO2": "fr", "Opis": "To tutaj stoi słynna Wieża Eiffla, a ludzie uwielbiają jeść chrupiące bagietki."},
    {"Kraj": "Hiszpania", "Stolica": "Madryt", "ISO3": "ESP", "ISO2": "es", "Opis": "Słoneczny kraj, gdzie zawsze jest ciepło, a w miastach rosną pomarańcze!"},
    {"Kraj": "Włochy", "Stolica": "Rzym", "ISO3": "ITA", "ISO2": "it", "Opis": "Kraj w kształcie buta! Ojczyzna najlepszej pizzy i spaghetti na świecie."},
    {"Kraj": "Wielka Brytania", "Stolica": "Londyn", "ISO3": "GBR", "ISO2": "gb", "Opis": "Kraj, w którym mieszka król. Mają tam słynne, czerwone, piętrowe autobusy."},
    {"Kraj": "Grecja", "Stolica": "Ateny", "ISO3": "GRC", "ISO2": "gr", "Opis": "Bardzo stary kraj pełen wysp i białych domków z niebieskimi dachami."},
    {"Kraj": "Szwecja", "Stolica": "Sztokholm", "ISO3": "SWE", "ISO2": "se", "Opis": "Zimny kraj na północy, skąd pochodzi Pippi Pończoszanka."},
    {"Kraj": "Norwegia", "Stolica": "Oslo", "ISO3": "NOR", "ISO2": "no", "Opis": "Kraj wikingów, gdzie można zobaczyć zorzę polarną na niebie!"},
    {"Kraj": "Finlandia", "Stolica": "FIN", "ISO3": "FIN", "ISO2": "fi", "Opis": "To tutaj, w krainie zwanej Laponią, mieszka prawdziwy Święty Mikołaj."},
    {"Kraj": "Portugalia", "Stolica": "Lizbona", "ISO3": "PRT", "ISO2": "pt", "Opis": "Leży nad samym oceanem, stąd w dawnych czasach wypływali najwięksi odkrywcy."},
    {"Kraj": "Czechy", "Stolica": "Praga", "ISO3": "CZE", "ISO2": "cz", "Opis": "Kraj słynący z Krecika i pięknej stolicy pełnej mostów."},
    {"Kraj": "Austria", "Stolica": "Wiedeń", "ISO3": "AUT", "ISO2": "at", "Opis": "Kraj pięknych Alp, gdzie zimą wszyscy jeżdżą na nartach."},
    {"Kraj": "Szwajcaria", "Stolica": "Berno", "ISO3": "CHE", "ISO2": "ch", "Opis": "Słynie z produkcji najpyszniejszej mlecznej czekolady i dokładnych zegarków."},
    {"Kraj": "Holandia", "Stolica": "Amsterdam", "ISO3": "NLD", "ISO2": "nl", "Opis": "Kraj wiatraków, serów i milionów rowerów, którymi jeżdżą prawie wszyscy!"},
    {"Kraj": "Belgia", "Stolica": "Bruksela", "ISO3": "BEL", "ISO2": "be", "Opis": "Ojczyzna pysznych, gorących gofrów oraz słynnych komiksów o Smerfach."},
    {"Kraj": "Irlandia", "Stolica": "Dublin", "ISO3": "IRL", "ISO2": "ie", "Opis": "Zielona wyspa, której symbolem jest koniczynka i małe skrzaty - Leprechauny."},
    {"Kraj": "Dania", "Stolica": "Kopenhaga", "ISO3": "DNK", "ISO2": "dk", "Opis": "Prawdziwa ojczyzna klocków LEGO! Mają tam ogromny park rozrywki Legoland."},
    {"Kraj": "Chorwacja", "Stolica": "Zagrzeb", "ISO3": "HRV", "ISO2": "hr", "Opis": "Kraj nad ciepłym morzem, w którym plaże są kamieniste, a woda przejrzysta jak szkło."},
    {"Kraj": "Węgry", "Stolica": "Budapeszt", "ISO3": "HUN", "ISO2": "hu", "Opis": "Znani z pysznych dań doprawianych czerwoną papryką oraz basenów z gorącą wodą."},
    {"Kraj": "Rumunia", "Stolica": "Bukareszt", "ISO3": "ROU", "ISO2": "ro", "Opis": "Tutaj, w krainie zwanej Transylwanią, znajduje się mroczny zamek hrabiego Draculi."},
    {"Kraj": "Słowacja", "Stolica": "Bratysława", "ISO3": "SVK", "ISO2": "sk", "Opis": "Mają wspaniałe góry Tatry (te same co my!) oraz mnóstwo starych zamków."},
    {"Kraj": "Ukraina", "Stolica": "Kijów", "ISO3": "UKR", "ISO2": "ua", "Opis": "Nasz duży sąsiad, w którym znajdują się złote pola pszenicy i rosną piękne słoneczniki."},
    {"Kraj": "Litwa", "Stolica": "Wilno", "ISO3": "LTU", "ISO2": "lt", "Opis": "Kraj naszych wschodnich sąsiadów, z którym kiedyś tworzyliśmy jedno wielkie państwo."},
    {"Kraj": "Łotwa", "Stolica": "Ryga", "ISO3": "LVA", "ISO2": "lv", "Opis": "Leży nad zimnym Morzem Bałtyckim i słynie z gęstych, zielonych lasów."},
    {"Kraj": "Estonia", "Stolica": "Tallinn", "ISO3": "EST", "ISO2": "ee", "Opis": "Najbardziej nowoczesny kraj na wschodzie Europy, gdzie mnóstwo rzeczy robi się przez internet!"}
]

df = pd.DataFrame(baza)

# --- 4. ZARZĄDZANIE STANEM (Pamięć wybranego kraju) ---
if "wybrany_kraj" not in st.session_state:
    st.session_state.wybrany_kraj = "Polska"

# --- 5. PANEL BOCZNY ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/854/854894.png", width=100)
    st.markdown("<h2>🌍 Odkrywca</h2>", unsafe_allow_html=True)
    st.info("Obracaj globusem i **klikaj w kolorowe państwa**, aby poznać ich sekrety!")
    
    # Alternatywny wybór z listy - synchronizuje się z mapą
    lista_krajow = sorted(df["Kraj"].tolist())
    wybor_z_listy = st.selectbox("Możesz też wybrać z listy:", lista_krajow, index=lista_krajow.index(st.session_state.wybrany_kraj))
    
    if wybor_z_listy != st.session_state.wybrany_kraj:
        st.session_state.wybrany_kraj = wybor_z_listy
        st.rerun()

# --- 6. EKRAN GŁÓWNY ---
st.markdown("## 🌍 Kolorowa Mapa Europy")

col_map, col_card = st.columns([2.5, 1.5]) 

with col_map:
    # Używamy Choropleth (mapa obszarowa), aby całe państwa były klikalne
    fig = px.choropleth(
        df,
        locations="ISO3",       # Klucz łączący z mapą Plotly
        color="Kraj",           # Każdy kraj będzie miał swój kolor z palety
        hover_name="Kraj",
        hover_data={"ISO3": False, "Kraj": False}, # Ukrywamy kody w dymku
        color_discrete_sequence=px.colors.qualitative.Pastel # Pastelowa, dziecięca paleta barw!
    )

    # Ustawienia globusa edukacyjnego
    fig.update_geos(
        projection=dict(
            type="orthographic",
            rotation=dict(lon=15, lat=50, roll=0) # Ustawia środek kuli domyślnie na Europę
        ),
        showcoastlines=True, coastlinecolor="#bdc3c7",
        showland=True, landcolor="#ecf0f1",      # Szare tło dla państw, których nie ma w bazie
        showocean=True, oceancolor="#ddf1f8",    # Jasnoniebieski ocean
        showcountries=True, countrycolor="#bdc3c7",
        resolution=50,
        showframe=False
    )

    fig.update_layout(
        margin=dict(l=0, r=0, t=0, b=0),
        paper_bgcolor='rgba(0,0,0,0)',
        geo=dict(bgcolor='rgba(0,0,0,0)'),
        showlegend=False, # Wyłączamy ogromną legendę z prawej strony
    )

    # Rysujemy mapę i ZBIERAMY DANE O KLIKNIĘCIU
    event_data = st.plotly_chart(fig, use_container_width=True, height=600, on_select="rerun")
    
    # Obsługa kliknięcia przez dziecko w kształt na mapie
    if event_data and len(event_data.get("selection", {}).get("points", [])) > 0:
        # Odczytujemy ISO3 klikniętego państwa
        klikniete_iso = event_data["selection"]["points"][0].get("location")
        
        # Jeśli kliknięto w państwo z naszej bazy
        if klikniete_iso in df["ISO3"].values:
            klikniety_kraj = df[df["ISO3"] == klikniete_iso].iloc[0]["Kraj"]
            
            # Jeśli to nowy kraj, aktualizujemy i odświeżamy kartę
            if st.session_state.wybrany_kraj != klikniety_kraj:
                st.session_state.wybrany_kraj = klikniety_kraj
                st.rerun()

# --- 7. KARTA EDUKACYJNA KRAJU ---
with col_card:
    # Wyciągamy dane z DataFrame dla wybranego kraju
    dane_kraju = df[df["Kraj"] == st.session_state.wybrany_kraj].iloc[0]
    
    st.markdown(f"### 📍 {dane_kraju['Kraj']}")
    with st.container():
        # Pobieranie flagi na podstawie kodu ISO2
        st.markdown(
            f'<img src="https://flagpedia.net/data/flags/w580/{dane_kraju["ISO2"]}.png" style="border-radius: 10px; width: 100%; border: 1px solid #ddd; margin-bottom: 15px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">',
            unsafe_allow_html=True
        )
        st.markdown(f"**🏛️ Stolica:** {dane_kraju['Stolica']}")
        st.markdown("---")
        st.markdown(f"**🧐 Ciekawostka:**")
        st.success(dane_kraju['Opis'])
