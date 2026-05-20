import streamlit as st
import plotly.graph_objects as go
import math
from datetime import datetime

# --- 1. KONFIGURACJA STRONY (Kluczowe dla interfejsu pełnoekranowego) ---
st.set_page_config(page_title="Global Tactical HUD", layout="wide", initial_sidebar_state="expanded")

# --- 2. CSS: HOLOGRAFICZNY HUD & CYBER GRID ---
st.markdown("""
<style>
    /* Tło z cybernetyczną, taktyczną siatką */
    .stApp {
        background-color: #020617; /* Bardzo głęboki granat/czerń */
        background-image: 
            linear-gradient(rgba(0, 242, 254, 0.03) 1px, transparent 1px),
            linear-gradient(90deg, rgba(0, 242, 254, 0.03) 1px, transparent 1px);
        background-size: 30px 30px;
        color: #e2e8f0;
        font-family: 'Courier New', Courier, monospace; /* Techniczny font */
    }

    /* Ukrycie standardowych śmieci Streamlit */
    #MainMenu, footer, header {visibility: hidden;}

    /* Kontenery - efekt HUD (Heads Up Display) */
    [data-testid="stVerticalBlock"] > [data-testid="stVerticalBlock"] {
        background: rgba(2, 6, 23, 0.6);
        backdrop-filter: blur(8px);
        -webkit-backdrop-filter: blur(8px);
        border: 1px solid rgba(0, 242, 254, 0.2);
        border-top: 3px solid #00f2fe; /* Świecąca górna krawędź */
        border-radius: 5px; /* Ostre, techniczne krawędzie zamiast dużych zaokrągleń */
        padding: 20px;
        box-shadow: 0 0 20px rgba(0, 242, 254, 0.05);
    }

    /* Wygląd paska bocznego */
    [data-testid="stSidebar"] {
        background-color: rgba(2, 6, 23, 0.9) !important;
        border-right: 1px solid rgba(0, 242, 254, 0.2);
    }
    
    /* Typografia HUD */
    h1, h2, h3 {
        font-family: 'Orbitron', 'Courier New', sans-serif; /* Kosmiczny klimat */
        text-transform: uppercase;
        letter-spacing: 2px;
    }
    h2 { color: #f8fafc; font-weight: 300; margin-bottom: 2rem; border-bottom: 1px solid rgba(0,242,254,0.3); padding-bottom: 10px;}
    h3 { color: #00f2fe; font-size: 1.2rem; }
    
    /* Telemetria - własne klasy HTML */
    .telemetry-box {
        border-left: 2px solid #e94560;
        padding-left: 15px;
        margin-bottom: 15px;
        background: linear-gradient(90deg, rgba(233, 69, 96, 0.1) 0%, transparent 100%);
    }
    .telemetry-value { font-size: 1.8rem; color: #e94560; font-weight: bold; text-shadow: 0 0 10px rgba(233,69,96,0.5); }
    .telemetry-label { font-size: 0.8rem; color: #94a3b8; text-transform: uppercase; letter-spacing: 1px; }
    
    /* Zielony status */
    .status-ok { color: #10b981; font-weight: bold; text-shadow: 0 0 5px rgba(16, 185, 129, 0.5); }
    
    /* Pulsacja dla przycisku */
    .stButton button {
        background: transparent;
        border: 1px solid #00f2fe;
        color: #00f2fe;
        transition: all 0.3s ease;
    }
    .stButton button:hover {
        background: rgba(0, 242, 254, 0.2);
        box-shadow: 0 0 15px rgba(0, 242, 254, 0.5);
        border: 1px solid #ffffff;
        color: #ffffff;
    }
</style>
""", unsafe_allow_html=True)

