# Currency Exchange Converter

A real-time currency exchange converter application built with Python and Tkinter, demonstrating Object-Oriented Programming (OOP) principles.

## Overview

This application fetches live exchange rates from OpenExchangeRates API and provides a user-friendly interface for currency conversion with autocomplete functionality and a swap feature.

## Object-Oriented Programming (OOP) Concepts

### 1. **Encapsulation**
The application uses private attributes (prefixed with `__`) to hide internal data and provides public getter methods:

- **Currency Class**: Encapsulates currency code and name with private attributes `__code` and `__name`
- **ExchangeRate Class**: Encapsulates rate and timestamp with private attributes `__rate` and `__last_update`
- **Access Methods**: `get_code()`, `get_name()` provide controlled access to private data

```python
class Currency:
    def __init__(self, code, name):
        self.__code = code      # Private attribute
        self.__name = name      # Private attribute
    
    def get_code(self):         # Public getter
        return self.__code
```

### 2. **Inheritance**
The `ExchangeRate` class inherits from the `Currency` class, extending its functionality:

```python
class ExchangeRate(Currency):
    def __init__(self, code, name, rate, last_update):
        super().__init__(code, name)  # Inherits from Currency
        self.__rate = rate
        self.__last_update = last_update
```

**Benefits:**
- Code reusability: ExchangeRate inherits `get_code()` and `get_name()` from Currency
- Logical hierarchy: An exchange rate IS-A currency with additional rate information
- Extensibility: Easy to add new currency-related classes

### 3. **Polymorphism**
The `calculate()` and `to_string()` methods in `ExchangeRate` demonstrate polymorphism:

```python
def calculate(self, amount):
    return amount * self.__rate  # Different calculation for each exchange rate

def to_string(self):
    return f"{self.get_code()}: {self.__rate}"  # Custom string representation
```

These methods can behave differently for different currency pairs while sharing the same interface.

### 4. **Abstraction**
Complex operations are hidden behind simple interfaces:

- **APIService**: Abstracts API communication details
- **ExchangeManager**: Abstracts currency conversion logic
- **UIController**: Abstracts UI complexity

Users interact with simple methods like `convert()` without knowing the implementation details.

### 5. **Separation of Concerns**
Each class has a single, well-defined responsibility:

- **Currency**: Represents currency data
- **ExchangeRate**: Represents exchange rate with conversion logic
- **APIService**: Handles all API communications
- **ExchangeManager**: Manages currencies and exchange rates
- **UIController**: Manages user interface and interactions

## Class Diagram

```
┌─────────────────────────────┐
│       Currency              │
├─────────────────────────────┤
│ - __code: str               │
│ - __name: str               │
├─────────────────────────────┤
│ + __init__(code, name)      │
│ + get_code(): str           │
│ + get_name(): str           │
└─────────────────────────────┘
            △
            │ inherits
            │
┌─────────────────────────────┐
│     ExchangeRate            │
├─────────────────────────────┤
│ - __rate: float             │
│ - __last_update: str        │
├─────────────────────────────┤
│ + __init__(code, name,      │
│   rate, last_update)        │
│ + calculate(amount): float  │
│ + to_string(): str          │
└─────────────────────────────┘


┌─────────────────────────────┐
│       APIService            │
├─────────────────────────────┤
│ - app_id: str               │
│ - base_url: str             │
├─────────────────────────────┤
│ + __init__(app_id)          │
│ + fetch_latest(): dict      │
│ + fetch_currency_list():    │
│   dict                      │
│ + fetch_history(date): dict │
│ + handle_error(): void      │
└─────────────────────────────┘
            △
            │ uses
            │
┌─────────────────────────────┐
│    ExchangeManager          │
├─────────────────────────────┤
│ - api: APIService           │
│ - exchange_rates: dict      │
│ - currencies: dict          │
├─────────────────────────────┤
│ + __init__(app_id)          │
│ + refresh_rates(): void     │
│ + load_currency_list():void │
│ + get_currency_codes():list │
│ + get_currency_name(code):  │
│   str                       │
│ + convert(frm, to, amount): │
│   float                     │
│ + get_exchange_rate_info    │
│   (code): ExchangeRate      │
└─────────────────────────────┘
            △
            │ uses
            │
┌─────────────────────────────┐
│      UIController           │
├─────────────────────────────┤
│ - root: ThemedTk            │
│ - manager: ExchangeManager  │
│ - amount_var: StringVar     │
│ - result_var: StringVar     │
│ - status_var: StringVar     │
│ - from_var: StringVar       │
│ - to_var: StringVar         │
├─────────────────────────────┤
│ + __init__(manager)         │
│ + setup_ui(): void          │
│ + setup_autocomplete(): void│
│ + swap_currencies(): void   │
│ + convert(): void           │
│ + refresh_rates(): void     │
│ + run(): void               │
└─────────────────────────────┘
```

## Relationships

### Inheritance
- `ExchangeRate` **extends** `Currency`
  - Inherits: `__code`, `__name`, `get_code()`, `get_name()`
  - Adds: `__rate`, `__last_update`, `calculate()`, `to_string()`

### Composition
- `ExchangeManager` **has-a** `APIService`
  - ExchangeManager uses APIService for all network operations
  
- `ExchangeManager` **has-many** `Currency` objects
  - Stores Currency objects in `currencies` dictionary
  
- `ExchangeManager` **has-many** `ExchangeRate` objects
  - Stores ExchangeRate objects in `exchange_rates` dictionary

- `UIController` **has-a** `ExchangeManager`
  - UIController delegates business logic to ExchangeManager

### Dependency
- `UIController` **depends on** `ExchangeManager`
- `ExchangeManager` **depends on** `APIService`
- All classes **depend on** external libraries (tkinter, requests, ttkthemes)

## Features

1. **Real-time Exchange Rates**: Fetches live rates from OpenExchangeRates API
2. **Autocomplete**: Type-ahead functionality for currency selection
3. **Swap Currencies**: Quick button to reverse conversion direction
4. **Modern UI**: Themed interface using ttkthemes
5. **Error Handling**: Comprehensive validation and error messages
6. **Status Updates**: Real-time status bar showing operation feedback

## Installation

1. Install required dependencies:
```bash
pip install requests ttkthemes python-dotenv
```

2. Create a `.env` file with your API key:
```
APP_ID=your_openexchangerates_api_key
```

3. Get your free API key from [OpenExchangeRates](https://openexchangerates.org/)

## 🎮 Usage

Run the application:
```bash
python main.py
```

1. Enter the amount to convert
2. Select "From" currency (use autocomplete by typing)
3. Select "To" currency
4. Click "Convert" or use the swap button (⇄) to reverse currencies
5. View the result and exchange rate