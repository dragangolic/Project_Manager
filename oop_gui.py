from abc import ABC, abstractmethod
import tkinter as tk
from tkinter import ttk
from tkinter import font as tkFont
import temp_query as query

class AbstractTab(ABC):
    def __init__(self, parent, button, tab_canvas):
        self.notebook = parent
        self.frame = tk.Frame(parent, bg="#241E2B")
        self.button = button
        self.tab = tab_canvas
        self.button.bind("<Button-1>", lambda event: self.select_tab())
        self.width = 1000
        self.frame.bind("<Configure>", lambda event: self.update_tab() if self.notebook.select() == str(self.frame) else None)

    def select_tab(self):
        if str(self.frame) == self.notebook.select():
            return
        self.notebook.select(self.frame)
        x1, x2 = self.button.winfo_x(), self.button.winfo_x() + self.button.winfo_width()
        
        # Calculate the actual visible region of the canvas in terms of content coordinates
        visible_x1 = self.tab.xview()[0] * self.tab.winfo_width()
        visible_x2 = self.tab.xview()[1] * self.tab.winfo_width()
        
        # Check if the button's x-coordinates are outside the visible region
        if x1 < visible_x1 or x2 > visible_x2:
            self.tab.xview_moveto(x1 / self.tab.winfo_width())
        
        self.tab.delete("selected")
        self.tab.create_line(x1, 45, x2, 45, fill="blue", width=4, tag='selected')

    def create_rounded_rectangle(self, canvas, x1, y1, x2, y2, corner_radius, **kwargs):
        canvas.create_polygon(
            x1 + corner_radius, y1,
            x1 + corner_radius, y1,
            x2 - corner_radius, y1,
            x2 - corner_radius, y1,
            x2, y1,
            x2, y1 + corner_radius,
            x2, y1 + corner_radius,
            x2, y2 - corner_radius,
            x2, y2 - corner_radius,
            x2, y2,
            x2 - corner_radius, y2,
            x2 - corner_radius, y2,
            x1 + corner_radius, y2,
            x1 + corner_radius, y2,
            x1, y2,
            x1, y2 - corner_radius,
            x1, y2 - corner_radius,
            x1, y1 + corner_radius,
            x1, y1 + corner_radius,
            x1, y1,
            x1 + corner_radius, y1,
            smooth=True,
            **kwargs
        )

    def wrap_text(self, text, font, max_width, max_lines = None):
        lines = []
        words = text.split()
        
        while words:
            line = ''
            while words and font.measure(line + words[0]) <= max_width:
                line += (words.pop(0) + ' ')
            lines.append(line)
        if max_lines != None and len(lines) > max_lines:
            lines = lines[0:max_lines]
            lines[max_lines-1] = lines[max_lines-1][0:-1]
            lines[max_lines-1] += "..."
        if len(lines) == 1: lines = lines[0]
        return lines

    def get_longest(self, texts, font):
        longest_length = 0
        for text in texts:
            text_width = font.measure(text)
            longest_length = max(longest_length, text_width)
        return longest_length
    
    def on_mousewheel(self,event, canvas, direction = 'y'):
        """
        This allows the canvas to be scrolled through
        """
        canvas.focus_set()
        if direction == 'y':
            canvas.yview_scroll(-1*(event.delta//120), "units")
        else:
            canvas.xview_scroll(-1*(event.delta//120), "units")
    
    def on_var_change(self, var):
        #print(var.get())
        pass

    @abstractmethod
    def update_tab(self):
        pass

class ExploreTab(AbstractTab):
    def __init__(self, parent, button, tab_canvas):
        super().__init__(parent, button, tab_canvas)
        self.selected = None

        canvas = tk.Canvas(self.frame, bg='#241E2B', bd=0, highlightthickness=0, width=1000)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Create a top frame to contain the 'avail' label and 'entry' widget
        top_frame = tk.Frame(canvas, bg='#241E2B')
        top_frame.pack(pady=20, fill='x')  # pad in the y direction to provide spacing

        avail = tk.Label(top_frame, text="Available Projects", bg='#241E2B', fg='white', font=('Arial', 18, 'bold'))
        avail.pack(side='left', padx=20)

        # Create a StringVar for your entry
        entry_var = tk.StringVar()
        entry_var.set("🔍 Search For Projects")  # initial value

        # Set a trace on the StringVar
        entry_var.trace_add("write", lambda *args: self.on_var_change(entry_var))

        self.entry = tk.Entry(top_frame, textvariable=entry_var, fg='white', font=('Arial', 12), bg="#282828", width=40, bd=0, highlightbackground='#18141D', highlightthickness=3)
        self.entry.pack(side='left', padx=(500 , 10))

        self.main_canvas = tk.Canvas(canvas, bg='#241E2B', bd=0, highlightthickness=0, width=1000)
        self.main_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(20, 0))
        self.display_all_proj()
        self.main_canvas.bind("<MouseWheel>", lambda event, canvas=self.main_canvas: self.on_mousewheel(event, canvas))
        self.main_canvas.bind("<Button-1>", lambda event: self.click(event))
        self.entry.bind("<FocusIn>", lambda event: self.remove_placeholder(self.entry, "🔍 Search For Projects"))
        self.entry.bind("<FocusOut>", lambda event: self.restore_placeholder(self.entry, "🔍 Search For Projects"))

    def update_tab(self):
        if self.width != self.frame.winfo_width():
            self.width = self.frame.winfo_width()
            self.entry.pack(side='left', padx=(self.width-500 , 10))
            self.display_all_proj()

    def display_project(self, project, y= 0):
        """
        This Method Creates a Project that is well visualized and shows all important pieces of data for the Project

        param: canvas: This is a tk object that this project should be placed into
        type: tk.Canvas

        param: project: This is the name of the project but might soon be changed to Proj_id
        type: String

        param: y: this is the y location that this project display should be placed at
        type: int
        """
        #Making project name into a single tagable name
        project = project.replace(" ", "_")

        #Determining how much space to give on the right side
        font = tkFont.Font(font=("Arial", 12, 'bold'))
        right_offset = self.get_longest(["Contributors: " + query.project_info()[3], "Project Age: " + query.project_info()[4], "Completed Tasks: " + query.project_info()[2]],font)+50

        #Creating background for the project
        self.create_rounded_rectangle(self.main_canvas, 10, y, self.width-40, y+90, 20, outline= '#FFFFFF', fill='#18141C', tag=project)
        y+= 20

        #font for measurement
        font = tkFont.Font(font=("Arial", 18, 'bold', 'underline'))
        #Writing Project Name
        self.main_canvas.create_text(20, y, text = project.replace("_", " "), anchor='w', font=font, tag=[project, 'header'], fill='#69D7FF')
        #Writing Incomplete Tasks
        self.main_canvas.create_text(font.measure(project) + 50, y+5, text = "Incomplete Tasks: " + query.project_info()[1], anchor='w', font=("Arial", 12, 'bold'), tag=project, fill='#69D7FF')
        #Writing Amount of Contributors
        self.main_canvas.create_text(self.width-right_offset, y, text = "Contributors: " + query.project_info()[3], anchor='w', font=("Arial", 12, 'bold'), tag=project, fill = '#69D7FF')
        #Writing the Projects Age
        self.main_canvas.create_text(self.width-right_offset, y+25, text = "Project Age: " + query.project_info()[4], anchor='w', font=("Arial", 12, 'bold'), tag=project, fill = '#69D7FF')
        #Writing amount of tasks completed
        self.main_canvas.create_text(self.width-right_offset, y+50, text = "Completed Tasks: " + query.project_info()[2], anchor='w', font=("Arial", 12, 'bold'), tag=project, fill = '#69D7FF')

        #shifting down to write the description
        y+= 32
        #Wrapping the text for the description into 2 lines
        wrapped_text = self.wrap_text(query.project_info()[0], tkFont.Font(font=("Arial", 12)), self.width-right_offset -50, 2)
        #Looping to write it down
        for line in wrapped_text:
            self.main_canvas.create_text(20, y, text=line, anchor='w', font=("Arial", 12), tag=project, fill = '#1193C2')
            y += 20
        return y

    def display_task(self, canvas, task, y =0):
        """
        This function is meant to display a singlar task

        param: canvas: This determines what canvas to draw onto
        type: tk.Canvas

        param: tasks: This is the Primary key of the task from the database
        type: int

        param: y: This is determines the y axis location to draw onto
        type: int

        return: y: This is the bottom of the task so it can easily be passed on and not be drawn onto
        type: int    
        """
        #Clearing this task so just in case it doesnt ever have 2 versions
        canvas.delete("task_"+str(task))

        font = tkFont.Font(font=("Arial", 10, 'bold')) #most used font

        #Determining how much space to give on the right side
        right_offset = self.get_longest(["Assigned to: " + query.task_info(task)[4], "Deadline: " +  query.task_info(task)[3]],font) +60

        #Determining how much space there is to write the required skills
        skill_space = self.width - right_offset - tkFont.Font(font=("Arial", 12, 'bold')).measure(query.task_info(task)[0]) -100
        skill = self.wrap_text("Required Skills: " + query.task_info(task)[2], font, skill_space, 1)

        #Creating the Task background
        self.create_rounded_rectangle(canvas, 20, y, self.width-50, y+50, 15, outline= '#FFFFFF', fill='#18141C', tag="task_"+str(task))
        
        y+= 15 # Moving down to the first line of text
        #Writing Task Name
        canvas.create_text(30, y, text = query.task_info(task)[0], anchor='w', font=("Arial", 12, 'bold'), tag="task_"+str(task), fill = '#FFFFFF')
        #Writing Assigned User 
        canvas.create_text(self.width-right_offset, y, text = "Assigned to: " + query.task_info(task)[4], anchor='w', font=font, tag="task_"+str(task), fill = '#FFFFFF')
        #Writng the Required Skills
        canvas.create_text(tkFont.Font(font=("Arial", 12, 'bold')).measure(query.task_info(task)[0])+ 50, y, text = skill, anchor='w', font=font, tag="task_"+str(task), fill = '#FFFFFF')

        y+= 20 #Moving down to second line of text
        #Wrinting down the task description
        canvas.create_text(30, y, text = self.wrap_text(query.task_info(task)[1], font, self.width-right_offset -140, 1), anchor='w', font=font, tag="task_"+str(task), fill = '#FFFFFF')
        #Writing the deadline down
        canvas.create_text(self.width-right_offset, y, text = "Deadline: " +  query.task_info(task)[3], anchor='w', font=font, tag="task_"+str(task), fill = '#FFFFFF')

        y+= 15 #moving the y to the bottom of the task section 
        return y

    def display_proj_tasks(self, project, y = 0):
        #This allows the tags to work well while allowing users to have spaces in their project names
        project = project.replace(" ", "_")

        #cuts the tasks amount down to a max of 4
        tasks = query.project_tasks(project)
        if len(tasks) > 4: tasks = tasks[0:4]

        #Creates the "Dropdown"
        self.create_rounded_rectangle(self.main_canvas, 10, y, self.width-40, y + 95 + len(tasks)*55, 20, outline= '#FFFFFF', fill='#3B3147', tag="taskdrop")

        #Displays the Project
        y = self.display_project(project, y)
        spacing = 5
        #Display the Tasks
        for task in tasks:
            y = self.display_task(self.main_canvas, task, y +spacing)
        y += 5
        return y

    def display_all_proj(self, y = 0):
        """
        This function displays all projects and whichever projects tasks that are selected
        """
        #This will be changed to a function from query.py
        self.main_canvas.delete('all')
        projects = query.get_projects()
        for project in projects:
            if project == self.selected:
                y = self.display_proj_tasks(project, y+10)
            else:
                y = self.display_project(project, y+10)
        
        #After creating the projects making sure the scrolling region is set right
        self.main_canvas.config(scrollregion=self.main_canvas.bbox(tk.ALL))

    def click(self, event):
        # Get the current item under the mouse pointer
        self.main_canvas.focus_set()
        current_item = self.main_canvas.find_withtag(tk.CURRENT)
        
        if not current_item:
            return  # No item was clicked
        
        # Retrieve all tags of the clicked item
        tags = self.main_canvas.gettags(current_item[0])
        
        # Reconstruct the name from the tags
        name = " ".join(tag for tag in tags if tag != "current")
        if name == "taskdrop": 
            pass
        elif name.startswith("task_"):
            pass
        else:
            name = name.replace("_", " ")
            self.main_canvas.delete('all')
            if name == self.selected:
                self.selected = None
            else:
                self.selected = name.replace("_", " ")
            self.display_all_proj()
        #elif name.endswith("header"):
        #    print("Open Project Tab")

    def remove_placeholder(self, entry, placeholder):
        if entry.get() == placeholder:
            entry.delete(0, tk.END)

    def restore_placeholder(self, entry, placeholder):
        if entry.get().strip() == "":
            entry.insert(0, placeholder)

class LoginTab(AbstractTab):
    def update_tab(self):
        return super().update_tab()

class ProjectManager:
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry('1000x600')
        self.root.minsize(1000,600)
        self.root.title("Project Manager")
        self.root.iconbitmap('GUI_Design/Project_Manager.ico')
        self.root.configure(bg="#2C2634")
        self.root.bind("<Configure>", lambda event: self.update())

        style = ttk.Style()
        style.theme_use('default')
        style.configure('TNotebook', background="#2C2634", borderwidth=0, tabmargins=[0, 0, -1000, 0])
        style.configure('TNotebook.Tab', background="#2C2634", foreground="white", padding=0)
        style.layout('TNotebook.Tab', [])

        self.width = 1000
        
        self.create_header()

        self.notebook = ttk.Notebook(self.root)

        self.explore = ExploreTab(self.notebook, self.create_tab("Explore"), self.tab_canvas)
        self.notebook.add(self.explore.frame, text="Explore")
        
        self.login = LoginTab(self.notebook, self.create_tab("Login"), self.tab_canvas)
        self.notebook.add(self.login.frame, text="Login")

        self.notebook.pack(fill=tk.BOTH, expand=True)

        self.root.mainloop()

    def update(self):
        if self.width != self.root.winfo_width():
            self.width = self.root.winfo_width()
            self.update_scrolling()

    def create_header(self):
        header = tk.Canvas(self.root, bg='#18141D', bd=0, highlightthickness=0, width=1000)
        header.pack(side=tk.TOP, fill=tk.BOTH)

        menu_button = tk.Button(
            header,
            text="☰",
            bg='#18141D',
            activebackground='#2C2634',
            fg='white',
            font=('Arial', 18, 'bold'),
            borderwidth=0,
            highlightthickness=0,
        )
        menu_button.pack(side='right', padx=10, pady=0)

        welcome = tk.Label(header, text="Project Manager", bg='#18141D', fg='white', font=('Arial', 0, 'bold'))
        welcome.pack(side='left', pady =(5, 5), padx= (20,0))

        self.tab_canvas = tk.Canvas(header, bg='#18141D', highlightthickness=0, height=45)
        self.tab_canvas.pack(side='left', fill=tk.X, expand=True)

        self.tab_frame = tk.Frame(self.tab_canvas, bg='#18141D')
        self.tab_canvas.create_window((0,0), window=self.tab_frame, anchor='nw')
        self.bind_mousewheel(self.tab_frame, "<MouseWheel>", self.tab_canvas)
    
    def create_tab(self, label):
        button = tk.Button(
            self.tab_frame,
            text=label,
            bg='#18141D',
            activebackground='#2C2634',  
            fg='#5C596D',
            font=('Arial', 12, 'bold'),
            borderwidth=0,
            highlightthickness=0,
            width = 10 
        )
        button.pack(anchor='w', pady=(10,5), padx=10, side='left')
        self.update_scrolling()
        return button

    def on_mousewheel(self, event, canvas, direction = 'y'):
        """
        This allows the canvas to be scrolled through
        """
        if direction == 'y':
            canvas.yview_scroll(-1*(event.delta//120), "units")
        else:
            canvas.xview_scroll(-1*(event.delta//120), "units")
    
    def unbind_mousewheel_from_children(self, widget, event):
        """Recursively unbind an event from a widget and its children."""
        widget.unbind(event)
        for child in widget.winfo_children():
            self.unbind_mousewheel_from_children(child, event)

    def bind_mousewheel(self, widget, event, canvas):
        widget.bind(event, lambda e, canvas=canvas: self.on_mousewheel(e, canvas, 'x'))
        for child in widget.winfo_children():
            self.bind_mousewheel(child, event, canvas)

    def update_scrolling(self):
        # Force update of pending geometry management tasks
        self.tab_canvas.update_idletasks()
        
        # Calculate the total width of the buttons
        total_width = sum(btn.winfo_width() for btn in self.tab_frame.winfo_children())
        
        # Compare to the width of the tab_canvas
        canvas_width = self.tab_canvas.winfo_width()
        if canvas_width == 1: canvas_width = 757
        
        # Enable or disable scrolling based on the comparison
        if total_width <= canvas_width:
            self.tab_canvas.config(scrollregion=())
            # Unbind the MouseWheel event from tab_canvas and all its children
            self.unbind_mousewheel_from_children(self.tab_canvas, "<MouseWheel>")
        else:
            self.tab_canvas.config(scrollregion=self.tab_canvas.bbox('all'))
            self.bind_mousewheel(self.tab_frame, "<MouseWheel>", self.tab_canvas)

app = ProjectManager()