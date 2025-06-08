# Currency Converter

A modern, user-friendly desktop application for converting between different currencies using real-time exchange rates.

## Features

- Convert between 20 common currencies
- Real-time exchange rates from [ExchangeRate-API](https://www.exchangerate-api.com/)
- Clean, modern user interface
- Ability to swap currencies with a single click
- Offline support with cached exchange rates
- Background updates that don't freeze the UI

## Installation

### Prerequisites

- Python 3.11 or higher
- Internet connection (for fetching exchange rates)

### Steps

1. Clone or download this repository:
   ```
   git clone https://github.com/sreenivasulu2004/Currency-Converter.git
   cd currency-converter
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

Run the application:

```
python app.py
```

1. Enter the amount you want to convert
2. Select the source currency from the dropdown
3. Select the target currency from the dropdown
4. The converted amount will be displayed automatically
5. Use the swap button (⇅) to quickly reverse the conversion
6. Click "Refresh Rates" to update to the latest exchange rates

## Dependencies

- **tkinter**: GUI toolkit for Python
- **requests**: HTTP library for API requests

## Acknowledgements

- Exchange rates provided by [ExchangeRate-API](https://www.exchangerate-api.com/)
