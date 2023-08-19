import tkinter as tk
from tkinter import ttk
from tkinter import font as tkFont

prev_width = 0
selected = None
canvas = None
selected_tab = "Login"
explore = None
canvas = None
main_canvas = None
top_frame = None
entry = None
header_canvas = None

def create_rounded_rectangle(canvas, x1, y1, x2, y2, corner_radius, **kwargs):
    # Draw the main rectangle
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

def main_canvas_click(event):
    global selected
    # Get the current item under the mouse pointer
    main_canvas.focus_set()
    current_item = main_canvas.find_withtag(tk.CURRENT)
    
    if not current_item:
        return  # No item was clicked
    
    # Retrieve all tags of the clicked item
    tags = main_canvas.gettags(current_item[0])
    
    # Reconstruct the name from the tags
    name = " ".join(tag for tag in tags if tag != "current")
    if name == "taskdrop": 
        pass
    elif name.startswith("task_"):
        pass
    else:
        name = name.replace("_", " ")
        main_canvas.delete('all')
        if name == selected:
            selected = None
        else:
            selected = name.replace("_", " ")
        display_all_proj(main_canvas, 50)
    #elif name.endswith("header"):
    #    print("Open Project Tab")

def get_all_tags(canvas):
    all_tags = set()
    for item in canvas.find_all():
        tags = canvas.gettags(item)
        for tag in tags:
            all_tags.add(tag)
    return all_tags

def project_info():
    """
    TEMP FUNCTION REAL will be in query.py
    The data that is returned is 
    project_info:
    [0] : Project description
    [1] : Incompleted Tasks
    [2] : Completed Tasks
    [3] : Contributors
    [4] : Age in days
    """
    project_info = [
         "This project delves deeply into the nuances of project management and exploration. Designed to not just manage tasks and milestones, it also acts as a comprehensive database visualizer. Users can effortlessly browse through various projects, understanding their core objectives and current statuses. This platform encourages collaboration and knowledge-sharing, serving as a beacon for those searching for projects where their skills and expertise can make a tangible difference. We believe that collective wisdom can push the boundaries of what's possible. Hence, we warmly invite individuals from all backgrounds and expertise levels to contribute. By collaborating, we can drive innovation, ensure the completion of projects, and bring about transformative change.",
         "5", "2", "3", "5"
    ]
    return project_info

def project_tasks(project):
    """
    TEMP FUNCTION REAL will be in query.py
    This will return the task ids that are apart of the project
    """
    task_ids = [5,4,3,2,1]
    return task_ids

def task_info(id):
    """
    TEMP FUNCTION REAL will be in query.py
    This gives task info based on the id
    """
    task_data = {
    1: [
        "Define Project Scope and Objectives",
        "Clearly outline the scope and objectives of the 'Project Manager' project. This includes identifying key features, target audience, and desired outcomes.",
        "Project management, Requirements gathering, Communication",
        "September 5th, 2023",
        "Emily J."
    ],
    2: [
        "Develop User Interface Mockups",
        "Create detailed mockups for the project's user interface. These mockups should reflect the database visualizer's layout and user interaction flow.",
        "UI/UX design, Wireframing, Creativity",
        "September 8th, 2023",
        "Alex C."
    ],
    3: [
        "Implement Backend Database Integration",
        "Integrate the backend database system into the project. Ensure smooth data retrieval and manipulation, considering scalability and security.",
        "Database management, Backend development, API integration",
        "September 12th, 2023",
        "Michael R."
    ],
    4: [
        "Implement User Authentication",
        "Develop a secure user authentication system for the project, allowing contributors to log in, manage their profiles, and access relevant project information.",
        "Security, Authentication protocols, Backend development",
        "September 10th, 2023",
        "Sarah P."
    ],
    5: [
        "Test and Bug Fixing",
        "Conduct thorough testing of the project, identifying and addressing any bugs, glitches, or inconsistencies. Ensure a smooth user experience before the official launch.",
        "Quality assurance, Troubleshooting, Attention to detail",
        "September 14th, 2023",
        "David W."
    ]
    }
    return task_data[id] 

def wrap_text(text, font, max_width, max_lines = None):
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

def get_longest(texts, font):
    longest_length = 0
    for text in texts:
        text_width = font.measure(text)
        longest_length = max(longest_length, text_width)
    return longest_length

