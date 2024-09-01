import mysql.connector
from mysql.connector import Error
from tkinter import messagebox, ttk
import tkinter as tk
import ttkbootstrap as ttk
import datetime

class LoginWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Login")
        self.root.geometry("300x300")

        # Initialize the style before creating any widgets
        self.style = ttk.Style(theme="darkly")

        self.username_label = ttk.Label(root, text="Username:", style='TLabel')
        self.username_label.pack(pady=(20, 5))
        self.username_entry = ttk.Entry(root, width=30, style='TEntry')
        self.username_entry.pack(pady=5)

        self.password_label = ttk.Label(root, text="Password:", style='TLabel')
        self.password_label.pack(pady=(10, 5))
        self.password_entry = ttk.Entry(root, width=30, style='TEntry', show="*")
        self.password_entry.pack(pady=5)

        self.login_button = ttk.Button(root, text="Login", command=self.verify_login, style='TButton')
        self.login_button.pack(pady=(10, 10))

        self.register_button = ttk.Button(root, text="Register", command=self.open_register_window, style='TButton')
        self.register_button.pack(pady=(5, 10))

        self.connection = None
        self.connect_db()

    def connect_db(self):
        """Connect to the MySQL database."""
        try:
            self.connection = mysql.connector.connect(
                host='localhost',
                user='root',  # Replace with your MySQL username
                password='1234',  # Replace with your MySQL password
                database='notes'  # Replace with your database name
            )
            if self.connection.is_connected():
                print("Connected to MySQL database")
        except Error as e:
            messagebox.showerror("Error", f"Error connecting to database: {e}")
            self.connection = None

    def verify_login(self):
        """Verify the username and password against the database."""
        username = self.username_entry.get()
        password = self.password_entry.get()

        if self.connection:
            cursor = self.connection.cursor()
            cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
            user = cursor.fetchone()

            if user:
                messagebox.showinfo("Success", "Login successful!")
                app_window = tk.Tk()
                NoteApp(app_window)
                app_window.mainloop()
                self.root.destroy()  # Close the login window
            else:
                messagebox.showerror("Error", "Invalid username or password.")
        else:
            messagebox.showerror("Error", "Database connection not established.")

    def open_register_window(self):
        """Open the registration window."""
        register_window = tk.Toplevel(self.root)
        RegisterWindow(register_window, self.connection)

class RegisterWindow:
    def __init__(self, root, connection):
        self.root = root
        self.root.title("Register")
        self.root.geometry("300x300")

        self.connection = connection

        self.username_label = ttk.Label(root, text="Username:", style='TLabel')
        self.username_label.pack(pady=(20, 5))
        self.username_entry = ttk.Entry(root, width=30, style='TEntry')
        self.username_entry.pack(pady=5)

        self.password_label = ttk.Label(root, text="Password:", style='TLabel')
        self.password_label.pack(pady=(10, 5))
        self.password_entry = ttk.Entry(root, width=30, style='TEntry', show="*")
        self.password_entry.pack(pady=5)

        self.register_button = ttk.Button(root, text="Register", command=self.register_user, style='TButton')
        self.register_button.pack(pady=(10, 10))

    def register_user(self):
        """Register a new user in the database."""
        username = self.username_entry.get()
        password = self.password_entry.get()

        if username and password:
            try:
                cursor = self.connection.cursor()
                cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
                self.connection.commit()
                messagebox.showinfo("Success", "User registered successfully!")
                self.root.destroy()  # Close the registration window
            except Error as e:
                messagebox.showerror("Error", f"Error registering user: {e}")
        else:
            messagebox.showerror("Error", "Username and password cannot be empty.")

