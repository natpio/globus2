import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import math
import time

# --- 1. KONFIGURACJA STRONY ---
st.set_page_config(page_title="Geografia dla Dzieci", layout="wide", initial_sidebar_state="expanded")

# --- 2. CSS: JASNY, CZYTELNY, EDUKACYJNY STYL ---
st.markdown("""
<style>
    .stApp {
        background-color: #f4f9f9; /* Bardzo jasny, przyjemny błękit/szarość */
        color: #333333;
    }
    /* Zaokrąglone, przyjazne karty */
    [data-testid="stVerticalBlock"] > [data-testid="stVerticalBlock"] {
        background: white;
        border-radius: 20px;
        padding: 25px;
        border: 2px solid #d1e8e2;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
    }
    h2 { color: #2c3e50; text-align: center; font-weight: bold; margin-bottom: 20px;}
    h3 { color: #e74c3c; font-weight: bold;}
    .stSelectbox label { font-size: 1.1rem; font-weight: bold; color: #2c3e50; }
    
    /* Wygląd lewego panelu */
    [data-testid="stSidebar"] {
        background-color: #ffffff;
        border-right: 2px solid #e0e0e0;
    }
</style>
""", unsafe_allow_html=True)

# --- 3. BAZA DANYCH - KRAJE EUROPY ---
miejsca = {
    "Polska": {"stolica": "Warszawa", "lat": 52.229, "lon": 21.012, "kod": "pl", "opis": "Nasz piękny kraj! Słynie z pierogów, smoka wawelskiego i pięknych gór."},
    "Niemcy": {"stolica": "Berlin", "lat": 52.520, "lon": 13.405, "kod": "de", "opis": "Nasi sąsiedzi. Znani z pysznych precli i pięknych, baśniowych zamków."},
    "Francja": {"stolica": "Paryż", "lat": 48.856, "lon": 2.352, "kod": "fr", "opis": "To tutaj stoi słynna Wieża Eiffla, a ludzie uwielbiają jeść chrupiące bagietki."},
    "Hiszpania": {"stolica": "Madryt", "lat": 40.416, "lon": -3.703, "kod": "es", "opis": "Słoneczny kraj, gdzie zawsze jest ciepło, a w miastach rosną pomarańcze!"},
    "Włochy": {"stolica": "Rzym", "lat": 41.902, "lon": 12.496, "kod": "it", "opis": "Kraj w kształcie buta! Ojczyzna najlepszej pizzy i spaghetti na świecie."},
    "Wielka Brytania": {"stolica": "Londyn", "lat": 51.507, "lon": -0.127, "kod": "gb", "opis": "Kraj, w którym mieszka król. Mają tam słynne, czerwone, piętrowe autobusy."},
    "Grecja": {"stolica": "Ateny", "lat": 37.983, "lon": 23.727, "kod": "gr", "opis": "Bardzo stary kraj pełen wysp i białych domków z niebieskimi dachami."},
    "Szwecja": {"stolica": "Sztokholm", "lat": 59.329, "lon": 18.068, "kod": "se", "opis": "Zimny kraj na północy, skąd pochodzi Pippi Pończoszanka i klocki LEGO (blisko, bo z Danii!)."},
    "Norwegia": {"stolica": "Oslo", "lat": 59.913, "lon": 10.752, "kod": "no", "opis": "Kraj wikingów, gdzie można zobaczyć zorzę polarną na niebie!"},
    "Finlandia": {"stolica": "Helsinki", "lat": 60.169, "lon": 24.938, "kod": "fi", "opis": "To tutaj, w krainie zwanej Laponią, mieszka prawdziwy Święty Mikołaj."},
    "Portugalia": {"stolica": "Lizbona", "lat": 38.722, "lon": -9.139, "kod": "pt", "opis": "Leży nad samym oceanem, stąd w dawnych czasach wypływali najwięksi odkrywcy."},
    "Czechy": {"stolica": "Praga", "lat": 50.075, "lon": 14.437, "kod": "cz", "opis": "Kraj słynący z Krecika i pięknej stolicy pełnej mostów."},
    "Austria": {"stolica": "Wiedeń", "lat": 48.208, "lon": 16.373, "kod": "at", "opis": "Kraj pięknych Alp, gdzie zimą wszyscy jeżdżą na nartach."},
    "Szwajcaria": {"stolica": "Berno", "lat": 46.948, "lon": 7.447, "kod": "ch", "opis": "Słynie z produkcji najpyszniejszej mlecznej czekolady i dokładnych zegarków."},
    "Holandia": {"stolica": "Amsterdam", "lat": 52.367, "lon": 4.904, "kod": "nl", "opis": "Kraj wiatraków, serów i milionów rowerów, którymi jeżdżą prawie wszyscy!"},
    "Belgia": {"stolica": "Bruksela", "lat": 50.850, "lon": 4.351, "kod": "be", "opis": "Ojczyzna pysznych, gorących gofrów oraz słynnych komiksów o Smerfach."},
    "Irlandia": {"stolica": "Dublin", "lat": 53.349, "lon": -6.260, "kod": "ie", "opis": "Zielona wyspa, której symbolem jest koniczynka i małe skrzaty - Leprechauny."},
    "Dania": {"stolica": "Kopenhaga", "lat": 55.676, "lon": 12.568, "kod": "dk", "opis": "Prawdziwa ojczyzna klocków LEGO! Mają tam ogromny park rozrywki Legoland."},
    "Chorwacja": {"stolica": "Zagrzeb", "lat": 45.815, "lon": 15.981, "kod": "hr", "opis": "Kraj nad ciepłym morzem, w którym plaże są kamieniste, a woda przejrzysta jak szkło."},
    "Węgry": {"stolica": "Budapeszt", "lat": 47.497, "lon": 19.040, "kod": "hu", "opis": "Znani z pysznych dań doprawianych czerwoną papryką oraz basenów z gorącą wodą."},
    "Rumunia": {"stolica": "Bukareszt", "lat": 44.426, "lon": 26.102, "kod": "ro", "opis": "Tutaj, w krainie zwanej Transylwanią, znajduje się mroczny zamek hrabiego Draculi."},
    "Słowacja": {"stolica": "Bratysława", "lat": 48.148, "lon": 17.107, "kod": "sk", "opis": "Mają wspaniałe góry Tatry (te same co my!) oraz mnóstwo starych zamków."},
    "Ukraina": {"stolica": "Kijów", "lat": 50.450, "lon": 30.523, "kod": "ua", "opis": "Nasz duży sąsiad, w którym znajdują się złote pola pszenicy i rosną piękne słoneczniki."},
    "Litwa": {"stolica": "Wilno", "lat": 54.687, "lon": 25.279, "kod": "lt", "opis": "Kraj naszych wschodnich sąsiadów, z którym kiedyś tworzyliśmy jedno wielkie państwo."},
    "Łotwa": {"stolica": "Ryga", "lat": 56.949, "lon": 24.105, "kod": "lv", "opis": "Leży nad zimnym Morzem Bałtyckim i słynie z gęstych, zielonych lasów."},
    "Estonia": {"stolica": "Tallinn", "lat": 59.437, "lon": 24.753, "kod": "ee", "opis": "Najbardziej nowoczesny kraj na wschodzie Europy, gdzie mnóstwo rzeczy robi się przez internet!"}
}

