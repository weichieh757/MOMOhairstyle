import sqlite3

def init_db():
    # 1. 連線到資料庫 (如果不存在會自動建立)
    conn = sqlite3.connect('shop.db')
    cursor = conn.cursor()

    # 2. 確保先刪除舊的表，避免重複或衝突
    cursor.execute('DROP TABLE IF EXISTS products')

    # 3. 建立全新的商品資料表
    cursor.execute('''
        CREATE TABLE products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            price INTEGER NOT NULL,
            category TEXT NOT NULL,
            description TEXT,
            image TEXT,
            images TEXT
        )
    ''')

    # 4. 準備您的 9 樣商品資料
    products_data = [
        ("R.O.8髮浴系列", 800, "洗髮燙髮", "高效補水、溫和潔淨，適合日常清爽洗髮。", "R.O.8水漾髮浴.jpeg", '["R.O.8水漾髮浴.jpeg"]'),
        ("日本AQUA碳酸泉", 3500, "保養", "來自日本的AQUA碳酸錠，深層清潔。", "日本AQUA碳酸泉.jpeg", '["日本AQUA碳酸泉.jpeg"]'),
        ("ProShia活淬養髮系列", 750, "保養", "深層修護髮絲，注入植物活性成分。", "Proshia.jpeg", '["Proshia.jpeg"]'),
        ("專業染膏系列", 600, "染髮", "色彩飽和顯色持久，染髮同時護髮。", "染膏.jpeg", '["染膏.jpeg"]'),
        ("R.O.8更新凝膠", 700, "保養", "放鬆頭皮、舒緩壓力，去除老廢角質。", "R.O.8更新凝膠.jpeg", '["R.O.8更新凝膠.jpeg"]'),
        ("天使光水乳膜", 2000, "洗髮燙髮", "免沖洗護髮，瞬間吸收不油膩。", "天使光水乳膜.png", '["天使光水乳膜.png"]'),
        ("SIG礦物泥皂", 300, "其他", "天然礦物泥成分，吸附油脂能力極佳。", "去背的IMG_1003.png", '["去背的IMG_1003.png"]'),
        ("頭皮頭髮養護", 780, "保養", "活萃頭皮滋養。", "頭皮養護.jpeg", '["頭皮養護.jpeg"]'),
        ("肌守護手霜", 500, "保養", "護手霜。", "護手霜.png", '["護手霜.png"]')
    ]

    # 5. 寫入資料
    cursor.executemany('''
        INSERT INTO products (name, price, category, description, image, images)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', products_data)

    conn.commit()
    conn.close()
    print("✅ 成功！資料庫 shop.db 已建立，商品已寫入！")

if __name__ == '__main__':
    init_db()
