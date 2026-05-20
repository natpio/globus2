import streamlit as st
import plotly.express as px
import pandas as pd

# Ustawienia strony na pełną szerokość, co lepiej wygląda na tabletach
st.set_page_config(page_title="Interaktywny Globus", layout="wide")

st.title("🌍 Odkrywamy Świat")
st.markdown("Obracaj globusem przytrzymując lewy przycisk myszy lub przesuwając palcem po ekranie.")

# Przykładowe dane z ciekawostkami 
# Docelowo te dane pobierzesz z Google Sheets za pomocą st.connection
data = pd.DataFrame({
        "Miejsce": ["Komorniki", "Chicago", "Barcelona"],
        "Szerokość": [52.348, 41.878, 41.387],
        "Długość": [16.804, -87.629, 2.168],
        "Ciekawostka": [
            "Nasza baza startowa i centrum logistyczne!", 
            "1 lipca zaczynamy tu wielką przygodę!", 
            "Stolica Katalonii i świetne miejsce na targi."
        ],
        "Rozmiar": [20, 25, 15],
        "Kolor": ["#e74c3c", "#2ecc71", "#3498db"] # Kolory HEX
})

# Generowanie globusa
fig = px.scatter_geo(
    data,
    lat="Szerokość",
    lon="Długość",
    hover_name="Miejsce",
    # Konfiguracja dymku (tooltipa) - wyłączamy pokazywanie współrzędnych, 
    # zostawiamy tylko nazwę i ciekawostkę
    hover_data={
        "Ciekawostka": True, 
        "Szerokość": False, 
        "Długość": False, 
        "Rozmiar": False, 
        "Kolor": False
    },
    size="Rozmiar",
    color="Miejsce",
    color_discrete_sequence=data["Kolor"].tolist(),
    # To ten parametr odpowiada za zagięcie mapy w kulę
    projection="orthographic" 
)

# Kosmetyka wyglądu samej kuli ziemskiej
fig.update_geos(
    showcoastlines=True, coastlinecolor="DarkBlue",
    showland=True, landcolor="#f4f1de",
    showocean=True, oceancolor="#81b29a",
    showlakes=True, lakecolor="#81b29a",
    showcountries=True, countrycolor="#e07a5f",
    resolution=50, # Wartość 50 daje ładniejsze, dokładniejsze granice państw
    lataxis_showgrid=True, lonaxis_showgrid=True # Siatka geograficzna
)

# Usuwamy marginesy dookoła wykresu, żeby globus był jak największy
fig.update_layout(
    margin={"r":0, "t":0, "l":0, "b":0},
    showlegend=False,
    geo=dict(
        bgcolor='rgba(0,0,0,0)' # Przezroczyste tło za globusem
    )
)

# Wyświetlenie mapy w Streamlit
st.plotly_chart(fig, use_container_width=True)