# --- 3. BAZA DANYCH (Z dodatkowymi parametrami misji) ---
miejsca = {
    "Polska (Poznań)": {"lat": 52.406, "lon": 16.925, "kod": "pl", "klasa": "ALPHA", "opis": "Główny węzeł komunikacyjny uruchomiony. Gotowość do startu."},
    "USA (Chicago)": {"lat": 41.878, "lon": -87.629, "kod": "us", "klasa": "OMEGA", "opis": "Cel główny wyznaczony na 1 Lipca. Trwa kalibracja systemów."},
    "Hiszpania (Barcelona)": {"lat": 41.387, "lon": 2.168, "kod": "es", "klasa": "BETA", "opis": "Stacja pogodowa zgłasza optymalne warunki słoneczne."},
    "Portugalia (Lizbona)": {"lat": 38.722, "lon": -9.139, "kod": "pt", "klasa": "GAMMA", "opis": "Zachodni kraniec siatki. Systemy nawigacji morskiej włączone."},
    "Niemcy (Lipsk)": {"lat": 51.339, "lon": 12.373, "kod": "de", "klasa": "DELTA", "opis": "Sektor zaopatrzenia. Przepustowość logistyczna 100%."},
    "Rumunia (Bukareszt)": {"lat": 44.426, "lon": 26.102, "kod": "ro", "klasa": "EPSILON", "opis": "Skany wschodniej części kontynentu w normie."}
}

# --- 4. SILNIK OBLICZENIOWY TELEMETRII ---
def oblicz_dystans(lat1, lon1, lat2, lon2):
    R = 6371
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat/2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    return int(R * c)

def format_coords(lat, lon):
    ns = "N" if lat >= 0 else "S"
    ew = "E" if lon >= 0 else "W"
    return f"{abs(lat):.3f}° {ns} | {abs(lon):.3f}° {ew}"

