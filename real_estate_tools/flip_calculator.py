import pandas as pd
import plotly.express as px
import streamlit as st
from loguru import logger

from real_estate_tools import flip_calculator_components as fcc

logger.info("Starting a flip calculation cycle")

"""
# Flip Calculator

## General factors
"""
arv = st.number_input(
    label="Provide estimated ARV ($)",
    value=400000,
    step=1000,
    help="This will be used to derive the selling price.",
)
atractivity_factor = (
    st.number_input(
        label="Provide the attractivity factor (%)",
        value=2,
        min_value=0,
        max_value=100,
    )
    / 100
)
estimated_holding_period = st.number_input(
    label="Number of months expected for flip", min_value=1
)


selling_col, purchase_col = st.columns(2)

selling_col.write("## Selling factors")
purchase_col.write("## Purchase factors")

selling_col.write(
    ":blue[Provide estimations of the different factors to impact the **selling**"
    " costs]"
)
purchase_col.write(
    ":blue[Provide estimations of the different factors to impact the **purchase**"
    " costs]"
)

selling_factors = fcc.sell_or_purchase_factors(selling_col, mode="sell")
purchase_factors = fcc.sell_or_purchase_factors(purchase_col, mode="purchase")


"""
## Monthly holding costs

Indicate expected monthly costs
"""

monthly_costs = pd.Series(
    {
        "taxes_per_month": st.number_input(label="Tax ($)", min_value=0.0, step=10.0),
        "insurance_per_month": st.number_input(
            label="Insurance ($)", min_value=0.0, step=10.0
        ),
        "utilities_gas_per_month": st.number_input(
            label="Gas ($)", min_value=0.0, step=10.0
        ),
        "utilities_electricity_per_month": st.number_input(
            label="Electricity ($)", min_value=0.0, step=10.0
        ),
        "utilities_water_sewer_per_month": st.number_input(
            label="Water and sewer ($)", min_value=0.0, step=10.0
        ),
        "trash_per_month": st.number_input(label="Trash ($)", min_value=0.0, step=10.0),
    },
    name="monthly_costs",
)

holding_costs = pd.DataFrame(
    {
        "total": monthly_costs * estimated_holding_period,
        "monthly": monthly_costs,
    }
)


"""
## Rehab costs

Provide estimation of the rehab total costs
"""

total_rehab = st.number_input(label="Rehab costs ($)", min_value=0, step=500)


"""## Summary"""

min_purchase_price = st.number_input(
    label="What's the minimal purchase price ($)?",
    min_value=0,
    max_value=int(arv * (1 - atractivity_factor)),
    step=1000,
    value=int(arv * 0.3),
)

result = pd.DataFrame({"purchase_price": range(min_purchase_price, arv, 1000)})
result["purchase_costs"] = result["purchase_price"].apply(
    lambda x: purchase_factors.get_cost(x)
)
result["selling_costs"] = selling_factors.get_cost(arv)
result["holding_costs"] = holding_costs["total"].sum()
result["rehab_costs"] = total_rehab
result["total_expenses"] = result.sum(axis=1)
result["total_income"] = arv * (1 - atractivity_factor)
result["ROI"] = 100 * (result["total_income"] / result["total_expenses"] - 1)
# result = result.set_index("purchase_price")
st.dataframe(result, height=150)


fig = px.line(result, x="purchase_price", y="ROI")


st.plotly_chart(fig)
