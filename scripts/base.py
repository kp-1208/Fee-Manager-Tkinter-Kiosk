import tkinter as tk
from tkinter import messagebox, ttk, scrolledtext
from tkcalendar import DateEntry
import csv
import pandas as pd
from datetime import datetime
from PIL import Image, ImageTk
from report_generator import generate_report
from parameters import TRANS_FEE, TUT_FEE, STATIONERY_FEE, DEFAULTERS_PATH, CSV_PATH, HEADER_PATH, TITLE, WINDOW_SIZE

defaulters = pd.DataFrame()

def navigate_to_search_page():
    root.withdraw()  # Hide the main page
    search_page.deiconify()  # Show the search page

def navigate_to_update_page():
    root.withdraw()  # Hide the main page
    update_page.deiconify()  # Show the update page

def navigate_to_add_page():
    root.withdraw() # Hide the main page
    add_page.deiconify() #Show the add page

def navigate_to_main_page():
    search_page.withdraw()  # Hide the search page
    update_page.withdraw()  # Hide the update page
    add_page.withdraw() # Hide the add page
    root.deiconify()  # Show the main page

def close_window():
    messagebox.showinfo("Thank You", "Session Logged Out!")
    root.destroy()

def navigate_to_defaulter_page():
    search_page.withdraw()  # Hide the search page
    defaulter_page.deiconify()  # Show the defaulter page
    display_dataframe()

def navigate_to_search_page_from_defaulter():
    defaulter_page.withdraw()  # Hide the defaulter page
    search_page.deiconify()  # Show the search page

def save_dataframe_to_csv():
    # Save the dataframe to a CSV file
    defaulters.to_csv(DEFAULTERS_PATH, index=False)
    messagebox.showinfo("Success", "Defaulters Data Saved!")

def prepare_defaulters_dataframe():
    global defaulters
    data = pd.read_csv(CSV_PATH)
    defaulters = data[data.balance > 0]
    defaulters = defaulters.reset_index(drop=True)
    defaulters = defaulters[['ID', 'fname', 'lname', 'class', 'section',
                                        'tution_fee_p','tution_fee_a','trans_fee_p',
                                        'trans_fee_a','stationery_fee_p','stationery_fee_a','balance']]

def display_dataframe():
    # Prepare the dataframe to be displayed
    prepare_defaulters_dataframe()
    
    # Clear the existing content in the text widget
    df_text.delete('1.0', tk.END)

    # Insert the dataframe into the scrolled text widget
    df_text.insert(tk.END, defaulters.to_string())

