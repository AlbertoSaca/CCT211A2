import tkinter as tk
from tkinter import ttk
import csv
from tkinter import messagebox

# File paths
SEMESTER_FILE = "semesters.csv"
COURSES_FILE = "courses.csv"
GRADES_FILE = "grades.csv"

# Function to save a semester
def save_semester():
    term = term_var.get()
    year = year_var.get()
    
    if term == "Select Term" or not year.isdigit():
        messagebox.showerror("Input Error", "Please select a term and enter a valid year.")
        return
    
    semester_name = f"{term} {year}"
    
    try:
        with open(SEMESTER_FILE, mode="r") as file:
            reader = csv.reader(file)
            next(reader, None)
            if any(row and row[0] == semester_name for row in reader):
                messagebox.showerror("Duplicate Semester", f"The semester '{semester_name}' already exists.")
                return
    except FileNotFoundError:
        pass
    
    with open(SEMESTER_FILE, mode="a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([semester_name, ""])
    
    add_semester_to_display(semester_name)
    term_var.set("Select Term")
    year_var.set("")

# Function to add a semester to the UI
def add_semester_to_display(semester_name):
    frame = tk.Frame(output_frame, padx=5, pady=5)
    frame.pack(fill=tk.X, anchor="w")

    semester_label = tk.Label(frame, text=semester_name, font=("Arial", 12))
    semester_label.pack(side=tk.LEFT)

    gpa_var = tk.StringVar(value="GPA: N/A")
    gpa_label = tk.Label(frame, textvariable=gpa_var, font=("Arial", 12), padx=10)
    gpa_label.pack(side=tk.LEFT)

    delete_button = tk.Button(
        frame, text="X", font=("Arial", 10), fg="red", command=lambda: delete_semester(semester_name, frame)
    )
    delete_button.pack(side=tk.RIGHT)

    open_button = tk.Button(
        frame, text="Open", font=("Arial", 10), command=lambda: open_semester(semester_name)
    )
    open_button.pack(side=tk.RIGHT, padx=5)

# Function to open a semester window
def open_semester(semester_name):
    new_window = tk.Toplevel(root)
    new_window.title(semester_name)
    new_window.geometry("800x600")
    
    # Variables to track total credits and GPA
    total_credits = tk.StringVar(value="0.0")
    total_gpa = tk.StringVar(value="N/A")

    # Create two columns
    left_column = tk.Frame(new_window, padx=10, pady=10, width=300)
    left_column.pack(side=tk.LEFT, fill=tk.Y)

    right_column = tk.Frame(new_window, padx=10, pady=10)
    right_column.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

    # Center-align widgets in the left column
    for widget in left_column.winfo_children():
        widget.pack_forget()

    # Left column: Display GPA and credits summary
    tk.Label(left_column, text=semester_name + " CGPA", font=("Arial", 14)).pack(pady=5, anchor="center")
    total_gpa_entry = tk.Entry(left_column, textvariable=total_gpa, font=("Arial", 12), state="readonly")
    total_gpa_entry.pack(pady=5, anchor="center")

    tk.Label(left_column, text=semester_name + " Credits", font=("Arial", 14)).pack(pady=5, anchor="center")
    total_credits_label = tk.Entry(left_column, textvariable=total_credits, font=("Arial", 12), state="readonly")
    total_credits_label.pack(pady=5, anchor="center")

    tk.Label(left_column, text="Create Course", font=("Arial", 14)).pack(anchor="center", pady=5)
    
    # Course creation inputs
    course_name_var = tk.StringVar()
    course_name_entry = tk.Entry(left_column, textvariable=course_name_var, font=("Arial", 12))
    course_name_entry.pack(pady=5, anchor="center")
    
    course_credit_var = tk.StringVar(value="0.5")
    tk.Label(left_column, text="Credit Type", font=("Arial", 12)).pack(anchor="center")
    credit_dropdown = ttk.Combobox(left_column, textvariable=course_credit_var, state="readonly", font=("Arial", 12), width=10)
    credit_dropdown["values"] = ["0.5", "1.0"]
    credit_dropdown.pack(pady=5, anchor="center")
    
    save_course_button = tk.Button(
        left_column, text="Create", font=("Arial", 12), 
        command=lambda: save_course(semester_name, course_name_var, course_credit_var, course_list_frame, total_credits)
    )
    save_course_button.pack(pady=10, anchor="center")
    
    # Right column: Display courses
    tk.Label(right_column, text="Courses", font=("Arial", 14)).pack(anchor="w", pady=5)
    course_list_frame = tk.Frame(right_column)
    course_list_frame.pack(fill=tk.BOTH, expand=True)

    load_courses(semester_name, course_list_frame, total_credits)

# Function to save a course
def save_course(semester_name, course_name_var, course_credit_var, course_list_frame, total_credits):
    course_name = course_name_var.get().strip()
    course_credit = course_credit_var.get().strip()
    
    if not course_name or course_credit not in ["0.5", "1.0"]:
        messagebox.showerror("Input Error", "Please enter a valid course name and select a valid credit type.")
        return
    
    try:
        with open(COURSES_FILE, mode="a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([semester_name, course_name, course_credit, ""])
    except Exception as e:
        messagebox.showerror("File Error", f"Error saving course: {e}")
        return

    add_course_to_display(course_list_frame, semester_name, course_name, course_credit, total_credits)
    update_total_credits(total_credits, float(course_credit))
    course_name_var.set("")
    course_credit_var.set("0.5")
    messagebox.showinfo("Success", f"Course '{course_name}' added to {semester_name}!")


# Function to load courses for a semester
def load_courses(semester_name, course_list_frame, total_credits):
    total = 0.0
    try:
        with open(COURSES_FILE, mode="r") as file:
            reader = csv.reader(file)
            for row in reader:
                if row and row[0] == semester_name:
                    add_course_to_display(course_list_frame, row[0], row[1], row[2], total_credits)
                    total += float(row[2])
    except FileNotFoundError:
        pass
    total_credits.set(f"{total:.1f}")


# Function to add a course to the UI
def add_course_to_display(course_list_frame, semester_name, course_name, course_credit, total_credits):
    frame = tk.Frame(course_list_frame, padx=5, pady=5)
    frame.pack(fill=tk.X, anchor="w")

    course_label = tk.Label(frame, text=f"{course_name} ({course_credit} credits)", font=("Arial", 12))
    course_label.pack(side=tk.LEFT)

    delete_button = tk.Button(
        frame, text="X", font=("Arial", 10), fg="red",
        command=lambda: delete_course(semester_name, course_name, course_credit, frame, total_credits)
    )
    delete_button.pack(side=tk.RIGHT)


    open_button = tk.Button(
        frame, text="Open", font=("Arial", 10), command=lambda: open_course(semester_name, course_name)
    )
    open_button.pack(side=tk.RIGHT, padx=5)

# Function to update total credits
def update_total_credits(total_credits, credit_change):
    current_total = float(total_credits.get())
    new_total = current_total + credit_change
    total_credits.set(f"{new_total:.1f}")

# Function to delete a course
def delete_course(semester_name, course_name, course_credit, frame, total_credits):
    # Update courses.csv by removing the course
    updated_courses = []
    try:
        with open(COURSES_FILE, mode="r") as file:
            reader = csv.reader(file)
            updated_courses = [row for row in reader if not (row and row[0] == semester_name and row[1] == course_name)]
    except FileNotFoundError:
        messagebox.showerror("File Error", "Courses file not found.")
        return

    with open(COURSES_FILE, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerows(updated_courses)

    # Update grades.csv by removing syllabus items related to the course
    updated_grades = []
    try:
        with open(GRADES_FILE, mode="r") as file:
            reader = csv.reader(file)
            updated_grades = [row for row in reader if not (row and row[0] == semester_name and row[1] == course_name)]
    except FileNotFoundError:
        messagebox.showerror("File Error", "Grades file not found.")
        return

    with open(GRADES_FILE, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerows(updated_grades)

    # Update UI
    frame.destroy()
    update_total_credits(total_credits, -float(course_credit))
    messagebox.showinfo("Deleted", f"Course '{course_name}' and its syllabus items have been deleted.")


# Function to open a course (stub for further details)
def open_course(semester_name, course_name):
    messagebox.showinfo("Open Course", f"Opening course '{course_name}' in semester '{semester_name}'.")

# Function to delete a semester
def delete_semester(semester_name, frame):
    # Remove the semester from the semesters.csv file
    updated_semesters = []
    try:
        with open(SEMESTER_FILE, mode="r") as file:
            reader = csv.reader(file)
            updated_semesters = [row for row in reader if row and row[0] != semester_name]
    except FileNotFoundError:
        messagebox.showerror("File Error", "Semesters file not found.")
        return

    with open(SEMESTER_FILE, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerows(updated_semesters)

    # Remove all courses related to the semester from courses.csv
    updated_courses = []
    try:
        with open(COURSES_FILE, mode="r") as file:
            reader = csv.reader(file)
            updated_courses = [row for row in reader if row and row[0] != semester_name]
    except FileNotFoundError:
        pass

    with open(COURSES_FILE, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerows(updated_courses)

    # Remove all grades related to the semester from grades.csv
    updated_grades = []
    try:
        with open(GRADES_FILE, mode="r") as file:
            reader = csv.reader(file)
            updated_grades = [row for row in reader if row and row[0] != semester_name]
    except FileNotFoundError:
        pass

    with open(GRADES_FILE, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerows(updated_grades)

    # Update the UI
    frame.destroy()
    messagebox.showinfo("Deleted", f"Semester '{semester_name}', its courses, and syllabus items have been deleted.")


# Load semesters on startup
def load_semesters():
    try:
        with open(SEMESTER_FILE, mode="r") as file:
            reader = csv.reader(file)
            next(reader, None)
            for row in reader:
                if row:
                    add_semester_to_display(row[0])
    except FileNotFoundError:
        pass

# Function to save a syllabus item
def save_syllabus_item(semester_name, course_name, syllabus_item_var, weight_var, syllabus_frame):
    syllabus_item = syllabus_item_var.get().strip()
    weight = weight_var.get().strip()
    
    if not syllabus_item or not weight.isdigit():
        messagebox.showerror("Input Error", "Please enter a valid syllabus item and weight.")
        return
    
    try:
        with open(GRADES_FILE, mode="a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([semester_name, course_name, syllabus_item, weight, ""])
    except Exception as e:
        messagebox.showerror("File Error", f"Error saving syllabus item: {e}")
        return

    add_syllabus_item_to_display(syllabus_frame, syllabus_item, weight)
    syllabus_item_var.set("")
    weight_var.set("")
    messagebox.showinfo("Success", f"Syllabus item '{syllabus_item}' added to {course_name}!")

# Function to load syllabus items for a course
def load_syllabus_items(semester_name, course_name, syllabus_frame):
    try:
        with open(GRADES_FILE, mode="r") as file:
            reader = csv.reader(file)
            for row in reader:
                if row and row[0] == semester_name and row[1] == course_name:
                    add_syllabus_item_to_display(syllabus_frame, row[2], row[3])
    except FileNotFoundError:
        pass

# Function to add a syllabus item to the UI
def add_syllabus_item_to_display(syllabus_frame, syllabus_item, weight):
    frame = tk.Frame(syllabus_frame, padx=5, pady=5)
    frame.pack(fill=tk.X, anchor="w")

    syllabus_label = tk.Label(frame, text=f"{syllabus_item} (Weight: {weight}%)", font=("Arial", 12))
    syllabus_label.pack(side=tk.LEFT)

def open_course(semester_name, course_name):
    course_window = tk.Toplevel(root)
    course_window.title(f"{course_name} - {semester_name}")
    course_window.geometry("800x600")

    # Variables
    syllabus_item_name_var = tk.StringVar()
    syllabus_item_weight_var = tk.StringVar()

    current_grade_var = tk.StringVar(value="N/A")  # Current grade variable
    total_weight_var = tk.StringVar(value="0%")   # Total weight variable

    # Function to calculate total weight
    def calculate_total_weight():
        total_weight = 0
        try:
            with open(GRADES_FILE, mode="r") as file:
                reader = csv.reader(file)
                for row in reader:
                    if row[0] == semester_name and row[1] == course_name:
                        total_weight += int(row[3])  # Add weight of each syllabus item
        except FileNotFoundError:
            pass

        total_weight_var.set(f"{total_weight}%")  # Update the total weight display

    # Function to delete a syllabus item
    def delete_syllabus_item(semester, course, syllabus_name, frame):
        updated_rows = []
        try:
            with open(GRADES_FILE, mode="r") as file:
                reader = csv.reader(file)
                updated_rows = [row for row in reader if not (row[0] == semester and row[1] == course and row[2] == syllabus_name)]
        except FileNotFoundError:
            messagebox.showerror("File Error", "Grades file not found.")
            return

        with open(GRADES_FILE, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerows(updated_rows)

        frame.destroy()
        calculate_total_weight()  # Update total weight after deletion
        messagebox.showinfo("Deleted", f"Syllabus item '{syllabus_name}' has been deleted.")

    # Function to update a grade
    def update_grade(semester, course, syllabus_name, grade):
        updated_rows = []
        try:
            with open(GRADES_FILE, mode="r") as file:
                reader = csv.reader(file)
                for row in reader:
                    if row[0] == semester and row[1] == course and row[2] == syllabus_name:
                        row[4] = grade  # Update the grade
                    updated_rows.append(row)
        except FileNotFoundError:
            messagebox.showerror("File Error", "Grades file not found.")
            return

        with open(GRADES_FILE, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerows(updated_rows)

        messagebox.showinfo("Updated", f"Grade for '{syllabus_name}' updated to {grade}.")

    # Function to add syllabus item to the display
    def add_syllabus_item_to_display(frame, semester, course, syllabus_name, syllabus_weight, syllabus_grade):
        item_frame = tk.Frame(frame, padx=5, pady=5)
        item_frame.pack(fill=tk.X, anchor="w")

        # Syllabus details
        tk.Label(item_frame, text=f"Syllabus: {syllabus_name}", font=("Arial", 12)).pack(side=tk.LEFT, padx=5)
        tk.Label(item_frame, text=f"Weight: {syllabus_weight}%", font=("Arial", 12)).pack(side=tk.LEFT, padx=5)

        # Grade input
        grade_entry = tk.Entry(item_frame, font=("Arial", 12), width=8)
        grade_entry.insert(0, syllabus_grade or "")  # Pre-fill with existing grade if available
        grade_entry.pack(side=tk.RIGHT, padx=5)

        # Save grade button
        save_button = tk.Button(
            item_frame, text="Save Grade", font=("Arial", 10),
            command=lambda: update_grade(semester, course, syllabus_name, grade_entry.get())
        )
        save_button.pack(side=tk.RIGHT, padx=5)

        # Delete syllabus item button
        delete_button = tk.Button(
            item_frame, text="X", font=("Arial", 10), fg="red",
            command=lambda: delete_syllabus_item(semester, course, syllabus_name, item_frame)
        )
        delete_button.pack(side=tk.RIGHT, padx=5)

    # Function to save a new syllabus item
    def save_syllabus_item():
        syllabus_name = syllabus_item_name_var.get().strip()
        syllabus_weight = syllabus_item_weight_var.get().strip()

        if not syllabus_name or not syllabus_weight.isdigit():
            messagebox.showerror("Input Error", "Please provide valid inputs.")
            return

        try:
            with open(GRADES_FILE, mode="a", newline="") as file:
                writer = csv.writer(file)
                writer.writerow([semester_name, course_name, syllabus_name, syllabus_weight, ""])  # No grade initially
        except Exception as e:
            messagebox.showerror("File Error", f"Error saving syllabus item: {e}")
            return

        add_syllabus_item_to_display(
            syllabus_list_frame, semester_name, course_name, syllabus_name, syllabus_weight, ""
        )
        syllabus_item_name_var.set("")
        syllabus_item_weight_var.set("")
        calculate_total_weight()  # Recalculate total weight after adding a new item

    # Load existing syllabus items and calculate total weight
    def load_syllabus_items():
        try:
            with open(GRADES_FILE, mode="r") as file:
                reader = csv.reader(file)
                for row in reader:
                    if row[0] == semester_name and row[1] == course_name:
                        add_syllabus_item_to_display(syllabus_list_frame, row[0], row[1], row[2], row[3], row[4])
        except FileNotFoundError:
            pass
        calculate_total_weight()  # Update total weight on load

    # Left column: Display current grade and total weight
    left_column = tk.Frame(course_window, padx=10, pady=10, width=300)
    left_column.pack(side=tk.LEFT, fill=tk.Y)

    tk.Label(left_column, text=f"Course: {course_name}", font=("Arial", 14)).pack(pady=5, anchor="center")

    # Current Grade
    tk.Label(left_column, text="Current Grade:", font=("Arial", 12)).pack(anchor="w")
    current_grade_label = tk.Label(left_column, textvariable=current_grade_var, font=("Arial", 12))
    current_grade_label.pack(pady=5, anchor="w")

    # Total Weight
    tk.Label(left_column, text="Total Weight:", font=("Arial", 12)).pack(anchor="w")
    total_weight_label = tk.Label(left_column, textvariable=total_weight_var, font=("Arial", 12))
    total_weight_label.pack(pady=5, anchor="w")

    # Syllabus Item Inputs
    tk.Label(left_column, text="Add Syllabus Item", font=("Arial", 14)).pack(pady=10, anchor="center")

    tk.Label(left_column, text="Syllabus Item Name:", font=("Arial", 12)).pack(anchor="w")
    syllabus_item_name_entry = tk.Entry(left_column, textvariable=syllabus_item_name_var, font=("Arial", 12))
    syllabus_item_name_entry.pack(pady=5, anchor="w", fill=tk.X)

    tk.Label(left_column, text="Weight (%):", font=("Arial", 12)).pack(anchor="w")
    syllabus_item_weight_entry = tk.Entry(left_column, textvariable=syllabus_item_weight_var, font=("Arial", 12))
    syllabus_item_weight_entry.pack(pady=5, anchor="w", fill=tk.X)

    save_syllabus_button = tk.Button(
        left_column, text="Add Item", font=("Arial", 12), command=save_syllabus_item
    )
    save_syllabus_button.pack(pady=10)

    # Right column: Display syllabus items
    right_column = tk.Frame(course_window, padx=10, pady=10)
    right_column.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

    tk.Label(right_column, text=f"{course_name} - Syllabus Items", font=("Arial", 14)).pack(anchor="w", pady=5)
    syllabus_list_frame = tk.Frame(right_column)
    syllabus_list_frame.pack(fill=tk.BOTH, expand=True)

    load_syllabus_items()



# Main application window
root = tk.Tk()
root.title("CGPA Calculator")
root.geometry("800x600")

input_frame = tk.Frame(root, padx=10, pady=10, width=300)
input_frame.pack(side=tk.LEFT, fill=tk.Y)

output_frame = tk.Frame(root, padx=10, pady=10)
output_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

tk.Label(input_frame, text="My CGPA", font=("Arial", 14)).pack(pady=5)
cgpa_var = tk.StringVar()
cgpa_entry = tk.Entry(input_frame, textvariable=cgpa_var, font=("Arial", 12), state="readonly")
cgpa_entry.pack(pady=5)

tk.Label(input_frame, text="My Credits", font=("Arial", 14)).pack(pady=5)
credits_var = tk.StringVar()
credits_entry = tk.Entry(input_frame, textvariable=credits_var, font=("Arial", 12), state="readonly")
credits_entry.pack(pady=5)

tk.Label(input_frame, text="").pack(pady=10)
tk.Label(input_frame, text="Create Semester", font=("Arial", 14)).pack(pady=5)

term_var = tk.StringVar(value="Select Term")
term_dropdown = ttk.Combobox(input_frame, textvariable=term_var, state="readonly", font=("Arial", 12), width=20)
term_dropdown["values"] = ["Winter", "Summer", "Fall"]
term_dropdown.pack(pady=5)

year_var = tk.StringVar()
tk.Label(input_frame, text="Year:", font=("Arial", 12)).pack(pady=5)
year_entry = tk.Entry(input_frame, textvariable=year_var, font=("Arial", 12))
year_entry.pack(pady=5)

create_button = tk.Button(input_frame, text="Create", font=("Arial", 12), command=save_semester)
create_button.pack(pady=10)

tk.Label(output_frame, text="Semesters", font=("Arial", 14)).pack(anchor="w", pady=5)
load_semesters()

root.mainloop()