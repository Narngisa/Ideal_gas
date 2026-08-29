from dataclasses import dataclass, field
from typing import Optional, Literal

# Type aliases
PressureUnit = Literal["atm", "Torr", "mmHg"]
VolumeUnit = Literal["ml", "cm3", "L", "dm3"]
MoleUnit = Literal["mol"]
TemperatureUnit = Literal["K", "C"]
GramUnit = Literal["g", "kg"]
MolarMassUnit = Literal["g/mol"]
DensityUnit = Literal["g/L", "g/dm3"]
MolarityUnit = Literal["mol/dm3", "mol/L"]

# Gas Constant (R in L*atm / (mol*K))
GAS_CONSTANT_DEFAULT = 0.082057
GAS_CONSTANT_SCHOOL = 0.0821

# Kelvin Offset
KELVIN_OFFSET_DEFAULT = 273.15
KELVIN_OFFSET_SCHOOL = 273


@dataclass(kw_only=True)
class Pressure:
    """Represents a pressure value with automatic conversion to atmosphere (atm)."""

    pressure: float
    unit: PressureUnit

    def __post_init__(self) -> None:
        if self.pressure <= 0:
            raise ValueError("Pressure must be greater than zero")

    @property
    def atmosphere(self) -> float:
        """Return pressure in atmospheres (atm)."""
        if self.unit == "atm":
            return self.pressure
        elif self.unit in ("Torr", "mmHg"):
            return self.pressure / 760
        raise ValueError("Unsupported pressure unit")


@dataclass(kw_only=True)
class Volume:
    """Represents a volume value with automatic conversion to liters (L)."""

    volume: float
    unit: VolumeUnit

    def __post_init__(self) -> None:
        if self.volume <= 0:
            raise ValueError("Volume must be greater than zero")

    @property
    def liter(self) -> float:
        """Return volume in liters (L)."""
        if self.unit in ("L", "dm3"):
            return self.volume
        elif self.unit in ("ml", "cm3"):
            return self.volume / 1000
        raise ValueError("Unsupported volume unit")


@dataclass(kw_only=True)
class Mole:
    """Represents an amount of substance in moles (mol)."""

    mole: float
    unit: MoleUnit = "mol"

    def __post_init__(self) -> None:
        if self.mole <= 0:
            raise ValueError("Mole must be greater than zero")

    @property
    def mol(self) -> float:
        """Return amount of substance in moles (mol)."""
        if self.unit == "mol":
            return self.mole
        raise ValueError("Unsupported mole unit")


@dataclass(kw_only=True)
class GasConstant:
    """Represents the ideal gas constant (R)."""

    school_mode: bool = False

    @property
    def value(self) -> float:
        """Return the gas constant value in L*atm/(mol*K)."""
        return GAS_CONSTANT_SCHOOL if self.school_mode else GAS_CONSTANT_DEFAULT


@dataclass(kw_only=True)
class Temperature:
    """Represents a temperature value with automatic conversion to Kelvin (K)."""

    temperature: float
    unit: TemperatureUnit
    school_mode: bool = False

    def __post_init__(self) -> None:
        self.kelvin_offset = KELVIN_OFFSET_SCHOOL if self.school_mode else KELVIN_OFFSET_DEFAULT
        kelvin_value = self.temperature if self.unit == "K" else self.temperature + self.kelvin_offset

        if kelvin_value <= 0:
            raise ValueError("Temperature must be greater than zero")

    @property
    def kelvin(self) -> float:
        """Return temperature in Kelvin (K)."""
        if self.unit == "K":
            return self.temperature
        elif self.unit == "C":
            return self.temperature + self.kelvin_offset
        raise ValueError("Unsupported temperature unit")


@dataclass(kw_only=True)
class Gram:
    """Represents mass in grams (g)."""

    gram: float
    unit: GramUnit

    def __post_init__(self) -> None:
        if self.gram <= 0:
            raise ValueError("Gram must be greater than zero")

    @property
    def grams(self) -> float:
        """Return mass in grams (g)."""
        if self.unit == "g":
            return self.gram
        elif self.unit == "kg":
            return self.gram * 1000
        raise ValueError("Unsupported gram unit")


@dataclass(kw_only=True)
class MolarMass:
    """Represents molar mass in grams per mole (g/mol)."""

    molar_mass: float
    unit: MolarMassUnit = "g/mol"

    def __post_init__(self) -> None:
        if self.molar_mass <= 0:
            raise ValueError("Molar mass must be greater than zero")

    @property
    def gram_per_mol(self) -> float:
        """Return molar mass in g/mol."""
        if self.unit == "g/mol":
            return self.molar_mass
        raise ValueError("Unsupported molar mass unit")