# --- 4. FUNKCJE POMOCNICZE ---
def oblicz_dystans(lat1, lon1, lat2, lon2):
    R = 6371
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat/2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    return int(R * c)

# Funkcja rysująca globus - oddzielona, aby móc ją wywoływać podczas animacji
def rysuj_globus(start_kraj, cel_kraj, samolot_lat, samolot_lon):
    fig = go.Figure()

    lat1, lon1 = miejsca[start_kraj]["lat"], miejsca[start_kraj]["lon"]
    lat2, lon2 = miejsca[cel_kraj]["lat"], miejsca[cel_kraj]["lon"]

    # --- USTAWIENIA KULI ZIEMSKIEJ (DLA DZIECI) ---
    fig.update_geos(
        projection_type="orthographic",
        showcoastlines=True, coastlinecolor="black",
        showland=True, landcolor="#8de084",      # Jasna, ciepła zieleń
        showocean=True, oceancolor="#a8d5e2",    # Błękitny ocean
        showcountries=True, countrycolor="black", # WYRAŹNE granice państw!
        countrywidth=1.5,
        resolution=50,
        center=dict(lat=(lat1+lat2)/2, lon=(lon1+lon2)/2), # Środek kamery na Europie
        showframe=False
    )

    # 1. Rysowanie czerwonych punktów dla państw
    lats = [d["lat"] for d in miejsca.values()]
    lons = [d["lon"] for d in miejsca.values()]
    names = list(miejsca.keys())

    fig.add_trace(go.Scattergeo(
        lon=lons, lat=lats, text=names, hoverinfo='text', mode='markers',
        marker=dict(size=8, color='red', line=dict(width=1, color='white')),
        name="Kraje"
    ))

    # 2. Rysowanie przerywanej linii trasy (zawsze widoczna)
    if start_kraj != cel_kraj:
        fig.add_trace(go.Scattergeo(
            lon=[lon1, lon2], lat=[lat1, lat2], mode='lines',
            line=dict(width=3, color='#e74c3c', dash='dot'),
            name='Trasa'
        ))

    # 3. Rysowanie RUCHOMEGO SAMOLOTU
    fig.add_trace(go.Scattergeo(
        lon=[samolot_lon], lat=[samolot_lat], text=["✈️"], mode='text',
        textfont=dict(size=35), hoverinfo='none', name="Samolot"
    ))

    # 4. Bezpieczne marginesy - zapobiegają ucinaniu dołu mapy!
    fig.update_layout(
        margin=dict(l=40, r=40, t=40, b=40),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        geo=dict(bgcolor='rgba(0,0,0,0)'),
        showlegend=False,
    )
    return fig

