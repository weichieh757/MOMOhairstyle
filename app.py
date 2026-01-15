import sqlite3
import os
import json
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS

app = Flask(__name__)
# 允許跨域請求，這樣你的 HTML (5500 port) 才能跟 Python (5001 port) 溝通
CORS(app) 

# 設定圖片上傳資料夾
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def get_db_connection():
    conn = sqlite3.connect('shop.db')
    conn.row_factory = sqlite3.Row
    return conn

# --- 1. 取得所有商品 (API) ---
@app.route('/api/products', methods=['GET'])
def get_products():
    conn = get_db_connection()
    products = conn.execute('SELECT * FROM products').fetchall()
    conn.close()
    
    products_list = []
    for p in products:
        p_dict = dict(p)
        # 把 JSON 字串轉回 Python 列表/物件
        try:
            p_dict['images'] = json.loads(p['images']) if p['images'] else []
            p_dict['variants'] = json.loads(p['variants']) if 'variants' in p_dict and p_dict['variants'] else []
            p_dict['image_positions'] = json.loads(p['image_positions']) if 'image_positions' in p_dict and p_dict['image_positions'] else []
        except:
            pass # 如果解析失敗就維持原狀
        products_list.append(p_dict)
        
    return jsonify(products_list)

# --- 2. 取得單一商品詳情 (API) ---
@app.route('/api/products/<int:id>', methods=['GET'])
def get_product(id):
    conn = get_db_connection()
    product = conn.execute('SELECT * FROM products WHERE id = ?', (id,)).fetchone()
    conn.close()
    if product is None:
        return jsonify({'error': 'Product not found'}), 404
    
    p_dict = dict(product)
    try:
        p_dict['images'] = json.loads(p_dict['images']) if p_dict['images'] else []
        p_dict['variants'] = json.loads(p_dict['variants']) if 'variants' in p_dict and p_dict['variants'] else []
        p_dict['image_positions'] = json.loads(p_dict['image_positions']) if 'image_positions' in p_dict and p_dict['image_positions'] else []
    except:
        pass
    return jsonify(p_dict)

# --- 3. 新增/修改商品 (Admin) ---
@app.route('/api/products', methods=['POST'])
@app.route('/api/products/<int:id>', methods=['PUT'])
def save_product(id=None):
    data = request.form
    name = data.get('name')
    price = data.get('price')
    description = data.get('description')
    
    # 處理分類 (可能是多選)
    categories = request.form.getlist('category')
    # 如果只有一個值且包含逗號，或是前端送來的是字串
    if len(categories) == 0 and data.get('category'):
        categories = [data.get('category')]
    # 存入資料庫時轉為字串 (例如 "洗髮, 染髮") 或 JSON
    category_str = json.dumps(categories, ensure_ascii=False) # 建議存成 JSON 陣列字串

    variants = data.get('variants', '[]') # 規格 JSON 字串
    
    # --- 圖片處理 ---
    # 1. 處理新上傳的檔案
    uploaded_files = request.files.getlist('photos')
    new_filenames = []
    
    for file in uploaded_files:
        if file and file.filename != '':
            filename = file.filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            # 存入完整的 URL 路徑方便前端讀取
            new_filenames.append(f"http://127.0.0.1:5001/uploads/{filename}")

    # 2. 處理「已存在的舊圖片」(從圖庫選的 或 原本就有的)
    existing_images = request.form.getlist('existing_images')
    
    # 合併圖片列表
    final_images = existing_images + new_filenames
    
    # 第一張圖當作主圖
    main_image = final_images[0] if final_images else ''
    
    # 存成 JSON 字串
    images_json = json.dumps(final_images)

    conn = get_db_connection()
    if id:
        # 修改
        conn.execute('''
            UPDATE products 
            SET name=?, price=?, category=?, description=?, image=?, images=?, variants=?
            WHERE id=?
        ''', (name, price, category_str, description, main_image, images_json, variants, id))
    else:
        # 新增
        conn.execute('''
            INSERT INTO products (name, price, category, description, image, images, variants)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (name, price, category_str, description, main_image, images_json, variants))
        
    conn.commit()
    conn.close()
    return jsonify({'status': 'success'})

# --- 4. 刪除商品 ---
@app.route('/api/products/<int:id>', methods=['DELETE'])
def delete_product(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM products WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return jsonify({'status': 'deleted'})

# --- 5. 結帳 (Checkout) ---
@app.route('/api/checkout', methods=['POST'])
def checkout():
    data = request.json
    print("收到訂單：", data)
    # 這裡你可以實作寫入 orders 資料表的邏輯
    # 目前先單純回傳成功
    return jsonify({'status': 'success', 'message': 'Order received'})

# --- 6. 圖片庫 API (讓後台可以選舊圖) ---
@app.route('/api/images', methods=['GET'])
def get_images():
    images = []
    if os.path.exists(UPLOAD_FOLDER):
        for filename in os.listdir(UPLOAD_FOLDER):
            if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
                images.append(f"http://127.0.0.1:5001/uploads/{filename}")
    return jsonify(images)

# --- 7. 顯示圖片 (Static Files) ---
# 這樣前端 <img src="http://.../uploads/xxx.jpg"> 才能運作
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    # 這裡設定 port=5001，因為你的 admin.html 是呼叫 5001
    app.run(debug=True, port=5001)