@dataclass(kw_only=True)
class Density:
    """Represents gas density in grams per liter (g/L)."""

    density: float
    unit: DensityUnit

    def __post_init__(self) -> None:
        if self.density <= 0:
            raise ValueError("Density must be greater than zero")

    @property
    def gram_per_liter(self) -> float:
        """Return density in g/L."""
        if self.unit in ("g/L", "g/dm3"):
            return self.density
        raise ValueError("Unsupported density unit")


@dataclass(kw_only=True)
class Molarity:
    """Represents molar concentration in moles per liter (mol/L)."""

    molarity: float
    unit: MolarityUnit

    def __post_init__(self) -> None:
        if self.molarity <= 0:
            raise ValueError("Molarity must be greater than zero")

    @property
    def mol_per_liter(self) -> float:
        """Return molar concentration in mol/L."""
        if self.unit in ("mol/L", "mol/dm3"):
            return self.molarity
        raise ValueError("Unsupported molarity unit")


@dataclass(kw_only=True)
class PVnRT:
    """Calculates unknown variables for the Ideal Gas Law: PV = nRT."""

    pressure: Optional[Pressure] = None
    volume: Optional[Volume] = None
    mole: Optional[Mole] = None
    temperature: Optional[Temperature] = None
    gas_constant: GasConstant = field(default_factory=GasConstant)

    @property
    def calculate_pressure(self) -> float:
        """Calculate Pressure (in atm)."""
        if self.pressure is not None:
            raise ValueError("pressure already exists")
        if self.volume is None or self.mole is None or self.temperature is None:
            raise ValueError("volume, mole, and temperature are required")
        return (self.mole.mol * self.gas_constant.value * self.temperature.kelvin) / self.volume.liter

    @property
    def calculate_volume(self) -> float:
        """Calculate Volume (in L)."""
        if self.volume is not None:
            raise ValueError("volume already exists")
        if self.pressure is None or self.mole is None or self.temperature is None:
            raise ValueError("pressure, mole, and temperature are required")
        return (self.mole.mol * self.gas_constant.value * self.temperature.kelvin) / self.pressure.atmosphere

    @property
    def calculate_mole(self) -> float:
        """Calculate amount of substance (in mol)."""
        if self.mole is not None:
            raise ValueError("mole already exists")
        if self.pressure is None or self.volume is None or self.temperature is None:
            raise ValueError("pressure, volume, and temperature are required")
        return (self.pressure.atmosphere * self.volume.liter) / (self.gas_constant.value * self.temperature.kelvin)

    @property
    def calculate_temperature(self) -> float:
        """Calculate Temperature (in K)."""
        if self.temperature is not None:
            raise ValueError("temperature already exists")
        if self.pressure is None or self.volume is None or self.mole is None:
            raise ValueError("pressure, volume, and mole are required")
        return (self.pressure.atmosphere * self.volume.liter) / (self.mole.mol * self.gas_constant.value)


@dataclass(kw_only=True)
class PVgMRT:
    """Calculates unknown variables for the Ideal Gas Law: PV = (g/M)RT."""

    pressure: Optional[Pressure] = None
    volume: Optional[Volume] = None
    gram: Optional[Gram] = None
    molar_mass: Optional[MolarMass] = None
    temperature: Optional[Temperature] = None
    gas_constant: GasConstant = field(default_factory=GasConstant)

    @property
    def calculate_pressure(self) -> float:
        """Calculate Pressure (in atm)."""
        if self.pressure is not None:
            raise ValueError("pressure already exists")
        if self.volume is None or self.gram is None or self.molar_mass is None or self.temperature is None:
            raise ValueError("volume, gram, molar mass, and temperature are required")
        return ((self.gram.grams / self.molar_mass.gram_per_mol) * self.gas_constant.value * self.temperature.kelvin) / self.volume.liter

    @property
    def calculate_volume(self) -> float:
        """Calculate Volume (in L)."""
        if self.volume is not None:
            raise ValueError("volume already exists")
        if self.pressure is None or self.gram is None or self.molar_mass is None or self.temperature is None:
            raise ValueError("pressure, gram, molar mass, and temperature are required")
        return ((self.gram.grams / self.molar_mass.gram_per_mol) * self.gas_constant.value * self.temperature.kelvin) / self.pressure.atmosphere

    @property
    def calculate_gram(self) -> float:
        """Calculate Mass (in g)."""
        if self.gram is not None:
            raise ValueError("gram already exists")
        if self.pressure is None or self.volume is None or self.molar_mass is None or self.temperature is None:
            raise ValueError("pressure, volume, molar mass, and temperature are required")
        return (self.pressure.atmosphere * self.volume.liter * self.molar_mass.gram_per_mol) / (self.gas_constant.value * self.temperature.kelvin)

    @property
    def calculate_molar_mass(self) -> float:
        """Calculate Molar Mass (in g/mol)."""
        if self.molar_mass is not None:
            raise ValueError("molar mass already exists")
        if self.pressure is None or self.volume is None or self.gram is None or self.temperature is None:
            raise ValueError("pressure, volume, gram, and temperature are required")
        return (self.gram.grams * self.gas_constant.value * self.temperature.kelvin) / (self.pressure.atmosphere * self.volume.liter)

    @property
    def calculate_temperature(self) -> float:
        """Calculate Temperature (in K)."""
        if self.temperature is not None:
            raise ValueError("temperature already exists")
        if self.pressure is None or self.volume is None or self.gram is None or self.molar_mass is None:
            raise ValueError("pressure, volume, gram, and molar mass are required")
        return (self.pressure.atmosphere * self.volume.liter * self.molar_mass.gram_per_mol) / (self.gram.grams * self.gas_constant.value)