def search_id(entered_id):
    # Search for the ID in the CSV file
    with open(CSV_PATH, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row['ID'] == entered_id:
                # Initialize total, paid, and balance
                total = 0
                paid = 0
                balance = 0
                
                if not row['tution_fee_p']:
                    row['tution_fee_p'] = 0
                if not row['trans_fee_p']:
                    row['trans_fee_p'] = 0
                if not row['stationery_fee_p']:
                    row['stationery_fee_p'] = 0
                    
                total = float(row['tution_fee_a']) + float(row['trans_fee_a']) + float(row['stationery_fee_a'])
                paid = float(row['tution_fee_p']) + float(row['trans_fee_p']) + float(row['stationery_fee_p'])
                
                # Display details in labels
                details_label.config(text=f"Details:\nID: {row['ID']}\nName: {row['fname']} {row['mname']} {row['lname']}")
                details_table.config(text=f"Amount Payable: {total}\nAmount Paid: {paid}\nTotal Amount Due: {row['balance']}\n\nLast Updated: {row['last_updated']}")
                return  # Exit the function if ID is found

        # If the loop completes without finding the ID, show error message
        messagebox.showerror("Error", "ID not found!")

def update_data():
    # Get the ID and amount entered by the user
    id = id_entry.get()
    id = int(id)
    tut_fee = tutfee_entry.get()
    trans_fee = transfee_entry.get()
    stationery_fee = stationeryfee_entry.get()
    if not tut_fee:
        tut_fee = 0
    if not trans_fee:
        trans_fee = 0
    if not stationery_fee:
        stationery_fee = 0

    added_values = {'tution_fee_p':float(tut_fee), 'trans_fee_p':float(trans_fee), 'stationery_fee_p':float(stationery_fee)}
    updated_values = {'ID':id,'last_updated':datetime.now().strftime("%d-%m-%Y %H:%M:%S")}
    
    # Update fee_details.csv with the provided information
    data = pd.read_csv(CSV_PATH)
    id_set = set(data['ID'])
    if int(id) not in id_set:
        messagebox.showerror("Error", "ID not found!")
        return
    data.loc[data['ID'] == id, added_values.keys()] += added_values.values()
    data.loc[data['ID'] == id, updated_values.keys()] = updated_values.values()
    data['balance'] = (data['tution_fee_a'] + data['trans_fee_a'] + 
                       data['stationery_fee_a']) - (data['tution_fee_p'] + data['trans_fee_p'] + 
                                              data['stationery_fee_p'])
    data.to_csv(CSV_PATH, index=False)
    
    messagebox.showinfo("Success", "Data Updated!")

def add_data():
    # Get the values entered by the user
    id = add_id_entry.get()
    if not id:
        messagebox.showerror("Error", "Please Enter ID!") 
        return
    fname = fname_entry.get()
    if not fname:
        messagebox.showerror("Error", "First Name is Mandatory!") 
        return
    mname = mname_entry.get()
    lname = lname_entry.get()
    f_fname = father_fname_entry.get()
    f_lname = father_lname_entry.get()
    phone_no = phone_no_entry.get()
    if not phone_no:
        messagebox.showerror("Error", "Please Enter Phone Number!") 
        return
    gender = gender_var.get()
    if not gender:
        messagebox.showerror("Error", "Please Select Gender!") 
        return
    dob = dob_entry.get()
    class_selected = class_var.get()
    if not class_selected:
        messagebox.showerror("Error", "Please Select Class!") 
        return
    section_selected = section_var.get()
    if not section_selected:
        messagebox.showerror("Error", "Please Select Section!") 
        return
    doj = doj_entry.get()
    transport_fee_opt = transport_fee_var.get()
    if transport_fee_opt:
        if transport_fee_opt == 'Yes':
            trans_fee = TRANS_FEE
        else:
            trans_fee = 0
    else:
        messagebox.showerror("Error", "Please Select Transport Option!") 
        return   
    stationery_fee_opt = stationery_fee_var.get()
    if stationery_fee_opt:
        if stationery_fee_opt == 'Yes':
            stationery_fee = STATIONERY_FEE
        else:
            stationery_fee = 0
    else:
        messagebox.showerror("Error", "Please Select stationery Set Option!")   
        return 
    

    added_values = {'ID':id, 'fname':fname, 'mname':mname, 'lname':lname, 'f_fname':f_fname,
                    'f_lname':f_lname, 'phone_no':phone_no, 'gender':gender, 'dob':dob,
                    'class':class_selected, 'section':section_selected, 'doj':doj,
                    'tution_fee_a':TUT_FEE, 'trans_fee_a':trans_fee, 'stationery_fee_a':stationery_fee,
                    'tution_fee_p':0, 'trans_fee_p':0, 'stationery_fee_p':0,
                    'balance':TUT_FEE + trans_fee + stationery_fee,
                    'last_updated':datetime.now().strftime("%d-%m-%Y %H:%M:%S")}

    # Update fee_details.csv with the provided information
    data = pd.read_csv(CSV_PATH)
    id_set = set(data['ID'])
    if int(id) in id_set:
        messagebox.showerror("Error", "Entered ID already exists!")
        return
    new_data = pd.DataFrame([added_values])
    data = pd.concat([data, new_data], ignore_index=True)
    print(data[data.ID == id])
    data.to_csv(CSV_PATH, index=False)
    
    messagebox.showinfo("Success", "Data Added!")

root = tk.Tk()
root.title(TITLE)
root.attributes("-fullscreen", True)
# root.geometry(WINDOW_SIZE)

frame_1 = tk.Frame(root, bg="#00465e")
frame_1.place(relwidth=1, relheight=1)

# Load and resize the image
image = Image.open(HEADER_PATH)
window_width = root.winfo_screenwidth()
aspect_ratio = image.width / image.height
desired_width = int(window_width)
desired_height = int(desired_width / aspect_ratio)
image = image.resize((desired_width, desired_height))
photo = ImageTk.PhotoImage(image)

# Create a label to display the image
image_label = tk.Label(frame_1, image=photo)
image_label.grid(row=0, column=0, columnspan=9)

# Create buttons
# buttons_frame = tk.Frame(frame_1, bg="#00465e")
# buttons_frame.pack(fill="both", expand=True)

search_button = tk.Button(root, text="Search and Verify:\n\n\nVerify Individual Records.\nView Fee Defaulters.",
                          command=navigate_to_search_page, bg="#0c343d", fg="white",
                          activebackground="#006c91")
update_button = tk.Button(root, text="Add a transaction:\n\n\nEnter New Payments.\nGenerate Payment Receipt.",
                          command=navigate_to_update_page, bg="#0c343d", fg="white", activebackground="#006c91")
add_button = tk.Button(root, text="New Registration:\n\n\nRegister a new student.\nAdd details to the data.",
                       command=navigate_to_add_page, bg="#0c343d", fg="white", activebackground="#006c91")
close_button = tk.Button(root, text="Log Out", command=close_window, bg="#0c343d",
                         fg="red", activebackground="#b21100", activeforeground="black")

# Apply some basic styling to the buttons
search_button.config(width=30, height=20, font=("Arial", 12))
update_button.config(width=30, height=20, font=("Arial", 12))
add_button.config(width=30, height=20, font=("Arial", 12))
close_button.config(width=30, height=2, font=("Arial", 12))

# Calculate padding values relative to the window size
window_width, window_height = map(int, WINDOW_SIZE.split('x'))

# Define padding fractions relative to the window size
padding_x = window_width // 20  # 5% of the window width
padding_y = window_height // 20  # 5% of the window height

# Pack buttons with relative padding
search_button.grid(row=1, column=0, padx=padding_x, pady=(padding_y * 6,0))
update_button.grid(row=1, column=1, padx=padding_x, pady=(padding_y * 6,0))
add_button.grid(row=1, column=2, padx=padding_x, pady=(padding_y * 6,0))
close_button.grid(row=2, column=0, columnspan=9,padx=padding_x, pady=(padding_y,0))

# Create search page
search_page = tk.Toplevel()
search_page.title(TITLE)
# search_page.geometry(WINDOW_SIZE)
search_page.attributes("-fullscreen", True)
search_page.protocol("WM_DELETE_WINDOW", root.destroy)  # Handle window close event

# Create frame for search page
frame_2 = tk.Frame(search_page, bg="#00465e")  
frame_2.place(relwidth=1, relheight=1)

# Create a label to display the image
image_label = tk.Label(frame_2, image=photo)
image_label.grid(row=0, column=0, columnspan=5)

# Create widgets for search page
search_id_label = tk.Label(search_page, text="Enter ID:")
search_id_entry = tk.Entry(search_page, bg="#0c343d", fg="white")
submit_button = tk.Button(search_page, text="Show Record", 
                          command=lambda: search_id(search_id_entry.get()),
                          bg="#0c343d", fg="white", activebackground="#006c91")
details_label = tk.Label(search_page, text="")
details_table = tk.Label(search_page, text="")
report_button = tk.Button(search_page, text="Generate Report", 
                          command=lambda: generate_report(search_id_entry.get()),
                          bg="#0c343d", fg="white", activebackground="#006c91")
defaulter_button = tk.Button(search_page, text="View Defaulters", command=navigate_to_defaulter_page,
                             bg="#0c343d", fg="white", activebackground="#006c91")
back_button_search = tk.Button(search_page, text="Back to Main Page", 
                               command=navigate_to_main_page,
                               bg="#0c343d", fg="white", activebackground="#006c91")


# Apply some basic styling to the widgets
search_id_label.config(bg="#00465e", fg="white", font=("Arial", 12))
search_id_entry.config(font=("Arial", 12))
submit_button.config(width=20, height=1, font=("Arial", 12))
details_label.config(bg="#00465e", fg="white", font=("Arial", 12))
details_table.config(bg="#00465e", fg="white", font=("Arial", 12))
report_button.config(width=20, height=1, font=("Arial", 12))
back_button_search.config(width=20, height=1, font=("Arial", 12))
defaulter_button.config(width=20, height=1, font=("Arial", 12))

# Layout widgets for search page
search_page.columnconfigure(0, weight=1)
search_page.columnconfigure(1, weight=1)

search_id_label.grid(row=1, column=0, padx=padding_x, pady=(padding_y * 6,0))
search_id_entry.grid(row=1, column=1, padx=padding_x, pady=(padding_y * 6,0))
submit_button.grid(row=4, column=0, columnspan=1, padx=padding_x, pady=(padding_y,0))
details_label.grid(row=2, column=0, columnspan=3, padx=padding_x, pady=(padding_y,0))
details_table.grid(row=3, column=0, columnspan=3, padx=padding_x, pady=(padding_y,0))
report_button.grid(row=4, column=1, columnspan=3, padx=padding_x, pady=(padding_y,0))
defaulter_button.grid(row=5, column=0, columnspan=2, padx=padding_x, pady=(padding_y * 2,0))
back_button_search.grid(row=8, column=0, columnspan=3, padx=padding_x, pady=(padding_y,0))
search_page.withdraw()  # Hide the search page initially

# Create defaulter page
defaulter_page = tk.Toplevel()
defaulter_page.title("Defaulter Page")
# defaulter_page.geometry(WINDOW_SIZE)
defaulter_page.attributes("-fullscreen", True)
defaulter_page.protocol("WM_DELETE_WINDOW", root.destroy)  # Handle window close event

# Create frame for defaulter page
frame_2_1 = tk.Frame(defaulter_page, bg="#00465e")  
frame_2_1.place(relwidth=1, relheight=1)

# Add buttons to defaulter page
back_button_defaulter = tk.Button(defaulter_page, text="Back to Search Page", 
                                  command=navigate_to_search_page_from_defaulter,
                                  bg="#0c343d", fg="white", activebackground="#006c91")
back_button_defaulter.pack(pady=10)

save_button_defaulter = tk.Button(defaulter_page, text="Save Dataframe as CSV", 
                                  command=save_dataframe_to_csv,
                                  bg="#0c343d", fg="white", activebackground="#006c91")
save_button_defaulter.pack(pady=10)

# Display the dataframe in a scrolled text widget
df_frame = tk.Frame(defaulter_page, bg="#0c343d")
df_frame.pack(fill="both", expand=True)

# Create a scrolled text widget
df_text = scrolledtext.ScrolledText(df_frame, wrap=tk.WORD, width=30, height=30, bg="#0c343d", fg="white")
df_text.pack(fill="both", expand=True)

defaulter_page.withdraw()

# Create update page
update_page = tk.Toplevel()
update_page.title(TITLE)
# update_page.geometry(WINDOW_SIZE)
update_page.attributes("-fullscreen", True)
update_page.protocol("WM_DELETE_WINDOW", root.destroy)  # Handle window close event

# Create frame for update page
frame_3 = tk.Frame(update_page, bg="#00465e")  
frame_3.place(relwidth=1, relheight=1)

# Create a label to display the image
image_label = tk.Label(frame_3, image=photo)
image_label.grid(row=0, column=0, columnspan=9)

# Create widgets for update page 
id_label = tk.Label(update_page, bg="#00465e", fg="white", text="Enter ID:")
id_entry = tk.Entry(update_page, bg="#0c343d", fg="white", font=("ARIAL",12))
tutfee_label = tk.Label(update_page, bg="#00465e", fg="white", text="Enter Tution Fee Paid:")
tutfee_entry = tk.Entry(update_page, bg="#0c343d", fg="white", font=("ARIAL",12))
transfee_label = tk.Label(update_page, bg="#00465e", fg="white", text="Enter Transport Fee Paid:")
transfee_entry = tk.Entry(update_page, bg="#0c343d", fg="white", font=("ARIAL",12))
stationeryfee_label = tk.Label(update_page, bg="#00465e", fg="white", text="Enter Stationery Fee Paid:")
stationeryfee_entry = tk.Entry(update_page, bg="#0c343d", fg="white", font=("ARIAL",12))
update_button = tk.Button(update_page, text="Enter Data", command=update_data,
                          bg="#0c343d", fg="white", activebackground="#006c91")
report_button_update = tk.Button(update_page, text="Print Receipt", 
                          command=lambda: generate_report(id_entry.get()),
                          bg="#0c343d", fg="white", activebackground="#006c91")

back_button_update = tk.Button(update_page, text="Back to Main Page", 
                               command=navigate_to_main_page,
                               bg="#0c343d", fg="white", activebackground="#006c91")

# Apply Styling to Update Page Buttons and labels
id_label.config(bg="#00465e", fg="white", font=("Arial", 12))
tutfee_label.config(bg="#00465e", fg="white", font=("Arial", 12))
transfee_label.config(bg="#00465e", fg="white", font=("Arial", 12))
stationeryfee_label.config(bg="#00465e", fg="white", font=("Arial", 12))
update_button.config(width=20, height=1, font=("Arial", 12))
report_button_update.config(width=20, height=1, font=("Arial", 12))
back_button_update.config(width=20, height=1, font=("Arial", 12))

# Layout widgets for update page
update_page.columnconfigure(0, weight=1)
update_page.columnconfigure(1, weight=1)
# update_page.rowconfigure(4, weight=1)
# update_page.rowconfigure(7, weight=3)

id_label.grid(row=1, column=0, padx=padding_x, pady=(padding_y * 6,padding_y))
id_entry.grid(row=1, column=1, padx=padding_x, pady=(padding_y * 6,padding_y))
tutfee_label.grid(row=2, column=0, padx=5, pady=5)
tutfee_entry.grid(row=2, column=1, padx=5, pady=5)
transfee_label.grid(row=3, column=0, padx=5, pady=5)
transfee_entry.grid(row=3, column=1, padx=5, pady=5)
stationeryfee_label.grid(row=4, column=0, padx=5, pady=5)
stationeryfee_entry.grid(row=4, column=1, padx=5, pady=5)
update_button.grid(row=6, column=0, columnspan=2, padx=5, pady=40)
report_button_update.grid(row=7, column=0, columnspan=2, padx=5, pady=40)
back_button_update.grid(row=8, column=0, columnspan=2, padx=5, pady=100)
update_page.withdraw()  # Hide the update page initially

# Create add page
add_page = tk.Toplevel()
add_page.title(TITLE)
# add_page.geometry(WINDOW_SIZE)
add_page.attributes("-fullscreen", True)
add_page.protocol("WM_DELETE_WINDOW", root.destroy)  # Handle window close event

# Create frame for Add page
frame_4 = tk.Frame(add_page, bg="#00465e")  
frame_4.place(relwidth=1, relheight=1)

# Create a label to display the image
image_label = tk.Label(frame_4, image=photo)
image_label.grid(row=0, column=0, columnspan=9)

# Create widgets for add page 
add_id_label = tk.Label(add_page, bg="#00465e", fg="white", text="*Enter ID:", font=("ARIAL",12))
add_id_entry = tk.Entry(add_page, bg="#0c343d", fg="white", font=("ARIAL",12))
fname_label = tk.Label(add_page, bg="#00465e", fg="white", text="*Enter First Name:", font=("ARIAL",12))
fname_entry = tk.Entry(add_page, bg="#0c343d", fg="white", font=("ARIAL",12))
mname_label = tk.Label(add_page, bg="#00465e", fg="white", text="Enter Middle Name:", font=("ARIAL",12))
mname_entry = tk.Entry(add_page, bg="#0c343d", fg="white", font=("ARIAL",12))
lname_label = tk.Label(add_page, bg="#00465e", fg="white", text="Enter Last Name:", font=("ARIAL",12))
lname_entry = tk.Entry(add_page, bg="#0c343d", fg="white", font=("ARIAL",12))
father_fname_label = tk.Label(add_page, bg="#00465e", fg="white", text="Enter Father's First Name:", font=("ARIAL",12))
father_fname_entry = tk.Entry(add_page, bg="#0c343d", fg="white", font=("ARIAL",12))
father_lname_label = tk.Label(add_page, bg="#00465e", fg="white", text="Enter Father's Last Name:", font=("ARIAL",12))
father_lname_entry = tk.Entry(add_page, bg="#0c343d", fg="white", font=("ARIAL",12))
phone_no_label = tk.Label(add_page, bg="#00465e", fg="white", text="*Enter Phone Number:", font=("ARIAL",12))
phone_no_entry = tk.Entry(add_page, bg="#0c343d", fg="white", font=("ARIAL",12))
gender_label = tk.Label(add_page, bg="#00465e", fg="white", text="*Select Gender:", font=("ARIAL",12))
gender_var = tk.StringVar()
gender_radio_male = tk.Radiobutton(add_page, text="Male", variable=gender_var, value="Male",
                                   bg="#00465e", fg="black", activebackground="#00465e", font=("ARIAL",12))
gender_radio_female = tk.Radiobutton(add_page, text="Female", variable=gender_var, 
                                     value="Female",
                                     bg="#00465e", fg="black", activebackground="#00465e", font=("ARIAL",12))
gender_radio_other = tk.Radiobutton(add_page, text="Other", variable=gender_var, 
                                    value="Other",bg="#00465e", fg="black", activebackground="#00465e", font=("ARIAL",12))
dob_label = tk.Label(add_page, bg="#00465e", fg="white", text="Select Date of Birth:", font=("ARIAL",12))
dob_entry = DateEntry(add_page, width=12, background='darkblue', foreground='white', borderwidth=2)
class_label = tk.Label(add_page, bg="#00465e", fg="white", text="*Select Class:", font=("ARIAL",12))
class_var = tk.StringVar()
class_dropdown = ttk.Combobox(add_page, textvariable=class_var, values=["Class 1", "Class 2", "Class 3"])
section_label = tk.Label(add_page, bg="#00465e", fg="white", text="*Select Section:", font=("ARIAL",12))
section_var = tk.StringVar()
section_dropdown = ttk.Combobox(add_page, textvariable=section_var, values=["Section A", "Section B", "Section C"])
doj_label = tk.Label(add_page, bg="#00465e", fg="white", text="Select Date of Joining:", font=("ARIAL",12))
doj_entry = DateEntry(add_page, width=12, background='darkblue', foreground='white', borderwidth=2)
transport_fee_label = tk.Label(add_page, bg="#00465e", fg="white", text="*Transport Opted?:", font=("ARIAL",12))
transport_fee_var = tk.StringVar()
transport_fee_yes = tk.Radiobutton(add_page, text="Yes", variable=transport_fee_var, 
                                   value="Yes", bg="#00465e", fg="black", activebackground="#00465e", font=("ARIAL",12))
transport_fee_no = tk.Radiobutton(add_page, text="No", variable=transport_fee_var, value="No",
                                  bg="#00465e", fg="black", activebackground="#00465e", font=("ARIAL",12))
stationery_fee_label = tk.Label(add_page, bg="#00465e", fg="white", text="*stationery Set Opted?:", font=("ARIAL",12))
stationery_fee_var = tk.StringVar()
stationery_fee_yes = tk.Radiobutton(add_page, text="Yes", variable=stationery_fee_var, value="Yes",
                              bg="#00465e", fg="black", activebackground="#00465e", font=("ARIAL",12))
stationery_fee_no = tk.Radiobutton(add_page, text="No", variable=stationery_fee_var, value="No",
                             bg="#00465e", fg="black", activebackground="#00465e", font=("ARIAL",12))
add_button = tk.Button(add_page, text="Submit", command=add_data,
                       bg="#0c343d", fg="white", activebackground="#006c91")
back_button_add = tk.Button(add_page, text="Back to Main Page", 
                            command=navigate_to_main_page,
                            bg="#0c343d", fg="white", activebackground="#006c91")

# Apply styling to Add Page buttons
add_button.config(width=20, height=1, font=("Arial", 12))
back_button_add.config(width=20, height=1, font=("Arial", 12))

# Layout widgets for add page
add_id_label.grid(row=1, column=0, padx=padding_x, pady=(padding_y * 6,padding_y))
add_id_entry.grid(row=1, column=1, padx=padding_x, pady=(padding_y * 6,padding_y))
fname_label.grid(row=2, column=0, padx=padding_x/2, pady=20)
fname_entry.grid(row=2, column=1, padx=15, pady=20)
mname_label.grid(row=2, column=2, padx=15, pady=20)
mname_entry.grid(row=2, column=3, padx=15, pady=20)
lname_label.grid(row=2, column=4, padx=15, pady=20)
lname_entry.grid(row=2, column=5, padx=15, pady=20)
father_fname_label.grid(row=3, column=0, padx=15, pady=20)
father_fname_entry.grid(row=3, column=1, padx=15, pady=20)
father_lname_label.grid(row=3, column=4, padx=15, pady=20)
father_lname_entry.grid(row=3, column=5, padx=15, pady=20)
phone_no_label.grid(row=4, column=0, padx=15, pady=20)
phone_no_entry.grid(row=4, column=1, padx=15, pady=20)
gender_label.grid(row=5, column=0, padx=15, pady=20)
gender_radio_male.grid(row=5, column=2, padx=15, pady=20)
gender_radio_female.grid(row=5, column=3, padx=15, pady=20)
gender_radio_other.grid(row=5, column=4, padx=15, pady=20)
dob_label.grid(row=6, column=0, padx=15, pady=20)
dob_entry.grid(row=6, column=1, padx=15, pady=20)
class_label.grid(row=7, column=0, padx=15, pady=20)
class_dropdown.grid(row=7, column=1, padx=15, pady=20)
section_label.grid(row=7, column=3, padx=15, pady=20)
section_dropdown.grid(row=7, column=4, padx=15, pady=20)
doj_label.grid(row=6, column=3, padx=15, pady=20)
doj_entry.grid(row=6, column=4, padx=15, pady=20)
transport_fee_label.grid(row=8, column=0, padx=15, pady=20)
transport_fee_yes.grid(row=8, column=1, padx=15, pady=20)
transport_fee_no.grid(row=8, column=2, padx=15, pady=20)
stationery_fee_label.grid(row=8, column=3, padx=15, pady=20)
stationery_fee_yes.grid(row=8, column=4, padx=15, pady=20)
stationery_fee_no.grid(row=8, column=5, padx=15, pady=20)
add_button.grid(row=9, column=0, columnspan=9, padx=15, pady=(padding_y * 3,0))
back_button_add.grid(row=10, column=0, columnspan=9, padx=15, pady=20)
add_page.withdraw()  # Hide the add page initially

# Run the application
root.mainloop()