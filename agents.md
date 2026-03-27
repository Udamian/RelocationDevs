# AGENTS.md â€” Relocation Devs

Decisiones de arquitectura, stack y prioridades del proyecto.

## Stack
Python Â· pandas Â· numpy Â· scikit-learn Â· Plotly Â· Streamlit

## Prioridades
1. Claridad  2. Utilidad  3. Calidad de datos  4. Interpretabilidad

## Fuentes de datos planificadas
- Numbeo -> coste de vida, alquiler, poder adquisitivo
- OECD   -> indicadores fiscales y economicos
- World Bank -> macroeconomia
- Eurostat   -> mercado laboral europeo
# AGENTS.md — Relocation Devs

## 1. Project Overview

**Relocation Devs** is a data analysis and decision-support project designed to help technology professionals evaluate and compare cities when considering international relocation.

The platform combines public and open datasets to analyze:

- tech salaries
- cost of living
- taxation
- purchasing power
- job market attractiveness

The final goal is to provide an **interactive data product** where users can compare cities and estimate their economic situation based on their professional profile.

---

## 2. Main Objective

Build a data-driven application that helps developers and tech workers answer:

> “Which city is better for me to relocate to, based on salary, taxes, cost of living, and job opportunities?”

---

## 3. Target User

Primary target users:

- software developers
- data professionals
- IT workers
- tech professionals considering relocation

Secondary users:

- students exploring tech job markets
- recruiters or analysts interested in salary and relocation trends

---

## 4. Core Functionalities

The application should include these main modules:

### 4.1 City Explorer
Allows users to explore relevant city-level indicators such as:

- average tech salary
- cost of living
- rent level
- taxation
- purchasing power

### 4.2 City Comparison
Allows comparing multiple cities side by side.

Example:
- Berlin vs Dubai vs Amsterdam

### 4.3 Salary Estimator
A simple interactive questionnaire where the user provides:

- years of experience
- role / job title
- tech specialization
- city of destination

The system estimates:

- expected salary
- estimated net salary
- estimated purchasing power

### 4.4 Interactive Visualization
The application should include:

- charts
- rankings
- comparisons
- optionally a world/city map

---

## 5. Scope of the Project

### Included
- data collection from multiple open/public sources
- data cleaning and integration
- exploratory data analysis (EDA)
- derived business indicators
- salary prediction model
- interactive web-style application

### Not Included
- real-time job scraping infrastructure at scale
- immigration/legal advice
- visa recommendation engine
- full production-grade backend architecture
- user authentication / account system

This is an academic and portfolio-oriented **data product prototype**, not a commercial SaaS.

---

## 6. Data Sources (Planned)

Potential data sources include:

- **Numbeo** → cost of living, rent, purchasing power
- **OECD** → tax and economic indicators
- **World Bank** → macroeconomic indicators
- **Eurostat** → European labor/economic indicators
- open salary datasets for developers / tech roles
- open job market datasets (if available)

The project may also use curated CSV datasets when APIs are not available.

---

## 7. Main Data Entities

Likely key entities in the project:

### City
Fields may include:
- city_name
- country
- region
- average_salary
- average_rent
- tax_rate
- cost_of_living_index
- purchasing_power_index
- quality_of_life_index
- job_market_score

### User Profile
Fields may include:
- years_experience
- role
- specialization
- education_level
- target_city

### Prediction Output
Fields may include:
- predicted_salary
- estimated_net_salary
- estimated_annual_expenses
- estimated_savings
- relocation_score

---

## 8. Analytical Approach

The project should combine:

### Descriptive Analytics
To answer:
- what is the salary level in each city?
- what is the cost of living?
- how do cities compare?

### Diagnostic Analytics
To answer:
- why does one city provide more purchasing power than another?

### Predictive Analytics
To answer:
- what salary could a user expect in a given city?

This should position the project as a **Decision Support System (DSS)**.

---

## 9. Derived Indicators

The project should create custom indicators, not just display raw data.

Examples:

### Estimated Net Salary
gross_salary adjusted by tax rate

### Estimated Purchasing Power
net_salary / cost_of_living

### Estimated Annual Savings
net_salary - estimated_annual_expenses

### Relocation Score
Composite score based on:
- salary
- taxes
- cost of living
- job market attractiveness

This score should be explainable and transparent.

---

## 10. Machine Learning Component

A salary prediction model should be included.

### Problem Type
Supervised learning — regression

### Possible Input Features
- years_experience
- role
- specialization
- city
- education_level
- remote / on-site (optional)

### Possible Models
Start simple and interpretable:
- Linear Regression
- Random Forest Regressor
- Gradient Boosting Regressor

### Expected Output
- estimated annual salary

The model should prioritize **clarity and interpretability** over unnecessary complexity.

---

## 11. Recommended Tech Stack

### Core Language
- Python

### Data Processing
- pandas
- numpy

### Machine Learning
- scikit-learn

### Visualization
Preferred options:
- Plotly
- Altair
- PyDeck / Folium (if map is included)

### App Layer
Preferred options:
- Streamlit
- Dash

### Storage (optional)
- CSV / Parquet initially
- SQLite or PostgreSQL if needed

---

## 12. UX / Product Direction

The project should feel like a **data product**, not just a notebook.

Desired UX characteristics:

- clean and modern
- easy to understand
- useful for decision making
- interactive but not overloaded

The app should answer user questions quickly:
- “How much could I earn there?”
- “Would I save more money there?”
- “Is it worth relocating?”

---

## 13. Academic Positioning

This project is intended to fit within:

### Main Category
**Business Intelligence and Predictive Analytics**

### Relevant Subcategory
**Decision Support Systems (DSS)**

It also includes elements of:

- multi-source business analytics
- predictive modeling
- applied AI
- practical data product design

---

## 14. Deliverables

Expected deliverables may include:

- cleaned integrated dataset
- exploratory analysis notebook(s)
- salary prediction model
- interactive application
- visual dashboard
- project documentation
- portfolio-ready GitHub repository

---

## 15. Project Priorities

When making implementation decisions, prioritize in this order:

1. **Clarity**
2. **Usefulness**
3. **Data quality**
4. **Interpretability**
5. **Visual impact**
6. **Technical sophistication**

This means:
- avoid overengineering
- avoid unnecessary ML complexity
- prefer explainable indicators and useful comparisons

---

## 16. Important Constraints

- Data availability may limit granularity by city
- Salary datasets may require harmonization across countries
- Tax estimation may need simplification
- Cost-of-living data may vary in methodology between sources

Any simplifications should be clearly documented.

---

## 17. What This Project Should Feel Like

The final result should feel like:

> a relocation intelligence dashboard for tech professionals

Not:
- a generic school dashboard
- a random salary chart collection
- a pure ML experiment without product value

---

## 18. Guiding Principle

If a feature or analysis does not help answer:

> “Should I relocate to this city as a tech professional?”

then it is probably out of scope.
