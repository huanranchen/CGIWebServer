#!/usr/bin/env python3

import cgi
import cgitb
import sqlite3

cgitb.enable()

# 获取表单数据
form = cgi.FieldStorage()
student_id = form.getvalue('student_id')
student_name = form.getvalue('student_name')
student_class = form.getvalue('student_class')

print("Content-Type: text/html")
print()

# 数据库文件路径
db_path = 'webroot/students.db'

# 插入新学生信息到数据库
try:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    query = "INSERT INTO students (student_id, student_name, student_class) VALUES (?, ?, ?)"
    cursor.execute(query, (student_id, student_name, student_class))
    conn.commit()

    print("<html><body><h1>Student Added Successfully</h1>")
    print(f"<p>Student ID: {student_id}</p>")
    print(f"<p>Student Name: {student_name}</p>")
    print(f"<p>Student Class: {student_class}</p>")
    print("</body></html>")

    cursor.close()
    conn.close()
except sqlite3.IntegrityError:
    print("<html><body><h1>Error: Student ID already exists</h1></body></html>")
except sqlite3.Error as err:
    print(f"<html><body><h1>Error: {err}</h1></body></html>")