def display_project(canvas, project, y= 0):
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
    #Making sure there is only one instance of this project
    canvas.delete(project)

    #Determining how much space to give on the right side
    font = tkFont.Font(font=("Arial", 12, 'bold'))
    right_offset = get_longest(["Contributors: " + project_info()[3], "Project Age: " + project_info()[4], "Completed Tasks: " + project_info()[2]],font)+50

    #Creating background for the project
    create_rounded_rectangle(canvas, 10, y, root.winfo_width()-40, y+90, 20, outline= '#FFFFFF', fill='#18141C', tag=project)
    y+= 20

    #font for measurement
    font = tkFont.Font(font=("Arial", 18, 'bold', 'underline'))
    #Writing Project Name
    canvas.create_text(20, y, text = project.replace("_", " "), anchor='w', font=font, tag=[project, 'header'], fill='#69D7FF')
    #Writing Incomplete Tasks
    canvas.create_text(font.measure(project) + 50, y+5, text = "Incomplete Tasks: " + project_info()[1], anchor='w', font=("Arial", 12, 'bold'), tag=project, fill='#69D7FF')
    #Writing Amount of Contributors
    canvas.create_text(root.winfo_width()-right_offset, y, text = "Contributors: " + project_info()[3], anchor='w', font=("Arial", 12, 'bold'), tag=project, fill = '#69D7FF')
    #Writing the Projects Age
    canvas.create_text(root.winfo_width()-right_offset, y+25, text = "Project Age: " + project_info()[4], anchor='w', font=("Arial", 12, 'bold'), tag=project, fill = '#69D7FF')
    #Writing amount of tasks completed
    canvas.create_text(root.winfo_width()-right_offset, y+50, text = "Completed Tasks: " + project_info()[2], anchor='w', font=("Arial", 12, 'bold'), tag=project, fill = '#69D7FF')

    #shifting down to write the description
    y+= 32
    #Wrapping the text for the description into 2 lines
    wrapped_text = wrap_text(project_info()[0], tkFont.Font(font=("Arial", 12)), root.winfo_width()-right_offset -50, 2)
    #Looping to write it down
    for line in wrapped_text:
        canvas.create_text(20, y, text=line, anchor='w', font=("Arial", 12), tag=project, fill = '#1193C2')
        y += 20
    return y

def display_task(canvas, task, y =0):
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
    right_offset = get_longest(["Assigned to: " + task_info(task)[4], "Deadline: " +  task_info(task)[3]],font) +60

    #Determining how much space there is to write the required skills
    skill_space = root.winfo_width() - right_offset - tkFont.Font(font=("Arial", 12, 'bold')).measure(task_info(task)[0]) -100
    skill = wrap_text("Required Skills: " + task_info(task)[2], font, skill_space, 1)

    #Creating the Task background
    create_rounded_rectangle(canvas, 20, y, root.winfo_width()-50, y+50, 15, outline= '#FFFFFF', fill='#18141C', tag="task_"+str(task))
    
    y+= 15 # Moving down to the first line of text
    #Writing Task Name
    canvas.create_text(30, y, text = task_info(task)[0], anchor='w', font=("Arial", 12, 'bold'), tag="task_"+str(task), fill = '#FFFFFF')
    #Writing Assigned User 
    canvas.create_text(root.winfo_width()-right_offset, y, text = "Assigned to: " + task_info(task)[4], anchor='w', font=font, tag="task_"+str(task), fill = '#FFFFFF')
    #Writng the Required Skills
    canvas.create_text(tkFont.Font(font=("Arial", 12, 'bold')).measure(task_info(task)[0])+ 50, y, text = skill, anchor='w', font=font, tag="task_"+str(task), fill = '#FFFFFF')

    y+= 20 #Moving down to second line of text
    #Wrinting down the task description
    canvas.create_text(30, y, text = wrap_text(task_info(task)[1], font, root.winfo_width()-right_offset -140, 1), anchor='w', font=font, tag="task_"+str(task), fill = '#FFFFFF')
    #Writing the deadline down
    canvas.create_text(root.winfo_width()-right_offset, y, text = "Deadline: " +  task_info(task)[3], anchor='w', font=font, tag="task_"+str(task), fill = '#FFFFFF')

    y+= 15 #moving the y to the bottom of the task section 
    return y

