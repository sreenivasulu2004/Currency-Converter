import tkinter as tk
from tkinter import ttk, messagebox
import requests
import json
from datetime import datetime, timedelta
import threading


class CurrencyConverter:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Currency Converter")
        self.window.geometry("300x500")
        self.window.resizable(False, False)

        # Modern color scheme
        self.bg_color = "#f8f9fa"
        self.card_color = "#ffffff"
        self.accent_color = "#007bff"
        self.text_color = "#2c3e50"
        self.border_color = "#e9ecef"

        self.window.configure(bg=self.bg_color)

        # Exchange rates cache
        self.rates = {}
        self.last_update = None

        # Available currencies (most common ones)
        self.currencies = [
            "USD", "EUR", "GBP", "JPY", "AUD", "CAD", "CHF", "CNY",
            "SEK", "NZD", "MXN", "SGD", "HKD", "NOK", "KRW", "TRY",
            "RUB", "INR", "BRL", "ZAR"
        ]

        self.setup_ui()
        self.fetch_rates()

    def setup_ui(self):
        # Main container with padding
        main_frame = tk.Frame(self.window, bg=self.bg_color)
        main_frame.pack(expand=True, fill='both', padx=20, pady=20)

        # Title
        title_label = tk.Label(
            main_frame,
            text="Currency Converter",
            font=("Segoe UI", 18, "bold"),
            fg=self.text_color,
            bg=self.bg_color
        )
        title_label.pack(pady=(0, 20))

        # Converter card
        card_frame = tk.Frame(
            main_frame,
            bg=self.card_color,
            relief='flat',
            bd=1
        )
        card_frame.pack(fill='x', pady=10)

        # Add subtle border effect
        card_frame.configure(highlightbackground=self.border_color, highlightthickness=1)

        # Card content with padding
        content_frame = tk.Frame(card_frame, bg=self.card_color)
        content_frame.pack(padx=20, pady=20)

        # From currency section
        from_frame = tk.Frame(content_frame, bg=self.card_color)
        from_frame.pack(fill='x', pady=(0, 15))

        tk.Label(
            from_frame,
            text="From:",
            font=("Segoe UI", 10),
            fg=self.text_color,
            bg=self.card_color
        ).pack(anchor='w')

        from_input_frame = tk.Frame(from_frame, bg=self.card_color)
        from_input_frame.pack(fill='x', pady=(5, 0))

        self.amount_var = tk.StringVar(value="1.00")
        self.amount_entry = tk.Entry(
            from_input_frame,
            textvariable=self.amount_var,
            font=("Segoe UI", 12),
            relief='solid',
            bd=1,
            width=10
        )
        self.amount_entry.pack(side='left', padx=(0, 10))
        self.amount_entry.bind('<KeyRelease>', self.on_amount_change)

        self.from_currency = ttk.Combobox(
            from_input_frame,
            values=self.currencies,
            state="readonly",
            font=("Segoe UI", 10),
            width=8
        )
        self.from_currency.set("USD")
        self.from_currency.pack(side='left')
        self.from_currency.bind('<<ComboboxSelected>>', self.convert_currency)

        # Swap button
        swap_frame = tk.Frame(content_frame, bg=self.card_color)
        swap_frame.pack(pady=5)

        swap_btn = tk.Button(
            swap_frame,
            text="⇅",
            font=("Segoe UI", 14),
            bg=self.accent_color,
            fg="white",
            relief='flat',
            bd=0,
            width=3,
            height=1,
            command=self.swap_currencies
        )
        swap_btn.pack()

        # To currency section
        to_frame = tk.Frame(content_frame, bg=self.card_color)
        to_frame.pack(fill='x', pady=(15, 0))

        tk.Label(
            to_frame,
            text="To:",
            font=("Segoe UI", 10),
            fg=self.text_color,
            bg=self.card_color
        ).pack(anchor='w')

        to_input_frame = tk.Frame(to_frame, bg=self.card_color)
        to_input_frame.pack(fill='x', pady=(5, 0))

        self.result_var = tk.StringVar()
        self.result_entry = tk.Entry(
            to_input_frame,
            textvariable=self.result_var,
            font=("Segoe UI", 12),
            relief='solid',
            bd=1,
            width=10,
            state='readonly'
        )
        self.result_entry.pack(side='left', padx=(0, 10))

        self.to_currency = ttk.Combobox(
            to_input_frame,
            values=self.currencies,
            state="readonly",
            font=("Segoe UI", 10),
            width=8
        )
        self.to_currency.set("EUR")
        self.to_currency.pack(side='left')
        self.to_currency.bind('<<ComboboxSelected>>', self.convert_currency)

        # Status label
        self.status_label = tk.Label(
            main_frame,
            text="Loading exchange rates...",
            font=("Segoe UI", 9),
            fg="#6c757d",
            bg=self.bg_color
        )
        self.status_label.pack(pady=(10, 0))

        # Refresh button
        refresh_btn = tk.Button(
            main_frame,
            text="Refresh Rates",
            font=("Segoe UI", 9),
            bg=self.accent_color,
            fg="white",
            relief='flat',
            bd=0,
            padx=15,
            pady=5,
            command=self.fetch_rates
        )
        refresh_btn.pack(pady=(5, 0))

    def fetch_rates(self):
        """Fetch exchange rates in a separate thread"""

        def fetch():
            try:
                # Using exchangerate-api.com (free tier: 1500 requests/month)
                response = requests.get("https://api.exchangerate-api.com/v4/latest/USD", timeout=10)

                if response.status_code == 200:
                    data = response.json()
                    self.rates = data['rates']
                    self.rates['USD'] = 1.0  # Add USD as base
                    self.last_update = datetime.now()

                    self.window.after(0, lambda: self.status_label.config(
                        text=f"Rates updated: {self.last_update.strftime('%H:%M:%S')}"
                    ))
                    self.window.after(0, self.convert_currency)
                else:
                    raise Exception("API request failed")

            except requests.exceptions.RequestException:
                self.window.after(0, lambda: self.status_label.config(
                    text="Network error - using cached rates" if self.rates else "Network error - check connection"
                ))
            except Exception as e:
                self.window.after(0, lambda: self.status_label.config(
                    text="Error fetching rates - check connection"
                ))

        # Update status immediately
        self.status_label.config(text="Updating rates...")

        # Fetch in background thread
        thread = threading.Thread(target=fetch, daemon=True)
        thread.start()

    def convert_currency(self, event=None):
        """Convert currency based on current inputs"""
        try:
            if not self.rates:
                return

            amount = float(self.amount_var.get() or 0)
            from_curr = self.from_currency.get()
            to_curr = self.to_currency.get()

            if from_curr == to_curr:
                result = amount
            else:
                # Convert through USD
                usd_amount = amount / self.rates.get(from_curr, 1)
                result = usd_amount * self.rates.get(to_curr, 1)

            self.result_var.set(f"{result:.4f}")

        except (ValueError, ZeroDivisionError):
            self.result_var.set("0.0000")

    def on_amount_change(self, event=None):
        """Handle amount input changes"""
        # Add small delay to avoid excessive API calls during typing
        self.window.after(300, self.convert_currency)

    def swap_currencies(self):
        """Swap from and to currencies"""
        from_curr = self.from_currency.get()
        to_curr = self.to_currency.get()

        self.from_currency.set(to_curr)
        self.to_currency.set(from_curr)

        self.convert_currency()

    def run(self):
        """Start the application"""
        self.window.mainloop()


def main():
    app = CurrencyConverter()
    app.run()


if __name__ == "__main__":
    main()