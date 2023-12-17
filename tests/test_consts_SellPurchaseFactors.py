import pytest
from pydantic import ValidationError

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


@pytest.mark.parametrize("broker_commission_vals", [20, 1, 0.0, -1])
def test_broker_commission(broker_commission_vals):
    with pytest.raises(ValidationError):
        SellPurchaseFactors(
            broker_commission=broker_commission_vals,
            fixed_broker_fee=100,
            closing_costs=0.01,
            transfer_tax=0.02,
            fixed_notary=20,
            deed_recording_fee=11,
            legal_fee=22,
        )


@pytest.mark.parametrize("closing_costs_vals", [20, 1, -0.0001, -1])
def test_closing_costs(closing_costs_vals):
    with pytest.raises(ValidationError):
        SellPurchaseFactors(
            broker_commission=0.5,
            fixed_broker_fee=100,
            closing_costs=closing_costs_vals,
            transfer_tax=0.02,
            fixed_notary=20,
            deed_recording_fee=11,
            legal_fee=22,
        )


@pytest.mark.parametrize("transfer_tax_vals", [20, 1, -0.0001, -1])
def test_transfer_tax(transfer_tax_vals):
    with pytest.raises(ValidationError):
        SellPurchaseFactors(
            broker_commission=0.5,
            fixed_broker_fee=100,
            closing_costs=0.5,
            transfer_tax=transfer_tax_vals,
            fixed_notary=20,
            deed_recording_fee=11,
            legal_fee=22,
        )
