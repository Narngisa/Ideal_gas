# 💨Ideal Gas Module
Calculating The Ideal Gas Law in python, focusing make it easy and high school-friendly

## 🐍Language
Pure Python `version >= 3.10`

## ☕Features

### Unit
- Pressure `atm`, `Torr` and `mmHg`
- Volume `ml`, `cm3`, `L` and `dm3`
- Mole `mol`
- Temperature `C` and `K`
- Gram `g` and `kg`
- Molar mass `g/mol`
- Density `g/L`
- Molarity `mol/dm3` and `mol/L`

### Mode
Gas Constant (R) `0.082057`
Kelvin (K) `273.15`
### School Mode 
Gas Constant (R) `0.0821`
Kelvin (K) `273`

### Function
- PV=nRT
- PV=(g/M)RT
- PV=dRT
- P=MRT

## ⚙️Install
You can download file ideal_gas.py and import it to use in your file main.

## 📃Example

### PV = nRT
```py
from ideal_gas import PVnRT, Volume, Mole, Temperature
# Pressure, Volume, Mole, Temperature

gas = PVnRT(
    volume=Volume(volume=7600, unit="ml"),
    mole=Mole(mole=8, unit="mol"),
    temperature=Temperature(temperature=27, unit="C", school_mode=False),
)

# Pressure ~ 25.92569
print(gas.calculate_pressure)
```

### PV = (g/M)RT
```py
from ideal_gas import PVgMRT, Volume, Gram, MolarMass, Temperature
# Pressure, Volume, Gram, MolarMass, Temperature

gas = PVgMRT(
    volume=Volume(volume=400, unit="ml"),
    gram=Gram(gram=5, unit="kg"),
    molar_mass=MolarMass(molar_mass=4, unit="g/mol"),
    temperature=Temperature(temperature=298, unit="K", school_mode=False),
)

# Pressure ~ 76415.58125
print(gas.calculate_pressure)
```

### PV = dRT
```py
from ideal_gas import PVdRT, Volume, Density, Temperature
# Pressure, Volume, Density, Temperature

gas = PVdRT(
    volume=Volume(volume=800, unit="ml"),
    density=Density(density=2, unit="g/L"),
    temperature=Temperature(temperature=300, unit="K", school_mode=False),
)

# Pressure ~ 61.54275
print(gas.calculate_pressure)
```

### P = MRT
```py
from ideal_gas import PMRT, Molarity, Temperature
# Pressure, Molarity, Temperature

gas = PMRT(
    molarity=Molarity(molarity=7, unit="mol/L"),
    temperature=Temperature(temperature=300, unit="K", school_mode=False),
)

# Pressure ~ 172.3197
print(gas.calculate_pressure)
```

## Mode Gas Constant
```py
from ideal_gas import PVnRT, Volume, Mole, Temperature, GasConstant
# Pressure, Volume, Mole, Temperature

gas = PVnRT(
    volume=Volume(volume=7600, unit="ml"),
    mole=Mole(mole=8, unit="mol"),
    temperature=Temperature(temperature=27, unit="C", school_mode=False),
    gas_constant=GasConstant(school_mode=False)

    #gas_constant=GasConstant() [ Default Mode ]
    #gas_constant=GasConstant(school_mode=True) [School Mode]

)

# Pressure ~ 25.925693
print(gas.calculate_pressure)
```
