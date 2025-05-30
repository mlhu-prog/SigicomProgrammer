

def image_selector(cache_main_dir):
    import os
    from tkinter import messagebox, filedialog
    import tkinter as tk
    from PIL import Image, ImageTk

    def cancel():
        root.quit()
        root.destroy()

    def proceed():
    
        old_images_dir = os.path.join(cache_main_dir,"Rapport","Figurer","Oversigtsfoto")

        for filename in os.listdir(old_images_dir):
            file_path = os.path.join(old_images_dir, filename)
            os.remove(file_path)

        root.update_idletasks()
        # Get the number of images from the entry
        image_count = image_count_var.get()

        if image_count < 1:
            image_count = int(entry.get())

        # Ensure the user entered at least 1
        if image_count < 1:
            messagebox.showerror("Error", "Skriv venligst mindst 1 billede.")
            return

        # Hide or destroy the initial window
        root.withdraw()  # This hides the window
        # Alternatively, you could use: root.destroy()  # This would close the window

        # Create the next window to browse for images
        open_image_browsing_window(image_count, root)

    def open_hyperlink(event):
        import webbrowser
        webbrowser.open("https://cowi.sharepoint.com/:w:/r/sites/A004371-project/Shared%20Documents/3%20Projekt%20dokumenter/Generiske%20rapporter/Generisk%20rapport%20-%20Oversigtsbillede/AXXXXXX-XXX.00X%20-%20Vibration.docm?d=wd7811d42f7ab48c19d22f94f1bb487a9&csf=1&web=1&e=e9h6IX")  # Replace with your desired URL


    def open_image_browsing_window(image_count, root):
        def on_cancel():
            browsing_window.destroy()
            root.deiconify()

        def on_continue():
            root.quit()
            root.destroy()
            
        browsing_window = tk.Toplevel(root)
        browsing_window.title("Oversigtsfoto")
        browsing_window.geometry("500x300")

        image_paths = []

        for i in range(image_count):
            frame = tk.Frame(browsing_window)
            frame.pack(pady=5)

            label = tk.Label(frame, text=f"Oversigtsfoto {i + 1}:")
            label.pack(side=tk.LEFT)

            browse_button = tk.Button(frame, text="Browse", command=lambda i=i: browse_image(i, image_paths))
            browse_button.pack(side=tk.RIGHT)

            # Entry field to show the selected image path
            image_path_entry = tk.Entry(frame, width=50)
            image_path_entry.pack(side=tk.LEFT, padx=5)
            image_paths.append(image_path_entry)

        img_num_text = ["oversigtsbilleder", "disse", "billeder"] if image_count > 1 else ["oversigtsbillede", "denne", "billede"]

        tk.Label(browsing_window, text="Guide:").pack()
        tk.Label(browsing_window, text=f"Brug evt. generisk rapport til at lave {img_num_text[0]} \n Tag efterfølgende et screenshot af {img_num_text[1]} og gem som .jpg fil", anchor='e').pack(pady=1)
        hyperlink = tk.Label(browsing_window, text="Generisk rapport", fg="blue", cursor="hand2") 
        hyperlink.pack(pady=5)
        hyperlink.bind("<Button-1>", open_hyperlink)

        tk.Label(browsing_window, text="(Husk at åbne i word-appen)").pack()

        proceed_button = tk.Button(browsing_window, text=f"Se {img_num_text[2]}", command=lambda: process_images(image_paths))
        proceed_button.pack(pady=10)

        # Create a frame to contain the cancel and continue buttons
        button_frame = tk.Frame(browsing_window)
        button_frame.pack(pady=10)

        # Create a frame to contain the cancel and continue buttons
        button_frame = tk.Frame(browsing_window)
        button_frame.pack(pady=10)

        cancel_button = tk.Button(button_frame, text="Tilbage", command=on_cancel)
        cancel_button.pack(side=tk.LEFT, padx=5)

        continue_button = tk.Button(button_frame, text="Fortsæt", command=on_continue)
        continue_button.pack(side=tk.LEFT, padx=5)

    def browse_image(index, image_paths):
        file_path = filedialog.askopenfilename(filetypes=[("JPG files", "*.jpg"), ("JPEG files", "*.jpeg")])
        if file_path:
            # Update the corresponding entry field with the selected path
            image_paths[index].delete(0, tk.END)  # Clear the entry field first
            image_paths[index].insert(0, file_path)  # Insert the selected file path

    def process_images(image_paths):
        for i, image_path_entry in enumerate(image_paths):
            image_path = image_path_entry.get()
            if image_path:
                save_location = os.path.join(cache_main_dir,"Rapport","Figurer","Oversigtsfoto",f"oversigtsfoto_{i+1}.jpg")
                open_image_editor(image_path, save_location, root)
        
    def open_image_editor(image_path, save_location, parent_window):
        def on_ok():
            # Save the image to the given location
            image.save(save_location)
            messagebox.showinfo(title="Gemt", message="Oversigtsbilledet er gemt")
            editor_window.quit()
            editor_window.destroy()

        def on_cancel():
            editor_window.quit()
            editor_window.destroy()

        # Create a new window for the image editor
        editor_window = tk.Toplevel(parent_window)
        editor_window.title("Image Viewer")

        # Load the image
        image = Image.open(image_path)
        image_copy = image.copy()
        photo = ImageTk.PhotoImage(image_copy)

        # Create a label to display the image
        image_label = tk.Label(editor_window, image=photo)
        image_label.image = photo  # Keep a reference to avoid garbage collection
        image_label.pack(pady=10)

        # Create OK and Cancel buttons
        ok_button = tk.Button(editor_window, text="Forsæt", command=on_ok)
        ok_button.pack(side=tk.LEFT, padx=10, pady=10)

        cancel_button = tk.Button(editor_window, text="Afbryd", command=on_cancel)
        cancel_button.pack(side=tk.RIGHT, padx=10, pady=10)

        editor_window.mainloop()

    root = tk.Tk()
    root.title("Image Selector")
    root.geometry("300x150")
    
    label = tk.Label(root, text="Antal oversigtsbilleder?")
    label.pack(pady=10)

    image_count_var = tk.IntVar(value=1)  # Default to 1 image
    entry = tk.Entry(root, textvariable=image_count_var, justify='center')
    entry.pack(pady=10)

    # Frame for buttons
    button_frame = tk.Frame(root)
    button_frame.pack(pady=10)

    cancel_button = tk.Button(button_frame, text="Annuller", width=10, command=cancel)
    cancel_button.pack(side='left', padx=5)

    proceed_button = tk.Button(button_frame, text="Fortsæt", width=10, command=proceed)
    proceed_button.pack(side='left', padx=5)

    root.mainloop()


# Example usage
#cache_main_dir = "O:\\A000000\\A004371\\3_Pdoc\\Afrapportering\\A223276-050 - Frederik Obels Vej, Aalborg"
#image_selector(cache_main_dir)