import streamlit as st
import pandas as pd
import numpy as np
import joblib
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Page configuration
st.set_page_config(
    page_title="Concrete Strength Optimizer",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load model
@st.cache_resource
def load_model():
    return joblib.load("modelo_resistencia_concreto.pkl")

modelo = load_model()

# Custom CSS to improve appearance
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

# Main title
st.markdown('<h1 class="main-header">🏗️ Concrete Strength Optimizer</h1>', unsafe_allow_html=True)

# Tabs for different functionalities
tab1, tab2, tab3 = st.tabs(["📊 Manual Prediction", "🎯 Automatic Optimization", "📈 Results Analysis"])

with tab1:
    st.markdown("### 🔧 Manual Strength Prediction")
    st.markdown("Adjust your mix ingredients and estimate concrete strength.")

    # Create two columns for sliders
    col1, col2 = st.columns(2)
    
    with col1:
        cement = st.slider("Cement (kg/m³)", 100, 400, 300, help="Portland cement quantity")
        slag = st.slider("Blast furnace slag (kg/m³)", 0, 100, 0, help="Blast furnace slag as additive")
        fly_ash = st.slider("Fly ash (kg/m³)", 0, 100, 0, help="Fly ash as additive")
        water = st.slider("Water (kg/m³)", 100, 250, 180, help="Water quantity in the mix")
    
    with col2:
        superplasticizer = st.slider("Superplasticizer (kg/m³)", 0, 25, 0, help="Superplasticizer additive")
        coarse_agg = st.slider("Coarse aggregate (kg/m³)", 700, 1100, 950, help="Coarse aggregate (gravel)")
        fine_agg = st.slider("Fine aggregate (kg/m³)", 500, 1000, 700, help="Fine aggregate (sand)")
        age = st.slider("Age (days)", 1, 90, 28, help="Concrete age for testing")

    # Create DataFrame for the model
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

    # Prediction
    if st.button("🔮 Predict Strength", type="primary"):
        resultado = modelo.predict(entrada)[0]
        
        # Show result with metrics
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Estimated Strength", f"{resultado:.2f} MPa")
        
        with col2:
            # Classify strength
            if resultado < 20:
                clasificacion = "Low"
                color = "red"
            elif resultado < 35:
                clasificacion = "Medium"
                color = "orange"
            else:
                clasificacion = "High"
                color = "green"
            st.metric("Classification", clasificacion)
        
        with col3:
            st.metric("W/C Ratio", f"{water/cement:.2f}")

with tab2:
    st.markdown("### 🎯 Automatic Mix Optimization")
    st.markdown("Find the best combination of ingredients to maximize strength.")
    
    # Optimization configuration
    st.markdown("#### ⚙️ Range Configuration")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Material Ranges:**")
        cement_min, cement_max = st.slider("Cement (kg/m³)", 250, 400, (250, 350), key="cement_opt")
        slag_min, slag_max = st.slider("Slag (kg/m³)", 0, 100, (0, 50), key="slag_opt")
        fly_ash_min, fly_ash_max = st.slider("Fly ash (kg/m³)", 0, 100, (0, 30), key="fly_opt")
        water_min, water_max = st.slider("Water (kg/m³)", 150, 200, (160, 190), key="water_opt")
    
    with col2:
        st.markdown("**Additional Ranges:**")
        super_min, super_max = st.slider("Superplasticizer (kg/m³)", 0, 25, (0, 10), key="super_opt")
        coarse_min, coarse_max = st.slider("Coarse aggregate (kg/m³)", 800, 1100, (900, 1000), key="coarse_opt")
        fine_min, fine_max = st.slider("Fine aggregate (kg/m³)", 600, 900, (650, 750), key="fine_opt")
        age_min, age_max = st.slider("Age (days)", 3, 28, (7, 28), key="age_opt")
    
    # Simulation parameters
    n_simulaciones = st.slider("Number of simulations", 100, 5000, 1000, step=100)
    semilla = st.number_input("Random seed", value=91, min_value=1, max_value=999)
    
    if st.button("🚀 Run Optimization", type="primary"):
        with st.spinner("Running optimization..."):
            # Set seed
            np.random.seed(semilla)
            
            # Define material ranges
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
            
            # Generate simulations
            simulaciones = []
            for _ in range(n_simulaciones):
                mezcla = {
                    ingrediente: np.random.uniform(rango[0], rango[1])
                    for ingrediente, rango in materiales_disponibles.items()
                }
                simulaciones.append(mezcla)
            
            # Convert to DataFrame
            df_simulaciones = pd.DataFrame(simulaciones)
            
            # Predict strength
            df_simulaciones['Predicted Strength (MPa)'] = modelo.predict(df_simulaciones)
            
            # Get best mix
            mejor_mezcla = df_simulaciones.loc[df_simulaciones['Predicted Strength (MPa)'].idxmax()]
            
            # Save results in session state
            st.session_state['optimization_results'] = df_simulaciones
            st.session_state['best_mix'] = mejor_mezcla
            
            # Show results
            st.success("✅ Optimization completed!")
            
            # Main metrics
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Best Strength", f"{mejor_mezcla['Predicted Strength (MPa)']:.2f} MPa")
            
            with col2:
                st.metric("Average Strength", f"{df_simulaciones['Predicted Strength (MPa)'].mean():.2f} MPa")
            
            with col3:
                st.metric("Maximum Strength", f"{df_simulaciones['Predicted Strength (MPa)'].max():.2f} MPa")
            
            with col4:
                st.metric("Minimum Strength", f"{df_simulaciones['Predicted Strength (MPa)'].min():.2f} MPa")
            
            # Show best mix
            st.markdown("#### 🏆 Best Mix Found")
            
            # Create DataFrame to show best mix
            mejor_mezcla_display = pd.DataFrame({
                'Ingredient': [
                    'Cement', 'Blast furnace slag', 'Fly ash', 'Water',
                    'Superplasticizer', 'Coarse aggregate', 'Fine aggregate', 'Age'
                ],
                'Quantity': [
                    mejor_mezcla['Cement (component 1)(kg in a m^3 mixture)'],
                    mejor_mezcla['Blast Furnace Slag (component 2)(kg in a m^3 mixture)'],
                    mejor_mezcla['Fly Ash (component 3)(kg in a m^3 mixture)'],
                    mejor_mezcla['Water  (component 4)(kg in a m^3 mixture)'],
                    mejor_mezcla['Superplasticizer (component 5)(kg in a m^3 mixture)'],
                    mejor_mezcla['Coarse Aggregate  (component 6)(kg in a m^3 mixture)'],
                    mejor_mezcla['Fine Aggregate (component 7)(kg in a m^3 mixture)'],
                    mejor_mezcla['Age (day)']
                ],
                'Unit': ['kg/m³', 'kg/m³', 'kg/m³', 'kg/m³', 'kg/m³', 'kg/m³', 'kg/m³', 'days']
            })
            
            st.dataframe(mejor_mezcla_display, use_container_width=True)

with tab3:
    st.markdown("### 📈 Results Analysis")
    
    if 'optimization_results' in st.session_state:
        df_simulaciones = st.session_state['optimization_results']
        mejor_mezcla = st.session_state['best_mix']
        
        # Descriptive statistics
        st.markdown("#### 📊 Strength Statistics")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Strength histogram
            fig_hist = px.histogram(
                df_simulaciones, 
                x='Predicted Strength (MPa)',
                nbins=30,
                title="Strength Distribution",
                color_discrete_sequence=['#667eea']
            )
            fig_hist.update_layout(showlegend=False)
            st.plotly_chart(fig_hist, use_container_width=True)
        
        with col2:
            # Box plot
            fig_box = px.box(
                df_simulaciones,
                y='Predicted Strength (MPa)',
                title="Strength Distribution (Box Plot)",
                color_discrete_sequence=['#764ba2']
            )
            st.plotly_chart(fig_box, use_container_width=True)
        
        # Correlation analysis
        st.markdown("#### 🔍 Correlation Analysis")
        
        # Calculate correlations
        correlaciones = df_simulaciones.corr()['Predicted Strength (MPa)'].sort_values(ascending=False)
        
        # Correlation chart
        fig_corr = px.bar(
            x=correlaciones.index,
            y=correlaciones.values,
            title="Correlation with Strength",
            color=correlaciones.values,
            color_continuous_scale='RdBu'
        )
        fig_corr.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(fig_corr, use_container_width=True)
        
        # Correlation table
        st.markdown("**Correlation Table:**")
        correlaciones_df = pd.DataFrame({
            'Variable': correlaciones.index,
            'Correlation': correlaciones.values
        })
        st.dataframe(correlaciones_df, use_container_width=True)
        
        # Scatter plots of most important variables
        st.markdown("#### 📈 Relationships with Strength")
        
        # Get the 4 variables with highest correlation (excluding strength itself)
        top_vars = correlaciones[1:5].index.tolist()
        
        # Create subplots
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
        
        fig_scatter.update_layout(height=600, title_text="Relationships between Variables and Strength")
        st.plotly_chart(fig_scatter, use_container_width=True)
        
    else:
        st.info("👆 First run an optimization in the 'Automatic Optimization' tab to see the analysis.")

# Sidebar with additional information
with st.sidebar:
    st.markdown("### ℹ️ Information")
    st.markdown("""
    **How does it work?**
    
    🏗️ **Manual Prediction**: Manually adjust ingredients and get a strength estimate.
    
    🎯 **Optimization**: The system tests thousands of combinations to find the optimal mix.
    
    📈 **Analysis**: Visualize relationships between ingredients and strength.
    
    **Factors affecting strength:**
    - Water-cement ratio
    - Concrete age
    - Type and amount of additives
    - Aggregate quality
    """)
    
    st.markdown("### 📊 Quality Metrics")
    if 'optimization_results' in st.session_state:
        df_simulaciones = st.session_state['optimization_results']
        
        st.metric("Simulations", len(df_simulaciones))
        st.metric("Best Strength", f"{df_simulaciones['Predicted Strength (MPa)'].max():.2f} MPa")
        st.metric("Average", f"{df_simulaciones['Predicted Strength (MPa)'].mean():.2f} MPa")
        st.metric("Std. Dev.", f"{df_simulaciones['Predicted Strength (MPa)'].std():.2f} MPa")
