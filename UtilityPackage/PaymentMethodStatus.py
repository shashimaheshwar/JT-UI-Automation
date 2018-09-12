from ConfigVars.TestConfig import PaymentMethodControl
import pytest

wl_payment = pytest.mark.skipif(PaymentMethodControl.WL, reason="Wallet Payment Method is disabled")
pp_payment = pytest.mark.skipif(PaymentMethodControl.PP, reason="PhonePay Payment Method is disabled")
simpl_payment = pytest.mark.skipif(PaymentMethodControl.SIMPL, reason="Simpl Payment Method is disabled")
cc_payment = pytest.mark.skipif(PaymentMethodControl.CC, reason="Credit/Debit Payment Method is disabled")
ap_payment = pytest.mark.skipif(PaymentMethodControl.AP, reason="Amazon Pay Payment Method is disabled")