from ideal_gas import (
    PMRT,
    Density,
    Molarity,
    PMdRT,
    PVdRT,
    PVnRT,
    PVgMRT,
    Pressure,
    Volume,
    Mole,
    Temperature,
    Gram,
    MolarMass,
)
import pytest


def test_raise_pressure_exits():
    gas_PV_nRT = PVnRT(pressure=Pressure(pressure=1, unit="atm"))
    gas_PV_gMRT = PVgMRT(pressure=Pressure(pressure=1, unit="atm"))
    gas_PM_dRT = PMdRT(pressure=Pressure(pressure=1, unit="atm"))
    gas_P_MRT = PMRT(pressure=Pressure(pressure=1, unit="atm"))

    with pytest.raises(ValueError, match="pressure already exists"):
        _ = gas_PV_nRT.calculate_pressure
    with pytest.raises(ValueError, match="pressure already exists"):
        _ = gas_PV_gMRT.calculate_pressure
    with pytest.raises(ValueError, match="pressure already exists"):
        _ = gas_PM_dRT.calculate_pressure
    with pytest.raises(ValueError, match="pressure already exists"):
        _ = gas_P_MRT.calculate_pressure


def test_raise_volume_exits():
    gas_PV_nRT = PVnRT(volume=Volume(volume=1000, unit="cm3"))
    gas_PV_gMRT = PVgMRT(volume=Volume(volume=1000, unit="cm3"))

    with pytest.raises(ValueError, match="volume already exists"):
        _ = gas_PV_nRT.calculate_volume
    with pytest.raises(ValueError, match="volume already exists"):
        _ = gas_PV_gMRT.calculate_volume


def test_raise_mole_exits():
    gas_PV_nRT = PVnRT(mole=Mole(mole=15, unit="mol"))

    with pytest.raises(ValueError, match="mole already exists"):
        _ = gas_PV_nRT.calculate_mole


def test_raise_temperature_exits():
    gas_PV_nRT = PVnRT(temperature=Temperature(temperature=300, unit="K"))
    gas_PV_gMRT = PVgMRT(temperature=Temperature(temperature=300, unit="K"))
    gas_PM_dRT = PMdRT(temperature=Temperature(temperature=300, unit="K"))
    gas_P_MRT = PMRT(temperature=Temperature(temperature=300, unit="K"))

    with pytest.raises(ValueError, match="temperature already exists"):
        _ = gas_PV_nRT.calculate_temperature
    with pytest.raises(ValueError, match="temperature already exists"):
        _ = gas_PV_gMRT.calculate_temperature
    with pytest.raises(ValueError, match="temperature already exists"):
        _ = gas_PM_dRT.calculate_temperature
    with pytest.raises(ValueError, match="temperature already exists"):
        _ = gas_P_MRT.calculate_temperature


def test_raise_gram_exits():
    gas_PV_gMRT = PVgMRT(gram=Gram(gram=10, unit="g"))

    with pytest.raises(ValueError, match="gram already exists"):
        _ = gas_PV_gMRT.calculate_gram


def test_raise_molar_mass_exits():
    gas_PV_gMRT = PVgMRT(molar_mass=MolarMass(molar_mass=10, unit="g/mol"))
    gas_PM_dRT = PMdRT(molar_mass=MolarMass(molar_mass=10, unit="g/mol"))

    with pytest.raises(ValueError, match="molar mass already exists"):
        _ = gas_PV_gMRT.calculate_molar_mass
    with pytest.raises(ValueError, match="molar mass already exists"):
        _ = gas_PM_dRT.calculate_molar_mass


def test_raise_density_exits():
    gas_PM_dRT = PMdRT(density=Density(density=4, unit="g/L"))

    with pytest.raises(ValueError, match="density already exists"):
        _ = gas_PM_dRT.calculate_density


def test_raise_molarity_exits():
    gas_P_MRT = PMRT(molarity=Molarity(molarity=6, unit="mol/L"))

    with pytest.raises(ValueError, match="molarity already exists"):
        _ = gas_P_MRT.calculate_molarity
