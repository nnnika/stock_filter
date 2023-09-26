import tkinter as tk  # Import tkinter library to create GUI
import yfinance as yf  # Import yfinance library to get stock data
import matplotlib.pyplot as plt  # Import matplotlib library to draw charts
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg  # Import matplotlib's Tkinter interface
import os
from tkinter import scrolledtext


# Encapsulate the code in visual.py into a function
def run_visual():
    stock_code = ''
    if os.path.isfile('selected_stock.txt'):
        # Open the file and read the stock code
        with open('selected_stock.txt', 'r') as file:
            stock_code = file.read().strip()
            
        # Clear the file content
        with open('selected_stock.txt', 'w') as file:
            file.write('')
    else:
        stock_code = ''
    last_symbol = None  # Create a variable to store the last stock code

    def get_data(symbol, period):  # Define a function to get stock data
        data = yf.download(symbol, period=period)  # Get stock data
        if data.empty:  # If the data is empty
             symbol = 'NVDA'
             data = yf.download(symbol, period=period)
       
        return data  # Return data

    def plot_data(data):  # Define a function to draw stock data chart
        fig = plt.Figure(figsize=(9, 7), dpi=100)  # Create a larger chart
        ax = fig.add_subplot(111)  # Add a subplot
        ax.plot(data.index, data['Close'], label='Close')  # Draw the closing price curve
        ax.plot(data.index, data['Open'], label='Open')  # Draw the opening price curve
        ax.legend(loc='best')  # Add a legend
        return fig  # Return the chart

    def update_plot(canvas, fig):  # Define a function to update the chart
        canvas.get_tk_widget().grid_forget()  # Clear the old chart
        canvas = FigureCanvasTkAgg(fig, master=root)  # Create a new chart
        canvas.draw()  # Draw the chart
        canvas.get_tk_widget().grid(row=4, column=0, columnspan=4, padx=10, pady=10)  # Add the chart to the GUI and increase the distance between components

    def fetch_data():  # Define a function to get data and update the chart
        global last_symbol
        if e1.get()=="":
            tk.messagebox.showwarning('Reminder', 'Please input your stock code!')
            e1.delete(0, tk.END)
        else:
            
          # Declare a global variable
            if e1.get().isdigit()==False and e1.get().__len__()<=4:
                symbol = e1.get() # Get the stock code entered by the user
                period = v.get()  # Get the time period selected by the user
                data = get_data(symbol, period)  # Get stock data
                fig = plot_data(data)  # Draw the chart
                update_plot(canvas, fig)  # Update the chart
            else:
                tk.messagebox.showwarning('Reminder', 'Invalid stock symbol!')
                e1.delete(0, tk.END)
    
            # If the user does not enter a stock code

    root = tk.Tk()  # Create the main window
    v = tk.StringVar(root, "1y")  # Create a string variable to store the time period selected by the user

    def fetch_balance_sheet():  # Define a function to get balance sheet data
        symbol = e1.get()  # Get the stock code entered by the user
        if symbol and symbol.isdigit()==False and symbol.__len__()<=4:  # If the user enters a stock code
            ticker = yf.Ticker(symbol)  # Create a Ticker object
            balance_sheet = ticker.balancesheet  # Get balance sheet data
            if balance_sheet.empty:
                ticker = yf.Ticker('NVDA')  # Create a Ticker object
                balance_sheet = ticker.balancesheet
            balance_sheet_str = balance_sheet.to_string(index=True)
            show_dataframe_popup(balance_sheet_str)
        else:
            if symbol:  # If the user does not enter a stock code
                show_error_popup("Invalid stock symbol!")
                e1.delete(0, tk.END)
            else:
                show_error_popup("Please enter a stock symbol.")

    def show_dataframe_popup(df_text):
        df_window = tk.Toplevel(root)
        df_window.title("Balance Sheet Viewer")
        df_window.geometry("900x800")  # Set width and height

        df_text_widget = scrolledtext.ScrolledText(df_window, wrap=tk.WORD, height=20, width=80)
        df_text_widget.insert(tk.END, df_text)
        df_text_widget.pack(fill="both", expand=True)

    def show_error_popup(message):
        error_window = tk.Toplevel(root)
        error_window.title("Error")
        error_label = tk.Label(error_window, text=message)
        error_label.pack(padx=10, pady=10)

    tk.Button(root, text='Fetch Balance Sheet', command=fetch_balance_sheet).grid(row=3, column=2, padx=10, pady=10)

    tk.Label(root, text="Stock symbol").grid(row=1, column=0, padx=10, pady=10)  # Create a label to prompt the user to enter the stock code and increase the distance between components
    e1 = tk.Entry(root)  # Create an input box for the user to enter the stock code
    e1.insert(0, stock_code)
    e1.grid(row=1, column=1, padx=5, pady=5)  # Add the input box to the GUI and increase the distance between components

    tk.Radiobutton(root, text="1 Week", variable=v, value="1wk").grid(row=2, column=0, padx=5, pady=5)  # Create a radio button for the user to select the time period
    tk.Radiobutton(root, text="1 Month", variable=v, value="1mo").grid(row=2, column=1, padx=5, pady=5)  # Create a radio button for the user to select the time period
    tk.Radiobutton(root, text="6 Months", variable=v, value="6mo").grid(row=2, column=2, padx=5, pady=5)  # Create a radio button for the user to select the time period
    tk.Radiobutton(root, text="1 Year", variable=v, value="1y").grid(row=2, column=3, padx=5, pady=5)  # Create a radio button for the user to select the time period
    v.set("1wk")

    tk.Button(root, text='Fetch Data', command=fetch_data).grid(row=3, column=1, padx=10, pady=10)  # Create a button to get data and update the chart, and increase the distance between components

    fig = plt.Figure(figsize=(10, 8), dpi=100)  # Create a chart
    canvas = FigureCanvasTkAgg(fig, master=root)  # Create a canvas to display the chart
    canvas.draw()  # Draw the chart
    canvas.get_tk_widget().grid(row=4, column=0, columnspan=4, padx=10, pady=10)
    root.title("Stock pricing")  # Set the title of the GUI

    root.mainloop()  # Start the main loop


if __name__ == "__main__":
    run_visual()



