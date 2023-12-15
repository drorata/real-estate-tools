from real_estate_tools.consts import SellPurchaseFactors


def test_basic():
    spf = SellPurchaseFactors(
        broker_commission=0.02,
        fixed_broker_fee=100,
        closing_costs=0.01,
        transfer_tax=0.02,
        fixed_notary=20,
        deed_recording_fee=11,
        legal_fee=22,
    )

    price = 1234.4
    result = spf.get_cost(price=price)

    expected_result = (
        price * spf.broker_commission
        + spf.fixed_broker_fee
        + price * spf.closing_costs
        + price * spf.transfer_tax
        + spf.fixed_notary
        + spf.deed_recording_fee
        + spf.legal_fee
    )
    assert result == expected_result
