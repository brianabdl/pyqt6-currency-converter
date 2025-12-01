import requests
import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedTk
import os
from dotenv import load_dotenv

load_dotenv()

# Get your own App ID from https://openexchangerates.org/
APP_ID = os.getenv('APP_ID')

class Currency:
    def __init__(self, code, name):
        self.__code = code
        self.__name = name

    def get_code(self):
        return self.__code

    def get_name(self):
        return self.__name


class ExchangeRate(Currency):
    def __init__(self, code, name, rate, last_update):
        super().__init__(code, name)
        self.__rate = rate
        self.__last_update = last_update

    def calculate(self, amount):
        return amount * self.__rate  # polymorphism method

    def to_string(self):
        return f"{self.get_code()}: {self.__rate}"


class APIService:
    def __init__(self, app_id):
        self.app_id = app_id
        self.base_url = "https://openexchangerates.org/api/"

    def fetch_latest(self):
        url = f"{self.base_url}latest.json?app_id={self.app_id}"
        try:
            response = requests.get(url)
            return response.json()
        except Exception:
            self.handle_error()
            return None

    def fetch_currency_list(self):
        url = f"{self.base_url}currencies.json"
        try:
            response = requests.get(url)
            return response.json()
        except Exception:
            self.handle_error()
            return None

    def fetch_history(self, date):
        url = f"{self.base_url}historical/{date}.json?app_id={self.app_id}"
        try:
            response = requests.get(url)
            return response.json()
        except Exception:
            self.handle_error()
            return None

    def handle_error(self):
        print("Error: Unable to fetch data from OpenExchangeRates API.")

class ExchangeManager:
    def __init__(self, app_id):
        self.api = APIService(app_id)
        self.exchange_rates = {}  # Store ExchangeRate objects
        self.currencies = {}  # Store Currency objects

    def refresh_rates(self):
        data = self.api.fetch_latest()
        if data:
            timestamp = data.get('timestamp', 'Unknown')
            for code, rate in data["rates"].items():
                # Get currency name from currencies dict, or use code as fallback
                name = self.currencies.get(code).get_name() if code in self.currencies else code
                
                # Create ExchangeRate object
                exchange_rate = ExchangeRate(code, name, rate, timestamp)
                self.exchange_rates[code] = exchange_rate

    def load_currency_list(self):
        data = self.api.fetch_currency_list()
        if data:
            for code, name in data.items():
                # Create Currency objects
                currency = Currency(code, name)
                self.currencies[code] = currency

    def get_currency_codes(self):
        """Get list of all currency codes"""
        return list(self.currencies.keys())
    
    def get_currency_name(self, code):
        """Get currency name from Currency object"""
        if code in self.currencies:
            return self.currencies[code].get_name()
        return code

    def convert(self, frm, to, amount):
        """Convert amount using ExchangeRate objects"""
        if frm not in self.exchange_rates or to not in self.exchange_rates:
            raise KeyError(f"Currency rate not found")
        
        # Use the calculate method from ExchangeRate (polymorphism)
        from_rate = self.exchange_rates[frm]
        to_rate = self.exchange_rates[to]
        
        # Convert through USD (base currency)
        amount_in_base = amount / from_rate.calculate(1)
        result = to_rate.calculate(amount_in_base)
        
        return result
    
    def get_exchange_rate_info(self, code):
        """Get ExchangeRate object for a currency"""
        return self.exchange_rates.get(code)



