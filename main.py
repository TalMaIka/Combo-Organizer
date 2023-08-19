import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from ttkthemes import ThemedStyle
import os


def get_unique_filename(filename):
    base, ext = os.path.splitext(filename)
    counter = 1
    while os.path.exists(filename):
        filename = f"{base}_{counter}{ext}"
        counter += 1
    return filename


def separate_usernames_passwords(input_file, usernames_file, passwords_file):
    with open(input_file, 'r') as f:
        usernames = []
        passwords = []

        for line in f:
            parts = line.strip().split(':')
            if len(parts) == 2:
                username, password = parts
                usernames.append(username)
                passwords.append(password)

        with open(usernames_file, 'w') as uf:
            uf.write('\n'.join(usernames))

        with open(passwords_file, 'w') as pf:
            pf.write('\n'.join(passwords))


def extract_emails(input_file, output_file):
    with open(input_file, 'r') as f:
        lines = [line.strip() for line in f if '@' in line.split(':')[0]]

        output_file = get_unique_filename(output_file)
        with open(output_file, 'w') as of:
            of.write('\n'.join(lines))


def extract_non_emails(input_file, output_file):
    with open(input_file, 'r') as f:
        lines = [line.strip() for line in f if '@' not in line.split(':')[0]]

        output_file = get_unique_filename(output_file)
        with open(output_file, 'w') as of:
            of.write('\n'.join(lines))


def remove_duplicates(input_file, output_file):
    with open(input_file, 'r') as f:
        lines = set(line.strip() for line in f)

        output_file = get_unique_filename(output_file)
        with open(output_file, 'w') as of:
            of.write('\n'.join(lines))


def browse_input_file():
    file_path = filedialog.askopenfilename(filetypes=[('Text Files', '*.txt')])
    input_file_entry.delete(0, tk.END)
    input_file_entry.insert(0, file_path)
    update_process_button_state()


def process_files():
    input_file = input_file_entry.get()

    if separate_usernames_passwords_var.get():
        separate_usernames_passwords(input_file, 'usernames.txt', 'passwords.txt')

    if extract_emails_var.get():
        extract_emails(input_file, 'email_usernames.txt')

    if extract_non_emails_var.get():
        extract_non_emails(input_file, 'non_email_usernames.txt')

    if remove_duplicates_var.get():
        remove_duplicates(input_file, 'no_duplicates.txt')

    messagebox.showinfo('Success', 'Files processed successfully!')


def update_process_button_state():
    # Enable the Process Files button only if there is an input file and at least one option is selected
    input_file = input_file_entry.get()
    options_selected = (separate_usernames_passwords_var.get() or
                        extract_emails_var.get() or
                        extract_non_emails_var.get() or
                        remove_duplicates_var.get())
    process_button["state"] = tk.NORMAL if input_file and options_selected else tk.DISABLED


# Create the main window
root = tk.Tk()
root.title('Combo Organizer')

# Get the screen width and height
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Calculate the position for centering the window
x = (screen_width - 400) // 2  # Adjust the window width if needed
y = (screen_height - 400) // 2  # Adjust the window height if needed

root.geometry(f'380x280+{x}+{y}')  # Center the window on the screen

# Apply the "arc" theme from ttkthemes
style = ThemedStyle(root)
style.set_theme('arc')

# Adjust the checkbox style to remove the background color and dotted focus
style.configure("TCheckbutton", background=root.cget("background"), focuscolor=root.cget("background"), highlightthickness=0)

# Create and place widgets
input_label = ttk.Label(root, text='Select Input File:')
input_label.pack(pady=(10, 0), anchor='center')

input_file_entry = ttk.Entry(root)
input_file_entry.pack(fill=tk.X, padx=10, pady=5)

browse_button = ttk.Button(root, text='Browse', command=browse_input_file)
browse_button.pack(anchor='center')

# Title for options
options_title = ttk.Label(root, text='Options:', font=('Helvetica', 8, 'bold'), foreground='black')
options_title.pack(anchor='center', pady=(15, 5))

# Checkboxes for processing options
remove_duplicates_var = tk.BooleanVar()
remove_duplicates_checkbox = ttk.Checkbutton(root, text='Remove Duplicates', variable=remove_duplicates_var, command=update_process_button_state)
remove_duplicates_checkbox.pack(anchor='center', padx=20)

separate_usernames_passwords_var = tk.BooleanVar()
separate_usernames_passwords_checkbox = ttk.Checkbutton(root, text='Separate Usernames and Passwords', variable=separate_usernames_passwords_var, command=update_process_button_state)
separate_usernames_passwords_checkbox.pack(anchor='center', padx=20)

extract_emails_var = tk.BooleanVar()
extract_emails_checkbox = ttk.Checkbutton(root, text='Extract Emails', variable=extract_emails_var, command=update_process_button_state)
extract_emails_checkbox.pack(anchor='center', padx=20)

extract_non_emails_var = tk.BooleanVar()
extract_non_emails_checkbox = ttk.Checkbutton(root, text='Extract Non-Emails', variable=extract_non_emails_var, command=update_process_button_state)
extract_non_emails_checkbox.pack(anchor='center', padx=20)

process_button = ttk.Button(root, text='Process Files', command=process_files, state=tk.DISABLED)  # Disabled by default
process_button.pack(pady=10)

# Start the main loop
root.mainloop()
