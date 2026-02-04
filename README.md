
# Ethiopia Financial Inclusion Forecast (2014–2027)

This project analyzes trends in financial inclusion in Ethiopia and produces scenario-based forecasts for access and usage of financial services through 2027. It includes data exploration, feature engineering, forecasting models, and an interactive Streamlit dashboard for visualization.

---

## 📌 Project Objectives

* Explore historical financial inclusion indicators for Ethiopia
* Enrich raw datasets with reference codes and metadata
* Analyze trends in **account ownership (access)** and **digital payment usage (usage)**
* Engineer features for time-series modeling
* Forecast financial inclusion outcomes for **2025–2027** under multiple scenarios
* Provide an interactive dashboard for policymakers and analysts

---

## 📁 Project Structure

```
ethiopia-fi-forecast/
├── data/
│   ├── raw/
│   │   ├── ethiopia_fi_unified_data.xlsx
│   │   └── reference_codes.xlsx
│   └── processed/
│       └── ethiopia_fi_enriched.csv
├── src/
│   ├── task1_data_exploration_and_enrichment.py
│   ├── task2_exploratory_data_analysis.ipynb
│   ├── task3_feature_engineering.ipynb
│   └── task4_forecasting.ipynb
├── dashboard/
│   └── app.py
├── requirements.txt
└── README.md
```

---

## ⚙️ Setup Instructions

### 1️⃣ Create Virtual Environment (Optional but Recommended)

```bash
python -m venv venv
venv\Scripts\activate   # On Windows
```

### 2️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

If `requirements.txt` is missing, install manually:

```bash
pip install pandas numpy matplotlib seaborn statsmodels scikit-learn streamlit openpyxl
```

---

## ▶️ How to Run Each Task

### ✅ Task 1 – Data Exploration & Enrichment

```bash
python src/task1_data_exploration_and_enrichment.py
```

This loads raw Excel files, cleans and enriches the dataset, and outputs:

```
data/processed/ethiopia_fi_enriched.csv
```

---

### ✅ Task 2 – Exploratory Data Analysis (EDA)

Open and run:

```bash
src/task2_exploratory_data_analysis.ipynb
```

This notebook provides:

* Time-series trends
* Distribution plots
* Gender disaggregation (where available)
* Data quality checks

---

### ✅ Task 3 – Feature Engineering

Open and run:

```bash
src/task3_feature_engineering.ipynb
```

This notebook creates:

* Lag features
* Growth rates
* Policy dummies (e.g., post-Fayda)
* Final modeling dataset

---

### ✅ Task 4 – Forecasting (2025–2027)

Open and run:

```bash
src/task4_forecasting.ipynb
```

This includes:

* Linear trend model
* Log trend model
* Scenario-based forecasts (Optimistic / Base / Pessimistic)
* Visualizations for access and usage

---

### ✅ Task 5 – Interactive Dashboard

Launch the Streamlit app:

```bash
streamlit run dashboard/app.py
```

The dashboard includes:

* Overview metrics
* Trend visualizations
* Forecasts with scenarios
* Progress toward inclusion targets
* Downloadable dataset

---

## 📊 Data Sources

* World Bank Global Findex (2014, 2017, 2021)
* National-level indicators (as provided in raw dataset)
* Reference code mappings for harmonization

---

## ⚠️ Limitations

* Survey data is available only for select years (sparse time series)
* Digital payment usage indicators may be limited or proxied
* Forecasts are scenario-based and not causal predictions
* External macroeconomic and regulatory shocks are not explicitly modeled

---

## 📈 Key Insights

* Account ownership in Ethiopia shows a strong upward trend from 2014–2021.
* Digital payment usage is growing faster than account access, indicating deepening usage among existing users.
* Scenario-based projections suggest Ethiopia may approach, but not fully reach, universal access by 2027 without accelerated policy interventions.

---

## 🧠 Future Work

* Integrate GSMA mobile money transaction volumes
* Include regional disaggregation
* Add causal policy impact models
* Expand dashboard with filters and drill-downs



