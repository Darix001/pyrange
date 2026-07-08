# 🔢 PyRange

[![Python 3.12+](https://img.shields.io/badge/python-3.12%2B-blue)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A lightweight, efficient Python package for advanced mathematical operations with ranges. Perform complex range computations using optimized algorithms that avoid materializing the entire range into memory.

## ✨ Features

- **Efficient Range Operations**: Perform mathematical operations without materializing ranges into lists
- **Range Relationships**: Check if ranges are subranges, superranges, or disjoint
- **Range Algebra**: Compute intersections, unions, and transformations of ranges
- **Arithmetic Helpers**: Dedicated `Number` class for elegant arithmetic with ranges
- **Built on Python 3.12+**: Leverages modern Python features like pattern matching

## 📦 Installation

```bash
# Using pip
pip install git+https://github.com/Darix001/pyrange/tree/main/pyrange

# Using uv (recommended)
uv add git+https://github.com/Darix001/pyrange/tree/main/pyrange
```

## 🚀 Quick Start

```python
from pyrange import *

# Basic range operations
r1 = range(0, 10, 2)
r2 = range(5, 15, 2)

# Check range relationships
print(issubrange(r1, r2))      # False - r1 is not a subrange of r2
print(issuperrange(r1, r2))    # False

# Find intersection of ranges
result = intersection(r1, r2)
print(list(result))             # [6, 8] (optimized computation)

# Arithmetic with ranges
num = Number(5)
shifted_range = r1 + num       # Shifts all elements by 5
scaled_range = r1 * num        # Multiplies all elements by 5

print(list(shifted_range))      # [5, 7, 9, 11, 13, 15]
print(list(scaled_range))       # [0, 10, 20, 30, 40, 50]
```

## 📚 API Reference

### Range Queries

#### `issubrange(rng: range, other: range) -> bool`
Checks if `rng` is a subrange of `other`. A range is a subrange if all its elements are contained in the other range.

```python
issubrange(range(2, 6, 1), range(0, 10, 1))  # True
issubrange(range(0, 10, 2), range(0, 10, 3)) # False (incompatible steps)
```

#### `issuperrange(rng: range, other: range) -> bool`
Checks if `rng` is a superrange of `other`. Equivalent to `issubrange(other, rng)`.

```python
issuperrange(range(0, 10, 1), range(2, 6, 1))  # True
```

#### `intersection(*ranges: range) -> range`
Computes the intersection of multiple ranges efficiently. Returns a range containing elements present in all input ranges.

```python
r1 = range(0, 10, 2)   # [0, 2, 4, 6, 8]
r2 = range(5, 15, 2)   # [5, 7, 9, 11, 13]
intersection(r1, r2)    # range(6, 9, 2) -> [6, 8]
```

### Aggregation Functions

#### `sum(rng: range) -> int`
Computes the sum of all elements in the range using the arithmetic progression formula. O(1) time complexity.

```python
sum(range(1, 11))          # 55
sum(range(0, 100, 5))      # 950
```

#### `prod(rng: range) -> int`
Computes the product of all elements in the range. Optimized for special cases:
- Returns 0 if the range contains 0
- Uses `math.factorial()` for ranges `range(1, n)`

```python
prod(range(1, 6))          # 120 (equivalent to 5!)
prod(range(2, 5))          # 24 (2 × 3 × 4)
prod(range(0, 10))         # 0
```

### Range Transformations

#### `Number` Class
A dataclass for performing arithmetic operations with ranges. Supports arithmetic and bitwise operators.

```python
num = Number(3)

# Addition/Subtraction (shifts the range)
r = range(0, 5, 1)
num + r          # range(3, 8, 1) -> [3, 4, 5, 6, 7]
r + num          # Same as above (addition is commutative)

# Multiplication (scales the range)
num * r          # range(0, 15, 3) -> [0, 3, 6, 9, 12]

# Floor Division (scales down)
num // r         # range(0, 1, 0) - be careful with division!

# Bitwise Left Shift
num << r         # range(0, 16, 8) -> [0, 8]
```

#### `invert(rng: range) -> range` / `inv(rng: range) -> range`
Inverts the bitwise representation of all elements in the range.

```python
inv(range(0, 3, 1))  # range(-1, -4, -1) -> [-1, -2, -3]
```

#### `neg(rng: range) -> range`
Negates all elements in the range.

```python
neg(range(0, 5, 1))  # range(0, -5, -1) -> [0, -1, -2, -3, -4]
```

#### `pos(rng: range) -> range`
Returns the range unchanged (unary positive operator).

```python
pos(range(0, 5, 1))  # range(0, 5, 1)
```

## 💡 Design Philosophy

PyRange follows these principles:

1. **Zero-Copy**: Operations return new range objects, not materialized lists. Iterate them when needed.
2. **Mathematical Correctness**: Uses precise algorithms (LCM for intersection, arithmetic progression formulas for aggregation)
3. **Performance**: O(1) time complexity for most operations, regardless of range size
4. **Pythonic**: Integrates seamlessly with Python's `range` type and standard operators

## 📋 Examples

### Calculate the sum of an arithmetic sequence
```python
# Sum of 1 + 2 + 3 + ... + 100
total = sum(range(1, 101))  # 5050, computed in O(1)
```

### Find common elements in multiple ranges
```python
morning_shifts = range(8, 17, 1)    # 8am to 4pm
afternoon_shifts = range(12, 21, 1) # 12pm to 8pm
overlap = intersection(morning_shifts, afternoon_shifts)
print(list(overlap))  # [12, 13, 14, 15, 16]
```

### Transform a numeric range
```python
ids = range(100, 110, 1)           # [100, 101, ..., 109]
encrypted = ids * Number(2)         # [200, 202, ..., 218]
shifted = encrypted + Number(1000)  # [1200, 1202, ..., 1218]
```

### Check range containment
```python
query_range = range(0, 50, 5)       # Multiples of 5 up to 50
database_range = range(0, 100, 5)   # All multiples of 5 up to 100

if issubrange(query_range, database_range):
    print("All query results are in the database!")
```

## ⚠️ Known Limitations

- `isdisjoint(rng, other)` is not yet implemented (in progress)
- `intersection()` may require further testing for edge cases with negative steps
- Subtraction with `Number` currently shifts the range (not a true subtraction). Use negation with addition for correct behavior.

## 🛠️ Development

PyRange uses `uv` for project management and `pyproject.toml` for configuration.

```bash
# Install development dependencies
uv venv
uv pip install -e .

# Run tests (when available)
uv run pytest
```

## 📝 Project Structure

```
pyrange/
├── src/
│   └── pyrange/
│       └── __init__.py       # Main module with all operations
├── pyproject.toml            # Project configuration
├── uv.lock                   # Dependency lock file
└── README.md                 # This file
```

## 🤝 Contributing

Contributions are welcome! Areas for improvement:

- Implement `isdisjoint()` function
- Add comprehensive test suite
- Optimize `intersection()` for edge cases
- Extend operator support (division, modulo, etc.)
- Add type hints and comprehensive docstrings

## 📄 License

This project is licensed under the MIT License. See `LICENSE` file for details.

## 👤 Author

**Dariel Buret** - [GitHub](https://github.com/Darix001)

---

## 🎯 Use Cases

- **Data Processing**: Work with large numeric ranges without memory overhead
- **Mathematical Computation**: Solve problems involving arithmetic progressions
- **Algorithm Design**: Efficiently compute range properties for algorithmic solutions
- **Database Queries**: Optimize range-based lookups and intersections

---

<div align="center">

**Made with ❤️ for efficient range operations in Python**

</div>
