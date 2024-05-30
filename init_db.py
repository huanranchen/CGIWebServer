import sqlite3

# 数据库文件路径
db_path = 'webroot/students.db'

# 连接到SQLite数据库（如果数据库不存在，将会创建一个）
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# 创建表
cursor.execute('''
CREATE TABLE IF NOT EXISTS students (
    student_id TEXT PRIMARY KEY,
    student_name TEXT,
    student_class TEXT
)
''')

# 插入测试数据
cursor.execute('''
INSERT INTO students (student_id, student_name, student_class)
VALUES ('1120210704', 'Huanran Chen', '2148'),
       ('11202107049', '杨松', '2148')
''')

# 提交更改并关闭连接
conn.commit()
cursor.close()
conn.close()

print("Database initialized successfully.")
