from ideal_gas import Density, GasConstant, Gram, MolarMass, Molarity, Pressure, Volume, Mole, Temperature
import pytest

KELVIN_OFFSET_DEFAULT = 273.15
KELVIN_OFFSET_SCHOOL = 273
GAS_CONSTANT_DEFAULT = 0.082057
GAS_CONSTANT_SCHOOL = 0.0821

@pytest.mark.parametrize("value, unit, expected",[
        (760, "Torr", 1),
        (760, "mmHg", 1),
        (1, "atm", 1),
    ]
)

def test_pressure_conversion(value, unit, expected):
    p = Pressure(pressure=value, unit=unit)
    assert p.atmosphere == expected

def test_pressure_zero():
    with pytest.raises(ValueError, match="Pressure must be greater than zero"):
        Pressure(pressure=0, unit="atm")
        Pressure(pressure=0, unit="Torr")
        Pressure(pressure=0, unit="mmHg")

@pytest.mark.parametrize("value, unit, expected", [
    (1000, "cm3", 1),
    (1000, "ml", 1),
    (1, "L", 1),
    (1, "dm3", 1)
])

def test_volume_conversion(value, unit, expected):
    v = Volume(volume=value, unit=unit)
    assert v.liter == expected

def test_volume_zero():
    with pytest.raises(ValueError, match="Volume must be greater than zero"):
        Volume(volume=0, unit="L")
        Volume(volume=0, unit="dm3")
        Volume(volume=0, unit="cm3")
        Volume(volume=0, unit="ml")

@pytest.mark.parametrize("value, unit, expected", [
    (1, "mol", 1)
])

def test_mole_conversion(value, unit, expected):
    m = Mole(mole=value, unit=unit)
    assert m.mol == expected

def test_mole_zero():
    with pytest.raises(ValueError, match="Mole must be greater than zero"):
        Mole(mole=0, unit="mol")

def test_gas_constant_default():
    R = GasConstant(school_mode=False)
    assert R.value == GAS_CONSTANT_DEFAULT

    R_f = GasConstant()
    assert R_f.value == GAS_CONSTANT_DEFAULT

def test_gas_constant_school():
    R = GasConstant(school_mode=True)
    assert R.value == GAS_CONSTANT_SCHOOL

def test_gas_constant_change_mode():
    R = GasConstant(school_mode=False)
    assert R.value == GAS_CONSTANT_DEFAULT

    R.school_mode = True
    assert R.value == GAS_CONSTANT_SCHOOL

    R.school_mode = False
    assert R.value == GAS_CONSTANT_DEFAULT

@pytest.mark.parametrize("value, unit, expected, school_mode", [
    (27, "C", 27 + KELVIN_OFFSET_DEFAULT, False),
    (0, "C", 0 + KELVIN_OFFSET_DEFAULT, False),
    (273.15, "K", 273.15, False),
    (27, "C", 27 + KELVIN_OFFSET_SCHOOL, True),
    (0, "C", 0 + KELVIN_OFFSET_SCHOOL, True),
    (273, "K", 273, True)
])

def test_temperature_conversion(value, unit, expected, school_mode):
    t = Temperature(temperature=value, unit=unit, school_mode=school_mode)
    assert t.kelvin == expected

def test_temperature_kelvin_zero():
    # Default mode
    with pytest.raises(ValueError, match="Temperature must be greater than zero"):
        Temperature(temperature=-273.15, unit="C", school_mode=False)

    # School mode
    with pytest.raises(ValueError, match="Temperature must be greater than zero"):
        Temperature(temperature=-273, unit="C", school_mode=True)

def test_temperature_above_absolute_zero():
    t_1 = Temperature(temperature=-273.15 + 1, unit="C", school_mode=False)
    assert t_1.kelvin == 1
    assert t_1.kelvin_offset == KELVIN_OFFSET_DEFAULT

    t_2 = Temperature(temperature=-273 + 1, unit="C", school_mode=True)
    assert t_2.kelvin == 1
    assert t_2.kelvin_offset == KELVIN_OFFSET_SCHOOL

@pytest.mark.parametrize("value, unit, expected", [
    (1000, "g", 1000),
    (1, "kg", 1000)
])

def test_gram_conversion(value, unit, expected):
    g = Gram(gram=value, unit=unit)
    assert g.grams == expected

def test_gram_zero():
    with pytest.raises(ValueError, match="Gram must be greater than zero"):
        Gram(gram=0, unit="g")
        Gram(gram=0, unit="kg")

@pytest.mark.parametrize("value, unit, expected", [
    (1, "g/mol", 1)
])

def test_molar_mass_conversion(value, unit, expected):
    mm = MolarMass(molar_mass=value, unit=unit)
    assert mm.gram_per_mol == expected

def test_molar_mass_zero():
    with pytest.raises(ValueError, match="Molar mass must be greater than zero"):
        MolarMass(molar_mass=0, unit="g/mol")

@pytest.mark.parametrize("value, unit, expected", [
    (1, "g/L", 1)
])

def test_density_conversion(value, unit, expected):
    d = Density(density=value, unit=unit)
    assert d.gram_per_liter == expected

def test_density_zero():
    with pytest.raises(ValueError, match="Density must be greater than zero"):
        Density(density=0, unit="g/dm3")
        Density(density=0, unit="g/L")

@pytest.mark.parametrize("value, unit, expected", [
    (1, "mol/L", 1),
    (1, "mol/dm3", 1)
])

def test_molarity_conversion(value, unit, expected):
    mr = Molarity(molarity=value, unit=unit)
    assert mr.mol_per_liter == expected

def test_molarity_zero():
    with pytest.raises(ValueError, match="Molarity must be greater than zero"):
        Molarity(molarity=0, unit="mol/dm3")
        Molarity(molarity=0, unit="mol/L")
