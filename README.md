# 📊 Equity Option Scenario Analysis Dashboard

Dashboard interactif de pricing d'options vanilla sur le S&P 500, 
développé dans le cadre d'un projet Finance de Marché (M1 ESLSCA Paris).

---

## 🎯 Contexte métier

Simulation d'un outil Sales pour pitcher des stratégies de couverture 
en options à un client institutionnel (fonds de pension exposé à la 
volatilité des marchés actions).

Black-Scholes suppose une volatilité constante et des marchés continus — 
ce projet implémente ce modèle comme base de pricing et expose ses 
limites via l'analyse de scénarios en temps réel.

---

## ✨ Fonctionnalités

- Pricing Black-Scholes en temps réel (call / put)
- Greeks interactifs : Delta, Gamma, Vega
- Graphique payoff dynamique avec strike et spot visualisés
- Analyse de scénarios ±10% / ±20% sur le S&P 500
- Texte de pitch client automatique adapté aux paramètres

---

## 📸 Aperçu

### Paramètres & Résultats
![Dashboard](screenshots/paramètres_et_résultats.png)

### Payoff à maturité
![Payoff](screenshots/payoff_maturite.png)

### Analyse de scénarios & Pitch client
![Scénarios](screenshots/scenarios_pitch.png)

---

## 📐 Modèle utilisé

**Black-Scholes avec dividendes continus**

$$C = S e^{-qT} N(d_1) - K e^{-rT} N(d_2)$$

$$d_1 = \frac{\ln(S/K) + (r - q + \sigma^2/2)T}{\sigma\sqrt{T}}$$

**Greeks implémentés :**
| Greek | Formule | Interprétation |
|-------|---------|----------------|
| Delta | $N(d_1)$ | Sensibilité au prix du sous-jacent |
| Gamma | $\frac{N'(d_1)}{S\sigma\sqrt{T}}$ | Variation du delta |
| Vega | $S\sqrt{T}N'(d_1)$ | Sensibilité à la volatilité |

---

## 📊 Résultats — Exemple ITM

Paramètres : S=5000, K=4800, σ=20%, r=2%, q=1%, T=1 an

| Scénario | Prix S&P 500 | Valeur option | Payoff à maturité | Delta |
|----------|-------------|---------------|-------------------|-------|
| -20% | 4000 | $92.69 | $0 | 0.2209 |
| -10% | 4500 | $253.40 | $0 | 0.4272 |
| +10% | 5500 | $877.20 | $700 | 0.7890 |
| +20% | 6000 | $1298.75 | $1200 | 0.8883 |

---

## ⚠️ Limites de Black-Scholes

- **Volatilité constante** → en réalité on observe un smile de volatilité
- **Distribution log-normale** → les fat tails (crises) sont sous-estimés  
- **Marchés continus** → les gaps de prix ne sont pas modélisés

*Pour aller plus loin : modèle de Heston (volatilité stochastique)*

---

## 🚀 Installation & Lancement

```bash
pip install numpy scipy streamlit matplotlib pandas
streamlit run app.py
```

---

## 🛠️ Technologies

![Python](https://img.shields.io/badge/Python-3.11-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-interactive-red)
![NumPy](https://img.shields.io/badge/NumPy-scientific-green)

**Stack :** Python | Black-Scholes | Streamlit | NumPy | SciPy | Matplotlib

---

## 👤 Auteur

**Sacha** — Étudiant M1 Finance, ESLSCA Paris  
*Projet réalisé dans le cadre d'une démarche d'apprentissage de la finance de marché*
