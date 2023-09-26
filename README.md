# Stock Filtering and Visualization with User Login and Registration System  

This project combines a user login and registration system with stock filtering and visualization capabilities, all presented through a graphical user interface (GUI). It utilizes the Tkinter library for the GUI, SQLite for database storage, yfinance for stock data retrieval, and Matplotlib for chart visualization.

## Table of Contents

- [Introduction](#introduction)
- [Dependencies](#dependencies)
- [Usage](#usage)
- [Login](#login)
- [Registration](#registration)
- [Stock Filtering](#stock-filtering)
- [Stock Visualization](#stock-visualization)
- [Contributors](#contributors)

## Introduction

This project offers a multifunctional application that includes user authentication, stock filtering based on market value, industry, and sector, and the ability to visualize stock data using interactive charts.

## Dependencies

Before running this project, ensure you have the following dependencies installed:

- [Python](https://www.python.org/downloads/) (version 3.7 or higher)
- [Tkinter](https://docs.python.org/3/library/tkinter.html) (for GUI)
- [Pillow](https://pillow.readthedocs.io/en/stable/) (for image display)
- [SQLite](https://www.sqlite.org/index.html) (for database storage)
- [Pandas](https://pandas.pydata.org/) (for data manipulation)
- [yfinance](https://pypi.org/project/yfinance/) (for stock data retrieval)
- [Matplotlib](https://matplotlib.org/stable/users/installing.html) (for chart visualization)

You can install the required libraries using pip:

```
pip install Pillow pandas yfinance matplotlib
```
## Usage

To run the application, execute the following command:
```
python login_interface.py
```
The main GUI window will open, allowing you to log in, register, filter stocks, and visualize stock data.

## Login

- Enter your username and password in the respective text fields.
- Click the "Log in" button.
- If the credentials are correct, a success message will appear, and you will be logged in.
- If the credentials are incorrect, an error message will be displayed.

## Registration

- Click the "Register" button on the login screen to open the registration window.
- Enter your desired username and password in the provided fields.
- Click the "Confirm" button to register.
- If the username is already taken, you will receive a warning.
- If registration is successful, you will receive a confirmation message.

## Stock Filtering

- Select a stock sector and industry from the dropdown menus.
- Check the "MarketCap" checkbox to enable market value filtering.
- Adjust the minimum and maximum value sliders to define the filtering range.
- Click the "Filter" button to display filtered stocks in the table.
- Double-click a stock in the table to select it and write its code to a file named selected_stock.txt.

## Stock Visualization

- Enter a stock symbol in the provided input box.
- Select the desired time period (1 Week, 1 Month, 6 Months, 1 Year).
- Click the "Fetch Data" button to retrieve stock data.
- The interactive chart will display the closing and opening prices of the selected stock over the specified time period.


