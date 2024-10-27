import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

st.markdown("---") 
st.image("images/logolocalizalo.png", use_column_width=True)

# Código CSS para cambiar el color de fondo
background_color = """
<style>
body {
    background-color: #94f080; /* Color de fondo en formato hexadecimal */
}
</style>
"""
# Inyectar el código CSS en la aplicación
st.markdown(background_color, unsafe_allow_html=True)

# Tu aplicación Streamlit
st.write("Con localízalo, tu local a un clic")

# Estilo CSS para personalizar el botón
st.markdown("""
<style>
    .mi-boton {
        padding: 10px 20px; /* Espaciado interno */
        background-color: #4CAF50; /* Color de fondo */
        color: white; /* Color del texto */
        border: none; /* Sin borde */
        border-radius: 5px; /* Bordes redondeados */
        cursor: pointer; /* Cambia el cursor al pasar el mouse */
    }
</style>
""", unsafe_allow_html=True)

# Usar un botón
if st.button('Busca tu local!'):
    st.success("¡Haz clic en el enlace para ver el mapa!")
    location = "Bogotá D.C" 
    map_link = f"https://www.openstreetmap.org/search?query={location}"
    st.markdown(f"[Ver en el mapa]({map_link})")

st.markdown("---")  # Línea horizontal

# Crear columnas para el menú horizontal
col1, col2, col3 = st.columns(3)

with col1:
    if st.button('Inicio'):
        st.write('Inicio.')

with col2:
    if st.button('Acerca de nosotros'):
       st.markdown('<a href="https://docs.google.com/document/d/e/2PACX-1vRzkHCfEkrZK7UK4KlLiJh0ovwM9QpkxGSN1r6GZzeixaiu8Qteooq1V9VEw38W8N8uz25nspRjWiIS/pub" target="_blank">Misión-Visión</a>', unsafe_allow_html=True)
with col3:
    if st.button('Contacto'):
        st.write('Puedes contactarnos a través del email localcomercial@dominiolocalizalo.com o nuestras redes sociales')

st.markdown("---") 

# Leer el archivo CSV
df = pd.read_csv('C:/Users/Ana/Desktop/virtualhak/archivo.csv', sep=';', encoding='latin1')
st.write(df) 

# Renombrar columnas si es necesario
df.rename(columns={'Latitude': 'latitud', 'Longitude': 'longitud'}, inplace=True)

# Verificar si 'latitud' y 'longitud' existen
df['latitud'] = pd.to_numeric(df['latitud'])
df['longitud'] = pd.to_numeric(df['longitud'])
if 'latitud' in df.columns and 'longitud' in df.columns:
    if df['latitud'].notnull().any() and df['longitud'].notnull().any():
        m = folium.Map(location=[df['latitud'].mean(), df['longitud'].mean()], zoom_start=13)
        
        # Añadir marcadores al mapa
        for idx, row in df.iterrows():
            folium.Marker(
                location=[row['latitud'], row['longitud']],
                popup=row.get('ciudad', 'Sin nombre'),  # Usar el nombre del local como popup
            ).add_to(m)

        # Mostrar el mapa en Streamlit
        st.title("Mapa de Locales")
        st_folium(m, width=725)
    else:
        st.error("El archivo no contiene valores válidos para 'latitud' y 'longitud'.")
else:
    st.error("El archivo debe contener las columnas 'latitud' y 'longitud'.")