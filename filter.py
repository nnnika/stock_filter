import tkinter as tk
from tkinter import ttk
import pandas as pd
import os
import subprocess


def filter_data():
    # Market value filter
    try:
        min_value = float(min_value_entry.get())
        max_value = float(max_value_entry.get())
    except ValueError:
        result_label.config(text="")
        result_label.config(text="Invalid input. Please enter a valid number.")
        raise ValueError("Invalid input. Please enter a valid number.")

    # Industry and sector filter
    selected_industry = industry_menu.get()
    selected_sector = sector_menu.get()
    if selected_industry not in industry_menu['values']:
        treeview.delete(*treeview.get_children())  # Clear old data
        result_label.config(text="")
        result_label.config(text="Invalid industry input. Please select a valid industry.")
        raise ValueError("Invalid industry input. Please select a valid industry.")

    if selected_sector not in sector_menu['values']:
        treeview.delete(*treeview.get_children())  # Clear old data
        result_label.config(text="")
        result_label.config(text="Invalid sector input. Please select a valid sector.")
        raise ValueError("Invalid sector input. Please select a valid sector.")

    if selected_industry.upper() != "ALL" and selected_sector.upper() != "ALL":
        filtered_data = stocks.query(
            f"MarketCap >={min_value}&MarketCap<={max_value}&Industry=='{selected_industry}'"
            f"&Sector=='{selected_sector}'")
    elif selected_industry.upper() == "ALL" and selected_sector.upper() != "ALL":
        filtered_data = stocks.query(f"MarketCap >={min_value}&MarketCap<={max_value}&Sector=='{selected_sector}'")
    elif selected_industry.upper() != "ALL" and selected_sector.upper() == "ALL":
        filtered_data = stocks.query(
            f"MarketCap >={min_value}&MarketCap<={max_value}&Industry=='{selected_industry}'")
    else:
        filtered_data = stocks.query(f"MarketCap >={min_value}&MarketCap<={max_value}")

    if len(filtered_data) == 0:
        treeview.delete(*treeview.get_children())  # Clear old data
        result_label.config(text="")
        result_label.config(text="Filtered Stocks:\nNo stocks meet the criteria.")
    else:
        result_label.config(text="")
        select_column = ['Symbol', 'Name']  
        filtered_data_info = filtered_data[select_column]
        # Insert data into the table
        treeview.delete(*treeview.get_children())  # Clear old data
        for index, row in filtered_data_info.iterrows():
            treeview.insert('', 'end', values=row.tolist())


def on_item_click(event):
    selected_item = treeview.selection()[0]  # Get the identifier of the selected item
    values = treeview.item(selected_item, "values")
    print("Selected Item Values:", values)

    # Write the selected stock code into the file, create it if it does not exist
    if not os.path.exists('selected_stock.txt'):
        with open('selected_stock.txt', 'w') as f:
            pass
    with open('selected_stock.txt', 'w') as f:
        f.write(values[0])  # Assume the stock code is in the first position of values

    # Call out test.py
    subprocess.Popen(["python", "visual.py"])


def update_min_slider(value):
    min_value_entry.delete(0, tk.END)
    min_value_entry.insert(0, str(int(min_slider.get())))


def update_slider_from_min_entry(event):
    try:
        min_slider.set(float(min_value_entry.get()))
    except ValueError:
        pass


def update_slider_from_max_entry(event):
    try:
        max_slider.set(float(max_value_entry.get()))
    except ValueError:
        pass


def update_max_slider(value):
    max_value_entry.delete(0, tk.END)
    max_value_entry.insert(0, str(int(max_slider.get())))


def find_industry_list(event):
    selected_sector = sector_menu.get()
    industry_menu.set("ALL")
    if selected_sector not in sector_menu['values']:
        raise ValueError
    else:
        stocks['Industry'].fillna('other', inplace=True)
        if selected_sector == 'ALL':
            industry_lst = sorted(stocks['Industry'].unique().tolist() + ['ALL'])
        else:
            industry_lst = stocks.query(f"Sector=='{selected_sector}'")['Industry']
            industry_lst = industry_lst.unique().tolist() + ['ALL']
        industry_menu['values'] = industry_lst


# Determine whether to display the slider module
def toggle_scale_visibility():
    # Get checkbox status
    if show_market_cap.get():
        min_slider_label.grid(row=2, column=0, padx=10, pady=10)
        min_slider.grid(row=2, column=1, padx=10, pady=10)
        min_value_entry.grid(row=2, column=2, padx=10, pady=10)
        max_slider_label.grid(row=3, column=0, padx=10, pady=10)
        max_slider.grid(row=3, column=1, padx=10, pady=10)
        max_value_entry.grid(row=3, column=2, padx=10, pady=10)
    else:
        min_slider_label.grid_remove()
        min_slider.grid_remove()
        min_value_entry.grid_remove()
        max_slider_label.grid_remove()
        max_slider.grid_remove()
        max_value_entry.grid_remove()
        min_value_entry.delete(0, tk.END)
        min_value_entry.insert(0, str(default_min_value))
        max_value_entry.delete(0, tk.END)
        max_value_entry.insert(0, str(default_max_value))


