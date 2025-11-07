from optical_properties import opt_prop, comp_split
from Batch_equation_splitting2 import eqtn_split
from Batch_calculation_gf3 import batch_calc
from mmsep_den_cn import M_M_sep, coord_num_avg
from pd_pf_opd import oxy_pack_density, effect_rem, optical_basicity
from density_v2 import molar_volume  # updated molar volume for v1.22
import pytest
from test_helper import validate_v122

"""
Tests for PhysicalParameters_v1.22

Validates computed optical and structural parameters against
published data for Dy3+-doped Li2O–CaO–B2O3 glasses.

@article{madhu2025dy,
  author    = {Madhu, A. and Kesavulu, C. R. and Alqarni, Areej S. and Basavegowda, Nagaraj and Amir, Assadi Achraf and Srinatha, N.},
  title     = {Unravelling energy transfer mechanisms in Dy\textsuperscript{3+}-doped Li\textsubscript{2}O + CaO + B\textsubscript{2}O\textsubscript{3} glasses through optical, luminescence and JO analysis},
  journal   = {The European Physical Journal Plus},
  volume    = {140},
  number    = {7},
  pages     = {715},
  year      = {2025},
  doi       = {10.1140/epjp/s13360-025-06649-7}
}


Each glass composition follows:
    (20−x)Li2CO3[Li2O] + 10CaCO3[CaO] + 70H3BO3[B2O3] + xDy2O3
"""

# ---------------------------------------------------------------------------
# Glass data — v1.22 format (inputs like v1.21)
# ---------------------------------------------------------------------------
glass_data_v122 = [
    {
        "code": "LCBDy0.1",
        "eq": "19.9Li2CO3[Li2O] + 10CaCO3[CaO] + 70H3BO3[B2O3] + 0.1Dy2O3",
        "batch_weight": 10,
        "density": 2.462,
        "ri": 1.6535,
        "expected": {
            "mol_wt": 60.66,
            "molar_vol": 24.64,
            "oxy_pack_density": 97.51,
            "opt_basicity": 0.55,
            "dielectric_const": 2.73,
            "molar_refract": 9.02,
        },
    },
    {
        "code": "LCBDy0.5",
        "eq": "19.5Li2CO3[Li2O] + 10CaCO3[CaO] + 70H3BO3[B2O3] + 0.5Dy2O3",
        "batch_weight": 10,
        "density": 2.497,
        "ri": 1.6540,
        "expected": {
            "mol_wt": 62.03,
            "molar_vol": 24.84,
            "oxy_pack_density": 97.01,
            "opt_basicity": 0.56,
            "dielectric_const": 2.74,
            "molar_refract": 9.10,
        },
    },
    {
        "code": "LCBDy1.0",
        "eq": "19.0Li2CO3[Li2O] + 10CaCO3[CaO] + 70H3BO3[B2O3] + 1.0Dy2O3",
        "batch_weight": 10,
        "density": 2.458,
        "ri": 1.6545,
        "expected": {
            "mol_wt": 63.75,
            "molar_vol": 25.93,
            "oxy_pack_density": 93.32,
            "opt_basicity": 0.60,
            "dielectric_const": 2.74,
            "molar_refract": 9.51,
        },
    },
]


# ---------------------------------------------------------------------------
# Parametric tests
# ---------------------------------------------------------------------------
@pytest.mark.parametrize("glass", glass_data_v122)
def test_physical_parameters_v122(glass):
    """Test Dy3+-doped Li2O–CaO–B2O3 system."""
    validate_v122(glass, eqtn_split, batch_calc, molar_volume, opt_prop)
