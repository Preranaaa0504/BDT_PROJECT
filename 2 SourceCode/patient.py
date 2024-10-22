from tkinter import *
import tkinter.messagebox
from hospital import create_patient, update_patient, delete_patient, search_patient

class Patient:
    def __init__(self, master, mode="register"):
        self.master = master
        self.mode = mode
        self.master.title(f"{mode.capitalize()} Patient")
        self.master.geometry("600x500")
        self.master.config(bg='lightblue')

        self.lblTitle = Label(self.master, text=f"{mode.capitalize()} Patient", font=("Helvetica", 16, 'bold'), bg='lightblue', fg='#350d42')
        self.lblTitle.pack(pady=20)

        self.patient_id = StringVar()
        self.name = StringVar()
        self.age = IntVar()
        self.gender = StringVar()
        self.disease_domain = StringVar()
        self.aadhaar_card_no = StringVar()
        self.diagnosis = StringVar()
        self.diagnosis_date = StringVar()  # Date input as string for simplicity
        self.symptoms = StringVar()
        self.treatment = StringVar()
        self.family_history = StringVar()

        self.create_widgets()

    def create_widgets(self):
        form_frame = Frame(self.master, bg='lightblue', padx=20, pady=10)
        form_frame.pack(padx=20, pady=10)

        # Create form based on mode
        if self.mode in ["register", "update"]:
            self.create_form(form_frame)
            if self.mode == "register":
                self.create_buttons(["Register"], form_frame)
            elif self.mode == "update":
                self.create_buttons(["Update"], form_frame)
        elif self.mode == "search":
            self.create_search_form(form_frame)
            self.create_buttons(["Search"], form_frame)
        elif self.mode == "delete":
            self.create_delete_form(form_frame)
            self.create_buttons(["Delete"], form_frame)

    def create_form(self, parent_frame):
        Label(parent_frame, text="Patient ID:", bg='lightblue').grid(row=0, column=0, sticky=W, padx=10, pady=5)
        Entry(parent_frame, textvariable=self.patient_id).grid(row=0, column=1, padx=10, pady=5)

        Label(parent_frame, text="Aadhaar Card No:", bg='lightblue').grid(row=1, column=0, sticky=W, padx=10, pady=5)
        Entry(parent_frame, textvariable=self.aadhaar_card_no).grid(row=1, column=1, padx=10, pady=5)

        Label(parent_frame, text="Name:", bg='lightblue').grid(row=2, column=0, sticky=W, padx=10, pady=5)
        Entry(parent_frame, textvariable=self.name).grid(row=2, column=1, padx=10, pady=5)

        Label(parent_frame, text="Age:", bg='lightblue').grid(row=3, column=0, sticky=W, padx=10, pady=5)
        Entry(parent_frame, textvariable=self.age).grid(row=3, column=1, padx=10, pady=5)

        Label(parent_frame, text="Gender:", bg='lightblue').grid(row=4, column=0, sticky=W, padx=10, pady=5)
        gender_options = ["Male", "Female", "Other"]
        OptionMenu(parent_frame, self.gender, *gender_options).grid(row=4, column=1, padx=10, pady=5)

        Label(parent_frame, text="Domain of Treatment:", bg='lightblue').grid(row=5, column=0, sticky=W, padx=10, pady=5)
        disease_options = ["HeartProject", "LungsProject", "KidneyProject", "BrainProject", "OrthoProject", "DiabetesProject"]
        OptionMenu(parent_frame, self.disease_domain, *disease_options).grid(row=5, column=1, padx=10, pady=5)

        Label(parent_frame, text="Diagnosis:", bg='lightblue').grid(row=6, column=0, sticky=W, padx=10, pady=5)
        Entry(parent_frame, textvariable=self.diagnosis).grid(row=6, column=1, padx=10, pady=5)

        Label(parent_frame, text="Diagnosis Date:", bg='lightblue').grid(row=7, column=0, sticky=W, padx=10, pady=5)
        Entry(parent_frame, textvariable=self.diagnosis_date).grid(row=7, column=1, padx=10, pady=5)

        Label(parent_frame, text="Symptoms:", bg='lightblue').grid(row=8, column=0, sticky=W, padx=10, pady=5)
        Entry(parent_frame, textvariable=self.symptoms).grid(row=8, column=1, padx=10, pady=5)

        Label(parent_frame, text="Treatment:", bg='lightblue').grid(row=9, column=0, sticky=W, padx=10, pady=5)
        Entry(parent_frame, textvariable=self.treatment).grid(row=9, column=1, padx=10, pady=5)

        Label(parent_frame, text="Family History:", bg='lightblue').grid(row=10, column=0, sticky=W, padx=10, pady=5)
        Entry(parent_frame, textvariable=self.family_history).grid(row=10, column=1, padx=10, pady=5)

    def create_search_form(self, parent_frame):
        Label(parent_frame, text="Patient ID:", bg='lightblue').grid(row=0, column=0, sticky=W, padx=10, pady=5)
        Entry(parent_frame, textvariable=self.patient_id).grid(row=0, column=1, padx=10, pady=5)

    def create_delete_form(self, parent_frame):
        Label(parent_frame, text="Patient ID:", bg='lightblue').grid(row=0, column=0, sticky=W, padx=10, pady=5)
        Entry(parent_frame, textvariable=self.patient_id).grid(row=0, column=1, padx=10, pady=5)

    def create_buttons(self, buttons, parent_frame):
        button_frame = Frame(parent_frame, bg='lightblue')
        button_frame.grid(row=11, column=0, columnspan=2, pady=20)

        for button in buttons:
            btn = Button(button_frame, text=button, command=self.get_command(button),
                         bg='green' if button == "Register" else
                            'blue' if button == "Update" else
                            'orange' if button == "Search" else
                            'red' if button == "Delete" else 'purple',
                         fg='white', font=("Helvetica", 10, 'bold'))
            btn.pack(side=LEFT, padx=5)

        # Add Clear button
        btn_clear = Button(button_frame, text="Clear", command=self.clear_form,
                           bg='gray', fg='white', font=("Helvetica", 10, 'bold'))
        btn_clear.pack(side=LEFT, padx=5)

    def get_command(self, action):
        if action == "Register":
            return self.register_patient
        elif action == "Update":
            return self.update_patient
        elif action == "Search":
            return self.search_patient
        elif action == "Delete":
            return self.delete_patient

    def check_patient_exists(self, patient_id):
        patients = search_patient(patient_id)
        return bool(patients)

    def validate_mandatory_fields(self):
        patient_id = self.patient_id.get()
        name = self.name.get()
        age = self.age.get()
        domain = self.disease_domain.get()

        if not patient_id or not name or age <= 0 or not domain:
            tkinter.messagebox.showwarning("Input Error", "Please fill Patient ID, Name, Age, and Domain of Treatment.")
            return False
        return True

    def register_patient(self):
        if not self.validate_mandatory_fields():
            return

        aadhaar = self.aadhaar_card_no.get()

        # Check if Aadhaar card number is exactly 12 digits
        if len(aadhaar) != 12 or not aadhaar.isdigit():
            tkinter.messagebox.showwarning("Input Error", "Aadhaar Card No must be exactly 12 digits.")
            return

        name = self.name.get()
        age = self.age.get()
        domain = self.disease_domain.get()

        patient_data = {
            "_id": self.patient_id.get(),
            "Name": name,
            "Age": age,
            "Gender": self.gender.get(),
            "AadhaarCard": int(aadhaar),
            "Diagnosis": self.diagnosis.get(),
            "DiagnosisDate": self.diagnosis_date.get(),
            "Symptoms": self.symptoms.get(),
            "Treatment": self.treatment.get(),
            "FamilyHistory": self.family_history.get()
        }
        create_patient(domain, patient_data)
        tkinter.messagebox.showinfo("Success", "Patient Registered Successfully")

    def update_patient(self):
        if not self.validate_mandatory_fields():
            return

        aadhaar = self.aadhaar_card_no.get()
        patient_id = self.patient_id.get()
        name = self.name.get()
        age = self.age.get()
        domain = self.disease_domain.get()

        if not self.check_patient_exists(patient_id):
            tkinter.messagebox.showwarning("Not Found", "Patient ID does not exist. Redirecting to Registration Page.")
            self.master.destroy()
            self.open_registration()  # Redirect to Registration page
            return

        update_data = {
            "Name": name,
            "Age": age,
            "Gender": self.gender.get(),
            "AadhaarCard": int(aadhaar),
            "Diagnosis": self.diagnosis.get(),
            "DiagnosisDate": self.diagnosis_date.get(),
            "Symptoms": self.symptoms.get(),
            "Treatment": self.treatment.get(),
            "FamilyHistory": self.family_history.get()
        }
        update_patient(domain, patient_id, update_data)
        tkinter.messagebox.showinfo("Success", "Patient Updated Successfully")

    def search_patient(self):
        patient_id = self.patient_id.get()

        if not patient_id:
            tkinter.messagebox.showwarning("Input Error", "Please enter Patient ID.")
            return

        result = search_patient(patient_id)
        if result:
            self.show_search_results(result)
        else:
            tkinter.messagebox.showinfo("Not Found", "No Patient Found with the given ID.")

    def show_search_results(self, result):
        result_window = Toplevel(self.master)
        result_window.title("Search Results")
        result_window.geometry("400x300")

        text_area = Text(result_window, wrap=WORD)
        text_area.insert(END, result)
        text_area.pack(padx=20, pady=20)

    def delete_patient(self):
        patient_id = self.patient_id.get()

        if not patient_id:
            tkinter.messagebox.showwarning("Input Error", "Please enter Patient ID.")
            return

        if not self.check_patient_exists(patient_id):
            tkinter.messagebox.showwarning("Not Found", "No Patient Found with the given ID.")
            return

        confirmation = tkinter.messagebox.askyesno("Delete Confirmation", "Are you sure you want to delete this record?")
        if confirmation:
            delete_patient(patient_id)
            tkinter.messagebox.showinfo("Success", "Patient Deleted Successfully")

    def clear_form(self):
        self.patient_id.set("")
        self.name.set("")
        self.age.set(0)
        self.gender.set("")
        self.disease_domain.set("")
        self.aadhaar_card_no.set("")
        self.diagnosis.set("")
        self.diagnosis_date.set("")
        self.symptoms.set("")
        self.treatment.set("")
        self.family_history.set("")

    def open_registration(self):
        reg_window = Toplevel(self.master)
        reg_app = Patient(reg_window, "register")

# This code assumes the existence of create_patient, update_patient, delete_patient, search_patient functions
