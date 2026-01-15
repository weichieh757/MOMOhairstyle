// ==========================================
// 檔案名稱：data.js
// 用途：模擬後端資料庫，儲存所有商品的資訊
// 注意：真實開發中，這些資料通常會從 API 獲取
// ==========================================

// 將 products 定義在 window 物件下，確保全域皆可存取
window.products = [
    { 
        id: 1, 
        name: "R.O.8髮浴系列", 
        price: 800, 
        category: "洗髮燙髮", // 用於分類過濾
        description: "高效補水、溫和潔淨，適合日常清爽洗髮。", 
        image: "R.O.8水漾髮浴.jpeg" // 圖片檔名
    },
    { 
        id: 2, 
        name: "日本AQUA碳酸泉", 
        price: 3500, 
        category: "保養", 
        description: "來自日本的AQUA碳酸錠，深層清潔。", 
        image: "日本AQUA碳酸泉.jpeg" 
    },
    { 
        id: 3, 
        name: "ProShia活淬養髮系列", 
        price: 750, 
        category: "保養", 
        description: "深層修護髮絲，注入植物活性成分。", 
        image: "Proshia.jpeg" 
    },
    { 
        id: 4, 
        name: "專業染膏系列", 
        price: 600, 
        category: "染髮", 
        description: "色彩飽和顯色持久，染髮同時護髮。", 
        image: "染膏.jpeg" 
    },
    { 
        id: 5, 
        name: "R.O.8更新凝膠", 
        price: 700, 
        category: "保養", 
        description: "放鬆頭皮、舒緩壓力，去除老廢角質。", 
        image: "R.O.8更新凝膠.jpeg" 
    },
    { 
        id: 6, 
        name: "天使光水乳膜", 
        price: 2000, 
        category: "洗髮燙髮", 
        description: "免沖洗護髮，瞬間吸收不油膩。", 
        image: "天使光水乳膜.png" 
    },
    { 
        id: 7, 
        name: "SIG礦物泥皂", 
        price: 300, 
        category: "其他", 
        description: "天然礦物泥成分，吸附油脂能力極佳。", 
        image: "去背的IMG_1003.png" 
    },
    { 
        id: 8, 
        name: "頭皮頭髮養護", 
        price: 780, 
        category: "保養", 
        description: "活萃頭皮滋養。", 
        image: "頭皮養護.jpeg" 
    },
    {
        id: 9, 
        name: "肌守護手霜", 
        price: 500, 
        category: "保養", 
        description: "護手霜。", 
        image: "護手霜.png" 
    },
    {
        id: 10, 
        name: "活淬瓜拿納頭皮滋養噴霧", 
        price: 650,
        // 新增 images 陣列，可以放無限多張
        images: [
            "IMG_5501.JPG",   // 第一張 (主圖)
            "IMG_5326.JPG",      // 第二張
            "IMG_5325.JPG"    // 第三張 
        ],
        category: "保養", 
        description: "涼。", 
    },
];