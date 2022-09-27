from bs4 import BeautifulSoup
import httpx
import pandas
import tkinter
from tkinter import messagebox
import os

CSV_FILE = os.path.join(os.path.join(os.path.expanduser('~')), 'Desktop\stock_data_file.csv')
COL_NAME = ["Stock Name", "Previous Close", "Open", "Bid", "Ask", "Day's Range", "52 Week Range", "Volume",
            "Avg. Volume", "Market Cap", "Beta (5Y Monthly)", "PE Ratio (TTM)", "EPS (TTM)", "Earnings Date",
            "Forward Dividend & Yield", "Ex-Dividend Date", "1y Target Est"]
FONT = ("Arial", 15)


def main():
    windows = tkinter.Tk()
    windows.title("Stock Scraping")
    windows.configure(padx=10, pady=10)

    # create label
    company_label = tkinter.Label(text="Please type the ACRONYM of the stock, separated by coma(s) ',':", font=FONT)
    company_label.pack()

    # create entry to get user input
    company_var = tkinter.StringVar()
    company_entry = tkinter.Entry(textvariable=company_var, width=50, font=FONT, bg="#E1FFEE", borderwidth=5)
    company_entry.insert(0, "E.g: amzn, Tsla,GOOG... ")
    company_entry.focus()
    company_entry.pack()

    # create button to start scraping
    company_button = tkinter.Button(font=FONT, width=25, text="START SCRAPING!",
                                    command=lambda: stock_scrape(company_var.get()))
    company_button.pack()

    windows.mainloop()


def stock_scrape(companies: str):
    # initialize the data to be saved
    df = pandas.DataFrame(columns=COL_NAME)

    for name in companies.split(","):
        # access the content of the website
        name = name.strip().upper()
        response = httpx.get(url=f"https://finance.yahoo.com/quote/{name}")
        try:  # try for any error (user input wrong name)
            response.raise_for_status()
        except httpx.HTTPStatusError:
            messagebox.showwarning(title=f"{name} NOT FOUND", message=f"NO {name} STOCK found ON YAHOO FINANCE")
        else:
            # if found: get content of the tables for the company's stock data
            stock_content = BeautifulSoup(response.content, 'html.parser')
            table_rows = stock_content.find_all(name="td", class_="Ta(end) Fw(600) Lh(14px)")
            stock_data = [name.strip().upper()] + [row.get_text() for row in table_rows]

            # export the data out to dataFrame to be saved in file
            df.loc[len(df.index)] = stock_data

    # export the collected data to file
    with open(CSV_FILE, 'w') as _:
        df.to_csv(CSV_FILE, index=False)
        messagebox.showinfo(title="Successful!",
                            message=f"The data has been stored successfully on your DESKTOP in "
                                    f"file: stock_data_file.csv.\n    - Path: {CSV_FILE}")
        os.startfile(CSV_FILE)


if __name__ == "__main__":
    main()
