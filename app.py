import streamlit as st
import plotly.express as px
import pandas as pd

# --- KONFIGURACJA STRONY (PRO Level Layout) ---
st.set_page_config(
    page_title="Geograficzny Globus PRO",
    layout="wide", # Ważne dla układu kolumnowego
    initial_sidebar_state="expanded"
)

# --- STYLIZACJA CSS (Hack do dodania "kart" informacyjnych) ---
# Streamlit domyślnie nie ma "kart", symulujemy je za pomocą kontenerów i CSS.
st.markdown("""
<style>
    /* Stylowanie kontenera na kartę informacyjną */
    [data-testid="stVerticalBlock"] > [data-testid="stVerticalBlock"] {
        border-radius: 20px;
        background-color: rgba(255, 255, 255, 0.05); /* Przezroczyste, ciemne tło */
        padding: 20px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    /* Zmniejszenie odstępów między elementami na karcie */
    .stMarkdown p {
        margin-bottom: 0.2rem;
    }
</style>
""", unsafe_allow_html=True)

# --- PRO BAZA DANYCH (Rozszerzona o kod kraju dla flagi) ---
# Docelowo pobierane z Google Sheets
data = pd.DataFrame([
    {"Miejsce": "Polska", "Kod": "pl", "Szerokość": 52.348, "Długość": 16.804, "Ciekawostka": "Nasza baza! Rozpocznij naukę stąd.", "Rozmiar": 30, "Kolor": "#e74c3c"},
    {"Miejsce": "Stany Zjednoczone", "Kod": "us", "Szerokość": 37.090, "Długość": -95.712, "Ciekawostka": "Siedziba NASA. Stąd wysyła się rakiety na Księżyc!", "Rozmiar": 20, "Kolor": "#2ecc71"},
    {"Miejsce": "Hiszpania", "Kod": "es", "Szerokość": 40.463, "Długość": -3.749, "Ciekawostka": "Kraj, w którym rośnie najwięcej oliwek na świecie.", "Rozmiar": 20, "Kolor": "#3498db"}
])

# --- ZARZĄDZANIE STANEM APLIKACJI (Session State) ---
# Pamiętamy wybrany kraj, aby karta się nie odświeżała przy obracaniu globusa
if 'selected_country' not in st.session_state:
    st.session_state.selected_country = data.iloc[0].to_dict() # Domyślnie Polska

# --- PANEL BOCZNY (Sidebar PRO) ---
with st.sidebar:
    st.image("https://flagpedia.net/data/flags/w580/pl.png", width=100) # Placeholder logo
    st.title("Globus Wiedzy 🌍")
    st.markdown("### Centrum Dowodzenia")
    st.markdown("Użyj menu lub kliknij kropkę na globusie.")

    # Dropdown do wyboru kraju (aktualizuje Session State)
    country_names = data["Miejsce"].tolist()
    chosen_name = st.selectbox(
        "🔎 Wybierz kraj, który chcesz odkryć:", 
        country_names, 
        index=country_names.index(st.session_state.selected_country["Miejsce"])
    )
    
    # Aktualizacja stanu, jeśli użytkownik zmienił kraj z menu
    if chosen_name != st.session_state.selected_country["Miejsce"]:
        st.session_state.selected_country = data[data["Miejsce"] == chosen_name].iloc[0].to_dict()
        # st.rerun() # Opcjonalne wymuszenie odświeżenia

    st.info("💡 Kliknij na kropkę na mapie, aby zobaczyć ciekawostkę tutaj!")


# --- GŁÓWNY UKŁAD (Globus i Karta) ---
col_map, col_card = st.columns([2, 1]) # Proporcje 2:1

with col_map:
    # --- GENEROWANIE GLOBUSA "DEEP SPACE" PRO ---
    fig = px.scatter_geo(
        data,
        lat="Szerokość",
        lon="Długość",
        hover_name="Miejsce",
        hover_data={"Ciekawostka": False, "Szerokość": False, "Długość": False, "Rozmiar": False, "Kod": False},
        size="Rozmiar",
        projection="orthographic"
    )

    # Nowoczesna kolorystyka PRO
    fig.update_geos(
        showcoastlines=True, coastlinecolor="#4a4e69", # Stonowany niebieski
        showland=True, landcolor="#1d2d44", # Bardzo ciemny ląd
        showocean=True, oceancolor="#0d1117", # Prawie czarny ocean ("kosmos")
        showcountries=True, countrycolor="#4a4e69", # Stonowane granice
        resolution=50,
        lataxis_showgrid=False, lonaxis_showgrid=False # Usuwamy siatkę dla czystości
    )

    fig.update_layout(
        margin={"r":0, "t":0, "l":0, "b":0},
        paper_bgcolor='rgba(0,0,0,0)', # Przezroczyste tło
        plot_bgcolor='rgba(0,0,0,0)',
        showlegend=False
    )

    # Reakcja na kliknięcie kropki na globusie
    # St.plotly_chart zwraca dane o kliknięciu
    event_data = st.plotly_chart(fig, use_container_width=True, on_select="rerun")
    
    # Jeśli użytkownik kliknął kropkę, aktualizujemy wybrany kraj
    if event_data and event_data.selection and event_data.selection.points:
        point_index = event_data.selection.points[0].point_index
        st.session_state.selected_country = data.iloc[point_index].to_dict()
        st.rerun() # Wymuszone odświeżenie karty

with col_card:
    # --- PRO KARTA INFORMACYJNA (Card System) ---
    selected = st.session_state.selected_country
    
    st.markdown("### Szczegóły Odkrycia")
    
    # Kontener działający jako karta (dzięki CSS na górze)
    with st.container():
        # Nagłówek karty z flagą i nazwą
        flag_url = f"https://flagpedia.net/data/flags/w580/{selected['Kod']}.png"
        col_flag, col_name = st.columns([1, 3])
        
        with col_flag:
            st.image(flag_url, use_column_width=True)
        with col_name:
            st.subheader(selected['Miejsce'])

        st.markdown("---") # Linia oddzielająca
        
        # Treść karty z ikonami
        st.markdown(f"**📍 Współrzędne:** `{selected['Szerokość']:.3f}, {selected['Długość']:.3f}`")
        st.markdown(f"**🧐 Ciekawostka dla dziecka:**")
        st.info(selected['Ciekawostka'])
        
        # Przycisk "Zalicz kraj"
        if st.button("✅ Zalicz ten kraj!"):
            st.balloons()
            st.success(f"Brawo! Poznałeś: {selected['Miejsce']}")
