from tkinter import *
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import cv2
import numpy as np
import csv
from tkcalendar import DateEntry
import speech_recognition as sr
import threading

class Criminal:
    def __init__(self, root):
        self.root = root
        self.root.geometry('1530x790')
        self.root.title('Criminal Database Management')

        lbl_title = Label(self.root, text='Criminal Database Management', 
                          font=('Helvetica', 32, 'bold'), bg='#333333', fg='#ffcc00')
        lbl_title.pack(fill=X, pady=10)

        main_frame = Frame(self.root)
        main_frame.pack(fill=BOTH, expand=True)

        canvas = Canvas(main_frame)
        canvas.pack(side=LEFT, fill=BOTH, expand=True)

        scrollbar = Scrollbar(main_frame, orient=VERTICAL, command=canvas.yview)
        scrollbar.pack(side=RIGHT, fill=Y)

        self.form_frame = Frame(canvas, bg='#f0f0f0')
        self.form_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=self.form_frame, anchor="nw")


        Label(self.form_frame, text='Name:', bg='#f0f0f0').grid(row=0, column=0, padx=10, pady=5, sticky='e')
        self.name_entry = Entry(self.form_frame)
        self.name_entry.grid(row=0, column=1, padx=10, pady=5)
        
        self.name_voice_btn = Button(self.form_frame, text='Speak Name', command=self.speak_name, bg='#007bff', fg='white')
        self.name_voice_btn.grid(row=0, column=2, padx=10, pady=5)
        
        Label(self.form_frame, text='Occupation:', bg='#f0f0f0').grid(row=1, column=0, padx=10, pady=5, sticky='e')
        self.occupation_entry = Entry(self.form_frame)
        self.occupation_entry.grid(row=1, column=1, padx=10, pady=5)

        Label(self.form_frame, text='Birth Date:', bg='#f0f0f0').grid(row=2, column=0, padx=10, pady=5, sticky='e')
        self.birthdate_entry = DateEntry(self.form_frame, width=20, background='darkblue', foreground='white', borderwidth=2)
        self.birthdate_entry.grid(row=2, column=1, padx=10, pady=5)

        Label(self.form_frame, text='Aadhaar ID:', bg='#f0f0f0').grid(row=3, column=0, padx=10, pady=5, sticky='e')
        self.aadhaar_entry = Entry(self.form_frame)
        self.aadhaar_entry.grid(row=3, column=1, padx=10, pady=5)

        Label(self.form_frame, text='Crime Type:', bg='#f0f0f0').grid(row=4, column=0, padx=10, pady=5, sticky='e')
        self.crime_type_entry = Entry(self.form_frame)
        self.crime_type_entry.grid(row=4, column=1, padx=10, pady=5)

        Label(self.form_frame, text='Age:', bg='#f0f0f0').grid(row=5, column=0, padx=10, pady=5, sticky='e')
        self.age_entry = Entry(self.form_frame)
        self.age_entry.grid(row=5, column=1, padx=10, pady=5)

        Label(self.form_frame, text='Father ID:', bg='#f0f0f0').grid(row=6, column=0, padx=10, pady=5, sticky='e')
        self.father_id_entry = Entry(self.form_frame)
        self.father_id_entry.grid(row=6, column=1, padx=10, pady=5)

        Label(self.form_frame, text='Crime ID:', bg='#f0f0f0').grid(row=7, column=0, padx=10, pady=5, sticky='e')
        self.crime_id_entry = Entry(self.form_frame)
        self.crime_id_entry.grid(row=7, column=1, padx=10, pady=5)

        Label(self.form_frame, text='Gender:', bg='#f0f0f0').grid(row=8, column=0, padx=10, pady=5, sticky='e')
        self.gender_var = StringVar()
        self.gender_var.set('Male')
        gender_menu = OptionMenu(self.form_frame, self.gender_var, 'Male', 'Female', 'Other')
        gender_menu.grid(row=8, column=1, padx=10, pady=5)


        self.img_label = Label(self.form_frame, text='No Image', bg='#f0f0f0', width=20, height=20)
        self.img_label.grid(row=9, column=0, columnspan=3, pady=10)

        upload_img_btn = Button(self.form_frame, text='Upload Image', command=self.open_camera_dialog, bg='#007bff', fg='white')
        upload_img_btn.grid(row=10, column=0, columnspan=3, pady=10)

        Button(self.form_frame, text='Add', command=self.add_record, bg='#28a745', fg='white').grid(row=11, column=0, columnspan=3, pady=10)


        lower_frame = Frame(self.root, bg='#f0f0f0')
        lower_frame.pack(fill=BOTH, expand=True, pady=5)

        tree_scroll_y = Scrollbar(lower_frame, orient='vertical')
        tree_scroll_y.pack(side=RIGHT, fill=Y)

        self.tree = ttk.Treeview(lower_frame, columns=('Name', 'Occupation', 'Birth Date', 'Aadhaar ID', 'Crime Type', 'Age', 'Father ID', 'Crime ID', 'Gender', 'Image'), show='headings', yscrollcommand=tree_scroll_y.set)
        self.tree.pack(fill=BOTH, expand=True)
        tree_scroll_y.config(command=self.tree.yview)


        self.tree.heading('Name', text='Name')
        self.tree.heading('Occupation', text='Occupation')
        self.tree.heading('Birth Date', text='Birth Date')
        self.tree.heading('Aadhaar ID', text='Aadhaar ID')
        self.tree.heading('Crime Type', text='Crime Type')
        self.tree.heading('Age', text='Age')
        self.tree.heading('Father ID', text='Father ID')
        self.tree.heading('Crime ID', text='Crime ID')
        self.tree.heading('Gender', text='Gender')
        self.tree.heading('Image', text='Image')


        self.tree.tag_configure('oddrow', background='#f9f9f9')
        self.tree.tag_configure('evenrow', background='#ffffff')

        button_frame = Frame(self.root, bg='#f0f0f0')
        button_frame.pack(fill=X, pady=5)

        Button(button_frame, text='Delete', command=self.delete_record, bg='#dc3545', fg='white').pack(side=LEFT, padx=10)
        Button(button_frame, text='Update', command=self.update_record, bg='#ffc107', fg='white').pack(side=LEFT, padx=10)
        Button(button_frame, text='Export CSV', command=self.export_to_csv, bg='#007bff', fg='white').pack(side=LEFT, padx=10)
        Button(button_frame, text='Import CSV', command=self.import_from_csv, bg='#007bff', fg='white').pack(side=LEFT, padx=10)

        lower_bar = Frame(lower_frame, bg='#333333')
        lower_bar.pack(fill=X, side=BOTTOM, pady=5)

        Label(lower_bar, text='Total Records:', bg='#333333', fg='#ffffff').pack(side=LEFT, padx=10)
        self.total_records_label = Label(lower_bar, text='0', bg='#333333', fg='#ffffff')
        self.total_records_label.pack(side=LEFT, padx=10)

        self.update_total_records()

    def speak_name(self):
        def recognize_speech():
            recognizer = sr.Recognizer()
            with sr.Microphone() as source:
                self.name_voice_btn.config(text='Listening...')
                try:
                    audio = recognizer.listen(source, timeout=2)
                    text = recognizer.recognize_google(audio)
                    self.name_entry.delete(0, END)
                    self.name_entry.insert(0, text)
                except sr.UnknownValueError:
                    messagebox.showerror("Voice Recognition Error", "Sorry, could not understand the audio.")
                except sr.RequestError:
                    messagebox.showerror("Voice Recognition Error", "Sorry, there was an error with the service.")
                except Exception as e:
                    messagebox.showerror("Error", str(e))
                finally:
                    self.name_voice_btn.config(text='Speak Name')

        thread = threading.Thread(target=recognize_speech)
        thread.start()

    def open_camera_dialog(self):
        self.camera_dialog = Toplevel(self.root)
        self.camera_dialog.title('Capture Image')
        self.camera_dialog.geometry('640x480')

        self.camera_frame = Frame(self.camera_dialog)
        self.camera_frame.pack(fill=BOTH, expand=True)

        self.img_label = Label(self.camera_frame, text='No Image', bg='#f0f0f0')
        self.img_label.pack()

        capture_btn = Button(self.camera_frame, text='Capture', command=self.capture_image, bg='#007bff', fg='white')
        capture_btn.pack(pady=10)

        # Initialize camera
        self.cap = cv2.VideoCapture(0)
        self.update_frame()

    def update_frame(self):
        ret, frame = self.cap.read()
        if ret:
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            pil_image = Image.fromarray(rgb_frame)
            pil_image = pil_image.resize((640, 480), Image.ANTIALIAS)
            self.tk_image = ImageTk.PhotoImage(pil_image)
            self.img_label.config(image=self.tk_image)
        self.camera_dialog.after(10, self.update_frame)

    def capture_image(self):
        ret, frame = self.cap.read()
        if ret:
            image_path = 'captured_image.jpg'
            cv2.imwrite(image_path, frame)
            messagebox.showinfo("Image Captured", f"Image saved as {image_path}.")
            self.add_record(image_path)
        self.cap.release()
        self.camera_dialog.destroy()

    def add_record(self, image_path=None):
        name = self.name_entry.get()
        occupation = self.occupation_entry.get()
        birth_date = self.birthdate_entry.get()
        aadhaar_id = self.aadhaar_entry.get()
        crime_type = self.crime_type_entry.get()
        age = self.age_entry.get()
        father_id = self.father_id_entry.get()
        crime_id = self.crime_id_entry.get()
        gender = self.gender_var.get()

        if not all([name, occupation, birth_date, aadhaar_id, crime_type, age, father_id, crime_id, gender]):
            messagebox.showerror('Error', 'Please fill all fields.')
            return

        # Add record to Treeview
        img_display = 'No Image' if image_path is None else 'Image Captured'
        self.tree.insert('', 'end', values=(name, occupation, birth_date, aadhaar_id, crime_type, age, father_id, crime_id, gender, img_display))
        self.update_total_records()
        self.clear_form()

    def clear_form(self):
        self.name_entry.delete(0, END)
        self.occupation_entry.delete(0, END)
        self.birthdate_entry.delete(0, END)
        self.aadhaar_entry.delete(0, END)
        self.crime_type_entry.delete(0, END)
        self.age_entry.delete(0, END)
        self.father_id_entry.delete(0, END)
        self.crime_id_entry.delete(0, END)
        self.gender_var.set('Male')
        self.img_label.config(image='')

    def delete_record(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror('Error', 'Please select a record to delete.')
            return
        self.tree.delete(selected_item)
        self.update_total_records()

    def update_record(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror('Error', 'Please select a record to update.')
            return
        self.tree.delete(selected_item)
        self.add_record()

    def export_to_csv(self):
        with open('criminal_records.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Name', 'Occupation', 'Birth Date', 'Aadhaar ID', 'Crime Type', 'Age', 'Father ID', 'Crime ID', 'Gender', 'Image'])
            for row in self.tree.get_children():
                writer.writerow(self.tree.item(row)['values'])
        messagebox.showinfo('Success', 'Records exported to CSV.')

    def import_from_csv(self):
        try:
            with open('criminal_records.csv', 'r') as file:
                reader = csv.reader(file)
                next(reader)  # Skip header
                for row in reader:
                    self.tree.insert('', 'end', values=row)
            self.update_total_records()
            messagebox.showinfo('Success', 'Records imported from CSV.')
        except FileNotFoundError:
            messagebox.showerror('Error', 'CSV file not found.')

    def update_total_records(self):
        total_records = len(self.tree.get_children())
        self.total_records_label.config(text=str(total_records))

if __name__ == "__main__":
    root = Tk()
    app = Criminal(root)
    root.mainloop()
