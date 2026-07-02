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

# Gas Constant
GAS_CONSTANT_DEFAULT = 0.082057
GAS_CONSTANT_SCHOOL = 0.0821

# Kelvin
KELVIN_OFFSET_DEFAULT = 273.15
KELVIN_OFFSET_SCHOOL = 273

@dataclass(kw_only=True)
class Pressure:
    pressure: float
    unit: PressureUnit

    def __post_init__(self):
        if self.pressure <= 0:
            raise ValueError("Pressure must be greater than zero")


    @property
    def atmosphere(self) -> float:
        if self.unit == "atm":
            return self.pressure
        elif self.unit in ("Torr", "mmHg"):
            return self.pressure / 760
        raise ValueError("Unsupported pressure unit")

@dataclass(kw_only=True)
class Volume:
    volume: float
    unit: VolumeUnit

    def __post_init__(self):
        if self.volume <= 0:
            raise ValueError("Volume must be greater than zero")

    @property
    def liter(self) -> float:
        if self.unit in ("L", "dm3"):
            return self.volume
        elif self.unit in ("ml", "cm3"):
            return self.volume / 1000
        raise ValueError("Unsupported volume unit")

@dataclass(kw_only=True)
class Mole:
    mole: float
    unit: MoleUnit = "mol"

    def __post_init__(self):
        if self.mole <= 0:
            raise ValueError("Mole must be greater than zero")

    @property
    def mol(self) -> float:
        if self.unit == "mol":
            return self.mole
        raise ValueError("Unsupported mole unit")

@dataclass(kw_only=True)
class GasConstant:
    school_mode: bool = False

    @property
    def value(self) -> float:
        return GAS_CONSTANT_SCHOOL if self.school_mode else GAS_CONSTANT_DEFAULT

@dataclass(kw_only=True)
class Temperature:
    temperature: float
    unit: TemperatureUnit
    school_mode: bool = False

    def __post_init__(self):
        self.kelvin_offset = KELVIN_OFFSET_SCHOOL if self.school_mode else KELVIN_OFFSET_DEFAULT

        kelvin_value = self.temperature if self.unit == "K" else self.temperature + self.kelvin_offset

        if kelvin_value <= 0:
            raise ValueError("Temperature must be greater than zero")

    @property
    def kelvin(self) -> float:
        if self.unit == "K":
            return self.temperature
        elif self.unit == "C":
            return self.temperature + self.kelvin_offset
        raise ValueError("Unsupported temperature unit")

@dataclass(kw_only=True)
class Gram:
    gram: float
    unit: GramUnit

    def __post_init__(self):
        if self.gram <= 0:
            raise ValueError("Gram must be greater than zero")

    @property
    def grams(self) -> float:
        if self.unit == "g":
            return self.gram
        elif self.unit == "kg":
            return self.gram * 1000
        raise ValueError("Unsupported gram unit")

@dataclass(kw_only=True)
class MolarMass:
    molar_mass: float
    unit: MolarMassUnit = "g/mol"

    def __post_init__(self):
        if self.molar_mass <= 0:
            raise ValueError("Molar mass must be greater than zero")

    @property
    def gram_per_mol(self) -> float:
        if self.unit == "g/mol":
            return self.molar_mass
        raise ValueError("Unsupported molar mass unit")

@dataclass(kw_only=True)
class Density:
    density: float
    unit: DensityUnit

    def __post_init__(self):
        if self.density <= 0:
            raise ValueError("Density must be greater than zero")

    @property
    def gram_per_liter(self) -> float:
        if self.unit in ("g/L", "g/dm3"):
            return self.density
        raise ValueError("Unsupported density unit")

@dataclass(kw_only=True)
class Molarity:
    molarity: float
    unit: MolarityUnit

    def __post_init__(self):
        if self.molarity <= 0:
            raise ValueError("Molarity must be greater than zero")

    @property
    def mol_per_liter(self) -> float:
        if self.unit in ("mol/L", "mol/dm3"):
            return self.molarity
        raise ValueError("Unsupported molarity unit")

@dataclass(kw_only=True)
class PVnRT:
    pressure: Optional[Pressure] = None
    volume: Optional[Volume] = None
    mole: Optional[Mole] = None
    temperature: Optional[Temperature] = None
    gas_constant: GasConstant = field(default_factory=GasConstant)

    @property
    def calculate_pressure(self):

        if self.pressure is not None:
            raise ValueError("pressure already exists")

        if (self.volume is None or self.mole is None or self.temperature is None):
            raise ValueError("volume, mole, and temperature are required")

        return (self.mole.mol * self.gas_constant.value * self.temperature.kelvin) / self.volume.liter

    @property
    def calculate_volume(self):

        if self.volume is not None:
            raise ValueError("volume already exists")

        if (self.pressure is None or self.mole is None or self.temperature is None):
            raise ValueError("pressure, mole, and temperature are required")

        return (self.mole.mol * self.gas_constant.value * self.temperature.kelvin) / self.pressure.atmosphere

    @property
    def calculate_mole(self):

        if self.mole is not None:
            raise ValueError("mole already exists")

        if (self.pressure is None or self.volume is None or self.temperature is None):
            raise ValueError("pressure, volume, and temperature are required")

        return (self.pressure.atmosphere * self.volume.liter) / (self.gas_constant.value * self.temperature.kelvin)

    @property
    def calculate_temperature(self):

        """Return temperature in Kelvin"""

        if self.temperature is not None:
            raise ValueError("temperature already exists")

        if (self.pressure is None or self.volume is None or self.mole is None):
            raise ValueError("pressure, volume, and mole are required")

        return (self.pressure.atmosphere * self.volume.liter) / (self.mole.mol * self.gas_constant.value)

