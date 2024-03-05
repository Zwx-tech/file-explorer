import os
import shutil
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox, simpledialog

class FileExplorer(tk.Tk):
    clipoboard_path: str
    clipboard_operation: str

    def __init__(self):
        super().__init__()
        self.title("File Explorer")
        self.geometry("500x400")
        
        # styling
        self.style = ttk.Style(self)
        self.tk.call('source', 'azure.tcl')
        self.tk.call("set_theme", "dark")
        
        # curent dirr
        self.current_directory = tk.StringVar()
        self.current_directory.set(os.getcwd())
        
        # paste dir
        self.clipoboard_path = None
        self.clipboard_operation = None

        # interface
        self.file_buttons = ttk.Frame(self)
        self.file_buttons.pack(pady=10)
        
        self.files_wrapper = ttk.Frame(self)
        self.scrollbar = ttk.Scrollbar(self.files_wrapper)
        self.file_listbox = ttk.Treeview(self.files_wrapper, yscrollcommand=self.scrollbar.set, show="tree")
        self.files_wrapper.pack(fill='x', padx=10)
        self.scrollbar.pack(side="right", fill="y")
        self.file_listbox.pack(side="left", fill="both", expand=True)

        self.action_buttons = ttk.Frame(self)
        self.action_buttons.pack(pady=10)
        self.copypaste_buttons = ttk.Frame(self)
        self.copypaste_buttons.pack()
        
        self.update_files()

        # blue butttons use
        # style='Accent.TButton'
        self.btn_open = ttk.Button(self.action_buttons, text="Open", command=self.open_file)
        self.btn_open.pack(side=tk.LEFT, padx=10)
        
        self.btn_delete = ttk.Button(self.action_buttons, text="Delete", command=self.delete_file)
        self.btn_delete.pack(side=tk.LEFT, padx=10)
        
        self.btn_rename = ttk.Button(self.action_buttons, text="Rename", command=self.rename_file)
        self.btn_rename.pack(side=tk.LEFT, padx=10)
 
        self.btn_copy = ttk.Button(self.copypaste_buttons, text="Copy", command=self.copy)
        self.btn_copy.pack(side=tk.LEFT, padx=10)
        
        self.btn_paste = ttk.Button(self.copypaste_buttons, text="Paste", command=self.paste)
        self.btn_paste.pack(side=tk.LEFT, padx=10)
     
        self.btn_move = ttk.Button(self.copypaste_buttons, text="Move", command=self.move)
        self.btn_move.pack(side=tk.LEFT, padx=10)
        
        self.btn_refresh = ttk.Button(self.file_buttons, text="Refresh", command=self.update_files)
        self.btn_refresh.pack(side=tk.LEFT, padx=10)
        
        self.btn_back = ttk.Button(self.file_buttons, text="Back", command=self.go_back)
        self.btn_back.pack(side=tk.RIGHT, padx=10)
        
        self.btn_up = ttk.Button(self.file_buttons, text="Go", command=self.go_up)
        self.btn_up.pack(side=tk.RIGHT, padx=10)
        
        self.create = ttk.Button(self.file_buttons, text="New Folder", command=self.create_new_dir)
        self.create.pack(side=tk.RIGHT, padx=10)
    
    @property
    def selected_file(self) -> str:
        curItem = self.file_listbox.focus()
        return self.file_listbox.item(curItem)["text"]
    
    def update_files(self):
        self.file_listbox.delete(*self.file_listbox.get_children())
        files = os.listdir(self.current_directory.get())
        for file in files:
            self.file_listbox.insert("", "end", text=file)
            
    def open_file(self):
        if not self.selected_file: 
            return
        file_path = os.path.join(self.current_directory.get(), self.selected_file)
        if os.path.isdir(file_path):
            self.current_directory.set(file_path)
            self.update_files()
        else:
            messagebox.showinfo("Info", f"Selected file: {file_path}")

    def copy(self):
        if not self.selected_file:
            return
        path = os.path.join(self.current_directory.get(), self.selected_file)
        messagebox.showinfo(title='Cool dialog', message='Copied successfully')
        self.clipoboard_path = path
        self.clipboard_operation = 'copy'
    
    def move(self):
        if not self.selected_file:
            return
        # old new path
        old_path = os.path.join(self.current_directory.get(), self.selected_file)
        new_path = simpledialog.askstring(
            'new path',
            'Plaese specify new path',
            initialvalue=self.current_directory.get()
        )
        # check if route exists
        if not os.path.isdir(new_path): 
            return
        destination_path = os.path.join(new_path, self.sel)
        print(destination_path)
        # preform move
        try:
            shutil.move(old_path, destination_path)
            self.update_files()
            messagebox.showinfo(title='Paste Successful', message='File moved successfully')
        except Exception as e:
            messagebox.showerror(title='Error', message=f'Error moving file: {str(e)}')

    def paste(self):
        if not self.clipoboard_path:
            messagebox.showerror(title='No file copied', message='Please copy a file first')
            return

        if self.clipboard_operation == 'copy':
            try:
                destination_path = os.path.join(self.current_directory.get(), os.path.basename(self.clipoboard_path))
                if os.path.isdir(self.clipoboard_path):
                    shutil.copytree(self.clipoboard_path, destination_path)
                else:
                    shutil.copy2(self.clipoboard_path, destination_path)
                self.update_files()
                messagebox.showinfo(title='Paste Successful', message='File copied successfully')
            except Exception as e:
                messagebox.showerror(title='Error', message=f'Error copying file: {str(e)}')
        # actually nevermind
        elif self.clipboard_operation == 'cut':
            try:
                shutil.move(self.clipoboard_path, os.path.join(self.current_directory.get(), os.path.basename(self.clipoboard_path)))
                self.update_files()
                messagebox.showinfo(title='Paste Successful', message='File moved successfully')
            except Exception as e:
                messagebox.showerror(title='Error', message=f'Error moving file: {str(e)}')
        else:
            messagebox.showerror(title='Invalid Operation', message='Invalid clipboard operation')


    
    def delete_file(self):
        if not self.selected_file: 
            return
        selected_file = self.selected_file
        file_path = os.path.join(self.current_directory.get(), selected_file)
        if messagebox.askyesnocancel(title='Delete the file?', message='Are you sure that you want to delte this file?', type=messagebox.WARNING):
            try:
                os.remove(file_path)
                self.update_files()
                messagebox.showinfo("Info", f"File '{selected_file}' deleted successfully")
            except Exception as e:
                messagebox.showerror("Error", f"Error deleting file: {str(e)}")
            
    def rename_file(self):
        if not self.selected_file: 
            return
        file_path = os.path.join(self.current_directory.get(), self.selected_file)
        new_name = simpledialog.askstring("Rename", f"Enter new name for '{self.selected_file}':", initialvalue=self.selected_file)
        if new_name:
            try:
                os.rename(file_path, os.path.join(self.current_directory.get(), new_name))
                self.update_files() 
                messagebox.showinfo("Info", f"File '{self.selected_file}' renamed to '{new_name}' successfully")
            except Exception as e:
                messagebox.showerror("Error", f"Error renaming file: {str(e)}")
                
    def go_back(self):
        self.current_directory.set(os.path.dirname(self.current_directory.get()))
        self.update_files()
        
    def go_up(self):
        if os.path.isfile((new_dir := os.path.join(self.current_directory.get(), self.selected_file))):
            return
        self.current_directory.set(new_dir)
        self.update_files()
        
    def create_new_dir(self):
        print(123)
        new_dir_name = simpledialog.askstring("New Folder", "Enter the name of the new folder:")
        if new_dir_name:
            new_dir_path = os.path.join(self.current_directory.get(), new_dir_name)
            if os.path.exists(new_dir_path):
                messagebox.showerror("Error", f"Folder '{new_dir_name}' already exists")
            else:
                try:
                    os.mkdir(new_dir_path)
                    self.update_files()
                    messagebox.showinfo("Info", f"New folder '{new_dir_name}' created successfully")
                except Exception as e:
                    messagebox.showerror("Error", f"Error creating folder: {str(e)}")


if __name__ == "__main__":
    app = FileExplorer()
    app.mainloop()
