import streamlit as st
import plotly.graph_objects as go
import math

# --- 1. KONFIGURACJA STRONY (Wymuszony układ szeroki, ukryte menu) ---
st.set_page_config(page_title="Globe Explorer Premium", layout="wide", initial_sidebar_state="expanded")

# --- 2. ZAAWANSOWANY CSS: Glassmorphism i Cinematic Dark Mode ---
st.markdown("""
<style>
    /* Wymuszenie kosmicznego gradientu na całym tle aplikacji */
    .stApp {
        background: radial-gradient(circle at center, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
        color: #e6e6ea;
    }

    /* Ukrycie domyślnych elementów interfejsu Streamlit (header, footer, menu) */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* Efekt Glassmorphism (mrożone szkło) dla paneli informacyjnych */
    [data-testid="stVerticalBlock"] > [data-testid="stVerticalBlock"] {
        background: rgba(15, 52, 96, 0.25);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.15);
        border-radius: 20px;
        padding: 30px;
        box-shadow: 0 12px 40px 0 rgba(0, 0, 0, 0.4);
        transition: transform 0.3s ease;
    }
    [data-testid="stVerticalBlock"] > [data-testid="stVerticalBlock"]:hover {
        border: 1px solid rgba(0, 242, 254, 0.4); /* Neonowy akcent po najechaniu */
    }

    /* Typografia Premium */
    h1, h2, h3, p, span {
        font-family: 'Inter', 'Helvetica Neue', sans-serif;
    }
    h2 { 
        text-align: center; 
        font-weight: 200; 
        letter-spacing: 4px; 
        text-transform: uppercase; 
        margin-bottom: 2rem; 
        color: #ffffff;
        text-shadow: 0 0 10px rgba(255,255,255,0.2);
    }
    h3 { color: #00f2fe; font-weight: 600; letter-spacing: 1px; margin-bottom: 1rem;}
    
    /* Panel boczny */
    [data-testid="stSidebar"] {
        background-color: rgba(15, 23, 42, 0.95);
        border-right: 1px solid rgba(255,255,255,0.05);
    }
    
    /* Neonowe wartości (odległość) */
    .stSuccess {
        background-color: rgba(0, 242, 254, 0.1) !important;
        color: #00f2fe !important;
        border: 1px solid rgba(0, 242, 254, 0.3) !important;
        border-radius: 10px;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# --- 3. BAZA DANYCH ---
miejsca = {
    "Polska (Poznań)": {"lat": 52.406, "lon": 16.925, "kod": "pl", "opis": "Baza startowa. Odczyty z systemów: w normie."},
    "USA (Chicago)": {"lat": 41.878, "lon": -87.629, "kod": "us", "opis": "Cel misji. Wielka wyprawa zaplanowana na 1 lipca."},
    "Hiszpania (Barcelona)": {"lat": 41.387, "lon": 2.168, "kod": "es", "opis": "Sektor targowy. Wysokie nasłonecznienie, idealne warunki."},
    "Portugalia (Lizbona)": {"lat": 38.722, "lon": -9.139, "kod": "pt", "opis": "Kraniec kontynentu. Historyczny punkt nawigacyjny."},
    "Niemcy (Lipsk)": {"lat": 51.339, "lon": 12.373, "kod": "de", "opis": "Węzeł logistyczny. Przepływ ciężkich konstrukcji."},
    "Rumunia (Bukareszt)": {"lat": 44.426, "lon": 26.102, "kod": "ro", "opis": "Sektor wschodni. Bogata historia do zbadania."}
}

# --- 4. FUNKCJA OBLICZAJĄCA DYSTANS ---
def oblicz_dystans(lat1, lon1, lat2, lon2):
    R = 6371
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat/2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    return int(R * c)

# --- 5. PANEL BOCZNY (Nawigacja) ---
with st.sidebar:
    st.markdown("<h2 style='font-size: 1.5rem; text-align: left;'>🛰️ Terminal Lotów</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color: #8892b0;'>Wprowadź koordynaty misji:</p>", unsafe_allow_html=True)
    
    lista_miast = list(miejsca.keys())
    
    if 'start' not in st.session_state:
        st.session_state.start = lista_miast[0]
    if 'cel' not in st.session_state:
        st.session_state.cel = lista_miast[1]

    start = st.selectbox("🛫 Punkt początkowy", lista_miast, index=lista_miast.index(st.session_state.start))
    cel = st.selectbox("🛬 Punkt docelowy", lista_miast, index=lista_miast.index(st.session_state.cel))

    st.session_state.start = start
    st.session_state.cel = cel
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    if start != cel:
        dystans = oblicz_dystans(miejsca[start]["lat"], miejsca[start]["lon"], miejsca[cel]["lat"], miejsca[cel]["lon"])
        st.success(f"Dystans do pokonania: {dystans} km")
    else:
        st.warning("Oczekuję na podanie punktu docelowego.")

# --- 6. EKRAN GŁÓWNY ---
st.markdown("## Globalna Sieć Nawigacyjna")

# Zmiana proporcji dla lepszego wyeksponowania kuli
col_map, col_card = st.columns([3, 1.5]) 

lat1, lon1 = miejsca[start]["lat"], miejsca[start]["lon"]
lat2, lon2 = miejsca[cel]["lat"], miejsca[cel]["lon"]

with col_map:
    fig = go.Figure()

    # Premium Tech-Noir Style dla kuli
    fig.update_geos(
        projection_type="orthographic",
        showcoastlines=True, coastlinecolor="rgba(0, 242, 254, 0.3)", # Świecące wybrzeża
        showland=True, landcolor="#0a192f",    # Głębia oceanu/lądu
        showocean=True, oceancolor="rgba(0,0,0,0)", # Przezroczysty ocean (widać tło aplikacji!)
        showcountries=True, countrycolor="rgba(255,255,255,0.05)",
        resolution=50,
        center=dict(lat=(lat1+lat2)/2, lon=(lon1+lon2)/2),
        showframe=False # Usunięcie obramowania kuli
    )

    lats = [d["lat"] for d in miejsca.values()]
    lons = [d["lon"] for d in miejsca.values()]
    names = list(miejsca.keys())

    # Punkty miast (Neonowe węzły)
    fig.add_trace(go.Scattergeo(
        lon=lons, lat=lats, text=names, hoverinfo='text', mode='markers',
        marker=dict(size=10, color='#00f2fe', line=dict(width=2, color='rgba(255,255,255,0.8)')),
        name="Węzły"
    ))

    # Rysowanie trasy z efektem jarzenia
    if start != cel:
        fig.add_trace(go.Scattergeo(
            lon=[lon1, lon2], lat=[lat1, lat2], mode='lines',
            line=dict(width=4, color='#e94560', dash='solid'),
            name='Trajektoria'
        ))
        # Samolot (Wektorowy trójkąt symbolizujący statek)
        fig.add_trace(go.Scattergeo(
            lon=[lon2], lat=[lat2], text=["✈"], mode='text',
            textfont=dict(size=28, color="white"), hoverinfo='none', name="Statek"
        ))

    # KLUCZOWE DLA USUNIĘCIA CZARNYCH PASÓW:
    fig.update_layout(
        margin=dict(l=0, r=0, t=0, b=0),
        paper_bgcolor='rgba(0,0,0,0)', # Przezroczyste tło wykresu
        plot_bgcolor='rgba(0,0,0,0)',  # Przezroczyste tło rysowania
        geo=dict(bgcolor='rgba(0,0,0,0)'), # Przezroczyste tło geografii
        showlegend=False,
    )

    # Renderowanie (zmieniony height na odpowiedni do szerokiego układu)
    st.plotly_chart(fig, use_container_width=True, height=650, config={'displayModeBar': False})

with col_card:
    st.markdown(f"### Raport Sektora: {cel.split(' ')[0]}")
    with st.container():
        kod_flagi = miejsca[cel]["kod"]
        # Dodanie zaokrąglonych rogów również dla obrazka flagi
        st.markdown(
            f'<img src="https://flagpedia.net/data/flags/w580/{kod_flagi}.png" style="border-radius: 10px; width: 100%; box-shadow: 0 4px 15px rgba(0,0,0,0.5); margin-bottom: 20px;">',
            unsafe_allow_html=True
        )
        st.markdown(f"<p style='color: #ccd6f6; font-size: 0.9rem; letter-spacing: 1px; text-transform: uppercase;'>Dane operacyjne:</p>", unsafe_allow_html=True)
        st.markdown(f"<p style='color: #8892b0; font-size: 1.1rem; line-height: 1.6;'>{miejsca[cel]['opis']}</p>", unsafe_allow_html=True)
