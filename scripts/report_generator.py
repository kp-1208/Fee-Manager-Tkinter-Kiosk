from tkinter import messagebox
import csv
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Image, Table, TableStyle, Paragraph
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from datetime import datetime
from parameters import CSV_PATH, LOGO_PATH, SIGN_PATH, REPORT_PATH

def generate_report(entered_id):
    # Get the ID entered by the user
    # entered_id = search_id_entry.get()
    
    # If the ID entry is empty, show error message
    if not entered_id:
        messagebox.showerror("Error", "Please enter an ID.")
        return

    # Search for the ID in the CSV file
    with open(CSV_PATH, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row['ID'] == entered_id:
                # Initialize total, paid, and balance
                total = 0
                paid = 0
                tut_bal = 0
                trans_bal = 0
                book_bal = 0
                
                if not row['tution_fee_p']:
                    row['tution_fee_p'] = 0
                if not row['trans_fee_p']:
                    row['trans_fee_p'] = 0
                if not row['stationery_fee_p']:
                    row['stationery_fee_p'] = 0
                if not row['balance']:
                    row['balance'] = 0

                total = float(row['tution_fee_a']) + float(row['trans_fee_a']) + float(row['stationery_fee_a'])
                paid = float(row['tution_fee_p']) + float(row['trans_fee_p']) + float(row['stationery_fee_p'])
                
                # Calculate balance
                tut_bal = float(row['tution_fee_a']) - float(row['tution_fee_p'])
                trans_bal = float(row['trans_fee_a']) - float(row['trans_fee_p'])
                book_bal = float(row['stationery_fee_a']) - float(row['stationery_fee_p'])

                # Current Timestamp
                now = datetime.now().strftime("%d%m%Y%H%M%S")
                now1 = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
                
                # Create a PDF report with the details
                doc = SimpleDocTemplate(f"{REPORT_PATH}{entered_id}_{now}.pdf", pagesize=letter)

                # Load the images
                top_image = Image(LOGO_PATH, width=533, height=100)  # Adjust width and height as needed
                bottom_image = Image(SIGN_PATH, width=100, height=50)  # Adjust width and height as needed

                # Student Personal Data
                l1 = [["STUDENT DETAILS"]]
                label1 = Table(l1, colWidths=[480], rowHeights=20)
                label1.setStyle(TableStyle([
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black),
                    ('BACKGROUND', (0, 0), (-1, -1), colors.blue),
                    ('TEXTCOLOR', (0, 0), (-1, -1), colors.whitesmoke)
                ]))
                data1 = [
                    ["ID:", row['ID']],
                    ["Name:", f"{row['fname']} {row['mname']} {row['lname']}"],
                    ["Class:", f"{row['class']}"],
                    ["Section:", f"{row['section']}"],
                    ["Father's Name:", f"{row['f_fname']} {row['f_lname']}"],
                    ["Gender:", f"{row['gender']}"],
                    ["Date of Birth:", f"{row['dob']}"],
                    ["Date of Joining:", f"{row['doj']}"],
                    ["Contact Number:", f"{row['phone_no']}"]
                ]
                table1 = Table(data1, colWidths=[200, 280], rowHeights=15)
                table1.setStyle(TableStyle([
                    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                    ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
                    ('BACKGROUND', (0, 0), (-1, -1), colors.white),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black)
                ]))

                # Student Fee Record
                l2 = [["FEE DETAILS"]]
                label2 = Table(l2, colWidths=[480], rowHeights=20)
                label2.setStyle(TableStyle([
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black),
                    ('BACKGROUND', (0, 0), (-1, -1), colors.blue),
                    ('TEXTCOLOR', (0, 0), (-1, -1), colors.whitesmoke)
                ]))
                data2 = [
                    ["Fee Type", "Applicable", "Paid", "Balance"],
                    ["Tution Fee", row['tution_fee_a'], row['tution_fee_p'], tut_bal],
                    ["Transport Fee", row['trans_fee_a'], row['trans_fee_p'], trans_bal],
                    ["Stationery Fee", row['stationery_fee_a'], row['stationery_fee_p'], book_bal]
                ]
                table2 = Table(data2, colWidths=[120, 120, 120, 120], rowHeights=15)
                table2.setStyle(TableStyle([
                    ('ALIGN', (0, 0), (-1, 0), 'LEFT'),
                    ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('BACKGROUND', (0, 0), (-1, -1), colors.white),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black)
                ]))
                bal_data = [["Current Balance", row['balance']]]
                bal_table = Table(bal_data,colWidths=[240, 240], rowHeights=15)
                bal_table.setStyle(TableStyle([
                    ('ALIGN', (0, 0), (-1, 0), 'LEFT'),
                    ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('BACKGROUND', (0, 0), (-1, -1), colors.white),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black)
                ]))
                # Fee Summary
                l3 = [["SUMMARY"]]
                label3 = Table(l3, colWidths=[480], rowHeights=20)
                label3.setStyle(TableStyle([
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black),
                    ('BACKGROUND', (0, 0), (-1, -1), colors.blue),
                    ('TEXTCOLOR', (0, 0), (-1, -1), colors.whitesmoke)
                ]))
                data3 = [
                    ["Amount Payable", total],
                    ["Amount Paid", paid],
                    ["Total Dues", row['balance']]
                ]
                table3 = Table(data3, colWidths=[200, 280], rowHeights=15)
                table3.setStyle(TableStyle([
                    ('ALIGN', (0, 0), (-1, 0), 'LEFT'),
                    ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
                    ('BACKGROUND', (0, 0), (-2, -1), colors.white),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black),
                    ('BACKGROUND', (0, -1), (-1, -1), colors.grey),
                    ('TEXTCOLOR', (0, -1), (-1, -1), colors.whitesmoke),
                    ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold')
                ]))

                blankd1 = [
                    ["", f""],
                    ["", f""],
                    ["", f""],
                    ["", f""],
                    ["", f""],
                    ["", f""],
                    ["", f""],
                    ["", f""],
                    ["", f""],
                    
                ]
                blank1 = Table(blankd1, colWidths=[200, 280], rowHeights=15)
                blank1.setStyle(TableStyle([
                    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                    ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
                    ('BACKGROUND', (0, 0), (-1, -1), colors.white),
                    ('GRID', (0, 0), (-1, -1), 1, colors.white),
                    ('TEXTCOLOR', (0, 0), (-1, -1), colors.white)
                ]))

                styles = getSampleStyleSheet()
                timetext = f"<b>Invoice Generated At:</b> {now1}"  # Assuming now1 is the timestamp you want to include
                timepara = Paragraph(timetext, styles['Normal'])

                doc.build([top_image, label1, table1, label2, table2, bal_table, label3, table3, blank1, bottom_image, timepara])
                messagebox.showinfo("Success", "Report generated successfully")
                return

        # If the loop completes without finding the ID, show error message
        messagebox.showerror("Error", "ID not found")