# --- 5. PANEL BOCZNY ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/854/854894.png", width=100) # Ikonka globusa
    st.markdown("<h2>✈️ Plan Lotu</h2>", unsafe_allow_html=True)
    
    lista_krajow = sorted(list(miejsca.keys()))
    
    start = st.selectbox("🛫 Skąd lecimy?", lista_krajow, index=lista_krajow.index("Polska"))
    cel = st.selectbox("🛬 Dokąd lecimy?", lista_krajow, index=lista_krajow.index("Francja"))
    
    st.markdown("---")
    dystans = oblicz_dystans(miejsca[start]["lat"], miejsca[start]["lon"], miejsca[cel]["lat"], miejsca[cel]["lon"])
    
    st.info(f"📍 **Odległość:** {dystans} km")
    
    # Przycisk startu lotu
    start_lotu = st.button("🚀 Wystartuj samolot!", use_container_width=True)

# --- 6. EKRAN GŁÓWNY ---
st.markdown("## 🌍 Odkrywamy Europę!")

col_map, col_card = st.columns([2.5, 1.5]) 

# Współrzędne startowe i końcowe
lat1, lon1 = miejsca[start]["lat"], miejsca[start]["lon"]
lat2, lon2 = miejsca[cel]["lat"], miejsca[cel]["lon"]

with col_map:
    # Używamy st.empty(), aby stworzyć ramkę, w której będziemy podmieniać klatki animacji
    mapa_placeholder = st.empty()

    if start_lotu and start != cel:
        # LOGIKA ANIMACJI LOTU
        liczba_klatek = 15
        for klatka in range(liczba_klatek + 1):
            # Obliczanie aktualnej pozycji samolotu w danej klatce (interpolacja)
            obecny_lat = lat1 + (lat2 - lat1) * (klatka / liczba_klatek)
            obecny_lon = lon1 + (lon2 - lon1) * (klatka / liczba_klatek)
            
            # Rysowanie nowej mapy
            fig = rysuj_globus(start, cel, obecny_lat, obecny_lon)
            
            # Podmiana mapy w interfejsie
            mapa_placeholder.plotly_chart(fig, use_container_width=True, height=600, config={'displayModeBar': False})
            
            # Krótka pauza przed narysowaniem kolejnej klatki
            time.sleep(0.05)
            
        st.balloons() # Nagroda po wylądowaniu
    else:
        # Stan domyślny (samolot stoi na starcie)
        fig = rysuj_globus(start, cel, lat1, lon1)
        mapa_placeholder.plotly_chart(fig, use_container_width=True, height=600, config={'displayModeBar': False})

# --- KARTA EDUKACYJNA KRAJU ---
with col_card:
    st.markdown(f"### Cel: {cel}")
    with st.container():
        kod_flagi = miejsca[cel]["kod"]
        st.markdown(
            f'<img src="https://flagpedia.net/data/flags/w580/{kod_flagi}.png" style="border-radius: 10px; width: 100%; border: 1px solid #ddd; margin-bottom: 15px;">',
            unsafe_allow_html=True
        )
        st.markdown(f"**🏛️ Stolica:** {miejsca[cel]['stolica']}")
        st.markdown("---")
        st.markdown(f"**🧐 Czy wiesz, że...**")
        st.success(miejsca[cel]["opis"])
