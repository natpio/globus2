import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import math

# --- KONFIGURACJA STRONY (Domowy klimat, ale dostosowany do ciemnego tła) ---
st.set_page_config(page_title="Rodzinny Globus Laury i Zosi", layout="wide", initial_sidebar_state="expanded")

# --- CSS: Urealnione, kosmiczne tło, radosne panele ---
# Dostosowuję gradienty i kolory, aby wyglądały dobrze na ciemnym tle.
st.markdown("""
<style>
    /* Zaokrąglone, kolorowe panele - jasne na ciemnym tle */
    [data-testid="stVerticalBlock"] > [data-testid="stVerticalBlock"] {
        border-radius: 25px;
        background: rgba(255, 255, 255, 0.95); /* Prawie białe, matowe tło */
        padding: 25px;
        border: 3px solid #ff6b6b; /* Czerwony akcent dla paneli */
        box-shadow: 0 8px 15px rgba(0, 0, 0, 0.2);
        color: #333;
    }
    /* Powiększenie i pokolorowanie tekstów */
    .stMarkdown h3 { color: #ff6b6b; font-weight: bold; margin-bottom: 0.5rem; }
    .stMarkdown p { font-size: 1.1rem; }
    .stMarkdown h2 { color: white; text-align: center; margin-bottom: 2rem; } /* Główny tytuł biały */

    /* Ulepszenie paska bocznego na ciemnym tle */
    [data-testid="stSidebar"] {
        background-color: #2c3e50;
        color: #ecf0f1;
    }
    [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h3 { color: #ff9f43; }
    [data-testid="stSidebar"] .stSelectbox, [data-testid="stSidebar"] .stButton button {
        color: #333;
    }

    /* Urealnienie tekstu 'Odległość' na jasnym panelu */
    .stSuccess { color: #27ae60; }
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
    
    # Stan sesji, aby zachować wybór miast
    if 'start' not in st.session_state:
        st.session_state.start = lista_miast[0]
    if 'cel' not in st.session_state:
        st.session_state.cel = lista_miast[1]

    start = st.selectbox("🛫 Skąd lecimy?", lista_miast, index=lista_miast.index(st.session_state.start))
    cel = st.selectbox("🛬 Dokąd lecimy?", lista_miast, index=lista_miast.index(st.session_state.cel))

    # Aktualizacja stanu sesji
    st.session_state.start = start
    st.session_state.cel = cel
    
    st.markdown("---")
    if start != cel:
        dystans = oblicz_dystans(miejsca[start]["lat"], miejsca[start]["lon"], miejsca[cel]["lat"], miejsca[cel]["lon"])
        st.success(f"**Odległość:** {dystans} kilometrów")
        if st.button("🚀 Wystartuj samolot!"):
            st.balloons()
    else:
        st.warning("Wybierz dwa różne miejsca, żeby wytyczyć trasę lotu.")

# --- GŁÓWNY EKRAN ---
st.markdown("## 🌍 Odkrywca Świata Laury i Zosi")

col_map, col_card = st.columns([2, 1])

# Pobranie współrzędnych do narysowania trasy
lat1, lon1 = miejsca[start]["lat"], miejsca[start]["lon"]
lat2, lon2 = miejsca[cel]["lat"], miejsca[cel]["lon"]

with col_map:
    # --- RYSOWANIE GLOBUSA (Fotorealizm i Pełny Widok) ---
    fig = go.Figure()

    # 1. Dodajemy fotorealistyczną warstwę topograficzną
    fig.update_geos(
        projection_type="orthographic",
        base_layer="esri-imagery",  # Fotorealistyczna tekstura
        showcoastlines=True, coastlinecolor="rgba(255,255,255,0.4)", # Subtelne, jasne wybrzeża
        showland=False, # Wyłączone, bo używamy obrazu
        showocean=False, # Wyłączone, bo używamy obrazu
        showcountries=False, # Bez granic państw, dla czystości
        resolution=50,
        center=dict(lat=(lat1+lat2)/2, lon=(lon1+lon2)/2)
    )

    # 2. Dodajemy wszystkie punkty miast na mapę - urealnione punkty
    lats = [d["lat"] for d in miejsca.values()]
    lons = [d["lon"] for d in miejsca.values()]
    names = list(miejsca.keys())

    fig.add_trace(go.Scattergeo(
        lon=lons,
        lat=lats,
        text=names,
        hoverinfo='text',
        mode='markers',
        # Małe, subtelne, "błyszczące" złote punkty
        marker=dict(size=8, color='#f1c40f', line=dict(width=1, color='white')),
        name="Miejsca"
    ))

    # 3. Rysujemy RZECZYWISTĄ trasę lotu (Ortodroma) - urealniona ciągła linia
    if start != cel:
        fig.add_trace(go.Scattergeo(
            lon=[lon1, lon2],
            lat=[lat1, lat2],
            mode='lines',
            # Ciągła linia z delikatnym efektem poświaty (grubsza i kolorowa)
            line=dict(width=5, color='#3498db', dash='solid'),
            name='Trasa'
        ))
        # Dodajemy mniejszą, urealnioną ikonę samolotu w miejscu docelowym
        fig.add_trace(go.Scattergeo(
            lon=[lon2],
            lat=[lat2],
            text=["✈️"],
            mode='text',
            textfont=dict(size=25), # Umniejszony samolot
            hoverinfo='none',
            name="Samolot"
        ))

    fig.update_layout(
        margin={"r":0, "t":0, "l":0, "b":0},
        paper_bgcolor='#0d1117', # Ciemne, kosmiczne tło dla kolumny
        showlegend=False,
    )

    # Wyświetlenie mapy w Streamlit z wymuszoną, stałą wysokością, aby pokazać cały globus
    st.plotly_chart(fig, use_container_width=True, height=700, config={'displayModeBar': False})

# --- KARTA CELU PODRÓŻY ---
with col_card:
    st.markdown(f"### Cel Podróży: {cel.split(' ')[0]}")
    
    with st.container():
        kod_flagi = miejsca[cel]["kod"]
        st.image(f"https://flagpedia.net/data/flags/w580/{kod_flagi}.png", use_column_width=True)
        st.markdown(f"**Ciekawostka na dziś:**")
        st.info(miejsca[cel]["opis"])
