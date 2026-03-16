import sqlite3

conn = sqlite3.connect('apps.db')
cursor = conn.cursor()

# ---------------- USERS TABLE ----------------
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT,
    password TEXT,
    language TEXT
)
''')

# ---------------- APPS TABLE ----------------
cursor.execute('''
CREATE TABLE IF NOT EXISTS apps (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    app_name TEXT,
    language TEXT,
    video_link TEXT
)
''')

# ---------------- INSERT APP VIDEOS ----------------
cursor.executemany(
'''
INSERT INTO apps (app_name, language, video_link)
VALUES (?, ?, ?)
''',
[
('instagram','English','https://youtu.be/j4nBDjsyGZ0?si=1vL6LUqFty1CHyt3'),
('instagram','Telugu','https://www.youtube.com/embed/VIDEOID1'),
('instagram','Hindi','https://www.youtube.com/embed/VIDEOID2'),

('whatsapp','English','https://www.youtube.com/embed/1XlYFzv3CwY'),
('whatsapp','Telugu','https://www.youtube.com/embed/VIDEOID3'),
('whatsapp','Hindi','https://www.youtube.com/embed/VIDEOID4')
]
)

conn.commit()
conn.close()

print("Database Created Successfully!")