stocks = pd.read_csv('companylist.csv').iloc[:, :-1]

try:
    root = tk.Tk()  # Create main window
    filtered_data = pd.DataFrame()

    # Stock sector dropdown box
    tk.Label(root, text="Stock Sector").grid(row=0, column=0, padx=10, pady=10)  # Create a label to prompt the user to select the stock sector and increase the distance between components
    sector_menu = ttk.Combobox(root)  # Create a dropdown menu for the user to select the stock sector
    stocks['Sector'].fillna('other', inplace=True)  # ++
    sector_menu['values'] = sorted(stocks['Sector'].unique().tolist() + ['ALL'])
    sector_menu.set("ALL")  # Default is ALL
    sector_menu.grid(row=0, column=1, padx=10, pady=10)  # Add the dropdown menu to the GUI and increase the distance between components
    sector_menu.bind("<<ComboboxSelected>>", find_industry_list)

    # Stock industry dropdown box (sector determines industry) # ++
    tk.Label(root, text="Stock Industry").grid(row=0, column=2, padx=10, pady=10)  # Create a label to prompt the user to select the stock industry and increase the distance between components
    industry_menu = ttk.Combobox(root)  # Create a dropdown menu for the user to select the stock industry
    industry_menu['values'] = ['ALL']
    industry_menu.set("ALL")  # Default is ALL
    industry_menu.grid(row=0, column=3, padx=10, pady=10)  # Add the dropdown menu to the GUI and increase the distance between components

    # Create checkbox variable
    show_market_cap = tk.BooleanVar()
    # Create checkbox and bind variable
    market_cap_checkbox = tk.Checkbutton(root, text="MarketCap", variable=show_market_cap,
                                         command=toggle_scale_visibility)
    market_cap_checkbox.grid(row=1, column=0, padx=10, pady=10)

    # Label to display checkbox status
    result_label = tk.Label(root, text="")
    result_label.grid(row=6, column=0, padx=10, pady=10)

    # Minimum value slider
    min_slider_label = ttk.Label(root, text="MarketCap Min Value:")
    min_slider_label.grid(row=2, column=0, padx=10, pady=10)
    min_slider = ttk.Scale(root, from_=min(stocks['MarketCap']), to=max(stocks['MarketCap']), orient="horizontal",
                           command=update_min_slider)
    min_slider.grid(row=2, column=1, padx=10, pady=10)

    # Minimum value input box
    default_min_value = int(min(stocks['MarketCap']))
    min_value_entry = ttk.Entry(root)
    min_value_entry.insert(0, str(default_min_value))
    min_value_entry.grid(row=2, column=2, padx=10, pady=10)
    min_slider.set(float(min_value_entry.get()))
    min_value_entry.bind("<FocusOut>", update_slider_from_min_entry)

    # Maximum value slider
    max_slider_label = ttk.Label(root, text="MarketCap Max Value:")
    max_slider_label.grid(row=3, column=0, padx=10, pady=10)
    max_slider = ttk.Scale(root, from_=min(stocks['MarketCap']), to=max(stocks['MarketCap']), orient="horizontal",
                           command=update_max_slider)
    max_slider.grid(row=3, column=1, padx=10, pady=10)

    # Maximum value input box
    default_max_value = int(max(stocks['MarketCap']))
    max_value_entry = ttk.Entry(root)
    max_value_entry.insert(0, str(default_max_value))
    max_value_entry.grid(row=3, column=2, padx=10, pady=10)
    max_slider.set(float(max_value_entry.get()))
    max_value_entry.bind("<FocusOut>", update_slider_from_max_entry)

    # Default to hide the corresponding components
    min_slider_label.grid_remove()
    min_slider.grid_remove()
    min_value_entry.grid_remove()
    max_slider_label.grid_remove()
    max_slider.grid_remove()
    max_value_entry.grid_remove()

    # Button to perform filtering operation
    filter_button = ttk.Button(root, text="Filter", command=filter_data)
    filter_button.grid(row=4, column=0, columnspan=3, padx=10, pady=10)

    # Create Treeview table
    select_column = ['Symbol', 'Name']
    treeview = ttk.Treeview(root, columns=select_column, show="headings")

    treeview.grid(row=5, column=1, padx=10, pady=10)

    # Create vertical scrollbar
    vsb = ttk.Scrollbar(root, orient="vertical", command=treeview.yview)
    vsb.grid(row=5, column=2, sticky="ns")
    treeview.configure(yscrollcommand=vsb.set)

    # Set table and scrollbar to change with window size
    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, weight=1)

    treeview.bind("<Double-1>", on_item_click)
    # Set column name
    treeview.heading('Symbol', text='Symbol')
    treeview.heading('Name', text='Name')

    root.title("Stock filter")  # Set GUI title
    root.mainloop()

except Exception as e:
    print("An error occurred:", str(e))

