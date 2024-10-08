---

# 📝 Notes.app

**A sleek, modern note-taking application with a twist — track your productivity with a streak system, all wrapped in a dark/light theme toggle.** Built with Python, Tkinter, and MySQL, this app ensures your notes are organized, secure, and always within reach.

## 🌟 Features

- **User Authentication:** Secure login and registration system to protect your notes.
- **Elegant UI:** Responsive and polished interface with a theme toggle (Darkly & Litera) powered by `ttkbootstrap`.
- **Notes Management:** Create, edit, and delete notes with ease. Sidebar navigation keeps your notes just a click away.
- **Streak Tracker:** Keep your productivity high! Track your daily note-taking streaks with an intuitive heatmap.
- **Database Integration:** All notes, users, and streak data are securely stored in a MySQL database, ensuring your information is always safe.
- **Dynamic Heatmap:** Visualize your streaks with a dynamically updated 30-day heatmap.

## 🛠️ Tech Stack

- **Python:** Core language powering the app.
- **Tkinter & ttkbootstrap:** For a responsive and customizable GUI.
- **MySQL:** Secure database management for user authentication, notes, and streak tracking.

## 🛡️ Security

User credentials are securely stored in the MySQL database with basic encryption practices. Further enhancements will include password hashing and more robust authentication mechanisms.

![python_XG9eGXUIYT](https://github.com/user-attachments/assets/0437510e-a2ca-46df-9867-29e3cbe93976)


## 🎨 Themes & Customization

Toggle between dark and light modes effortlessly. The dark mode enhances focus and minimizes eye strain, while the light mode offers a clean and crisp reading experience.

![python_7qWRWcyZdD](https://github.com/user-attachments/assets/8c24879c-8b6c-4178-9213-75584726c23a)



## 🚀 Getting Started

1. **Clone the repository:**

   ```bash
   git clone https://github.com/your-username/Notes.git
   cd Notes
   ```

2. **Install dependencies:**
   Run the following command in terminal pip install -r requirements.txt
   Ensure you have Python, MySQL, and `ttkbootstrap` installed:

   ```bash
   pip install mysql-connector-python ttkbootstrap
   ```

3. **Set up your MySQL database:**

   - Create a new MySQL database named `notes`.
   - Update the database credentials in the `connect_db` method of `LoginWindow` and `NoteApp` classes.

4. **Run the application:**

   ```bash
   python app.py
   ```


