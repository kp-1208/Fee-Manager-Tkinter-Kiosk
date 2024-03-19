import tkinter as tk
from datetime import datetime

now = datetime.now().strftime("%d%m%Y%H%M%S")

def get_screen_size():
    root = tk.Tk()
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    root.destroy()
    return screen_width, screen_height

# Title of the window
TITLE = 'Fee Manager Kiosk'

# Transport Fee 
TRANS_FEE = 250
#Book Set Fee
STATIONERY_FEE = 150
# Tution Fee
TUT_FEE = 2000

# Path to the Fee Data CSV File
CSV_PATH = 'data/fee_details.csv'
# Path to defaulters data
DEFAULTERS_PATH = f'reports/defaulters_{now}.csv'
# Path to Logo Image
LOGO_PATH = 'static/Report_Header.png'
# Path to Sign Image
SIGN_PATH = 'static/sign.png'
# Path to Store Reports
REPORT_PATH = 'reports/'
# Path to Header Image
HEADER_PATH = 'static/Kiosk_Header.jpeg'

# Interface Window Size
width, height = get_screen_size()
WINDOW_SIZE = f"{width}x{height}"
