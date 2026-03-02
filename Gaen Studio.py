import tkinter as tk
from tkinter import ttk, filedialog, messagebox, simpledialog
import subprocess
import os
import shutil
import re

class GaenStudio:
    def __init__(self, root):
        self.root = root
        self.root.title("Gaen Studio")
        self.root.geometry("1200x800")
        
        self.current_project_path = None
        self.active_file = None  

        self.syntax_rules = [
            (r"#c-ne|async", "#ff7b72"),  
            (r";", "#60dcbf"), 
            (r"@[a-zA-Z0-9_.]+", "#d2a8ff"), 
            (r"\.[a-zA-Z0-9_.]+\(", "#79c0ff"),
            (r'(".*?"|\'.*?\')', "#a5d6ff"),
            (r"\/\/.*", "#8b949e"),
            (r"\b(document|window|elements)\b", "#ffa657"),
            (r"\b(const|var|class|function|trigA|trigB)\b", "#6e64ff"),
            (r"\b(createElement|addTextNode)\b", "#16a71f"),
        ]

        self.paned = tk.PanedWindow(root, orient=tk.HORIZONTAL, bg="#1e1e1e", sashwidth=4)
        self.paned.pack(fill="both", expand=True)

        self.left_frame = tk.Frame(self.paned, bg="#1e1e1e")
        self.paned.add(self.left_frame, width=300)

        self.tree = ttk.Treeview(self.left_frame, show="tree")
        self.tree.pack(fill="both", expand=True)
        
        self.tree.bind("<Double-1>", self.on_double_click)
        self.tree.bind("<Button-3>", self.show_context_menu)

        self.right_frame = tk.Frame(self.paned, bg="#1e1e1e")
        self.paned.add(self.right_frame)

        self.editor = tk.Text(self.right_frame, bg="#1e1e1e", fg="#d4d4d4", 
                             insertbackground="white", font=("Consolas", 12), undo=True)
        self.editor.pack(fill="both", expand=True)

        for idx, (_, color) in enumerate(self.syntax_rules):
            self.editor.tag_configure(f"rule_{idx}", foreground=color)

        self.editor.bind("<KeyRelease>", lambda e: self.apply_highlighting())

        self.console = tk.Text(self.right_frame, height=10, bg="#000000", fg="#00ff00", font=("Consolas", 10))
        self.console.pack(fill="x")

        self.context_menu = tk.Menu(self.root, tearoff=0)
        self.context_menu.add_command(label="Yeni Dosya", command=self.create_new_file)
        self.context_menu.add_command(label="Yeni Klasör", command=self.create_new_folder)
        self.context_menu.add_separator()
        self.context_menu.add_command(label="Sil", command=self.delete_item)
        self.context_menu.add_command(label="Yeniden Adlandır", command=self.rename_item)

        self.setup_main_menu()

    def apply_highlighting(self):
        content = self.editor.get("1.0", tk.END)
        
        for idx in range(len(self.syntax_rules)):
            self.editor.tag_remove(f"rule_{idx}", "1.0", tk.END)

        for idx, (pattern, _) in enumerate(self.syntax_rules):
            for match in re.finditer(pattern, content):
                start = f"1.0 + {match.start()} chars"
                end = f"1.0 + {match.end()} chars"
                self.editor.tag_add(f"rule_{idx}", start, end)

    def setup_main_menu(self):
        m = tk.Menu(self.root)
        file_m = tk.Menu(m, tearoff=0)
        file_m.add_command(label="Klasör Aç", command=self.open_dir)
        file_m.add_command(label="Kaydet (Ctrl+S)", command=self.save_file)
        m.add_cascade(label="Proje", menu=file_m)
        
        built_m = tk.Menu(m, tearoff=0)
        built_m.add_command(label="EYC Derle (F5)", command=self.compile_eyc)
        m.add_cascade(label="Built", menu=built_m)
        
        self.root.config(menu=m)
        self.root.bind("<Control-s>", lambda e: self.save_file())
        self.root.bind("<F5>", lambda e: self.compile_eyc())

    def open_dir(self):
        path = filedialog.askdirectory()
        if path:
            self.current_project_path = path
            self.refresh_tree()

    def refresh_tree(self):
        self.tree.delete(*self.tree.get_children())
        if self.current_project_path:
            self._load_tree_nodes("", self.current_project_path)

    def _load_tree_nodes(self, parent, path):
        try:
            items = os.listdir(path)
            for item in items:
                abspath = os.path.join(path, item)
                is_dir = os.path.isdir(abspath)
                node = self.tree.insert(parent, "end", text=item, values=[abspath, is_dir])
                if is_dir:
                    self._load_tree_nodes(node, abspath)
        except Exception as e:
            self.log(f"Hata: {e}")

    def on_double_click(self, event):
        item_id = self.tree.focus()
        if not item_id: return
        path, is_dir = self.tree.item(item_id, "values")
        if is_dir == '0' or is_dir == 'False':
            self.active_file = path
            try:
                with open(path, "r", encoding="utf-8") as f:
                    content = f.read()
                    self.editor.delete(1.0, tk.END)
                    self.editor.insert(tk.END, content)
                self.apply_highlighting()
                self.log(f"Açıldı: {os.path.basename(path)}")
                self.root.title(f"Gaen Studio - {os.path.basename(path)}")
            except Exception as e:
                messagebox.showerror("Hata", f"Dosya okunamadı: {e}")

    def create_new_file(self):
        if not self.current_project_path: return
        name = simpledialog.askstring("Yeni Dosya", "Dosya adı ve uzantısı:")
        if name:
            selected = self.tree.focus()
            base_path = self.current_project_path
            if selected:
                s_path, s_is_dir = self.tree.item(selected, "values")
                base_path = s_path if s_is_dir == '1' or s_is_dir == 'True' else os.path.dirname(s_path)
            full_path = os.path.join(base_path, name)
            open(full_path, "w", encoding="utf-8").close()
            self.refresh_tree()

    def create_new_folder(self):
        if not self.current_project_path: return
        name = simpledialog.askstring("Yeni Klasör", "Klasör adı:")
        if name:
            selected = self.tree.focus()
            base_path = self.current_project_path
            if selected:
                s_path, s_is_dir = self.tree.item(selected, "values")
                base_path = s_path if s_is_dir == '1' or s_is_dir == 'True' else os.path.dirname(s_path)
            os.makedirs(os.path.join(base_path, name), exist_ok=True)
            self.refresh_tree()

    def show_context_menu(self, event):
        item = self.tree.identify_row(event.y)
        if item:
            self.tree.selection_set(item)
            self.context_menu.post(event.x_root, event.y_root)

    def save_file(self):
        if self.active_file:
            content = self.editor.get(1.0, tk.END)
            with open(self.active_file, "w", encoding="utf-8") as f:
                f.write(content)
            self.log("Kaydedildi.")

    def compile_eyc(self):
        if self.active_file and self.active_file.endswith(".eyc"):
            self.save_file()
            res = subprocess.run(["eyc", "-c", self.active_file], capture_output=True, text=True, shell=True)
            self.log(res.stdout if res.stdout else f"{os.path.basename(self.active_file)} derlendi.")
            if res.stderr: self.log(f"HATA: {res.stderr}")
            self.refresh_tree()

    def delete_item(self):
        item_id = self.tree.focus()
        if not item_id: return
        path, is_dir = self.tree.item(item_id, "values")
        if messagebox.askyesno("Sil", "Emin misiniz?"):
            if is_dir == '1' or is_dir == 'True': shutil.rmtree(path)
            else: os.remove(path)
            self.refresh_tree()

    def rename_item(self):
        item_id = self.tree.focus()
        if not item_id: return
        old_path, _ = self.tree.item(item_id, "values")
        new_name = simpledialog.askstring("Ad Değiştir", "Yeni ad:", initialvalue=os.path.basename(old_path))
        if new_name:
            new_path = os.path.join(os.path.dirname(old_path), new_name)
            os.rename(old_path, new_path)
            self.refresh_tree()

    def log(self, msg):
        self.console.insert(tk.END, f">> {msg}\n")
        self.console.see(tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = GaenStudio(root)
    root.mainloop()