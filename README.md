# 💨 Ideal Gas Module

A modern, type-safe Python library for calculating and solving the **Ideal Gas Law** ($PV = nRT$ and its variations), designed to be intuitive, robust, and high school-friendly.

---

## 🐍 Requirements
- Pure Python `>= 3.10`
- Zero external runtime dependencies

---

## 📦 Installation

```bash
pip install ideal-gas
```

---

## ✨ Features

### 1. Automatic Unit Conversion
Wrap your values in dedicated type-safe unit classes, and the library handles all conversions automatically:

| Physical Quantity | Supported Units | Internal Standard Unit |
| :--- | :--- | :--- |
| **Pressure** ($P$) | `atm`, `Torr`, `mmHg` | $\text{atm}$ |
| **Volume** ($V$) | `L`, `dm3`, `ml`, `cm3` | $\text{L}$ |
| **Amount** ($n$) | `mol` | $\text{mol}$ |
| **Temperature** ($T$) | `K`, `C` ($^\circ\text{C}$) | $\text{K}$ |
| **Mass** ($g$) | `g`, `kg` | $\text{g}$ |
| **Molar Mass** ($M$) | `g/mol` | $\text{g/mol}$ |
| **Density** ($d$) | `g/L`, `g/dm3` | $\text{g/L}$ |
| **Molarity** ($M_{\text{olarity}}$) | `mol/L`, `mol/dm3` | $\text{mol/L}$ |

---

### 2. Dual Modes (Default Scientific & School Mode)
Easily switch between scientific precision and standard high school curriculum constants:

| Parameter | Default Scientific Mode | School Mode (`school_mode=True`) |
| :--- | :--- | :--- |
| **Gas Constant ($R$)** | `0.082057` $\text{L}\cdot\text{atm}/(\text{mol}\cdot\text{K})$ | `0.0821` $\text{L}\cdot\text{atm}/(\text{mol}\cdot\text{K})$ |
| **$0^\circ\text{C}$ to Kelvin Offset** | `+ 273.15` | `+ 273` |

---

### 3. Supported Gas Law Formulas

1. **$PV = nRT$** via `PVnRT`
2. **$PV = \frac{g}{M}RT$** via `PVgMRT`
3. **$PM = dRT$** via `PMdRT` *(also aliased as `PVdRT`)*
4. **$P = MRT$** via `PMRT`

---

## 🚀 Quick Start & Examples

### 1. $PV = nRT$
Calculate the missing variable by omitting it from the constructor and accessing `calculate_<variable>`:

```python
from ideal_gas import PVnRT, Volume, Mole, Temperature

# Calculate Pressure (atm)
gas = PVnRT(
    volume=Volume(volume=7600, unit="ml"),
    mole=Mole(mole=8, unit="mol"),
    temperature=Temperature(temperature=27, unit="C"),
)

print(gas.calculate_pressure)  # Pressure in atm ~ 25.92569
```

```python
from ideal_gas import PVnRT, Pressure, Mole, Temperature

# Calculate Volume (L)
gas = PVnRT(
    pressure=Pressure(pressure=1520, unit="mmHg"),
    mole=Mole(mole=7, unit="mol"),
    temperature=Temperature(temperature=298, unit="K"),
)

print(gas.calculate_volume)  # Volume in L ~ 85.54442
```

---

### 2. $PV = \frac{g}{M}RT$

```python
from ideal_gas import PVgMRT, Volume, Gram, MolarMass, Temperature

# Calculate Pressure (atm)
gas = PVgMRT(
    volume=Volume(volume=3, unit="L"),
    gram=Gram(gram=4, unit="kg"),
    molar_mass=MolarMass(molar_mass=8, unit="g/mol"),
    temperature=Temperature(temperature=45, unit="C"),
)

print(gas.calculate_pressure)  # Pressure in atm
```

```python
from ideal_gas import PVgMRT, Pressure, Volume, Gram, Temperature

# Calculate Molar Mass (g/mol)
gas = PVgMRT(
    pressure=Pressure(pressure=1520, unit="Torr"),
    volume=Volume(volume=20, unit="ml"),
    gram=Gram(gram=6, unit="kg"),
    temperature=Temperature(temperature=25, unit="C"),
)

print(gas.calculate_molar_mass)  # Molar Mass in g/mol
```

---

### 3. $PM = dRT$

```python
from ideal_gas import PMdRT, Density, MolarMass, Temperature

# Calculate Pressure (atm) from density and molar mass
gas = PMdRT(
    density=Density(density=1.429, unit="g/L"),
    molar_mass=MolarMass(molar_mass=32, unit="g/mol"),
    temperature=Temperature(temperature=0, unit="C"),
)

print(gas.calculate_pressure)  # Pressure in atm
```

```python
from ideal_gas import PMdRT, Pressure, MolarMass, Temperature

# Calculate Gas Density (g/L)
gas = PMdRT(
    pressure=Pressure(pressure=2, unit="atm"),
    molar_mass=MolarMass(molar_mass=44, unit="g/mol"),
    temperature=Temperature(temperature=27, unit="C"),
)

print(gas.calculate_density)  # Density in g/L
```

---

### 4. $P = MRT$ (where $M$ = Molarity)

```python
from ideal_gas import PMRT, Molarity, Temperature

# Calculate Pressure (atm)
gas = PMRT(
    molarity=Molarity(molarity=8, unit="mol/L"),
    temperature=Temperature(temperature=277, unit="K"),
)

print(gas.calculate_pressure)  # Pressure in atm
```

---

### 5. Using School Mode

```python
from ideal_gas import PVnRT, Volume, Mole, Temperature, GasConstant

gas = PVnRT(
    volume=Volume(volume=7600, unit="ml"),
    mole=Mole(mole=8, unit="mol"),
    # Set school_mode=True on Temperature (Kelvin offset = 273)
    temperature=Temperature(temperature=27, unit="C", school_mode=True),
    # Set school_mode=True on GasConstant (R = 0.0821)
    gas_constant=GasConstant(school_mode=True),
)

print(gas.calculate_pressure)  # Output: 25.926315789473686
```

---

## 🛠️ Development & Testing

Run all unit tests with pytest:

```bash
pip install pytest
pytest
```

Build the distribution package:

```bash
pip install --upgrade build
python -m build
```

---

## 📄 License
This project is licensed under the [MIT License](LICENSE).
