# This software is licensed to you under the GNU General Public
# License as published by the Free Software Foundation; either version
# 2 of the License (GPLv2) or (at your option) any later version.
# There is NO WARRANTY for this software, express or implied,
# including the implied warranties of MERCHANTABILITY,
# NON-INFRINGEMENT, or FITNESS FOR A PARTICULAR PURPOSE. You should
# have received a copy of GPLv2 along with this software; if not, see
# http://www.gnu.org/licenses/old-licenses/gpl-2.0.txt.

# Imports
import customtkinter
from CTkListbox import *
from CTkTable import *
import tkinter.ttk
from probate_search import ProbateSearch
from PIL import Image, ImageTk
import csv

class Options:

    def __init__(self, lastname=None, firstname=None, middlename=None):
        self.lastname = lastname
        self.firstname = firstname
        self.middlename = middlename

# Constants
COUNTIES = ['Aiken', 'Bamberg', 'Barnwell', 'Beaufort', 'Charleston', 'Cherokee', 'Chester', 'Colleton', 'Dorchester', 'Florence', 'Georgetown', 'Greenwood', 'Jasper', 'Kershaw', 'Lancaster', 'Marlboro', 'Newberry', 'Oconee', 'Orangeburg', 'Saluda', 'Sumter', 'York']
TABLE_HEADING = ['CaseNumber','CaseName','Party','CaseType','FilingDate','County','AppointmentDate','CreditorClaimDue','CaseStatus']

# Set Theme and Mode
customtkinter.set_appearance_mode("dark")  # Modes: system (default), light, dark
customtkinter.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green


# Main App
app = customtkinter.CTk()
app.geometry("1550x650")
app.title("Probate Search - South Carolina")

# Functions
def search_function():
    search_button.configure(state=customtkinter.DISABLED)

    selectedCounties = []

    for idx in listbox.curselection():
        selectedCounties.append(COUNTIES[idx])

    results = ProbateSearch().search(selectedCounties, Options(lastname=lastname_entry.get(), firstname=firstname_entry.get(), middlename=middlename_entry.get()), "Estate")
    table_data = []
    table_data.append(TABLE_HEADING)
    for i in results:
        table_data.append(list(i.values()))

    #update table
    table.rows = len(table_data)
    table.update_values(table_data)

    results_label.configure(text = str(len(table_data)-1) + "  Records Found.")

    search_button.configure(state=customtkinter.NORMAL)
    
def combobox_callback(choice):
    print("combobox dropdown clicked:", choice)

def validate_county_selection(choices):
    #must have atleast one county selected
    if choices is None:
        listbox.activate(0)

def radiobutton_event():
    print("radiobutton toggled, current value:", radio_var.get())

def export_csv():
    print("Export CSV")
    with open('results.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(table.get())

# UI Components
search_button = customtkinter.CTkButton(master=app, text="Search", command=search_function)
search_button.grid(row=9, column=0, padx=5, pady=25)

county_label = customtkinter.CTkLabel(master=app, text="Select Counties:", fg_color="transparent")
county_label.grid(row=0, column=0, padx=5, pady=5)

listbox = CTkListbox(master=app, multiple_selection=True, height=200, command=validate_county_selection)
listbox.grid(row=1, column=0, padx=5, pady=5)

# Populate County DropDown Selector
for item in COUNTIES:
    listbox.insert(item.index, item)
listbox.activate(0) #Select first option as default

options_label = customtkinter.CTkLabel(master=app, text="Select Options:", fg_color="transparent")
options_label.grid(row=2, column=0, padx=5, pady=5)

lastname_entry = customtkinter.CTkEntry(master=app, placeholder_text="Last Name")
lastname_entry.grid(row=3, column=0, padx=5, pady=5)

firstname_entry = customtkinter.CTkEntry(master=app, placeholder_text="First Name")
firstname_entry.grid(row=4, column=0, padx=5, pady=5)

middlename_entry = customtkinter.CTkEntry(master=app, placeholder_text="Middle Name")
middlename_entry.grid(row=5, column=0, padx=5, pady=5)

separator = tkinter.ttk.Separator(master=app, orient=tkinter.VERTICAL)
separator.place(x=190, y=0, relheight=1.0)

radio_var = tkinter.IntVar(value=0)
radiobutton_1 = customtkinter.CTkRadioButton(master=app, text="Estate",
                                             command=radiobutton_event, variable= radio_var, value=1)
radiobutton_2 = customtkinter.CTkRadioButton(app, text="Marriage",
                                             command=radiobutton_event, variable= radio_var, value=2)

radiobutton_1.select()

radiobutton_1.grid(row=7, column=0, padx=5, pady=5)
radiobutton_2.grid(row=8, column=0, padx=5, pady=5)

type_label = customtkinter.CTkLabel(master=app, text="Select Type:", fg_color="transparent")
type_label.grid(row=6, column=0, padx=5, pady=5)

frame = customtkinter.CTkScrollableFrame(master=app, orientation=tkinter.VERTICAL, width=1300, height=550)
frame.grid(row=0, column=1, rowspan=15, padx=20, pady=20, sticky="n")

value = [['CaseNumber','CaseName','Party','CaseType','FilingDate','County','AppointmentDate','CreditorClaimDue','CaseStatus']]

table = CTkTable(master=frame, row=20, column=9, values=value, header_color="lightblue")
table.edit_row(0, text_color="black")
table.pack(expand=True, fill="both", padx=5, pady=5)

results_label = customtkinter.CTkLabel(master=app, text="0 Records Found.", fg_color="transparent")
results_label.grid(row=15, column=1, padx=25, pady=0, sticky='nw')

#Load export image
export_image = customtkinter.CTkImage(Image.open("images/export.png").resize((25,25), Image.LANCZOS))
export_button = customtkinter.CTkButton(master=app, image=export_image, text="Export CSV", width=125, height=15, compound="right", command=export_csv)
export_button.grid(row=15, column=1, padx=25, sticky="e")


app.mainloop()