class UIController:
    def __init__(self, manager):
        self.root = ThemedTk(theme="arc")
        self.manager = manager
        self.root.title("Currency Exchange Converter")
        self.root.geometry("600x550")
        self.root.resizable(False, False)
        
        self.amount_var = tk.StringVar(value="1.00")
        self.result_var = tk.StringVar()
        self.status_var = tk.StringVar(value="Ready")
        
        # Variables for autocomplete
        self.from_var = tk.StringVar()
        self.to_var = tk.StringVar()

    def setup_ui(self):
        self.manager.refresh_rates()
        
        # Main container with padding
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title_label = ttk.Label(
            main_frame, 
            text="Currency Exchange Converter",
            font=("Arial", 18, "bold"),
            foreground="#2c3e50",
        )
        title_label.pack(pady=(0, 20))
        
        # Input frame
        input_frame = ttk.LabelFrame(main_frame, text="Conversion Details", padding="15")
        input_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Amount
        ttk.Label(input_frame, text="Amount:", font=("Arial", 10, "bold")).grid(
            row=0, column=0, sticky=tk.W, pady=5
        )
        amount_entry = ttk.Entry(
            input_frame, 
            textvariable=self.amount_var,
            font=("Arial", 12),
            width=25
        )
        amount_entry.grid(row=0, column=1, sticky=tk.EW, pady=5, padx=(10, 0))
        
        # From Currency
        ttk.Label(input_frame, text="From:", font=("Arial", 10, "bold")).grid(
            row=1, column=0, sticky=tk.W, pady=5
        )
        self.from_box = ttk.Combobox(
            input_frame, 
            textvariable=self.from_var,
            values=sorted(self.manager.get_currency_codes()),
            font=("Arial", 11),
            width=23,
        )
        self.from_box.grid(row=1, column=1, sticky=tk.EW, pady=5, padx=(10, 0))
        self.from_box.set("USD")
        self.setup_autocomplete(self.from_box, sorted(self.manager.get_currency_codes()))
        
        # Swap button
        swap_btn = tk.Button(
            input_frame,
            text="⇄",
            command=self.swap_currencies,
            font=("Arial", 16),
            bg="#95a5a6",
            fg="white",
            activebackground="#7f8c8d",
            activeforeground="white",
            cursor="hand2",
            relief=tk.FLAT,
            width=3,
            height=1
        )
        swap_btn.grid(row=1, column=2, rowspan=2, padx=(10, 0), pady=5)
        
        # To Currency
        ttk.Label(input_frame, text="To:", font=("Arial", 10, "bold")).grid(
            row=2, column=0, sticky=tk.W, pady=5
        )
        self.to_box = ttk.Combobox(
            input_frame, 
            textvariable=self.to_var,
            values=sorted(self.manager.get_currency_codes()),
            font=("Arial", 11),
            width=23,
        )
        self.to_box.grid(row=2, column=1, sticky=tk.EW, pady=5, padx=(10, 0))
        self.to_box.set("IDR")
        self.setup_autocomplete(self.to_box, sorted(self.manager.get_currency_codes()))
        
        input_frame.columnconfigure(1, weight=1)
        
        # Convert button
        convert_btn = tk.Button(
            main_frame,
            text="Convert",
            command=self.convert,
            font=("Arial", 12, "bold"),
            bg="#3498db",
            fg="white",
            activebackground="#2980b9",
            activeforeground="white",
            cursor="hand2",
            relief=tk.FLAT,
            padx=20,
            pady=10
        )
        convert_btn.pack(pady=10)
        
        # Result frame
        result_frame = ttk.LabelFrame(main_frame, text="Result", padding="15")
        result_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 15))
        
        result_label = ttk.Label(
            result_frame,
            textvariable=self.result_var,
            font=("Arial", 14, "bold"),
            wraplength=550,
            justify=tk.CENTER
        )
        result_label.pack(expand=True)
        
        # Status bar
        status_frame = ttk.Frame(main_frame)
        status_frame.pack(fill=tk.X, side=tk.BOTTOM)
        
        status_label = ttk.Label(
            status_frame,
            textvariable=self.status_var,
            font=("Arial", 9),
            foreground="#7f8c8d"
        )
        status_label.pack(side=tk.LEFT)
        
        refresh_btn = ttk.Button(
            status_frame,
            text="↻ Refresh Rates",
            command=self.refresh_rates,
            width=15
        )
        refresh_btn.pack(side=tk.RIGHT)

    def setup_autocomplete(self, combobox, value_list):
        """Setup autocomplete functionality for a combobox"""
        def on_keyrelease(event):
            # Ignore navigation keys
            if event.keysym in ('BackSpace', 'Delete', 'Left', 'Right', 'Home', 'End'):
                return
            
            # Get the typed text
            typed = combobox.get()
            
            if typed == '':
                return
            
            # Find first match (case-insensitive)
            typed_upper = typed.upper()
            for item in value_list:
                if item.upper().startswith(typed_upper):
                    # Set the full value
                    combobox.set(item)
                    # Select the auto-completed part
                    combobox.icursor(len(typed))
                    combobox.selection_range(len(typed), tk.END)
                    break
        
        # Bind the keyrelease event
        combobox.bind('<KeyRelease>', on_keyrelease)

    def swap_currencies(self):
        """Swap the From and To currencies"""
        from_curr = self.from_box.get()
        to_curr = self.to_box.get()
        
        # Swap the values
        self.from_box.set(to_curr)
        self.to_box.set(from_curr)
        
    def convert(self):
        try:
            amount_str = self.amount_var.get().strip()
            if not amount_str:
                self.result_var.set("⚠ Please enter an amount")
                self.status_var.set("Error: No amount specified")
                return
                
            amount = float(amount_str)
            
            if amount <= 0:
                self.result_var.set("⚠ Please enter a positive amount")
                self.status_var.set("Error: Invalid amount")
                return
            
            frm = self.from_box.get()
            to = self.to_box.get()
            
            if not frm or not to:
                self.result_var.set("⚠ Please select both currencies")
                self.status_var.set("Error: Currency not selected")
                return
            
            result = self.manager.convert(frm, to, amount)
            
            # Get Currency objects for display
            from_currency = self.manager.currencies.get(frm)
            to_currency = self.manager.currencies.get(to)
            
            from_name = from_currency.get_name() if from_currency else frm
            to_name = to_currency.get_name() if to_currency else to
            
            # Get ExchangeRate info using to_string method
            from_rate = self.manager.get_exchange_rate_info(frm)
            to_rate = self.manager.get_exchange_rate_info(to)
            
            self.result_var.set(
                f"{amount:,.2f} {frm} ({from_name})\n"
                f"{result:,.2f} {to} ({to_name})"
            )
            
        except ValueError:
            self.result_var.set("⚠ Invalid amount format")
            self.status_var.set("Error: Please enter a valid number")
        except KeyError as e:
            self.result_var.set("⚠ Currency not found")
            self.status_var.set(f"Error: {str(e)}")
        except Exception as e:
            self.result_var.set("⚠ Conversion failed")
            self.status_var.set(f"Error: {str(e)}")
    
    def refresh_rates(self):
        self.status_var.set("Refreshing rates...")
        self.root.update()
        self.manager.refresh_rates()
        self.status_var.set("Rates refreshed successfully")

    def run(self):
        self.setup_ui()
        self.root.mainloop()


if __name__ == "__main__":
    manager = ExchangeManager(app_id=APP_ID)
    manager.refresh_rates()
    manager.load_currency_list()
    app = UIController(manager)
    app.run()