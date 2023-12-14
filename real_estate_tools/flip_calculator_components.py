import streamlit as st_import

from real_estate_tools.consts import SellPurchaseFactors


def sell_or_purchase_factors(st: st_import, mode: str) -> SellPurchaseFactors:
    broker_commission = (
        st.number_input(
            label="Broker commission (%)",
            value=6.0,
            min_value=0.0,
            max_value=100.0,
            step=5.0,
            key=f"{mode}_broker_commission",
        )
        / 100
    )
    fixed_broker_fee = st.number_input(
        label="Fixed broker fee ($)",
        value=500.0,
        min_value=0.0,
        step=10.0,
        key=f"{mode}_fixed_broker_fee",
    )
    closing_costs = (
        st.number_input(
            label="Closing costs(%)",
            value=0.0,
            min_value=0.0,
            max_value=100.0,
            step=5.0,
            key=f"{mode}_closing_costs",
        )
        / 100
    )
    transfer_tax = (
        st.number_input(
            label="Transfer tax (%)",
            value=2.5,
            min_value=0.0,
            max_value=100.0,
            step=5.0,
            key=f"{mode}_transfer_tax",
        )
        / 100
    )
    fixed_notary = st.number_input(
        label="Fixed notary costs($)",
        value=0.0,
        min_value=0.0,
        step=10.0,
        key=f"{mode}_notary",
    )
    deed_recording_fee = st.number_input(
        label="Deed recording fee ($)",
        value=0.0,
        min_value=0.0,
        step=10.0,
        key=f"{mode}_deed_recording",
    )
    legal_fee = st.number_input(
        label="Legal fees ($)",
        value=0.0,
        min_value=0.0,
        step=10.0,
        key=f"{mode}_legal_fees",
    )

    return SellPurchaseFactors(
        **{
            "broker_commission": broker_commission,
            "fixed_broker_fee": fixed_broker_fee,
            "closing_costs": closing_costs,
            "transfer_tax": transfer_tax,
            "fixed_notary": fixed_notary,
            "deed_recording_fee": deed_recording_fee,
            "legal_fee": legal_fee,
        }
    )
