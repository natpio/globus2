import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import math

# --- KONFIGURACJA STRONY (Przyjazny styl domowy) ---
st.set_page_config(page_title="Rodzinny Globus", layout="wide", initial_sidebar_state="expanded")

# --- CSS: Jasny, radosny motyw dla dzieci ---
st.markdown("""
<style>
    /* Zaokrąglone, kolorowe panele */
    [data-testid="stVerticalBlock"] > [data-testid="stVerticalBlock"] {
        border-radius: 25px;
        background: linear-gradient(135deg, #fdfbfb 0%, #ebedee 100%);
        padding: 25px;
        border: 3px solid #a8d5e2;
        box-shadow: 0 8px 15px rgba(0, 0, 0, 0.1);
        color: #333;
    }
    /* Powiększenie i pokolorowanie tekstów */
    .stMarkdown h3 { color: #ff6b6b; font-weight: bold; }
    .stMarkdown p { font-size: 1.1rem; }
</style>
""", unsafe_allow_html=True)

# --- BAZA DANYCH MIEJSC ---
# Miejsca dobrane tak, by łączyły europejskie kierunki z wielką amerykańską wyprawą
miejsca = {
    "Polska (Poznań)": {"lat": 52.406, "lon": 16.925, "kod": "pl", "opis": "Nasz dom! Stąd zaczyna się każda wielka przygoda."},
    "USA (Chicago)": {"lat": 41.878, "lon": -87.629, "kod": "us", "opis": "Pierwszego lipca zaczynamy tu naszą wielką, rodzinną wyprawę!"},
    "Hiszpania (Barcelona)": {"lat": 41.387, "lon": 2.168, "kod": "es", "opis": "Słoneczne miasto z pięknymi budowlami (i świetne miejsce na sprzęt targowy)."},
    "Portugalia (Lizbona)": {"lat": 38.722, "lon": -9.139, "kod": "pt", "opis": "Kraj wielkich odkrywców geograficznych nad samym oceanem."},
    "Niemcy (Lipsk)": {"lat": 51.339, "lon": 12.373, "kod": "de", "opis": "Nasi sąsiedzi. Jeżdżą tu ciężarówki z ważnymi konstrukcjami."},
    "Rumunia (Bukareszt)": {"lat": 44.426, "lon": 26.102, "kod": "ro", "opis": "Stolica kraju słynącego z legend o wampirze Drakuli!"}
}

# --- FUNKCJA MATEMATYCZNA: Odległość między punktami na kuli ---
def oblicz_dystans(lat1, lon1, lat2, lon2):
    R = 6371  # Promień Ziemi w km
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat/2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    return int(R * c)

# --- INTERFEJS BOCZNY: Planowanie lotu ---
with st.sidebar:
    st.title("✈️ Centrum Lotów")
    st.markdown("Wybierzcie trasę dla naszego samolotu!")
    
    lista_miast = list(miejsca.keys())
    
    start = st.selectbox("🛫 Skąd lecimy?", lista_miast, index=0) # Domyślnie Polska
    cel = st.selectbox("🛬 Dokąd lecimy?", lista_miast, index=1)   # Domyślnie Chicago
    
    st.markdown("---")
    if start != cel:
        dystans = oblicz_dystans(miejsca[start]["lat"], miejsca[start]["lon"], miejsca[cel]["lat"], miejsca[cel]["lon"])
        st.success(f"**Odległość:** {dystans} kilometrów")
        if st.button("🚀 Wystartuj samolot!"):
            st.balloons()
    else:
        st.warning("Wybierz dwa różne miejsca, żeby wytyczyć trasę lotu.")

# --- GŁÓWNY EKRAN ---
st.title("🌍 Odkrywca Świata Laury i Zosi")

col_map, col_card = st.columns([2, 1])

# Pobranie współrzędnych do narysowania trasy
lat1, lon1 = miejsca[start]["lat"], miejsca[start]["lon"]
lat2, lon2 = miejsca[cel]["lat"], miejsca[cel]["lon"]

with col_map:
    # --- RYSOWANIE GLOBUSA (Używamy Graph Objects dla pełnej kontroli) ---
    fig = go.Figure()

    # 1. Dodajemy wszystkie punkty miast na mapę
    lats = [d["lat"] for d in miejsca.values()]
    lons = [d["lon"] for d in miejsca.values()]
    names = list(miejsca.keys())

    fig.add_trace(go.Scattergeo(
        lon=lons,
        lat=lats,
        text=names,
        hoverinfo='text',
        mode='markers',
        marker=dict(size=14, color='#ff6b6b', line=dict(width=2, color='white')),
        name="Miejsca"
    ))

    # 2. Rysujemy RZECZYWISTĄ trasę lotu (Ortodroma)
    if start != cel:
        fig.add_trace(go.Scattergeo(
            lon=[lon1, lon2],
            lat=[lat1, lat2],
            mode='lines',
            line=dict(width=4, color='#4facfe', dash='dashdot'),
            name='Trasa'
        ))
        # Dodajemy ikonkę samolotu w miejscu docelowym
        fig.add_trace(go.Scattergeo(
            lon=[lon2],
            lat=[lat2],
            text=["✈️"],
            mode='text',
            textfont=dict(size=40),
            hoverinfo='none',
            name="Samolot"
        ))

    # Jasna, radosna kolorystyka Ziemi
    fig.update_geos(
        projection_type="orthographic",
        showcoastlines=True, coastlinecolor="#ffffff",
        showland=True, landcolor="#f1f7ed", # Jasna, ciepła zieleń
        showocean=True, oceancolor="#a8d5e2", # Przyjazny, jasny błękit
        showcountries=True, countrycolor="#dcebc8",
        # Wyśrodkowanie globusa na środek trasy lotu
        center=dict(lat=(lat1+lat2)/2, lon=(lon1+lon2)/2)
    )

    fig.update_layout(
        margin={"r":0, "t":0, "l":0, "b":0},
        paper_bgcolor='rgba(0,0,0,0)',
        showlegend=False
    )

    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

# --- KARTA CELU PODRÓŻY ---
with col_card:
    st.markdown(f"### Cel Podróży: {cel.split(' ')[0]}")
    
    with st.container():
        kod_flagi = miejsca[cel]["kod"]
        st.image(f"https://flagpedia.net/data/flags/w580/{kod_flagi}.png", use_column_width=True)
        st.markdown(f"**Ciekawostka na dziś:**")
        st.info(miejsca[cel]["opis"])
