import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import statsmodels.api as sm
from pathlib import Path

st.set_page_config(page_title="Ethiopia Financial Inclusion Forecast", layout="wide")

BASE_DIR = Path(__file__).resolve().parents[1]   # project root
DATA_PATH = BASE_DIR / "data" / "processed" / "ethiopia_fi_enriched.csv"

@st.cache_data
def load_data():
    df = pd.read_csv(DATA_PATH)
    df["observation_date"] = pd.to_datetime(df["observation_date"], errors="coerce")
    return df

df = load_data()

# -------------------------
# Helpers
# -------------------------
def get_access_series(df):
    acc = df[
        (df["indicator_code"] == "ACC_OWNERSHIP") &
        (df["record_type"] == "observation") &
        (df["gender"].astype(str).str.lower() == "all")
    ].copy()
    acc["year"] = acc["observation_date"].dt.year
    acc = acc.sort_values("year")
    return acc[["year", "value_numeric"]]

def get_usage_series(df):
    usage = df[
        (df["record_type"] == "observation") &
        (
            df["indicator"].str.contains("payment|digital|mobile", case=False, na=False) |
            df["indicator_code"].str.contains("PAY|DIG|MOB", case=False, na=False)
        )
    ].copy()

    usage["year"] = pd.to_datetime(usage["observation_date"], errors="coerce").dt.year
    usage = usage.dropna(subset=["year", "value_numeric"])
    usage = usage.groupby("year", as_index=False)["value_numeric"].mean()
    usage = usage.sort_values("year")

    return usage


def forecast_access(acc, years=[2025, 2026, 2027]):
    future = pd.DataFrame({"year": years})
    X = sm.add_constant(acc["year"])
    y = acc["value_numeric"]
    model_lin = sm.OLS(y, X).fit()
    Xf = sm.add_constant(future["year"])
    lin_pred = model_lin.predict(Xf)

    base_year = acc["year"].min() - 1
    acc["t"] = acc["year"] - base_year
    acc["log_t"] = np.log(acc["t"])
    Xlog = sm.add_constant(acc["log_t"])
    model_log = sm.OLS(y, Xlog).fit()
    future["t"] = future["year"] - base_year
    future["log_t"] = np.log(future["t"])

    base_slope = model_log.params["log_t"]
    scenarios = {"Pessimistic": base_slope * 0.7, "Base": base_slope, "Optimistic": base_slope * 1.3}

    last_log_t = acc["log_t"].iloc[-1]
    last_val = acc["value_numeric"].iloc[-1]

    scen = {}
    for k, s in scenarios.items():
        intercept = last_val - s * last_log_t
        scen[k] = intercept + s * future["log_t"]

    return future, lin_pred, scen

def forecast_usage(usage, years=[2025, 2026, 2027]):
    if len(usage) < 2:
        return pd.Series([np.nan]*len(years))
    X = sm.add_constant(usage["year"])
    y = usage["value_numeric"]
    model = sm.OLS(y, X).fit()
    future = pd.DataFrame({"year": years})
    Xf = sm.add_constant(future["year"])
    return model.predict(Xf)

# -------------------------
# Sidebar
# -------------------------
st.sidebar.title("Controls")
page = st.sidebar.radio("Navigate", ["Overview", "Trends", "Forecasts", "Inclusion Projections", "Data Download"])

# -------------------------
# Pages
# -------------------------
acc = get_access_series(df)
usage = get_usage_series(df)

latest_access = acc.iloc[-1]["value_numeric"] if len(acc) else np.nan
latest_year = acc.iloc[-1]["year"] if len(acc) else None

# --- Overview ---
if page == "Overview":
    st.title("Ethiopia – Financial Inclusion Dashboard")

    c1, c2, c3 = st.columns(3)
    c1.metric("Latest Access (Account Ownership)", f"{latest_access:.1f}%" if pd.notna(latest_access) else "N/A")
    c2.metric("Latest Year (Findex)", f"{int(latest_year)}" if latest_year else "N/A")
    c3.metric("Trend (2011–2024)", "Upward (slowing)")

    st.subheader("Key Notes")
    st.write("- Mobile money growth has outpaced increases in account ownership.")
    st.write("- Interoperability and Digital ID expected to deepen usage more than access.")

# --- Trends ---
elif page == "Trends":
    st.title("Trends")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Access – Account Ownership")
        fig, ax = plt.subplots()
        ax.plot(acc["year"], acc["value_numeric"], marker="o")
        ax.set_xlabel("Year")
        ax.set_ylabel("% of Adults")
        st.pyplot(fig)

    with col2:
        st.subheader("Usage – Digital Payments")
        fig, ax = plt.subplots()
        ax.plot(usage["year"], usage["value_numeric"], marker="o", color="green")
        ax.set_xlabel("Year")
        ax.set_ylabel("% of Adults")
        st.pyplot(fig)

# --- Forecasts ---
elif page == "Forecasts":
    st.title("Forecasts (2025–2027)")
    years = st.multiselect("Forecast Years", [2025, 2026, 2027], default=[2025, 2026, 2027])
    future, lin_pred, scen = forecast_access(acc, years)
    usage_pred = forecast_usage(usage, years)

    st.subheader("Access Forecast – Scenarios")
    fig, ax = plt.subplots()
    ax.plot(acc["year"], acc["value_numeric"], "o-", label="Observed")
    ax.plot(future["year"], scen["Base"], "o--", label="Base")
    ax.fill_between(future["year"], scen["Pessimistic"], scen["Optimistic"], alpha=0.2, label="Scenario Range")
    ax.legend()
    ax.set_xlabel("Year")
    ax.set_ylabel("% of Adults")
    st.pyplot(fig)

    st.subheader("Usage Forecast – Linear Trend")
    fig, ax = plt.subplots()
    ax.plot(usage["year"], usage["value_numeric"], "o-", label="Observed")
    ax.plot(future["year"], usage_pred, "o--", label="Forecast")
    ax.legend()
    ax.set_xlabel("Year")
    ax.set_ylabel("% of Adults")
    st.pyplot(fig)

    table = pd.DataFrame({
        "year": future["year"],
        "access_base": scen["Base"].values,
        "access_optimistic": scen["Optimistic"].values,
        "access_pessimistic": scen["Pessimistic"].values,
        "usage_linear": usage_pred.values if hasattr(usage_pred, "values") else usage_pred
    })
    st.dataframe(table)

# --- Inclusion Projections ---
elif page == "Inclusion Projections":
    st.title("Progress Toward 60% Access Target")
    target = 60.0
    years = [2025, 2026, 2027]
    future, _, scen = forecast_access(acc, years)

    fig, ax = plt.subplots()
    ax.plot(acc["year"], acc["value_numeric"], "o-", label="Observed")
    ax.plot(future["year"], scen["Base"], "o--", label="Base Forecast")
    ax.axhline(target, linestyle="--", color="red", label="60% Target")
    ax.legend()
    ax.set_xlabel("Year")
    ax.set_ylabel("% of Adults")
    st.pyplot(fig)

    st.write("Under the base scenario, Ethiopia approaches—but may not reach—60% by 2027.")

# --- Data Download ---
elif page == "Data Download":
    st.title("Download Data")
    st.download_button(
        "Download Enriched Dataset (CSV)",
        df.to_csv(index=False).encode("utf-8"),
        file_name="ethiopia_fi_enriched.csv",
        mime="text/csv",
    )
    st.dataframe(df.head(50))
