<div align="center">

<img src="assets/logo.svg" width="64" height="64" alt="RelocationDevs Logo" />

# RelocationDevs

**Herramienta de decisión para reubicación internacional de profesionales tech**

*by a Cambeiro*

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://relocationdevs.streamlit.app)
[![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python)](https://www.python.org/)
[![scikit-learn](https://img.shields.io/badge/scikit--learn-1.3-orange?logo=scikit-learn)](https://scikit-learn.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.25-red?logo=streamlit)](https://streamlit.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

</div>

---

## ¿Qué es RelocationDevs?

RelocationDevs es un **data product interactivo** que ayuda a developers, data scientists e ingenieros a tomar decisiones de reubicación internacional basadas en datos reales.

> *"¿A qué ciudad debería mudarme como profesional tech, teniendo en cuenta mi salario esperado, el coste de vida, los impuestos y el mercado laboral?"*

La app combina fuentes de datos públicas, indicadores derivados y un modelo de predicción salarial para responder esa pregunta de forma personalizada.

---

## Demo

🌍 **[Abrir la app en Streamlit Cloud](https://relocationdevs.streamlit.app)**

---

## Módulos

| Módulo | Descripción |
|--------|-------------|
| 🏠 **Pantalla de bienvenida** | Define tu perfil profesional — rol, experiencia, educación, país de origen |
| 🗺️ **City Explorer** | Ranking visual de ciudades por Relocation Score con tabla filtrable |
| ⚖️ **City Comparison** | Compara ciudades con barras por métrica y radar chart normalizado |
| 🌐 **Mapa interactivo** | Mapa Folium con CartoDB Dark Matter, clustering y popups detallados |
| 🔍 **Buscador de ciudad ideal** | Wizard 3 pasos con radar pentagonal de prioridades y scoring personalizado |
| 💰 **Salary Estimator** | Predicción salarial basada en tu perfil con modelo GBR |
| 📄 **Informe PDF** | Poster DIN A4 horizontal con fotos de ciudades, donuts de distribución salarial y consideraciones clave |

---

## Stack tecnológico

| Capa | Tecnología |
|------|------------|
| Lenguaje | Python 3.11 |
| Datos | pandas, numpy |
| Machine Learning | scikit-learn (GradientBoostingRegressor) |
| Visualización | Plotly, Folium, PyDeck |
| App | Streamlit |
| Storage | CSV, Parquet |
| Mapa | Folium + CartoDB Dark Matter |
| PDF | HTML + kaleido |

---

## Fuentes de datos

| Fuente | Dataset | Qué aporta |
|--------|---------|------------|
| Kaggle | cost-of-living-index-by-city-2022 | Índices de coste de vida, alquiler y poder adquisitivo — 578 ciudades |
| Stack Overflow | Developer Survey 2023 | Salarios reales de 18.112 developers en 149 países |
| OECD | Tax Database TABLE_I7 | Tipos impositivos marginales por país |
| Kaggle | world-cities-database | Coordenadas geográficas de 43.000+ ciudades |
| Wikipedia REST API | Page summaries | Fotos de ciudades para el informe PDF |

---

## Indicadores derivados

RelocationDevs no muestra datos crudos. Calcula indicadores propios:

| Indicador | Fórmula |
|-----------|---------|
| Salario neto | `gross_salary × (1 - tax_rate / 100)` |
| Poder adquisitivo | `net_salary / cost_of_living_index` |
| Alquiler en EUR | `NYC_RENT_EUR × (rent_index / nyc_rent_index)` |
| Ahorro anual | `net_salary × 0.30` |
| Relocation Score | `ppi×0.30 + job×0.25 + qol×0.25 + (100-tax)×0.20` |

---

## Modelo ML

- **Problema**: regresión supervisada — predicción de salario bruto anual en EUR
- **Algoritmo**: GradientBoostingRegressor (scikit-learn)
- **Features**: país, rol, especialización, nivel educativo, años de experiencia
- **Dataset**: 18.112 registros — Stack Overflow Developer Survey 2023
- **Métricas**: MAE €29.022 · R² 0.53
- **Pipeline**: OneHotEncoder + StandardScaler + GradientBoostingRegressor

El MAE refleja la alta variabilidad geográfica del dataset (149 países, rango €8k–€150k). La limitación está documentada y comunicada al usuario en la app.

---

## Arquitectura

```
Fuentes externas  (Kaggle · Stack Overflow · OECD · worldcitiespop)
       ↓
    data/raw/      (datos originales — nunca se modifican)
       ↓
  notebooks/       (limpieza · fusión · EDA · modelado)
       ↓
 data/processed/   (datasets listos para la app)
    models/        (artefactos ML serializados)
       ↓
      app/         (Streamlit — solo consume, no transforma)
```

### Estructura de carpetas

```
RelocationDevs/
├── app/
│   ├── main.py              # Punto de entrada + perfil de usuario
│   ├── styles.py            # Sistema de diseño Midnight Silver
│   ├── city_explorer.py     # Ranking visual de ciudades
│   ├── comparison.py        # Comparación con radar chart
│   ├── city_map.py          # Mapa interactivo Folium
│   ├── city_finder.py       # Buscador wizard con radar pentagonal
│   ├── salary_est.py        # Estimador salarial
│   └── pdf_generator.py     # Generador de poster HTML/PDF
├── src/
│   ├── data_loader.py       # Carga y guardado de datasets
│   ├── indicators.py        # Cálculo de indicadores derivados
│   ├── model.py             # Pipeline ML: train/predict/save/load
│   └── utils.py             # Utilidades compartidas
├── notebooks/
│   ├── 00_build_cities.ipynb   # Fusión de 4 fuentes → cities.csv
│   ├── 01_eda.ipynb            # Análisis exploratorio
│   ├── 02_indicators.ipynb     # Indicadores → cities_processed.csv
│   └── 03_modeling.ipynb       # Entrenamiento → salary_model.pkl
├── data/
│   ├── raw/                 # Datos originales (no versionados)
│   ├── interim/             # Datos en proceso
│   └── processed/           # Datasets finales (versionados)
├── models/
│   └── salary_model.pkl     # Modelo entrenado
├── assets/
│   └── logo.svg             # Logo de la app
├── requirements.txt
├── packages.txt
└── .streamlit/
    └── config.toml
```

---

## Instalación local

```bash
# 1. Clonar el repositorio
git clone https://github.com/Udamian/RelocationDevs.git
cd RelocationDevs

# 2. Crear entorno virtual
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Ejecutar la app
python -m streamlit run app/main.py
```

> **Nota**: Los datos raw no están versionados por su tamaño. Consulta la sección de fuentes de datos para descargarlos y ejecuta los notebooks en orden (00 → 01 → 02 → 03) para regenerar los datasets procesados.

---

## Orden de ejecución de notebooks

```
00_build_cities.ipynb   →  data/processed/cities.csv
01_eda.ipynb            →  análisis exploratorio (sin output)
02_indicators.ipynb     →  data/processed/cities_processed.csv
03_modeling.ipynb       →  data/processed/salaries.csv + models/salary_model.pkl
```

---

## Diseño

El sistema de diseño **Midnight Silver** está implementado en `app/styles.py`:

- Fondo: `#111111` — negro profundo
- Superficie: `#1c1c1e` — gris oscuro Apple
- Texto: `#f5f5f7` — blanco Apple
- Secundario: `#aeaeb2` — gris platino
- Terciario: `#6e6e73` — gris medio

---

## Posicionamiento académico

| Categoría | Descripción |
|-----------|-------------|
| **Área principal** | Business Intelligence y Analítica Predictiva |
| **Subcategoría** | Decision Support Systems (DSS) |
| **Elementos adicionales** | Multi-source analytics · Predictive modeling · Applied AI · Data product design |

---

## Prioridades del proyecto

1. **Claridad** — el código y los indicadores son comprensibles
2. **Utilidad** — cada feature responde a una pregunta real del usuario
3. **Calidad de datos** — las limitaciones están documentadas
4. **Interpretabilidad** — el modelo y los indicadores son explicables
5. **Impacto visual** — la app parece un producto, no un notebook

---

## Autor

**a Cambeiro** — Junior Developer · Big Data & Data Analysis

[![GitHub](https://img.shields.io/badge/GitHub-Udamian-black?logo=github)](https://github.com/Udamian/RelocationDevs)

---

<div align="center">
<sub>RelocationDevs · by a Cambeiro · 2025</sub>
</div>