@dataclass(kw_only=True)
class PMdRT:
    """Calculates unknown variables for the Ideal Gas Law: PM = dRT."""

    pressure: Optional[Pressure] = None
    molar_mass: Optional[MolarMass] = None
    density: Optional[Density] = None
    temperature: Optional[Temperature] = None
    gas_constant: GasConstant = field(default_factory=GasConstant)

    @property
    def calculate_pressure(self) -> float:
        """Calculate Pressure (in atm)."""
        if self.pressure is not None:
            raise ValueError("pressure already exists")
        if self.molar_mass is None or self.density is None or self.temperature is None:
            raise ValueError("molar mass, density, and temperature are required")
        return (self.density.gram_per_liter * self.gas_constant.value * self.temperature.kelvin) / self.molar_mass.gram_per_mol

    @property
    def calculate_molar_mass(self) -> float:
        """Calculate Molar Mass (in g/mol)."""
        if self.molar_mass is not None:
            raise ValueError("molar mass already exists")
        if self.pressure is None or self.density is None or self.temperature is None:
            raise ValueError("pressure, density, and temperature are required")
        return (self.density.gram_per_liter * self.gas_constant.value * self.temperature.kelvin) / self.pressure.atmosphere

    @property
    def calculate_density(self) -> float:
        """Calculate Density (in g/L)."""
        if self.density is not None:
            raise ValueError("density already exists")
        if self.pressure is None or self.molar_mass is None or self.temperature is None:
            raise ValueError("pressure, molar mass, and temperature are required")
        return (self.pressure.atmosphere * self.molar_mass.gram_per_mol) / (self.gas_constant.value * self.temperature.kelvin)

    @property
    def calculate_temperature(self) -> float:
        """Calculate Temperature (in K)."""
        if self.temperature is not None:
            raise ValueError("temperature already exists")
        if self.pressure is None or self.molar_mass is None or self.density is None:
            raise ValueError("pressure, molar mass, and density are required")
        return (self.pressure.atmosphere * self.molar_mass.gram_per_mol) / (self.density.gram_per_liter * self.gas_constant.value)


# Backward compatibility alias
PVdRT = PMdRT


@dataclass(kw_only=True)
class PMRT:
    """Calculates unknown variables for the Ideal Gas Law: P = MRT (where M is Molarity)."""

    pressure: Optional[Pressure] = None
    molarity: Optional[Molarity] = None
    temperature: Optional[Temperature] = None
    gas_constant: GasConstant = field(default_factory=GasConstant)

    @property
    def calculate_pressure(self) -> float:
        """Calculate Pressure (in atm)."""
        if self.pressure is not None:
            raise ValueError("pressure already exists")
        if self.molarity is None or self.temperature is None:
            raise ValueError("molarity, and temperature are required")
        return self.molarity.mol_per_liter * self.gas_constant.value * self.temperature.kelvin

    @property
    def calculate_molarity(self) -> float:
        """Calculate Molarity (in mol/L)."""
        if self.molarity is not None:
            raise ValueError("molarity already exists")
        if self.pressure is None or self.temperature is None:
            raise ValueError("pressure, and temperature are required")
        return self.pressure.atmosphere / (self.gas_constant.value * self.temperature.kelvin)

    @property
    def calculate_temperature(self) -> float:
        """Calculate Temperature (in K)."""
        if self.temperature is not None:
            raise ValueError("temperature already exists")
        if self.pressure is None or self.molarity is None:
            raise ValueError("pressure, and molarity are required")
        return self.pressure.atmosphere / (self.molarity.mol_per_liter * self.gas_constant.value)
