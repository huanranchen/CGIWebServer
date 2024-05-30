#!/usr/bin/env python3

import cgi
import cgitb
import sqlite3

cgitb.enable()

# 获取表单数据
form = cgi.FieldStorage()
student_id = form.getvalue('student_id')

print("Content-Type: text/html")
print()

# 数据库文件路径
db_path = 'webroot/students.db'

# 查询数据库
try:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    query = "SELECT student_name, student_class FROM students WHERE student_id = ?"
    cursor.execute(query, (student_id,))
    result = cursor.fetchone()

    if result:
        student_name, student_class = result
        print(f"<html><body><h1>Student Information</h1>")
        print(f"<p>Student ID: {student_id}</p>")
        print(f"<p>Student Name: {student_name}</p>")
        print(f"<p>Student Class: {student_class}</p>")
        print("</body></html>")
    else:
        print("<html><body><h1>Student Not Found</h1></body></html>")

    cursor.close()
    conn.close()
except sqlite3.Error as err:
    print(f"<html><body><h1>Error: {err}</h1></body></html>")
