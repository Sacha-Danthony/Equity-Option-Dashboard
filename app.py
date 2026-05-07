import numpy as np
from scipy.stats import norm
import streamlit as st

def bs_price(S, K, r, T, sigma, q=0.0, option_type="call"):
    if T <= 0:
        intrinsic = max(S - K, 0) if option_type == "call" else max(K - S, 0)
        return {"price": intrinsic, "delta": None, "gamma": None, "vega": None}
    if sigma <= 0:
        return {"price": 0, "delta": None, "gamma": None, "vega": None}

    d1 = (np.log(S / K) + (r - q + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)

    if option_type == "call":
        price = S * np.exp(-q * T) * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
        delta = np.exp(-q * T) * norm.cdf(d1)
    else:
        price = K * np.exp(-r * T) * norm.cdf(-d2) - S * np.exp(-q * T) * norm.cdf(-d1)
        delta = -np.exp(-q * T) * norm.cdf(-d1)

    gamma = (norm.pdf(d1) * np.exp(-q * T)) / (S * sigma * np.sqrt(T))
    vega  = S * np.exp(-q * T) * np.sqrt(T) * norm.pdf(d1) / 100

    return {"price": round(price, 2), "delta": round(delta, 4),
            "gamma": round(gamma, 6), "vega": round(vega, 2)}

# Interface Streamlit
st.title("Equity Option Scenario Analysis Dashboard")
st.subheader("Paramètres de l'option")

S = st.slider("Prix S&P 500", 4800, 5200, 5000)
K = st.slider("Strike", 4500, 5500, 5000)
sigma = st.slider("Volatilité (%)", 15, 25, 20) / 100
option_type = st.selectbox("Type d'option", ["call", "put"])

r = 0.02
q = 0.01
T = 1.0

result = bs_price(S, K, r, T, sigma, q, option_type)

st.subheader("Résultats")
st.metric("Prix", f"${result['price']}")
st.metric("Delta", result['delta'])
st.metric("Gamma", result['gamma'])
st.metric("Vega", result['vega'])

import matplotlib.pyplot as plt

# Graphique payoff
st.subheader("Payoff à maturité")

S_range = np.linspace(4000, 6000, 200)

if option_type == "call":
    payoff = np.maximum(S_range - K, 0)
else:
    payoff = np.maximum(K - S_range, 0)

fig, ax = plt.subplots()
ax.plot(S_range, payoff, label=f"Payoff {option_type}", color="blue", linewidth=2)
ax.axvline(x=K, color="red", linestyle="--", label=f"Strike K={K}")
ax.axvline(x=S, color="green", linestyle="--", label=f"Spot actuel S={S}")
ax.set_xlabel("Prix S&P 500 à maturité")
ax.set_ylabel("Payoff ($)")
ax.set_title("Payoff de l'option à maturité")
ax.legend()
ax.grid(True)

st.pyplot(fig)

# Scénarios
st.subheader("Analyse de scénarios")

scenarios = {
    "-20%": S * 0.80,
    "-10%": S * 0.90,
    "+10%": S * 1.10,
    "+20%": S * 1.20,
}

scenario_data = []
for label, S_scenario in scenarios.items():
    res = bs_price(S_scenario, K, r, T, sigma, q, option_type)
    payoff = max(S_scenario - K, 0) if option_type == "call" else max(K - S_scenario, 0)
    scenario_data.append({
        "Scénario": label,
        "Prix S&P 500": f"{S_scenario:.0f}",
        "Valeur option": f"${res['price']}",
        "Payoff à maturité": f"${payoff:.0f}",
        "Delta": res['delta']
    })

import pandas as pd
df = pd.DataFrame(scenario_data)
st.table(df)

# Texte pitch client
st.subheader("Pitch client")
protection = max(K - S * 0.90, 0)
st.info(f"""
**Recommandation pour votre client :**
- Ce {option_type} coûte **${result['price']}** aujourd'hui
- Il protège contre une baisse jusqu'à **{K}** points sur le S&P 500
- En cas de chute de 10% (S&P à {S*0.90:.0f}), votre option vaut **${bs_price(S*0.90, K, r, T, sigma, q, option_type)['price']}**
- Le delta de **{result['delta']}** signifie que pour chaque point gagné sur le S&P, l'option gagne **${result['delta']}**
""") 