# --- 5. PANEL BOCZNY (Konsola Operatora) ---
with st.sidebar:
    st.markdown("<h2 style='font-size: 1.3rem;'>🛰️ UPLINK TERMINAL</h2>", unsafe_allow_html=True)
    
    # "Live" Clock simulation
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    st.markdown(f"<p style='color: #00f2fe; font-size: 0.8rem;'>SYS_TIME: {now} Z</p>", unsafe_allow_html=True)
    st.markdown("---")
    
    lista_miast = list(miejsca.keys())
    if 'start' not in st.session_state: st.session_state.start = lista_miast[0]
    if 'cel' not in st.session_state: st.session_state.cel = lista_miast[1]

    start = st.selectbox("ORIGIN (PUNKT ZERO)", lista_miast, index=lista_miast.index(st.session_state.start))
    cel = st.selectbox("DESTINATION (CEL MISJI)", lista_miast, index=lista_miast.index(st.session_state.cel))

    st.session_state.start = start; st.session_state.cel = cel
    
    st.markdown("---")
    if start != cel:
        dystans = oblicz_dystans(miejsca[start]["lat"], miejsca[start]["lon"], miejsca[cel]["lat"], miejsca[cel]["lon"])
        czas_lotu = dystans / 850 # srednia predkosc pasazerska
        godziny = int(czas_lotu)
        minuty = int((czas_lotu - godziny) * 60)
        paliwo = dystans * 3.16 # estymacja galonów
        
        st.markdown(f"""
        <div class="telemetry-box">
            <div class="telemetry-label">Trajektoria lotu (Dystans)</div>
            <div class="telemetry-value">{dystans} KM</div>
        </div>
        <div class="telemetry-box">
            <div class="telemetry-label">Estymowany czas przelotu</div>
            <div class="telemetry-value" style="color:#00f2fe;">{godziny}H {minuty}M</div>
        </div>
        <div class="telemetry-box">
            <div class="telemetry-label">Wymagane paliwo lotnicze</div>
            <div class="telemetry-value" style="color:#f1c40f;">{int(paliwo)} GAL</div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("INICJUJ SEKWENCJĘ LOTU"):
            st.snow() # Efekt przecinania chmur w stratosferze
    else:
        st.error("BŁĄD: Pokrywanie się współrzędnych. Wybierz inny wektor.")

# --- 6. EKRAN GŁÓWNY (Holograficzny Wykres) ---
st.markdown("## GLOBALNY SYSTEM POZYCJONOWANIA TARTARUS")

col_map, col_card = st.columns([3.5, 1.5]) 

lat1, lon1 = miejsca[start]["lat"], miejsca[start]["lon"]
lat2, lon2 = miejsca[cel]["lat"], miejsca[cel]["lon"]

with col_map:
    fig = go.Figure()

    # HOLOGRAFICZNA KULA ZIEMSKA
    fig.update_geos(
        projection_type="orthographic",
        showcoastlines=True, coastlinecolor="rgba(0, 242, 254, 0.6)", # Jasnoświecące wybrzeża
        showland=True, landcolor="rgba(2, 12, 27, 0.8)",    # Ciemny, lekko przezroczysty ląd
        showocean=True, oceancolor="rgba(0,0,0,0)", # PEŁNA PRZEZROCZYSTOŚĆ (widać siatkę z CSS!)
        lataxis_showgrid=True, lonaxis_showgrid=True, # Siatka geograficzna jak w radarze
        lataxis_gridcolor="rgba(0, 242, 254, 0.1)", lonaxis_gridcolor="rgba(0, 242, 254, 0.1)",
        resolution=50,
        center=dict(lat=(lat1+lat2)/2, lon=(lon1+lon2)/2),
        showframe=False
    )

    lats = [d["lat"] for d in miejsca.values()]
    lons = [d["lon"] for d in miejsca.values()]
    names = list(miejsca.keys())

    # Węzły sieci (Podwójna warstwa dla efektu GLOW)
    # 1. Poświata (duże, półprzezroczyste kropki)
    fig.add_trace(go.Scattergeo(
        lon=lons, lat=lats, hoverinfo='none', mode='markers',
        marker=dict(size=20, color='rgba(0, 242, 254, 0.2)'), showlegend=False
    ))
    # 2. Rdzeń węzła
    fig.add_trace(go.Scattergeo(
        lon=lons, lat=lats, text=names, hoverinfo='text', mode='markers',
        marker=dict(size=8, color='#ffffff', line=dict(width=2, color='#00f2fe')), name="Węzły"
    ))

    # Wiązka Lasera (Trasa Lotu)
    if start != cel:
        fig.add_trace(go.Scattergeo(
            lon=[lon1, lon2], lat=[lat1, lat2], mode='lines',
            line=dict(width=3, color='#e94560', dash='solid'), name='Laser Link'
        ))
        # Symbol statku powietrznego
        fig.add_trace(go.Scattergeo(
            lon=[lon2], lat=[lat2], text=["✈"], mode='text',
            textfont=dict(size=30, color="#e94560"), hoverinfo='none', name="Statek"
        ))

    fig.update_layout(
        margin=dict(l=0, r=0, t=0, b=0),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        geo=dict(bgcolor='rgba(0,0,0,0)'),
        showlegend=False,
    )

    st.plotly_chart(fig, use_container_width=True, height=750, config={'displayModeBar': False})

# --- KARTA DANYCH WYWIADOWCZYCH ---
with col_card:
    st.markdown(f"### ODCZYT SEKTORA: {cel.split(' ')[0]}")
    with st.container():
        kod_flagi = miejsca[cel]["kod"]
        st.markdown(
            f'<img src="https://flagpedia.net/data/flags/w580/{kod_flagi}.png" style="border-radius: 4px; width: 100%; border: 1px solid rgba(255,255,255,0.2); filter: grayscale(20%) contrast(120%); margin-bottom: 20px;">',
            unsafe_allow_html=True
        )
        
        # Cyfrowe, wojskowe współrzędne
        coords = format_coords(lat2, lon2)
        st.markdown(f"<p style='color: #00f2fe; font-size: 0.9rem;'>LOC: [ {coords} ]</p>", unsafe_allow_html=True)
        
        st.markdown(f"<p style='color: #94a3b8; font-size: 0.8rem;'>KLASYFIKACJA WĘZŁA: <span style='color: white;'>{miejsca[cel]['klasa']}</span></p>", unsafe_allow_html=True)
        st.markdown(f"<p style='color: #94a3b8; font-size: 0.8rem;'>STATUS SIECI: <span class='status-ok'>ZABEZPIECZONY</span></p>", unsafe_allow_html=True)
        
        st.markdown("---")
        st.markdown(f"<p style='color: #cbd5e1; font-size: 1rem; line-height: 1.5; font-family: monospace;'>{miejsca[cel]['opis']}</p>", unsafe_allow_html=True)