def display_proj_tasks(canvas, project, y = 0):
    #This allows the tags to work well while allowing users to have spaces in their project names
    project = project.replace(" ", "_")

    #makes sure there is never another taskdrop down
    canvas.delete("taskdrop")

    #cuts the tasks amount down to a max of 4
    tasks = project_tasks(project)
    if len(tasks) > 4: tasks = tasks[0:4]

    #Creates the "Dropdown"
    create_rounded_rectangle(canvas, 10, y, root.winfo_width()-40, y + 95 + len(tasks)*55, 20, outline= '#FFFFFF', fill='#3B3147', tag="taskdrop")

    #Displays the Project
    y = display_project(canvas, project, y)
    spacing = 5
    #Display the Tasks
    for task in tasks:
        y = display_task(canvas, task, y +spacing)
    y += 5
    return y

def display_all_proj(canvas, y = 0):
    """
    This function displays all projects and whichever projects tasks that are selected
    """
    global selected
    #This will be changed to a function from query.py 
    projects = ["Project Manager", "Another Project", "1ewqe", "2weq", "dsa", "dsada", "aomethign"]
    for project in projects:
        if project == selected:
            y = display_proj_tasks(canvas, project, y+10)
        else:
            y = display_project(canvas, project, y+10)
    
    #After creating the projects making sure the scrolling region is set right
    main_canvas.config(scrollregion=main_canvas.bbox(tk.ALL))

def update_scale():
    """
    This is callled on <Configure> to make sure all components are of the right size to fit the screen
    """
    global prev_width
    if root.winfo_width() != prev_width:
        update_scrolling()
        tab_canvas.config(width=root.winfo_width()-500)
        prev_width = root.winfo_width()
        if selected_tab == 'Login': 
            canvas.config(width=root.winfo_width())
            login()
        elif selected_tab == 'Explore':
            entry.pack(side='left', padx=(prev_width-500, 10))
            main_canvas.config(width=root.winfo_width())
            display_all_proj(main_canvas)

