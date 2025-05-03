
import tkinter as tk
from pymysql import Connection
from tkinter import messagebox, ttk

DB_CONFIG = {
    'host': 'localhost',
    'port': 3306,
    'user': 'root',
    'password': "asdf8763",
    'database': 'studentmanagement'
}

class LoginApp:
    def __init__(self,rootwindow):
        self.rootwindow = rootwindow
        self.rootwindow.title("StudentManagement")
        self.rootwindow.geometry("500x500")
        self.rootwindow.resizable(False, False)
        self.create_widgets()

    def create_widgets(self):
        # 标题
        title_label = tk.Label(self.rootwindow, text="学生课程管理系统", font=("Arial", 16, "bold"))
        title_label.pack(pady=20)

        # 用户ID标签和输入框
        id_label = tk.Label(self.rootwindow, text="用户ID:", font=("Arial", 12))
        id_label.pack(pady=5)
        self.id_entry = tk.Entry(self.rootwindow, font=("Arial", 12), width=30)
        self.id_entry.pack(pady=5)

        # 密码标签和输入框
        password_label = tk.Label(self.rootwindow, text="密码:", font=("Arial", 12))
        password_label.pack(pady=5)
        self.password_entry = tk.Entry(self.rootwindow, font=("Arial", 12), width=30, show="*")
        self.password_entry.pack(pady=5)

        # 登录按钮
        login_button = tk.Button(self.rootwindow, text="登录", font=("Arial", 12),
                                 command=self.login, width=10)
        login_button.pack(pady=20)

    def hide_root(self):
        self.rootwindow.withdraw()

    def show_root(self):
        self.rootwindow.deiconify()
    def login(self):
        user_id = self.id_entry.get().strip()
        password = self.password_entry.get().strip()
        if not user_id or not password:
            tk.messagebox.showerror("error","enter id and password")
            return

        try:
            connection = Connection(**DB_CONFIG)
            cursor = connection.cursor()
            sql = "select Occupation,Password from accountpassword where account = %s"
            cursor.execute(sql, (user_id,))
            result = cursor.fetchone()
            if result:
                stored_occupation, stored_password = result
                if stored_password == password:
                    occupation = stored_occupation
                    self.hide_root()
                    if occupation == "student":
                        self.open_student_interface(user_id)
                    elif occupation == "teacher":
                        self.open_teacher_interface(user_id)
                    elif occupation == "admin":
                        self.open_admin_interface(user_id)
                    else:
                        messagebox.showerror("error","unknown user type")

                else:
                    messagebox.showerror("error","wrong password")
            else:
                messagebox.showerror("error","id not exist")
        except Exception as e:
            messagebox.showerror("error",str(e))

    def open_admin_interface(self, user_id):        #管理员主窗口
        admin_window = tk.Toplevel(self.rootwindow)
        admin_window.title("AdminInterface")
        admin_window.geometry("400x600")
        admin_window.resizable(False, False)

        button_frame = tk.Frame(admin_window)
        button_frame.pack(pady=20)

        #查询信息
        search_info_button = tk.Button(button_frame,text='searchInfo',
                                     font=("Arial", 12),width=15,
                                     command = lambda:self.search_info(admin_window))
        search_info_button.pack(pady=20)

        #修改信息
        modify_info_button = tk.Button(button_frame,text='modifyInfo',
                                       font=("Arial", 12),width=15,
                                       command = lambda:modify_info_admin(admin_window, user_id))
        modify_info_button.pack(pady=20)

        #修改密码
        change_password_button = tk.Button(button_frame,text='changePassword',
                                           font=("Arial", 12),width=15,
                                           command = lambda:self.change_password(admin_window, user_id))
        change_password_button.pack(pady=20)

        #退出登录
        logout_button = tk.Button(button_frame, text='logout',
                                  font=("Arial", 12), width=15,
                                  command =lambda:self.logout(admin_window))
        logout_button.pack(pady=20)

    def search_info(self, window):      #查询信息主窗口
        search_info_window = tk.Toplevel(window)
        window.withdraw()
        search_info_window.title("searchInfo")
        search_info_window.geometry("400x600")
        search_info_window.resizable(False, False)
        tk.Label(search_info_window,text="Search for Information",font=("Arial", 12)).pack(pady=5)

        # 查询学生信息窗口
        def select_student_info(window):
            student_info_window = tk.Toplevel(window)
            window.withdraw()
            student_info_window.title("studentInfo")
            student_info_window.geometry("800x600")
            student_info_window.resizable(False, False)
            tk.Label(student_info_window,text="Student Information",font=("Arial", 12)).pack(pady=5)
            tk.Label(student_info_window, fg="red",text="enter student id or student name",font=("Arial", 8)).pack(pady=5)

            student_id_entry = tk.Entry(student_info_window, font=("Arial", 12), width=30)
            student_id_entry.pack(pady=5)

            #表格
            columns = ("StudentID", "Name", "Sex", "EntranceAge",
                       "EntranceYear", "Class")
            student_tree = ttk.Treeview(student_info_window, columns=columns, show="headings")
            student_tree.pack(fill="both", expand=True, padx=20, pady=10)

            scrollbar = ttk.Scrollbar(student_info_window, orient="vertical", command=student_tree.yview)
            scrollbar.pack(side="right", fill="y")
            student_tree.configure(yscrollcommand=scrollbar.set)


            def query_student():            #查询学生信息按钮
                # 设置表格列
                student_tree["columns"] = ("StudentID", "Name", "Sex", "EntranceAge",
                                           "EntranceYear", "Class")
                student_tree["show"] = "headings"  # 隐藏默认的第一列

                # 设置列标题
                student_tree.heading("StudentID", text="Student ID")
                student_tree.heading("Name", text="Name")
                student_tree.heading("Sex", text="Sex")
                student_tree.heading("EntranceAge", text="Entrance Age")
                student_tree.heading("EntranceYear", text="Entrance Year")
                student_tree.heading("Class", text="Class")

                # 设置列宽
                student_tree.column("StudentID", width=200)
                student_tree.column("Name", width=50)
                student_tree.column("Sex", width=50)
                student_tree.column("EntranceAge", width=100)
                student_tree.column("EntranceYear", width=100)
                student_tree.column("Class", width=100)

                #获取输入框信息
                student_input = student_id_entry.get().strip()
                connection = Connection(**DB_CONFIG)
                cursor = connection.cursor()
                #清空表格
                for item in student_tree.get_children():
                    student_tree.delete(item)

                if not student_input:
                    try:
                        query = ("""
                        select * from students""")
                        cursor.execute(query)
                        result = cursor.fetchall()
                        for row in result:
                            student_tree.insert("", "end", values=(
                                row[0], row[1], row[2], row[3], row[4], row[5]
                            ))
                    except Exception as e:
                        messagebox.showerror("error",str(e))
                    finally:
                        cursor.close()
                        connection.close()
                        return

                try:
                    query = ("""                     
                            select StudentID,StudentName,Sex,EntranceAge,EntranceYear,Class
                            From students where StudentID = %s
                            """)
                    cursor.execute(query, (student_input,))
                    result = cursor.fetchall()
                    if not result:
                        query_name = ("""
                                        select StudentID,StudentName,Sex,EntranceAge,EntranceYear,Class
                                        From students where StudentName LIKE %s""")
                        cursor.execute(query_name, (student_input,))
                        result = cursor.fetchall()
                    if result:
                        for row in result:
                            student_tree.insert("", "end", values=(
                                row[0], row[1], row[2], row[3], row[4], row[5]
                            ))
                    else:
                        messagebox.showinfo("info", "student not exist")
                except Exception as e:
                    messagebox.showerror("error",str(e))
                finally:
                    cursor.close()
                    connection.close()
            query_button = tk.Button(student_info_window, text="Query",width=15,command=query_student)
            query_button.pack(pady=5)

            def go_back():
                student_info_window.destroy()
                window.deiconify()
            back_button = tk.Button(student_info_window,text="back",width=15,
                                    command=go_back)
            back_button.pack(pady=5)

        tk.Button(search_info_window, text="Student Info", font=("Arial", 12), width=20,
                  command=lambda:select_student_info(search_info_window)).pack(pady=10)

        # 查询学生成绩窗口
        def select_student_score_info(window):
            student_score_window = tk.Toplevel(window)
            window.withdraw()
            student_score_window.title("Students score")
            student_score_window.geometry("800x600")
            student_score_window.resizable(width=False, height=False)


            tk.Label(student_score_window ,text="Student ID or Name:", font=("Arial", 12)).grid(
                row=0, column=0, pady=5
            )
            tk.Label(student_score_window, text="Course ID or Name:", font=("Arial", 12)).grid(
                row=1, column=0, pady=5
            )
            student_input_entry = tk.Entry(student_score_window, font=("Arial", 12),width=40)
            student_input_entry.grid(row=0, column=1, padx=30,pady=20,sticky="nsew")
            course_input_entry = tk.Entry(student_score_window, font=("Arial", 12),width=40)
            course_input_entry.grid(row=1, column=1, padx=30,pady=20,sticky="nsew")

            table_frame = tk.Frame(student_score_window,bg="red")
            table_frame.grid(row=3,column=0,columnspan=4,padx=20,pady=20,sticky="nsew")
            columns = ("StudentID", "StudentName", "CourseID", "CourseName","Score")
            student_tree = ttk.Treeview(table_frame, columns=columns, show="headings")
            student_tree.grid(row=0, column=0,sticky="nsew")
            # scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=student_tree.yview)
            # scrollbar.grid(row=0, column=1, sticky="ns")
            # student_tree.configure(yscrollcommand=scrollbar.set)

            student_tree["show"]="headings"
            for col in columns:
                student_tree.heading(col, text=col)
                student_tree.column(col, width=100)
            student_tree.column("StudentID", width=100)
            student_tree.column("StudentName", width=100)
            student_tree.column("CourseID", width=100)
            student_tree.column("CourseName", width=50)
            student_tree.column("Score", width=70)

            student_score_window.grid_rowconfigure(3, weight=1)
            student_score_window.grid_columnconfigure(0, weight=1)
            table_frame.grid_rowconfigure(0, weight=1)
            table_frame.grid_columnconfigure(0, weight=1)

            def query_scores():
                student_input = student_input_entry.get().strip()
                course_input = course_input_entry.get().strip()
                for item in student_tree.get_children():
                    student_tree.delete(item)

                connection = Connection(**DB_CONFIG)
                cursor = connection.cursor()
                try:
                    query="""
                    Select s.StudentID,s.StudentName,c.CourseID,c.CourseName,cs.Score
                    from coursechoosing cs
                    join students s on cs.StudentID = s.StudentID
                    join courses c on cs.CourseID = c.CourseID
                    """

                    conditions = []
                    params = []
                    if student_input:
                        conditions.append("(cs.StudentID = %s OR s.StudentName LIKE %s)")
                        params.extend([student_input, f"%{student_input}%"])

                    if course_input:
                        conditions.append("(cs.CourseID = %s OR c.CourseName LIKE %s)")
                        params.extend([course_input, f"%{course_input}%"])

                    if conditions:
                        query += " WHERE " + " AND ".join(conditions)
                    query+="order by s.StudentID,c.CourseID"
                    cursor.execute(query,params)
                    result = cursor.fetchall()
                    if not result:
                        return
                    for row in result:
                        student_tree.insert("", "end", values=row)
                except Exception as e:
                    messagebox.showerror("error",str(e))
                finally:
                    cursor.close()
                    connection.close()

            query_button = tk.Button(student_score_window, text="Query", width=15, command=query_scores)
            query_button.grid(row=5, column=0, pady=5, padx=10)

            def go_back():
                student_score_window.destroy()
                window.deiconify()
            back_button = tk.Button(student_score_window, text="Back", width=15, command=go_back)
            back_button.grid(row=5, column=1, pady=5, padx=10)

        tk.Button(search_info_window,text="Student Score Info",font=("Arial", 12), width=20,
                  command=lambda:select_student_score_info(search_info_window)).pack(pady=10)

        def select_course_info(window):
            course_window = tk.Toplevel(window)
            window.withdraw()
            course_window.title("Students score")
            course_window.geometry("800x600")
            course_window.resizable(width=False, height=False)
            tk.Label(course_window, text="Course Information", font=("Arial", 12)).pack(pady=5)
            tk.Label(course_window, fg="red", text="enter course id or course name", font=("Arial", 8)).pack(
                pady=5)

            student_id_entry = tk.Entry(course_window, font=("Arial", 12), width=30)
            student_id_entry.pack(pady=5)

            # 表格
            columns = ("CourseID", "Name", "Teacher name", "Credit",
                       "Grade", "Canceled Year")
            student_tree = ttk.Treeview(course_window, columns=columns, show="headings")
            student_tree.pack(fill="both", expand=True, padx=20, pady=10)

        tk.Button(search_info_window,text="Course Info",font=("Arial", 12), width=20,
                  command=lambda:select_course_info(search_info_window)).pack(pady=10)

        #返回按钮
        def go_back():
            search_info_window.destroy()
            window.deiconify()
        tk.Button(search_info_window,text="Back",font=("Arial",10),width=15,
                  command=go_back).pack(pady=5)

        search_info_window.deiconify()

    def logout(self,window):
        self.show_root()
        window.destroy()


    def change_password(self,window,user_id):
        change_password_window = tk.Toplevel(window)
        window.withdraw()
        change_password_window.title("Change Password")
        change_password_window.geometry("400x400")
        change_password_window.resizable(False, False)

        tk.Label(change_password_window,text ="change password",font=("Arial",14)).pack(pady=5)
        tk.Label(change_password_window,text="new password",font = ("Arial", 12)).pack(pady=5)
        new_password_entry = tk.Entry(change_password_window, font=("Arial", 12), width=30)
        new_password_entry.pack(pady=5)

        error_label = tk.Label(change_password_window, text="",fg="red",font=("Arial", 10))
        error_label.pack(pady=5)

        def update():
            new_password = new_password_entry.get().strip()
            if not new_password:
                error_label.config(text="enter new password")
                return

            connection = Connection(**DB_CONFIG)
            cursor = connection.cursor()
            try:
                update_query = "UPDATE accountpassword SET Password = %s where Account = %s"
                cursor.execute(update_query, (new_password, user_id))
                connection.commit()
                messagebox.showinfo("success","password updated")
                change_password_window.destroy()
                window.deiconify()
            except Exception as e:
                print(e)
            finally:
                cursor.close()
                connection.close()

        def cancel_destroy():
            change_password_window.destroy()
            window.deiconify()

        tk.Button(change_password_window, text="changePassword",font=("Arial", 12),width=20,command=update).pack(pady=10)
        tk.Button(change_password_window,text = "cancel",font = ("Arial", 12),width=20,command = cancel_destroy).pack(pady=10)



def main():
    window = tk.Tk()
    LoginApp(window)
    window.mainloop()

if __name__ == '__main__':
    main()