class NoteApp:
    def __init__(self, root):
        self.root = root
        self.current_theme = "darkly"  # Default theme

        self.style = ttk.Style(theme=self.current_theme)  # Set the initial theme
        self.configure_styles()

        self.notes = []
        self.current_note_index = None
        self.connection = None
        self.streak_dates = []
        self.current_streak = 0

        # Sidebar for previous notes
        self.sidebar_frame = ttk.Frame(root, width=200, style='TFrame')
        self.sidebar_frame.pack(side=tk.LEFT, fill=tk.Y)

        self.sidebar_label = ttk.Label(self.sidebar_frame, text="Previous Notes", style='TLabel')
        self.sidebar_label.pack(pady=(10, 10))

        self.sidebar_listbox = tk.Listbox(self.sidebar_frame, width=30, bg='#2c2c2e', fg='#4937bd', bd=0, highlightthickness=0, selectbackground='#5e5ce6', relief='flat')
        self.sidebar_listbox.pack(side=tk.LEFT, fill=tk.Y, padx=(10, 0))

        self.sidebar_scrollbar = ttk.Scrollbar(self.sidebar_frame, orient=tk.VERTICAL, command=self.sidebar_listbox.yview, style='TScrollbar')
        self.sidebar_scrollbar.pack(side=tk.RIGHT, fill=tk.Y, padx=(0, 10))
        self.sidebar_listbox.config(yscrollcommand=self.sidebar_scrollbar.set)

        # Main frame for note content
        self.main_frame = ttk.Frame(root, style='TFrame')
        self.main_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.title_label = ttk.Label(self.main_frame, text="Title", style='TLabel')
        self.title_label.pack(pady=(0, 5))

        self.title_entry = ttk.Entry(self.main_frame, width=100, style='TEntry')
        self.title_entry.pack(pady=(0, 10))

        self.content_label = ttk.Label(self.main_frame, text="Content", style='TLabel')
        self.content_label.pack(pady=(0, 5))

        self.content_text = tk.Text(self.main_frame, height=20, width=100, bg='#3a3a3c', fg='#4937bd', bd=0, highlightthickness=0, relief='flat', insertbackground='white')
        self.content_text.pack(fill=tk.BOTH, expand=True, pady=(0, 10))

        self.new_note_button = ttk.Button(self.main_frame, text="New Note", command=self.new_note, style='TButton')
        self.new_note_button.pack(side=tk.RIGHT, pady=10)

        self.save_button = ttk.Button(self.main_frame, text="Save Note", command=self.save_note, style='TButton')
        self.save_button.pack(side=tk.LEFT, padx=10)

        self.delete_button = ttk.Button(self.main_frame, text="Delete Note", command=self.delete_note, style='TButton')
        self.delete_button.pack(side=tk.LEFT, padx=10)

        self.toggle_theme_button = ttk.Button(self.main_frame, text="Toggle Theme", command=self.toggle_theme, style='TButton')
        self.toggle_theme_button.pack(side=tk.RIGHT, padx=10)

        # Streak frame
        self.streak_frame = ttk.Frame(root, style='TFrame')
        self.streak_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=(10, 0))

        self.streak_label = ttk.Label(self.streak_frame, text="Your Streak: 0 days", style='TLabel')
        self.streak_label.pack()

        self.streak_heatmap = tk.Canvas(self.streak_frame, width=400, height=200, bg='#2c2c2e', bd=0, highlightthickness=0)
        self.streak_heatmap.pack(pady=(10, 10))

        self.reset_streak_button = ttk.Button(self.main_frame, text="Reset Streak", command=self.reset_streak, style='TButton')
        self.reset_streak_button.pack(side=tk.RIGHT, padx=10)

        self.connect_db()
        if self.connection:
            self.create_tables()
            self.load_notes()
            self.load_streaks()
            self.populate_sidebar()
            self.update_streak_heatmap()

        # Bind the listbox selection event to the on_note_select method
        self.sidebar_listbox.bind("<<ListboxSelect>>", self.on_note_select)

    def configure_styles(self):
        """Configure the styles for the widgets."""
        try:
            self.style.configure('TFrame', background='#2c2c2e')
            self.style.configure('TLabel', background='#2c2c2e', foreground='#ffffff')
            self.style.configure('TEntry', background='#3a3a3c', foreground='#ffffff', borderwidth=1, relief='solid')
            self.style.configure('TButton', background='#5e5ce6', foreground='#ffffff', borderwidth=1, relief='solid')

            # Configure the scrollbar styles if not already done
            if not self.style.lookup('TScrollbar', 'background'):
                self.style.configure('TScrollbar', background='#3a3a3c', troughcolor='#2c2c2e', gripcount=0)
        except Exception as e:
            print(f"Error configuring styles: {e}")


    def create_tables(self):
        """Create tables in the database if they don't exist."""
        try:
            if self.connection:
                cursor = self.connection.cursor()
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS notes (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        title VARCHAR(255) NOT NULL,
                        content TEXT NOT NULL
                    )
                """)
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS streaks (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        date DATE NOT NULL
                    )
                """)
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS users (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        username VARCHAR(255) NOT NULL UNIQUE,
                        password VARCHAR(255) NOT NULL
                    )
                """)
                self.connection.commit()
        except Error as e:
            messagebox.showerror("Error", f"Error creating tables: {e}")

    def load_notes(self):
        """Load notes from the database into the notes list."""
        try:
            if self.connection:
                cursor = self.connection.cursor()
                cursor.execute("SELECT * FROM notes")
                self.notes = cursor.fetchall()
        except Error as e:
            messagebox.showerror("Error", f"Error loading notes: {e}")

    def load_streaks(self):
        """Load streak dates from the database."""
        try:
            if self.connection:
                cursor = self.connection.cursor()
                cursor.execute("SELECT date FROM streaks")
                streak_dates = cursor.fetchall()
                self.streak_dates = [date[0] for date in streak_dates]
                self.calculate_streak()
        except Error as e:
            messagebox.showerror("Error", f"Error loading streaks: {e}")

    def calculate_streak(self):
        """Calculate the current streak."""
        if self.streak_dates:
            sorted_dates = sorted(self.streak_dates)
            streak_count = 0
            previous_date = None

            for date in sorted_dates:
                if previous_date is None:
                    streak_count = 1
                elif (date - previous_date).days == 1:
                    streak_count += 1
                else:
                    streak_count = 1

                previous_date = date

            self.current_streak = streak_count
            self.update_streak_label()

    def update_streak_label(self):
        """Update the streak label."""
        self.streak_label.config(text=f"Your Streak: {self.current_streak} days")

    def populate_sidebar(self):
        """Populate the sidebar with note titles."""
        self.sidebar_listbox.delete(0, tk.END)
        for note in self.notes:
            self.sidebar_listbox.insert(tk.END, note[1])

    def on_note_select(self, event):
        """Handle note selection from the sidebar."""
        selection = event.widget.curselection()
        if selection:
            self.current_note_index = selection[0]
            self.display_note()

    def display_note(self):
        """Display the selected note in the main area."""
        if self.current_note_index is not None:
            note = self.notes[self.current_note_index]
            self.title_entry.delete(0, tk.END)
            self.title_entry.insert(0, note[1])
            self.content_text.delete("1.0", tk.END)
            self.content_text.insert("1.0", note[2])

    def new_note(self):
        """Create a new note."""
        self.title_entry.delete(0, tk.END)
        self.content_text.delete("1.0", tk.END)
        self.current_note_index = None

    def save_note(self):
        """Save the current note to the database."""
        title = self.title_entry.get()
        content = self.content_text.get("1.0", tk.END).strip()

        if title and content:
            if self.current_note_index is None:
                # Insert new note
                try:
                    if self.connection:
                        cursor = self.connection.cursor()
                        cursor.execute("INSERT INTO notes (title, content) VALUES (%s, %s)", (title, content))
                        self.connection.commit()
                        self.load_notes()
                        self.populate_sidebar()
                        self.current_note_index = len(self.notes) - 1
                        self.sidebar_listbox.select_set(self.current_note_index)
                        self.update_streak()
                        messagebox.showinfo("Success", "Note saved successfully!")
                except Error as e:
                    messagebox.showerror("Error", f"Error saving note: {e}")
            else:
                # Update existing note
                note_id = self.notes[self.current_note_index][0]
                try:
                    if self.connection:
                        cursor = self.connection.cursor()
                        cursor.execute("UPDATE notes SET title = %s, content = %s WHERE id = %s", (title, content, note_id))
                        self.connection.commit()
                        self.load_notes()
                        self.populate_sidebar()
                        messagebox.showinfo("Success", "Note updated successfully!")
                except Error as e:
                    messagebox.showerror("Error", f"Error updating note: {e}")
        else:
            messagebox.showerror("Error", "Title and content cannot be empty.")

    def delete_note(self):
        """Delete the current note from the database."""
        if self.current_note_index is not None:
            note_id = self.notes[self.current_note_index][0]
            try:
                if self.connection:
                    cursor = self.connection.cursor()
                    cursor.execute("DELETE FROM notes WHERE id = %s", (note_id,))
                    self.connection.commit()
                    self.load_notes()
                    self.populate_sidebar()
                    self.new_note()
                    messagebox.showinfo("Success", "Note deleted successfully!")
            except Error as e:
                messagebox.showerror("Error", f"Error deleting note: {e}")

    def update_streak(self):
        """Update the streak after saving a note."""
        today = datetime.date.today()
        if today not in self.streak_dates:
            try:
                if self.connection:
                    cursor = self.connection.cursor()
                    cursor.execute("INSERT INTO streaks (date) VALUES (%s)", (today,))
                    self.connection.commit()
                    self.load_streaks()
                    self.update_streak_heatmap()
            except Error as e:
                messagebox.showerror("Error", f"Error updating streak: {e}")

    def reset_streak(self):
        """Reset the streak by deleting all streak records."""
        confirm = messagebox.askyesno("Reset Streak", "Are you sure you want to reset your streak?")
        if confirm:
            try:
                if self.connection:
                    cursor = self.connection.cursor()
                    cursor.execute("DELETE FROM streaks")
                    self.connection.commit()
                    self.streak_dates = []
                    self.current_streak = 0
                    self.update_streak_label()
                    self.update_streak_heatmap()
                    messagebox.showinfo("Success", "Streak reset successfully!")
            except Error as e:
                messagebox.showerror("Error", f"Error resetting streak: {e}")

    def update_streak_heatmap(self):
        """Update the streak heatmap canvas."""
        self.streak_heatmap.delete("all")
        today = datetime.date.today()
        day_size = 20
        padding = 5

        # Display the last 30 days in the heatmap
        for i in range(30):
            day = today - datetime.timedelta(days=i)
            x = 10 + (i % 7) * (day_size + padding)
            y = 10 + (i // 7) * (day_size + padding)
            color = "#5e5ce6" if day in self.streak_dates else "#3a3a3c"
            self.streak_heatmap.create_rectangle(x, y, x + day_size, y + day_size, fill=color, outline="")

    def toggle_theme(self):
        """Toggle between dark and light themes."""
        if self.current_theme == "darkly":
            self.current_theme = "litera"
        else:
            self.current_theme = "darkly"
        self.style.theme_use(self.current_theme)
        self.configure_styles()
        self.update_streak_heatmap()


def main():
    root = tk.Tk()
    app = LoginWindow(root)
    root.mainloop()

if __name__ == "__main__":
    main()