def on_mousewheel(event, canvas, direction = 'y'):
    """
    This allows the canvas to be scrolled through
    """
    if direction == 'y':
        canvas.yview_scroll(-1*(event.delta//120), "units")
    else:
        canvas.xview_scroll(-1*(event.delta//120), "units")
        
def button_selected(button):
    """
    This allows the function to have a visual of which button is selected
    """
    x1, x2 = button.winfo_x(), button.winfo_x() + button.winfo_width()
    
    # Get the current x-scroll position of the canvas
    scroll_x1, scroll_x2 = tab_canvas.xview()
    canvas_width = tab_canvas.winfo_width()
    
    # Calculate the actual visible region of the canvas in terms of content coordinates
    visible_x1 = scroll_x1 * canvas_width
    visible_x2 = scroll_x2 * canvas_width
    
    # Check if the button's x-coordinates are outside the visible region
    if x1 < visible_x1 or x2 > visible_x2:
        tab_canvas.xview_moveto(x1 / canvas_width)
    
    if x1 == 0 and x2 == 1: 
        tab_canvas.create_line(563, 45, 667, 45, fill="blue", width=4, tag='selected')
    else:
        tab_canvas.delete("selected")
        tab_canvas.create_line(x1, 45, x2, 45, fill="blue", width=4, tag='selected')



def header_buttons():
    global explore
    explore = tk.Button(
        tab_frame,
        text="Explore",
        bg='#18141D',
        activebackground='#2C2634',  
        fg='#5C596D',
        font=('Arial', 12, 'bold'),
        borderwidth=0,
        highlightthickness=0,
        width = 10 
    )
    explore.bind("<Button-1>", lambda event: explore_canvas())

    u_projects = tk.Button(
        tab_frame,
        text="Your Projects",
        bg='#18141D',
        activebackground='#2C2634',
        fg='#5C596D',
        font=('Arial', 12, 'bold'),
        borderwidth=0,
        highlightthickness=0,
        width = 10 
    )

    u_tasks = tk.Button(
        tab_frame,
        text="Your Tasks",
        bg='#18141D',
        activebackground='#2C2634', 
        fg='#5C596D',
        font=('Arial', 12, 'bold'),
        borderwidth=0,
        highlightthickness=0,
        width = 10 
    )
    explore.pack(anchor='w', pady=(10,5), padx=10, side='left')
    u_projects.pack(anchor='w', pady=(10,5), padx=10, side='left')
    u_tasks.pack(anchor='w', pady=(10,5), padx=10, side='left')    

    u_projects.bind("<Button-1>", lambda event: button_selected(u_projects))
    u_tasks.bind("<Button-1>", lambda event: button_selected(u_tasks))
    bind_mousewheel(tab_frame, "<MouseWheel>", tab_canvas)

def unbind_mousewheel_from_children(widget, event):
    """Recursively unbind an event from a widget and its children."""
    widget.unbind(event)
    for child in widget.winfo_children():
        unbind_mousewheel_from_children(child, event)

def update_scrolling():
    # Force update of pending geometry management tasks
    tab_canvas.update_idletasks()
    
    # Calculate the total width of the buttons
    total_width = sum(btn.winfo_width() for btn in tab_frame.winfo_children())
    
    # Compare to the width of the tab_canvas
    canvas_width = tab_canvas.winfo_width()
    if canvas_width == 1: canvas_width = 757
    
    # Enable or disable scrolling based on the comparison
    if total_width <= canvas_width:
        tab_canvas.config(scrollregion=())
        # Unbind the MouseWheel event from tab_canvas and all its children
        unbind_mousewheel_from_children(tab_canvas, "<MouseWheel>")
    else:
        tab_canvas.config(scrollregion=tab_canvas.bbox('all'))
        bind_mousewheel(tab_frame, "<MouseWheel>", tab_canvas)


def remove_placeholder(event):
    if entry.get() == "🔍 Search For Projects":
        entry.delete(0, tk.END)
        entry.config(fg='white')  # Change the text color to black

def restore_placeholder(event):
    if entry.get().strip() == "":
        entry.insert(0, "🔍 Search For Projects")
        entry.config(fg='white')  # Change the text color to gray

def on_var_change(*args):
    print(entry_var.get())

def authenticate(username, password):
    if username == "admin" and password == "password":
        return True
    return False

def login():
    global selected_tab, tab_frame, canvas
    if not hasattr(tab_frame, "Login"):
        tab_frame.Login = tk.Button(
            tab_frame,
            text="Login",
            bg='#18141D',
            activebackground='#2C2634', 
            fg='#5C596D',
            font=('Arial', 12, 'bold'),
            borderwidth=0,
            highlightthickness=0,
            width = 10 
        )
        tab_frame.Login.pack(anchor='w', pady=(10,5), padx=10, side='left')

    selected_tab = "Login"
    canvas.pack_forget()
    canvas = tk.Canvas(root, bg='#241E2B', bd=0, highlightthickness=0, width=1000)
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    tab_frame.Login.bind("<Button-1>", lambda event: login() if selected_tab != "Login" else None)

    create_rounded_rectangle(canvas, prev_width/2 -250, 20, prev_width/2 +250, root.winfo_height()-200, 25, fill= '#241E2B', outline = '#5C596D', width= 4)
    
    fail_label = tk.Label(canvas, text="", bg='#241E2B', fg='red', font=('Arial', 12))
    fail_label.place(rely= 0.3, x= prev_width/2 -50)

    # Sign in message
    sign = tk.Label(canvas, text="Sign In", bg='#241E2B', fg='white', font=('Arial', 18, 'bold'))
    sign.place(relx = .5, rely=0.25, anchor='c')

    # Username label & entry
    username_label = tk.Label(canvas, text="Username:", bg='#241E2B', fg='white')
    username_label.place(x= prev_width/2 -150, rely=0.4, anchor='e')

    username_entry = tk.Entry(canvas, 
                            fg='white', 
                            font=('Arial', 12), 
                            bg="#282828", 
                            width=40, 
                            bd=0, 
                            highlightbackground='#241E2B', 
                            highlightthickness=3)
    username_entry.place(x= prev_width/2 -150, rely=0.4, anchor='w')

    # Password label & entry
    password_label = tk.Label(canvas, text="Password:", bg='#241E2B', fg='white')
    password_label.place(x= prev_width/2 - 150, rely=0.5, anchor='e')

    password_entry = tk.Entry(canvas, 
                            show="*", 
                            fg='white', 
                            font=('Arial', 12), 
                            bg="#282828", 
                            width=40, 
                            bd=0, 
                            highlightbackground='#241E2B', 
                            highlightthickness=3)
    password_entry.place(x= prev_width/2 - 150, rely=0.5, anchor='w')

    def back_to_start():
        global selected_tab
        tab_frame.Login.destroy()
        canvas.pack_forget()
        explore_canvas()


    def on_submit():
        global canvas
        user = username_entry.get()
        pwd = password_entry.get()

        if authenticate(user, pwd):
            for widget in canvas.winfo_children():
                widget.destroy()
            success_label = tk.Label(canvas, text="Successfully Logged In!", bg='#241E2B', fg='white', font=('Arial', 14))
            success_label.place(relx=0.5, rely=0.5, anchor='c')
            canvas.after(1000, back_to_start)
        else:
            fail_label.config(text="Failed to login")

    submit_button = ttk.Button(canvas, text="Submit", command=on_submit)
    submit_button.place(relx=0.5, rely=0.65, anchor='c')
    button_selected(tab_frame.Login)
    #"""

def bind_mousewheel(widget, event, canvas):
    widget.bind(event, lambda e, canvas=canvas: on_mousewheel(e, canvas, 'x'))
    for child in widget.winfo_children():
        bind_mousewheel(child, event, canvas)

def explore_canvas():
    global canvas, main_canvas, selected_tab, top_frame, entry
    if selected_tab == 'Explore':
        button_selected(explore)
        return
    selected_tab = 'Explore'
    canvas.pack_forget()

    canvas = tk.Canvas(root, bg='#241E2B', bd=0, highlightthickness=0, width=1000)
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
    entry_var.trace_add("write", on_var_change)

    entry = tk.Entry(top_frame, textvariable=entry_var, fg='white', font=('Arial', 12), bg="#282828", width=40, bd=0, highlightbackground='#18141D', highlightthickness=3)
    entry.pack(side='left', padx=(prev_width-500, 10))

    main_canvas = tk.Canvas(canvas, bg='#241E2B', bd=0, highlightthickness=0, width=1000)
    main_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(20,0))

    main_canvas.bind("<MouseWheel>", lambda event, canvas=main_canvas: on_mousewheel(event, canvas))
    main_canvas.bind("<Button-1>", lambda event: main_canvas_click(event))
    entry.bind("<FocusIn>", remove_placeholder)
    entry.bind("<FocusOut>", restore_placeholder)

    display_all_proj(main_canvas)
    button_selected(explore)

root = tk.Tk()
root.geometry('1000x600')
root.minsize(1000,600)
root.title("Project Manager")
root.iconbitmap('GUI_Design/Project_Manager.ico')
root.bind("<Configure>", lambda event: update_scale() if event.widget == root else None)

style = ttk.Style()
style.theme_use('clam')

entry_var = tk.StringVar()

header_canvas = tk.Canvas(root, bg='#18141D', bd=0, highlightthickness=0, width=1000)
header_canvas.pack(side=tk.TOP, fill=tk.BOTH)

# Packing menu_button first to ensure it's on the far right
menu_button = tk.Button(
        header_canvas,
        text="☰",
        bg='#18141D',
        activebackground='#2C2634',
        fg='white',
        font=('Arial', 18, 'bold'),
        borderwidth=0,
        highlightthickness=0,
    )
menu_button.pack(side='right', padx=10, pady=0)

welcome = tk.Label(header_canvas, text="Project Manager", bg='#18141D', fg='white', font=('Arial', 0, 'bold'))
welcome.pack(side='left', pady =(5, 5), padx= (20,0))

# Packing tab_canvas after welcome but before menu_button
tab_canvas = tk.Canvas(header_canvas, bg='#18141D', highlightthickness=0, height=45)
tab_canvas.pack(side='left', fill=tk.X, expand=True)

tab_frame = tk.Frame(tab_canvas, bg='#18141D')
tab_canvas.create_window((0,0), window=tab_frame, anchor='nw')

tab_canvas.bind("<MouseWheel>", lambda event, canvas=tab_canvas: on_mousewheel(event, canvas, 'x'))

canvas = tk.Canvas(root, bg='#241E2B', bd=0, highlightthickness=0, width=1000)

header_buttons()
login()

root.mainloop()