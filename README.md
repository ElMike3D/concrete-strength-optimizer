# 🏗️ Optimizador de Concreto

Aplicación web para predecir y optimizar la resistencia del concreto usando machine learning.

## 🚀 Características

- **Predicción Manual**: Ajusta ingredientes y obtén estimaciones de resistencia
- **Optimización Automática**: Encuentra la mejor mezcla mediante simulación
- **Análisis Visual**: Gráficos interactivos y análisis de correlaciones
- **Interfaz Moderna**: Diseño atractivo y fácil de usar

## 📦 Instalación Local

1. **Clona el repositorio:**
```bash
git clone <tu-repositorio>
cd <tu-repositorio>
```

2. **Instala las dependencias:**
```bash
pip install -r requirements.txt
```

3. **Ejecuta la aplicación:**
```bash
streamlit run streamlit_app.py
```

## 🌐 Deployment

### Opción 1: Streamlit Cloud (Recomendado)

1. **Sube tu código a GitHub**
2. **Ve a [share.streamlit.io](https://share.streamlit.io)**
3. **Conecta tu repositorio de GitHub**
4. **Selecciona el archivo principal:** `streamlit_app.py`
5. **¡Listo!** Tu app estará disponible en línea

### Opción 2: Heroku

1. **Instala Heroku CLI**
2. **Crea un archivo `Procfile`:**
```
web: streamlit run streamlit_app.py --server.port=$PORT --server.address=0.0.0.0
```

3. **Deploy:**
```bash
heroku create tu-app-nombre
git add .
git commit -m "Initial commit"
git push heroku main
```

### Opción 3: Railway

1. **Conecta tu repositorio a Railway**
2. **Railway detectará automáticamente que es una app Python**
3. **Configura las variables de entorno si es necesario**

## 📁 Estructura del Proyecto

```
├── streamlit_app.py          # Aplicación principal
├── modelo_resistencia_concreto.pkl  # Modelo entrenado
├── requirements.txt          # Dependencias
├── README.md                # Este archivo
└── CCPP.csv                 # Datos de entrenamiento (opcional)
```

## 🔧 Configuración del Modelo

El modelo se carga automáticamente desde `modelo_resistencia_concreto.pkl`. Asegúrate de que este archivo esté en el directorio raíz del proyecto.

## 📊 Variables del Modelo

- **Cemento** (kg/m³)
- **Escoria de alto horno** (kg/m³)
- **Ceniza volante** (kg/m³)
- **Agua** (kg/m³)
- **Aditivo plastificante** (kg/m³)
- **Agregado grueso** (kg/m³)
- **Agregado fino** (kg/m³)
- **Edad** (días)

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor, abre un issue o pull request.

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. 