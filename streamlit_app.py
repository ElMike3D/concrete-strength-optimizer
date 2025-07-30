import streamlit as st
import pandas as pd
import numpy as np
import joblib
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Configuración de la página
st.set_page_config(
    page_title="Optimizador de Concreto",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Cargar modelo
@st.cache_resource
def load_model():
    return joblib.load("modelo_resistencia_concreto.pkl")

modelo = load_model()

# CSS personalizado para mejorar la apariencia
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin: 0.5rem 0;
    }
    .optimization-section {
        background: #f8f9fa;
        padding: 2rem;
        border-radius: 15px;
        margin: 1rem 0;
        border-left: 5px solid #667eea;
    }
    .stSlider > div > div > div > div {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
    }
</style>
""", unsafe_allow_html=True)

# Título principal
st.markdown('<h1 class="main-header">🏗️ Optimizador de Concreto</h1>', unsafe_allow_html=True)

# Pestañas para diferentes funcionalidades
tab1, tab2, tab3 = st.tabs(["📊 Predicción Manual", "🎯 Optimización Automática", "📈 Análisis de Resultados"])

with tab1:
    st.markdown("### 🔧 Predicción Manual de Resistencia")
st.markdown("Ajusta los ingredientes de tu mezcla y estima la resistencia del concreto.")

    # Crear dos columnas para los sliders
    col1, col2 = st.columns(2)
    
    with col1:
        cement = st.slider("Cemento (kg/m³)", 100, 400, 300, help="Cantidad de cemento Portland")
        slag = st.slider("Escoria de alto horno (kg/m³)", 0, 100, 0, help="Escoria de alto horno como aditivo")
        fly_ash = st.slider("Ceniza volante (kg/m³)", 0, 100, 0, help="Ceniza volante como aditivo")
        water = st.slider("Agua (kg/m³)", 100, 250, 180, help="Cantidad de agua en la mezcla")
    
    with col2:
        superplasticizer = st.slider("Aditivo plastificante (kg/m³)", 0, 25, 0, help="Aditivo superplastificante")
        coarse_agg = st.slider("Agregado grueso (kg/m³)", 700, 1100, 950, help="Agregado grueso (grava)")
        fine_agg = st.slider("Agregado fino (kg/m³)", 500, 1000, 700, help="Agregado fino (arena)")
        age = st.slider("Edad (días)", 1, 90, 28, help="Edad del concreto para la prueba")

# Crear DataFrame para el modelo
entrada = pd.DataFrame([{
    'Cement (component 1)(kg in a m^3 mixture)': cement,
    'Blast Furnace Slag (component 2)(kg in a m^3 mixture)': slag,
    'Fly Ash (component 3)(kg in a m^3 mixture)': fly_ash,
    'Water  (component 4)(kg in a m^3 mixture)': water,
    'Superplasticizer (component 5)(kg in a m^3 mixture)': superplasticizer,
    'Coarse Aggregate  (component 6)(kg in a m^3 mixture)': coarse_agg,
    'Fine Aggregate (component 7)(kg in a m^3 mixture)': fine_agg,
    'Age (day)': age
}])

# Predicción
    if st.button("🔮 Predecir Resistencia", type="primary"):
    resultado = modelo.predict(entrada)[0]
        
        # Mostrar resultado con métricas
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Resistencia Estimada", f"{resultado:.2f} MPa")
        
        with col2:
            # Clasificar la resistencia
            if resultado < 20:
                clasificacion = "Baja"
                color = "red"
            elif resultado < 35:
                clasificacion = "Media"
                color = "orange"
            else:
                clasificacion = "Alta"
                color = "green"
            st.metric("Clasificación", clasificacion)
        
        with col3:
            st.metric("Relación A/C", f"{water/cement:.2f}")

with tab2:
    st.markdown("### 🎯 Optimización Automática de Mezclas")
    st.markdown("Encuentra la mejor combinación de ingredientes para maximizar la resistencia.")
    
    # Configuración de la optimización
    st.markdown("#### ⚙️ Configuración de Rangos")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Rangos de Materiales:**")
        cement_min, cement_max = st.slider("Cemento (kg/m³)", 250, 400, (250, 350), key="cement_opt")
        slag_min, slag_max = st.slider("Escoria (kg/m³)", 0, 100, (0, 50), key="slag_opt")
        fly_ash_min, fly_ash_max = st.slider("Ceniza volante (kg/m³)", 0, 100, (0, 30), key="fly_opt")
        water_min, water_max = st.slider("Agua (kg/m³)", 150, 200, (160, 190), key="water_opt")
    
    with col2:
        st.markdown("**Rangos Adicionales:**")
        super_min, super_max = st.slider("Aditivo plastificante (kg/m³)", 0, 25, (0, 10), key="super_opt")
        coarse_min, coarse_max = st.slider("Agregado grueso (kg/m³)", 800, 1100, (900, 1000), key="coarse_opt")
        fine_min, fine_max = st.slider("Agregado fino (kg/m³)", 600, 900, (650, 750), key="fine_opt")
        age_min, age_max = st.slider("Edad (días)", 3, 28, (7, 28), key="age_opt")
    
    # Parámetros de simulación
    n_simulaciones = st.slider("Número de simulaciones", 100, 5000, 1000, step=100)
    semilla = st.number_input("Semilla aleatoria", value=91, min_value=1, max_value=999)
    
    if st.button("🚀 Ejecutar Optimización", type="primary"):
        with st.spinner("Ejecutando optimización..."):
            # Configurar semilla
            np.random.seed(semilla)
            
            # Definir rangos de materiales
            materiales_disponibles = {
                'Cement (component 1)(kg in a m^3 mixture)': (cement_min, cement_max),
                'Blast Furnace Slag (component 2)(kg in a m^3 mixture)': (slag_min, slag_max),
                'Fly Ash (component 3)(kg in a m^3 mixture)': (fly_ash_min, fly_ash_max),
                'Water  (component 4)(kg in a m^3 mixture)': (water_min, water_max),
                'Superplasticizer (component 5)(kg in a m^3 mixture)': (super_min, super_max),
                'Coarse Aggregate  (component 6)(kg in a m^3 mixture)': (coarse_min, coarse_max),
                'Fine Aggregate (component 7)(kg in a m^3 mixture)': (fine_min, fine_max),
                'Age (day)': (age_min, age_max)
            }
            
            # Generar simulaciones
            simulaciones = []
            for _ in range(n_simulaciones):
                mezcla = {
                    ingrediente: np.random.uniform(rango[0], rango[1])
                    for ingrediente, rango in materiales_disponibles.items()
                }
                simulaciones.append(mezcla)
            
            # Convertir a DataFrame
            df_simulaciones = pd.DataFrame(simulaciones)
            
            # Predecir resistencia
            df_simulaciones['Predicted Strength (MPa)'] = modelo.predict(df_simulaciones)
            
            # Obtener la mejor mezcla
            mejor_mezcla = df_simulaciones.loc[df_simulaciones['Predicted Strength (MPa)'].idxmax()]
            
            # Guardar resultados en session state
            st.session_state['optimization_results'] = df_simulaciones
            st.session_state['best_mix'] = mejor_mezcla
            
            # Mostrar resultados
            st.success("✅ Optimización completada!")
            
            # Métricas principales
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Mejor Resistencia", f"{mejor_mezcla['Predicted Strength (MPa)']:.2f} MPa")
            
            with col2:
                st.metric("Resistencia Promedio", f"{df_simulaciones['Predicted Strength (MPa)'].mean():.2f} MPa")
            
            with col3:
                st.metric("Resistencia Máxima", f"{df_simulaciones['Predicted Strength (MPa)'].max():.2f} MPa")
            
            with col4:
                st.metric("Resistencia Mínima", f"{df_simulaciones['Predicted Strength (MPa)'].min():.2f} MPa")
            
            # Mostrar la mejor mezcla
            st.markdown("#### 🏆 Mejor Mezcla Encontrada")
            
            # Crear DataFrame para mostrar la mejor mezcla
            mejor_mezcla_display = pd.DataFrame({
                'Ingrediente': [
                    'Cemento', 'Escoria de alto horno', 'Ceniza volante', 'Agua',
                    'Aditivo plastificante', 'Agregado grueso', 'Agregado fino', 'Edad'
                ],
                'Cantidad': [
                    mejor_mezcla['Cement (component 1)(kg in a m^3 mixture)'],
                    mejor_mezcla['Blast Furnace Slag (component 2)(kg in a m^3 mixture)'],
                    mejor_mezcla['Fly Ash (component 3)(kg in a m^3 mixture)'],
                    mejor_mezcla['Water  (component 4)(kg in a m^3 mixture)'],
                    mejor_mezcla['Superplasticizer (component 5)(kg in a m^3 mixture)'],
                    mejor_mezcla['Coarse Aggregate  (component 6)(kg in a m^3 mixture)'],
                    mejor_mezcla['Fine Aggregate (component 7)(kg in a m^3 mixture)'],
                    mejor_mezcla['Age (day)']
                ],
                'Unidad': ['kg/m³', 'kg/m³', 'kg/m³', 'kg/m³', 'kg/m³', 'kg/m³', 'kg/m³', 'días']
            })
            
            st.dataframe(mejor_mezcla_display, use_container_width=True)

with tab3:
    st.markdown("### 📈 Análisis de Resultados")
    
    if 'optimization_results' in st.session_state:
        df_simulaciones = st.session_state['optimization_results']
        mejor_mezcla = st.session_state['best_mix']
        
        # Estadísticas descriptivas
        st.markdown("#### 📊 Estadísticas de Resistencia")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Histograma de resistencias
            fig_hist = px.histogram(
                df_simulaciones, 
                x='Predicted Strength (MPa)',
                nbins=30,
                title="Distribución de Resistencias",
                color_discrete_sequence=['#667eea']
            )
            fig_hist.update_layout(showlegend=False)
            st.plotly_chart(fig_hist, use_container_width=True)
        
        with col2:
            # Box plot
            fig_box = px.box(
                df_simulaciones,
                y='Predicted Strength (MPa)',
                title="Distribución de Resistencias (Box Plot)",
                color_discrete_sequence=['#764ba2']
            )
            st.plotly_chart(fig_box, use_container_width=True)
        
        # Análisis de correlaciones
        st.markdown("#### 🔍 Análisis de Correlaciones")
        
        # Calcular correlaciones
        correlaciones = df_simulaciones.corr()['Predicted Strength (MPa)'].sort_values(ascending=False)
        
        # Gráfico de correlaciones
        fig_corr = px.bar(
            x=correlaciones.index,
            y=correlaciones.values,
            title="Correlación con la Resistencia",
            color=correlaciones.values,
            color_continuous_scale='RdBu'
        )
        fig_corr.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(fig_corr, use_container_width=True)
        
        # Tabla de correlaciones
        st.markdown("**Tabla de Correlaciones:**")
        correlaciones_df = pd.DataFrame({
            'Variable': correlaciones.index,
            'Correlación': correlaciones.values
        })
        st.dataframe(correlaciones_df, use_container_width=True)
        
        # Scatter plots de las variables más importantes
        st.markdown("#### 📈 Relaciones con la Resistencia")
        
        # Obtener las 4 variables con mayor correlación (excluyendo la resistencia misma)
        top_vars = correlaciones[1:5].index.tolist()
        
        # Crear subplots
        fig_scatter = make_subplots(
            rows=2, cols=2,
            subplot_titles=[f"{var.split('(')[0].strip()}" for var in top_vars],
            specs=[[{"secondary_y": False}, {"secondary_y": False}],
                   [{"secondary_y": False}, {"secondary_y": False}]]
        )
        
        for i, var in enumerate(top_vars):
            row = (i // 2) + 1
            col = (i % 2) + 1
            
            fig_scatter.add_trace(
                go.Scatter(
                    x=df_simulaciones[var],
                    y=df_simulaciones['Predicted Strength (MPa)'],
                    mode='markers',
                    marker=dict(size=4, opacity=0.6),
                    name=var.split('(')[0].strip()
                ),
                row=row, col=col
            )
        
        fig_scatter.update_layout(height=600, title_text="Relaciones entre Variables y Resistencia")
        st.plotly_chart(fig_scatter, use_container_width=True)
        
    else:
        st.info("👆 Ejecuta primero una optimización en la pestaña 'Optimización Automática' para ver los análisis.")

# Sidebar con información adicional
with st.sidebar:
    st.markdown("### ℹ️ Información")
    st.markdown("""
    **¿Cómo funciona?**
    
    🏗️ **Predicción Manual**: Ajusta los ingredientes manualmente y obtén una estimación de la resistencia.
    
    🎯 **Optimización**: El sistema prueba miles de combinaciones para encontrar la mezcla óptima.
    
    📈 **Análisis**: Visualiza las relaciones entre ingredientes y resistencia.
    
    **Factores que afectan la resistencia:**
    - Relación agua-cemento
    - Edad del concreto
    - Tipo y cantidad de aditivos
    - Calidad de los agregados
    """)
    
    st.markdown("### 📊 Métricas de Calidad")
    if 'optimization_results' in st.session_state:
        df_simulaciones = st.session_state['optimization_results']
        
        st.metric("Simulaciones", len(df_simulaciones))
        st.metric("Mejor Resistencia", f"{df_simulaciones['Predicted Strength (MPa)'].max():.2f} MPa")
        st.metric("Promedio", f"{df_simulaciones['Predicted Strength (MPa)'].mean():.2f} MPa")
        st.metric("Desv. Estándar", f"{df_simulaciones['Predicted Strength (MPa)'].std():.2f} MPa")