@dataclass(kw_only=True)
class PVgMRT:
    pressure: Optional[Pressure] = None
    volume: Optional[Volume] = None
    gram: Optional[Gram] = None
    molar_mass: Optional[MolarMass] = None
    temperature: Optional[Temperature] = None
    gas_constant: GasConstant = field(default_factory=GasConstant)

    @property
    def calculate_pressure(self):
        if self.pressure is not None:
            raise ValueError("pressure already exists")

        if (self.volume is None or self.gram is None or self.molar_mass is None or self.temperature is None):
            raise ValueError("volume, gram, molar mass, and temperature are required")

        return ((self.gram.grams / self.molar_mass.gram_per_mol) * self.gas_constant.value * self.temperature.kelvin) / self.volume.liter

    @property
    def calculate_volume(self):
        if self.volume is not None:
            raise ValueError("volume already exists")
        if (self.pressure is None or self.gram is None or self.molar_mass is None or self.temperature is None):
            raise ValueError("pressure, gram, molar mass, and temperature are required")

        return ((self.gram.grams / self.molar_mass.gram_per_mol) * self.gas_constant.value * self.temperature.kelvin) / self.pressure.atmosphere

    @property
    def calculate_gram(self):
        if self.gram is not None:
            raise ValueError("gram already exists")
        if (self.pressure is None or self.volume is None or self.molar_mass is None or self.temperature is None):
            raise ValueError("pressure, volume, molar mass, and temperature are required")

        return (self.pressure.atmosphere * self.volume.liter * self.molar_mass.gram_per_mol) / (self.gas_constant.value * self.temperature.kelvin)

    @property
    def calculate_molar_mass(self):
        if self.molar_mass is not None:
            raise ValueError("molar mass already exists")
        if (self.pressure is None or self.volume is None or self.gram is None or self.temperature is None):
            raise ValueError("pressure, volume, gram, and temperature are required")

        return (self.gram.grams * self.gas_constant.value * self.temperature.kelvin) / (self.pressure.atmosphere * self.volume.liter)

    @property
    def calculate_temperature(self):
        if self.temperature is not None:
            raise ValueError("temperature already exists")
        if (self.pressure is None or self.volume is None or self.gram is None or self.molar_mass is None):
            raise ValueError("pressure, volume, gram, and molar mass are required")

        return (self.pressure.atmosphere * self.volume.liter * self.molar_mass.gram_per_mol) / (self.gram.grams * self.gas_constant.value)

@dataclass(kw_only=True)
class PVdRT:
    pressure: Optional[Pressure] = None
    volume: Optional[Volume] = None
    density: Optional[Density] = None
    temperature: Optional[Temperature] = None
    gas_constant: GasConstant = field(default_factory=GasConstant)

    @property
    def calculate_pressure(self):
        if self.pressure is not None:
            raise ValueError("pressure already exists")
        if (self.volume is None or self.density is None or self.temperature is None):
            raise ValueError("volume, density, and temperature are required")

        return (self.density.gram_per_liter * self.gas_constant.value * self.temperature.kelvin) / self.volume.liter

    @property
    def calculate_volume(self):
        if self.volume is not None:
            raise ValueError("volume already exists")
        if (self.pressure is None or self.density is None or self.temperature is None):
            raise ValueError("pressure, density, and temperature are required")

        return (self.density.gram_per_liter * self.gas_constant.value * self.temperature.kelvin) / self.pressure.atmosphere

    @property
    def calculate_density(self):
        if self.density is not None:
            raise ValueError("density already exists")
        if (self.pressure is None or self.volume is None or self.temperature is None):
            raise ValueError("pressure, volume, and temperature are required")

        return (self.pressure.atmosphere * self.volume.liter) / (self.gas_constant.value * self.temperature.kelvin)

    @property
    def calculate_temperature(self):
        if self.temperature is not None:
            raise ValueError("temperature already exists")
        if (self.pressure is None or self.volume is None or self.density is None):
            raise ValueError("pressure, volume, and density are required")

        return (self.pressure.atmosphere * self.volume.liter) / (self.density.gram_per_liter * self.gas_constant.value)

@dataclass(kw_only=True)
class PMRT:
    pressure: Optional[Pressure] = None
    molarity: Optional[Molarity] = None
    temperature: Optional[Temperature] = None
    gas_constant: GasConstant = field(default_factory=GasConstant)

    @property
    def calculate_pressure(self):
        if self.pressure is not None:
            raise ValueError("pressure already exists")
        if (self.molarity is None or self.temperature is None):
            raise ValueError("molarity, and temperature are required")

        return (self.molarity.mol_per_liter * self.gas_constant.value * self.temperature.kelvin)

    @property
    def calculate_molarity(self):
        if self.molarity is not None:
            raise ValueError("molarity already exists")
        if (self.pressure is None or self.temperature is None):
            raise ValueError("pressure, and temperature are required")

        return (self.pressure.atmosphere / (self.gas_constant.value * self.temperature.kelvin))

    @property
    def calculate_temperature(self):
        if self.temperature is not None:
            raise ValueError("temperature already exists")
        if (self.pressure is None or self.molarity is None):
            raise ValueError("pressure, and molarity are required")

        return (self.pressure.atmosphere / (self.molarity.mol_per_liter * self.gas_constant.value))
