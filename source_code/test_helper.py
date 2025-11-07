"""
Common test utilities for physical glass property validation.
Used by PhysicalParameters_v1.21 and v1.22 test scripts.
"""

import math
import re


# ---------------------------------------------------------------------------
# Approximation Helpers
# ---------------------------------------------------------------------------

def approx_equal(value, expected, tol):
    """Check approximate numerical equality."""
    if expected == 0:
        return abs(value) <= tol
    return abs(value - expected) <= tol


def assert_approx(value, expected, tol, label=""):
    """Raise AssertionError with context if comparison fails."""
    if not approx_equal(value, expected, tol):
        msg = (
            f"\n❌ {label or 'Value'} mismatch:\n"
            f"   Computed = {value}\n"
            f"   Expected = {expected}\n"
            f"   Tolerance = ±{tol}\n"
        )
        raise AssertionError(msg)
    return True


# ---------------------------------------------------------------------------
# Glass Property Validation Logic
# ---------------------------------------------------------------------------

def extract_optics_values(opt_output):
    """Extract key optical property values from backend string output."""
    values = {}
    if isinstance(opt_output, str):
        for line in opt_output.splitlines():
            match = re.match(r"\s*(.*?)\s*:\s*\t?([\d.eE+-]+)", line)
            if match:
                key, val = match.groups()
                key = key.strip().lower().replace(" ", "_")
                try:
                    values[key] = float(val)
                except ValueError:
                    pass
    return values


def validate_v121(glass, eqtn_split, batch_calc, molar_volume, opt_prop):
    """
    Validates B2O3–Bi2O3–SrO–Li2O–WO3 system glass properties (v1.21 backend).
    Uses 'Original Mass' returned by batch_calc() as molecular weight.
    """
    eq = glass["eq"]
    batch_wt = glass["batch_weight"]

    # Step 1: Equation parsing and batch calculation
    moles, comps, derived, oxides = eqtn_split(eq)
    wt_frac, org_mass, der_mass, grav_fact = batch_calc(moles, comps, derived, batch_wt)

    # Original mass (molecular weight)
    orig_mass_val = org_mass / 100

    # Step 2: Compute density & molar volume using immersion data
    den_liq, Vm = molar_volume(glass["wt_air"], glass["wt_imm"], glass["imm_liq"], orig_mass_val)

    # Step 3: Optical properties
    opt_output = opt_prop(r_i=glass["ri"], z=1.4251, Vm=Vm)
    opt_values = extract_optics_values(opt_output)

    # Step 4: Expected values
    exp = glass["expected"]

    # Step 5: Assertions
    assert_approx(orig_mass_val, exp["mol_wt"], 0.05, "Molecular Weight")
    assert_approx(den_liq, exp["density"], 0.05, "Density")
    assert_approx(Vm, exp["molar_vol"], 0.15, "Molar Volume")
    assert "molar_refract" in opt_values, "Molar refract value not found in optical output"
    assert_approx(opt_values["molar_refract"], exp["molar_refract"], 0.1, "Molar Refraction")

    print(f"✅ {glass['code']} verified successfully against literature data.")


def validate_v122(glass, eqtn_split, batch_calc, molar_volume, opt_prop):
    """
    Validates Li2O–CaO–B2O3–Dy2O3 system glass properties (v1.22 backend).
    Uses 'Original Mass' returned by batch_calc() as molecular weight.
    """
    eq = glass["eq"]
    batch_wt = glass["batch_weight"]

    # Step 1: Equation parsing and batch calculation
    moles, comps, derived, oxides = eqtn_split(eq)
    wt_frac, org_mass, der_mass, grav_fact = batch_calc(moles, comps, derived, batch_wt)

    # Original mass (molecular weight)
    orig_mass_val = org_mass / 100

    # Step 2: Compute molar volume (v1.22 backend uses density directly)
    Vm = molar_volume(orig_mass_val, glass["density"])

    # Step 3: Optical properties
    opt_output = opt_prop(r_i=glass["ri"], z=1.4251, Vm=Vm)
    opt_values = extract_optics_values(opt_output)

    # Step 4: Expected values
    exp = glass["expected"]

    # Step 5: Assertions
    assert_approx(orig_mass_val, exp["mol_wt"], 0.05, "Molecular Weight")
    assert_approx(Vm, exp["molar_vol"], 0.15, "Molar Volume")
    assert "molar_refract" in opt_values, "Molar refract value not found in optical output"
    assert_approx(opt_values["molar_refract"], exp["molar_refract"], 0.1, "Molar Refraction")

    print(f"✅ {glass['code']} verified successfully against literature data.")
