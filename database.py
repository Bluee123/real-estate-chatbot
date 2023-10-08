import sqlite3

# 连接到数据库，如果不存在则会创建一个新的数据库文件
conn = sqlite3.connect('houses.db')

# 创建一个游标对象，用于执行 SQL 语句
cursor = conn.cursor()

# 创建一个名为 houses 的表格
cursor.execute('''CREATE TABLE houses
                (id INTEGER PRIMARY KEY,
                area REAL,
                sale_price REAL,
                rent_price REAL,
                location TEXT)''')

# 插入示例数据
for i in range(50):
    cursor.execute("INSERT INTO houses (area, sale_price, rent_price, location) VALUES (?, ?, ?, ?)",
                   (100.0 + i*5, 250000.0 + i*10000, 1000.0 + i*50, 'City Center' if i % 2 == 0 else 'Suburb'))

# 提交更改并关闭连接
conn.commit()
conn.close()

