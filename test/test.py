from optical_properties import opt_prop, comp_split
from Batch_equation_splitting2 import eqtn_split
from Batch_calculation_gf3 import batch_calc
from mmsep_den_cn import M_M_sep, molar_volume, coord_num_avg
from pd_pf_opd import oxy_pack_density, effect_rem, optical_basicity
#from density_v2 import molar_volume
import pytest
from test_helper import validate_v121

"""
Tests for PhysicalParameters_v1.21

These tests validate the backend calculations against experimentally
reported data for the B2O3–Bi2O3–SrO–Li2O–WO3 glass system.

Reference
@article{shwetha2026,
  author    = {Shwetha, M. and Keenatampalle, Suresh and Alqarni, Areej S. and Angadi, Basavaraj and Madhu, A. and Jeffery, A. Anto and Srinatha, N.},
  title     = {Structural, optical and elastic characteristics of WO\textsubscript{3}-doped B\textsubscript{2}O\textsubscript{3}+Bi\textsubscript{2}O\textsubscript{3}+SrO+Li\textsubscript{2}O glasses},
  journal   = {Materials Chemistry and Physics},
  volume    = {348},
  pages     = {131709},
  year      = {2026},
  doi       = {10.1016/j.matchemphys.2025.131709}
}

Only LSBBW0, LSBBW3, and LSBBW5 compositions are tested,
as these have complete input data (composition, density inputs, etc.)
provided from the reference dataset.

Each composition follows the glass formula:
(60–x)B2O3 + 20Bi2O3 + 10SrO + 10Li2O + xWO3
"""


# ---------------------------------------------------------------------------
# Glass composition test data (from literature)
# ---------------------------------------------------------------------------

glass_data = [
    {
        "code": "LSBBW0",
        "eq": "60H3BO3[B2O3]+20Bi2O3+10SrCO3[SrO]+10Li2CO3[Li2O]",
        "batch_weight": 10,
        "wt_air": 2.860,
        "imm_liq": "toluene",
        "wt_imm": 2.306,
        "ri": 1.6545,
        "cn": [3, 6, 6, 4, 0],
        "expected": {
            "mol_wt": 148.31,
            "density": 4.471,
            "molar_vol": 33.17,
            "ref_index": 1.6545,
            "molar_refract": 12.17,
            "dielectric_const": 2.74,
            "trans_coeff": 0.8854,
        },
    },
    {
        "code": "LSBBW3",
        "eq": "57H3BO3[B2O3]+20Bi2O3+10SrCO3[SrO]+10Li2CO3[Li2O]+3WO3",
        "batch_weight": 10,
        "wt_air": 1.378,
        "imm_liq": "toluene",
        "wt_imm": 1.114,
        "ri": 1.6555,
        "cn": [3, 6, 6, 4, 6],
        "expected": {
            "mol_wt": 153.18,
            "density": 4.520,
            "molar_vol": 33.89,
            "ref_index": 1.6555,
            "molar_refract": 12.44,
            "dielectric_const": 2.74,
            "trans_coeff": 0.8851,
        },
    },
    {
        "code": "LSBBW5",
        "eq": "55H3BO3[B2O3]+20Bi2O3+10SrCO3[SrO]+10Li2CO3[Li2O]+5WO3",
        "batch_weight": 10,
        "wt_air": 1.356,
        "imm_liq": "toluene",
        "wt_imm": 1.100,
        "ri": 1.6560,
        "cn": [3, 6, 6, 4, 6],
        "expected": {
            "mol_wt": 156.42,
            "density": 4.587,
            "molar_vol": 34.10,
            "ref_index": 1.6560,
            "molar_refract": 12.53,
            "dielectric_const": 2.74,
            "trans_coeff": 0.8850,
        },
    },
]


# ---------------------------------------------------------------------------
# Helper
# ---------------------------------------------------------------------------

'''def approx_equal(value, expected, tol):
    """Check if two float values are approximately equal."""
    return abs(value - expected) <= tol'''


# ---------------------------------------------------------------------------
# Main test (parametric)
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("glass", glass_data)
def test_glass_properties_v121(glass):
    """Test B2O3–Bi2O3–SrO–Li2O–WO3 system."""
    validate_v121(glass, eqtn_split, batch_calc, molar_volume, opt_prop)
