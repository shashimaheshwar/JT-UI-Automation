from ConfigVars.TestConfig import SessionTypeControl
import pytest

free_seating = pytest.mark.skipif(SessionTypeControl.Skip_Free_Seating, reason="Free seating TCs are disabled")
qota = pytest.mark.skipif(SessionTypeControl.Skip_Qota, reason="Qota session TCs are disabled")
advance_free_seating = pytest.mark.skipif(SessionTypeControl.Skip_Advance_Free, reason="Advance Free seating disabled")
advance_qota = pytest.mark.skipif(SessionTypeControl.Skip_Advance_Qota, reason="Advance Qota TC are  disabled")