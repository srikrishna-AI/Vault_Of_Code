import json
import tkinter as tk
from tkinter import messagebox, ttk
import platform

# Task Management: Define the Task class
class Task:
    def __init__(self, title, description, category, completed=False):
        self.title = title
        self.description = description
        self.category = category
        self.completed = completed

    def mark_completed(self):
        self.completed = True

    def __repr__(self):
        status = '✓' if self.completed else '✗'
        return f"{self.title} [{self.category}] - {status}: {self.description}"

# File Handling: Functions to save and load tasks from a JSON file
def save_tasks(tasks, filename="tasks.json"):
    try:
        with open(filename, 'w') as f:
            json.dump([task.__dict__ for task in tasks], f, indent=4)
        print("Tasks have been saved successfully.")
    except Exception as e:
        print(f"Error saving tasks: {e}")

def load_tasks(filename="tasks.json"):
    try:
        with open(filename, 'r') as f:
            content = f.read().strip()  # Check if file is empty
            if content:
                return [Task(**data) for data in json.loads(content)]
            else:
                return []  # Return an empty list if the file is empty
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        print("Error decoding JSON. Starting with an empty task list.")
        return []
    except Exception as e:
        print(f"Error loading tasks: {e}")
        return []

# GUI Application using Tkinter with Enhanced Colors and Resizable Window
class ToDoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("To-Do List Application")
        self.root.geometry("700x500")  # Initial size, but window is resizable now

        # Define color scheme
        self.bg_color = "#f0f0f0"          # Light Gray for main background
        self.frame_bg = "#ffffff"          # White for frames
        self.button_bg = "#4CAF50"         # Green for buttons
        self.button_fg = "#ffffff"         # White text on buttons
        self.entry_bg = "#e8e8e8"          # Slightly darker gray for entry fields
        self.label_fg = "#333333"          # Dark gray for labels
        self.listbox_bg = "#ffffff"        # White background for listbox
        self.listbox_fg = "#333333"        # Dark gray text in listbox
        self.listbox_select_bg = "#4CAF50" # Green selection background
        self.listbox_select_fg = "#ffffff" # White selection text

        self.root.configure(bg=self.bg_color)

        self.tasks = load_tasks()

        # Configure grid layout for root to allow resizing
        self.root.columnconfigure(0, weight=1)
        self.root.columnconfigure(1, weight=3)
        self.root.rowconfigure(0, weight=1)

        # Frames
        self.frame_left = ttk.Frame(self.root, padding="20 20 20 20", style="Left.TFrame")
        self.frame_left.grid(row=0, column=0, sticky="nsew")

        self.frame_right = ttk.Frame(self.root, padding="20 20 20 20", style="Right.TFrame")
        self.frame_right.grid(row=0, column=1, sticky="nsew")

        # Style Configuration
        style = ttk.Style()
        style.theme_use('clam')  # Use 'clam' theme for better styling options

        # Configure styles for labels and buttons
        style.configure("Left.TFrame", background=self.bg_color)
        style.configure("Right.TFrame", background=self.bg_color)
        style.configure("TLabel", background=self.bg_color, foreground=self.label_fg, font=("Helvetica", 12))
        style.configure("Header.TLabel", background=self.bg_color, foreground=self.label_fg, font=("Helvetica", 16, "bold"))
        style.configure("TButton", background=self.button_bg, foreground=self.button_fg, font=("Helvetica", 10, "bold"))
        style.map("TButton",
                  background=[('active', '#45a049')],
                  foreground=[('active', self.button_fg)])

        # Left Frame Components: Add Task
        ttk.Label(self.frame_left, text="Add New Task", style="Header.TLabel").pack(pady=(0, 10), anchor='w')

        self.title_var = tk.StringVar()
        ttk.Label(self.frame_left, text="Title:").pack(anchor='w', pady=(5, 0))
        self.entry_title = ttk.Entry(self.frame_left, textvariable=self.title_var, font=("Helvetica", 12))
        self.entry_title.pack(fill='x', pady=5)
        self.entry_title.configure(background=self.entry_bg)

        self.description_var = tk.StringVar()
        ttk.Label(self.frame_left, text="Description:").pack(anchor='w', pady=(5, 0))
        self.entry_description = ttk.Entry(self.frame_left, textvariable=self.description_var, font=("Helvetica", 12))
        self.entry_description.pack(fill='x', pady=5)
        self.entry_description.configure(background=self.entry_bg)

        self.category_var = tk.StringVar()
        ttk.Label(self.frame_left, text="Category:").pack(anchor='w', pady=(5, 0))
        self.entry_category = ttk.Entry(self.frame_left, textvariable=self.category_var, font=("Helvetica", 12))
        self.entry_category.pack(fill='x', pady=5)
        self.entry_category.configure(background=self.entry_bg)

        self.btn_add = ttk.Button(self.frame_left, text="Add Task", command=self.add_task)
        self.btn_add.pack(pady=15, fill='x')

        # Right Frame Components: Task List and Actions
        ttk.Label(self.frame_right, text="Current Tasks", style="Header.TLabel").pack(pady=(0, 10), anchor='w')

        # Scrollbar for the listbox
        self.scrollbar = ttk.Scrollbar(self.frame_right)
        self.scrollbar.pack(side='right', fill='y')

        self.listbox_tasks = tk.Listbox(
            self.frame_right,
            height=15,
            yscrollcommand=self.scrollbar.set,
            font=("Helvetica", 12),
            bg=self.listbox_bg,
            fg=self.listbox_fg,
            selectbackground=self.listbox_select_bg,
            selectforeground=self.listbox_select_fg
        )
        self.listbox_tasks.pack(fill='both', expand=True)
        self.scrollbar.config(command=self.listbox_tasks.yview)

        # Bind mouse wheel to the listbox
        self.bind_mousewheel(self.listbox_tasks)

        # Action Buttons Frame
        self.frame_buttons = ttk.Frame(self.frame_right, padding="10 10 10 10", style="Right.TFrame")
        self.frame_buttons.pack(fill='x', pady=10)

        self.btn_complete = ttk.Button(self.frame_buttons, text="Mark as Completed", command=self.complete_task)
        self.btn_complete.pack(pady=5, fill='x')

        self.btn_delete = ttk.Button(self.frame_buttons, text="Delete Task", command=self.delete_task)
        self.btn_delete.pack(pady=5, fill='x')

        self.btn_save = ttk.Button(self.frame_buttons, text="Save Tasks", command=self.save_tasks_gui)
        self.btn_save.pack(pady=5, fill='x')

        self.btn_exit = ttk.Button(self.frame_buttons, text="Exit", command=self.exit_app)
        self.btn_exit.pack(pady=5, fill='x')

        self.populate_tasks()

    def bind_mousewheel(self, widget):
        # Detect the operating system and bind mouse wheel accordingly
        system = platform.system()
        if system == 'Windows':
            widget.bind("<MouseWheel>", self.on_mousewheel)
        elif system == 'Darwin':  # macOS
            widget.bind("<Button-4>", self.on_mousewheel)
            widget.bind("<Button-5>", self.on_mousewheel)
        else:  # Linux and others
            widget.bind("<Button-4>", self.on_mousewheel)
            widget.bind("<Button-5>", self.on_mousewheel)

    def on_mousewheel(self, event):
        system = platform.system()
        if system == 'Windows':
            # For Windows, event.delta is positive or negative
            self.listbox_tasks.yview_scroll(int(-1*(event.delta/120)), "units")
        elif system == 'Darwin':
            # For macOS, use event.delta
            self.listbox_tasks.yview_scroll(int(-1*event.delta), "units")
        else:
            # For Linux, use Button-4 and Button-5
            if event.num == 4:
                self.listbox_tasks.yview_scroll(-1, "units")
            elif event.num == 5:
                self.listbox_tasks.yview_scroll(1, "units")

    def add_task(self):
        title = self.title_var.get().strip()
        description = self.description_var.get().strip()
        category = self.category_var.get().strip() or "General"

        if not title:
            messagebox.showerror("Input Error", "Title cannot be empty.")
            return

        new_task = Task(title, description, category)
        self.tasks.append(new_task)
        self.populate_tasks()
        self.clear_entries()
        messagebox.showinfo("Success", "Task added successfully!")

    def populate_tasks(self):
        self.listbox_tasks.delete(0, tk.END)
        for idx, task in enumerate(self.tasks, 1):
            status = "✓" if task.completed else "✗"
            display_text = f"{idx}. {task.title} [{task.category}] - {status}"
            self.listbox_tasks.insert(tk.END, display_text)

    def complete_task(self):
        selected_indices = self.listbox_tasks.curselection()
        if not selected_indices:
            messagebox.showwarning("Selection Error", "Please select a task to mark as completed.")
            return
        index = selected_indices[0]
        task = self.tasks[index]
        if task.completed:
            messagebox.showinfo("Info", "Task is already marked as completed.")
        else:
            task.mark_completed()
            self.populate_tasks()
            messagebox.showinfo("Success", "Task marked as completed!")

    def delete_task(self):
        selected_indices = self.listbox_tasks.curselection()
        if not selected_indices:
            messagebox.showwarning("Selection Error", "Please select a task to delete.")
            return
        index = selected_indices[0]
        task = self.tasks[index]
        confirm = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete '{task.title}'?")
        if confirm:
            del self.tasks[index]
            self.populate_tasks()
            messagebox.showinfo("Deleted", "Task deleted successfully!")

    def save_tasks_gui(self):
        save_tasks(self.tasks)
        messagebox.showinfo("Saved", "Tasks have been saved successfully.")

    def exit_app(self):
        save_tasks(self.tasks)
        self.root.quit()

    def clear_entries(self):
        self.title_var.set("")
        self.description_var.set("")
        self.category_var.set("")

# Run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = ToDoApp(root)
    root.mainloop()
