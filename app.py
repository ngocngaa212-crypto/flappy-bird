import streamlit as st
import base64
import os

st.set_page_config(page_title="The journey of Tom", page_icon="🐱", layout="centered")

st.title("🐱 The journey of Tom - Pixel Edition")
st.write("Hành trình của Tom - Đã hỗ trợ đa ngôn ngữ (Tiếng Việt có dấu / English)!")

def get_image_base64(image_path):
    if os.path.exists(image_path):
        with open(image_path, "rb") as img_file:
            encoded = base64.b64encode(img_file.read()).decode()
            return f"data:image/png;base64,{encoded}"
    return ""

# Đọc các file ảnh từ thư mục GitHub
bg_data_url = get_image_base64("background.png")
normal_data_url = get_image_base64("cat_normal.png") if os.path.exists("cat_normal.png") else get_image_base64("bird.png")

# Đọc 3 file ảnh skin
rainbow_data_url = get_image_base64("rainbow_Tom.png")
donut_data_url = get_image_base64("Tom_with_donut.png")
strong_data_url = get_image_base64("super_strong_Tom.png")

flappy_bird_html = f"""
<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <title>The journey of Tom</title>
    <link href="https://fonts.googleapis.com/css2?family=Press+Start+2P&display=swap" rel="stylesheet">
    <style>
        body {{
            margin: 0;
            background: #111;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            font-family: 'Press Start 2P', monospace;
        }}
        canvas {{
            border: 4px solid #fff;
            box-shadow: 0px 0px 20px rgba(255,255,255,0.4);
            image-rendering: pixelated;
            image-rendering: crisp-edges;
        }}
    </style>
</head>
<body>
    <canvas id="gameCanvas" width="400" height="500"></canvas>
    <script>
        const canvas = document.getElementById("gameCanvas");
        const ctx = canvas.getContext("2d");

        const bgImage = new Image();
        bgImage.src = "{bg_data_url}";

        // Tải danh sách ảnh skin nhân vật
        const skinImages = {{
            "normal": new Image(),
            "rainbow": new Image(),
            "donut": new Image(),
            "strong": new Image()
        }};

        skinImages["normal"].src = "{normal_data_url}";
        skinImages["rainbow"].src = "{rainbow_data_url}";
        skinImages["donut"].src = "{donut_data_url}";
        skinImages["strong"].src = "{strong_data_url}";

        // Tự động lọc viền đen/sẫm cho tất cả ảnh nhân vật
        const cleanedSkinCanvases = {{}};

        function processSkinImage(key, img) {{
            img.onload = function() {{
                let c = document.createElement('canvas');
                c.width = img.width;
                c.height = img.height;
                let tCtx = c.getContext('2d');
                tCtx.drawImage(img, 0, 0);
                try {{
                    let imgData = tCtx.getImageData(0, 0, img.width, img.height);
                    let data = imgData.data;
                    for (let i = 0; i < data.length; i += 4) {{
                        let r = data[i], g = data[i+1], b = data[i+2];
                        if (r < 25 && g < 25 && b < 25) {{
                            data[i + 3] = 0;
                        }}
                    }}
                    tCtx.putImageData(imgData, 0, 0);
                    cleanedSkinCanvases[key] = c;
                }} catch(e) {{
                    cleanedSkinCanvases[key] = img;
                }}
            }};
        }}

        for (let key in skinImages) {{
            processSkinImage(key, skinImages[key]);
        }}

        // Quản lý Ngôn ngữ (Mặc định: 'vi')
        let currentLang = localStorage.getItem("tom_lang") || "vi";

        const i18n = {{
            "vi": {{
                play: "CHƠI GAME",
                shop: "CỬA HÀNG",
                selectLevel: "CHỌN CẤP ĐỘ",
                back: "<- LÙI",
                coins: "XU: 🪙 ",
                target: "Mục tiêu: ",
                reward: "Thưởng: 🪙 ",
                using: "ĐANG DÙNG",
                owned: "ĐÃ SỞ HỮU",
                price: "GIÁ: 🪙 ",
                confirmTitle: "XÁC NHẬN MUA",
                confirmAsk: "Bạn chắc chắn muốn mua?",
                buy: "MUA",
                cancel: "HỦY",
                failed: "THẤT BẠI!",
                retry: "Nhấn Space để chọn lại",
                completed: "HOÀN THÀNH!",
                earned: "Thưởng: + 🪙 ",
                continue: "Nhấn Space để tiếp tục",
                notEnoughCoins: "Bạn không đủ tiền xu!",
                lvlNames: {{
                    1: "CẤP 1: KHỞI ĐẦU",
                    2: "CẤP 2: VƯỢT THÁC",
                    3: "CẤP 3: RỪNG SÂU",
                    4: "CẤP 4: THỬ THÁCH",
                    5: "CẤP 5: ĐỈNH CAO"
                }}
            }},
            "en": {{
                play: "PLAY GAME",
                shop: "SKIN SHOP",
                selectLevel: "SELECT LEVEL",
                back: "<- BACK",
                coins: "COINS: 🪙 ",
                target: "Target: ",
                reward: "Reward: 🪙 ",
                using: "EQUIPPED",
                owned: "OWNED",
                price: "PRICE: 🪙 ",
                confirmTitle: "CONFIRM PURCHASE",
                confirmAsk: "Are you sure you want to buy?",
                buy: "BUY",
                cancel: "CANCEL",
                failed: "GAME OVER!",
                retry: "Press Space to retry",
                completed: "LEVEL CLEAR!",
                earned: "Reward: + 🪙 ",
                continue: "Press Space to continue",
                notEnoughCoins: "Not enough coins!",
                lvlNames: {{
                    1: "LEVEL 1: BEGINNING",
                    2: "LEVEL 2: WATERFALL",
                    3: "LEVEL 3: DEEP FOREST",
                    4: "LEVEL 4: CHALLENGE",
                    5: "LEVEL 5: PEAK MASTER"
                }}
            }}
        }};

        let totalCoins = parseInt(localStorage.getItem("tom_coins")) || 0;
        let unlockedSkins = JSON.parse(localStorage.getItem("tom_skins")) || ["normal"];
        let currentSkin = localStorage.getItem("tom_current_skin") || "normal";

        const skins = {{
            "normal": {{ name: "normal tom", price: 0, color: "#F4D03F" }},
            "rainbow": {{ name: "rainbow Tom", price: 50, color: "#9B59B6" }},
            "donut": {{ name: "Tom with donut", price: 100, color: "#E75480" }},
            "strong": {{ name: "Super strong Tom", price: 170, color: "#E74C3C" }}
        }};

        let gameState = 'menu';
        let pendingBuySkinKey = null;

        let bird = {{
            x: 30,
            y: 150,
            width: 125,
            height: 75,
            gravity: 0.42, 
            lift: -8.2,      
            velocity: 0
        }};

        let currentLevel = 1;
        const levels = {{
            1: {{ speed: 1.5, gap: 200, spawnRate: 120, targetScore: 3, reward: 15 }},
            2: {{ speed: 1.8, gap: 190, spawnRate: 110, targetScore: 5, reward: 30 }},
            3: {{ speed: 2.1, gap: 180, spawnRate: 100, targetScore: 8, reward: 50 }},
            4: {{ speed: 2.4, gap: 170, spawnRate: 90, targetScore: 12, reward: 80 }},
            5: {{ speed: 2.8, gap: 160, spawnRate: 80, targetScore: 15, reward: 120 }}
        }};

        let pipes = [];
        let frameCount = 0;
        let score = 0;
        let coinsEarnedThisRun = 0;
        let levelCompleted = false;

        function resetGame(level) {{
            currentLevel = level;
            bird.y = 150;
            bird.velocity = 0;
            pipes = [];
            score = 0;
            coinsEarnedThisRun = 0;
            frameCount = 0;
            levelCompleted = false;
            gameState = 'playing';
        }}

        document.addEventListener("keydown", function(e) {{
            if (e.code === "Space") {{
                if (gameState === 'playing') {{
                    bird.velocity = bird.lift;
                }} else if (gameState === 'gameover' || levelCompleted) {{
                    gameState = 'level_select';
                }}
            }}
        }});

        canvas.addEventListener("click", function(e) {{
            let rect = canvas.getBoundingClientRect();
            let mouseX = e.clientX - rect.left;
            let mouseY = e.clientY - rect.top;

            // Xử lý nút bấm Chuyển đổi Ngôn ngữ 🌐 VI / EN góc trên màn hình Menu
            if (gameState === 'menu' && mouseX >= 280 && mouseX <= 380 && mouseY >= 15 && mouseY <= 50) {{
                currentLang = (currentLang === "vi") ? "en" : "vi";
                localStorage.setItem("tom_lang", currentLang);
                return;
            }}

            if (pendingBuySkinKey) {{
                let t = i18n[currentLang];
                // Nút MUA
                if (mouseX >= 40 && mouseX <= 180 && mouseY >= 330 && mouseY <= 380) {{
                    let skin = skins[pendingBuySkinKey];
                    if (totalCoins >= skin.price) {{
                        totalCoins -= skin.price;
                        unlockedSkins.push(pendingBuySkinKey);
                        currentSkin = pendingBuySkinKey;
                        localStorage.setItem("tom_coins", totalCoins);
                        localStorage.setItem("tom_skins", JSON.stringify(unlockedSkins));
                        localStorage.setItem("tom_current_skin", currentSkin);
                    }} else {{
                        alert(t.notEnoughCoins);
                    }}
                    pendingBuySkinKey = null;
                }}
                // Nút HỦY
                else if (mouseX >= 220 && mouseX <= 360 && mouseY >= 330 && mouseY <= 380) {{
                    pendingBuySkinKey = null;
                }}
                return;
            }}

            if (gameState === 'menu') {{
                if (mouseX >= 60 && mouseX <= 340 && mouseY >= 210 && mouseY <= 270) {{
                    gameState = 'level_select';
                }}
                if (mouseX >= 60 && mouseX <= 340 && mouseY >= 290 && mouseY <= 350) {{
                    gameState = 'shop';
                }}
            }} else if (gameState === 'level_select') {{
                for (let i = 1; i <= 5; i++) {{
                    if (mouseX >= 20 && mouseX <= 380 && mouseY >= (55 + i * 68) && mouseY <= (110 + i * 68)) {{
                        resetGame(i);
                    }}
                }}
                if (mouseX >= 20 && mouseX <= 130 && mouseY >= 15 && mouseY <= 50) {{
                    gameState = 'menu';
                }}
            }} else if (gameState === 'shop') {{
                if (mouseX >= 20 && mouseX <= 130 && mouseY >= 15 && mouseY <= 50) {{
                    gameState = 'menu';
                }}
                let keys = Object.keys(skins);
                for (let i = 0; i < keys.length; i++) {{
                    let skinKey = keys[i];
                    if (mouseX >= 15 && mouseX <= 385 && mouseY >= (75 + i * 88) && mouseY <= (153 + i * 88)) {{
                        if (unlockedSkins.includes(skinKey)) {{
                            currentSkin = skinKey;
                            localStorage.setItem("tom_current_skin", currentSkin);
                        }} else {{
                            pendingBuySkinKey = skinKey;
                        }}
                    }}
                }}
            }} else if (gameState === 'playing') {{
                bird.velocity = bird.lift;
            }} else if (gameState === 'gameover' || levelCompleted) {{
                gameState = 'level_select';
            }}
        }});

        function spawnPipe() {{
            let lvl = levels[currentLevel];
            let topHeight = Math.floor(Math.random() * (canvas.height - lvl.gap - 130)) + 40;
            pipes.push({{
                x: canvas.width,
                top: topHeight,
                bottom: canvas.height - topHeight - lvl.gap,
                width: 58,
                passed: false
            }});
        }}

        function update() {{
            if (gameState !== 'playing' || pendingBuySkinKey) return;

            let lvl = levels[currentLevel];
            bird.velocity += bird.gravity;
            bird.y += bird.velocity;

            if (bird.y + bird.height >= canvas.height - 45 || bird.y <= 0) {{
                gameState = 'gameover';
            }}

            if (frameCount % lvl.spawnRate === 0) {{
                spawnPipe();
            }}

            let hitboxPaddingX = 20;
            let hitboxPaddingY = 12;

            for (let i = pipes.length - 1; i >= 0; i--) {{
                pipes[i].x -= lvl.speed;

                if (
                    (bird.x + hitboxPaddingX) < pipes[i].x + pipes[i].width &&
                    (bird.x + bird.width - hitboxPaddingX) > pipes[i].x &&
                    ((bird.y + hitboxPaddingY) < pipes[i].top || (bird.y + bird.height - hitboxPaddingY) > canvas.height - pipes[i].bottom - 45)
                ) {{
                    gameState = 'gameover';
                }}

                if (!pipes[i].passed && pipes[i].x + pipes[i].width < bird.x) {{
                    score++;
                    pipes[i].passed = true;

                    if (score >= lvl.targetScore && !levelCompleted) {{
                        levelCompleted = true;
                        coinsEarnedThisRun = lvl.reward;
                        totalCoins += coinsEarnedThisRun;
                        localStorage.setItem("tom_coins", totalCoins);
                    }}
                }}

                if (pipes[i].x + pipes[i].width < 0) {{
                    pipes.splice(i, 1);
                }}
            }}

            frameCount++;
        }}

        function drawBackground() {{
            if (bgImage.src !== "" && bgImage.complete && bgImage.naturalWidth !== 0) {{
                ctx.drawImage(bgImage, 0, 0, canvas.width, canvas.height);
            }} else {{
                ctx.fillStyle = "#4FB7DB";
                ctx.fillRect(0, 0, canvas.width, canvas.height);
            }}
        }}

        function drawPixelText(text, x, y, size, align = "center", textColor = "#FFFFFF") {{
            ctx.font = size + "px 'Press Start 2P', sans-serif";
            ctx.textAlign = align;
            ctx.fillStyle = "#000000";
            ctx.lineWidth = Math.max(4, Math.floor(size / 3));
            ctx.strokeText(text, x, y);
            ctx.fillStyle = textColor;
            ctx.fillText(text, x, y);
        }}

        function drawPixelPipeSection(x, y, w, h, isCap = false) {{
            ctx.fillStyle = "#73BF2E";
            ctx.fillRect(x, y, w, h);

            ctx.fillStyle = "#B5E61D";
            ctx.fillRect(x + 6, y, 8, h);

            ctx.fillStyle = "#FFFFFF";
            ctx.fillRect(x + 8, y, 2, h);

            ctx.fillStyle = "#3F7A00";
            ctx.fillRect(x + w - 14, y, 8, h);

            ctx.fillStyle = "#1E4700";
            ctx.fillRect(x + w - 6, y, 6, h);

            ctx.strokeStyle = "#000000";
            ctx.lineWidth = 3;
            ctx.strokeRect(x, y, w, h);
        }}

        function drawPixelPipe(x, topHeight, bottomHeight) {{
            const pipeW = 56;
            const capW = 66;
            const capH = 24;
            const capOffsetX = (capW - pipeW) / 2;

            if (topHeight > capH) {{
                drawPixelPipeSection(x, 0, pipeW, topHeight - capH);
                drawPixelPipeSection(x - capOffsetX, topHeight - capH, capW, capH, true);
            }} else {{
                drawPixelPipeSection(x - capOffsetX, 0, capW, topHeight, true);
            }}

            const bottomY = canvas.height - bottomHeight - 45;
            if (bottomHeight > capH) {{
                drawPixelPipeSection(x - capOffsetX, bottomY, capW, capH, true);
                drawPixelPipeSection(x, bottomY + capH, pipeW, bottomHeight - capH);
            }} else {{
                drawPixelPipeSection(x - capOffsetX, bottomY, capW, bottomHeight, true);
            }}
        }}

        function drawBird() {{
            let imgToDraw = cleanedSkinCanvases[currentSkin] || skinImages[currentSkin];
            if (imgToDraw && (imgToDraw.complete || imgToDraw.width)) {{
                ctx.imageSmoothingEnabled = false;
                ctx.drawImage(imgToDraw, bird.x, bird.y, bird.width, bird.height);
            }} else {{
                ctx.fillStyle = skins[currentSkin].color;
                ctx.fillRect(bird.x, bird.y, bird.width, bird.height);
                ctx.strokeStyle = "#000";
                ctx.lineWidth = 3;
                ctx.strokeRect(bird.x, bird.y, bird.width, bird.height);
            }}
        }}

        function drawConfirmationModal() {{
            if (!pendingBuySkinKey) return;
            let skin = skins[pendingBuySkinKey];
            let t = i18n[currentLang];

            ctx.fillStyle = "rgba(0, 0, 0, 0.85)";
            ctx.fillRect(0, 0, canvas.width, canvas.height);

            ctx.fillStyle = "#2C3E50";
            ctx.fillRect(15, 65, 370, 345);
            ctx.strokeStyle = "#FFFFFF";
            ctx.lineWidth = 4;
            ctx.strokeRect(15, 65, 370, 345);

            drawPixelText(t.confirmTitle, canvas.width / 2, 102, 13, "center", "#F1C40F");

            let imgPreview = cleanedSkinCanvases[pendingBuySkinKey] || skinImages[pendingBuySkinKey];
            if (imgPreview && (imgPreview.complete || imgPreview.width)) {{
                ctx.imageSmoothingEnabled = false;
                ctx.fillStyle = "rgba(0,0,0,0.6)";
                ctx.fillRect(130, 120, 140, 85);
                ctx.strokeStyle = "#F1C40F";
                ctx.lineWidth = 3;
                ctx.strokeRect(130, 120, 140, 85);
                ctx.drawImage(imgPreview, 135, 125, 130, 75);
            }}

            drawPixelText(t.confirmAsk, canvas.width / 2, 235, 10);
            drawPixelText(skin.name, canvas.width / 2, 265, 12, "center", "#3498DB");
            drawPixelText(t.price + skin.price, canvas.width / 2, 295, 12, "center", "#F1C40F");

            // Nút MUA
            ctx.fillStyle = "#27AE60";
            ctx.fillRect(40, 330, 140, 50);
            ctx.strokeStyle = "#000";
            ctx.lineWidth = 3;
            ctx.strokeRect(40, 330, 140, 50);
            drawPixelText(t.buy, 110, 363, 14);

            // Nút HỦY
            ctx.fillStyle = "#C0392B";
            ctx.fillRect(220, 330, 140, 50);
            ctx.strokeRect(220, 330, 140, 50);
            drawPixelText(t.cancel, 290, 363, 14);
        }}

        function draw() {{
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            let t = i18n[currentLang];

            if (gameState === 'menu') {{
                drawBackground();
                drawPixelText("JOURNEY OF TOM", canvas.width / 2, 110, 17, "center", "#F1C40F");
                drawPixelText(t.coins + totalCoins, canvas.width / 2, 165, 14);

                // Nút chuyển đổi Ngôn ngữ góc trên
                ctx.fillStyle = "#8E44AD";
                ctx.fillRect(280, 15, 100, 35);
                ctx.strokeStyle = "#FFF";
                ctx.lineWidth = 3;
                ctx.strokeRect(280, 15, 100, 35);
                drawPixelText((currentLang === "vi" ? "🌐 VI" : "🌐 EN"), 330, 38, 10);

                // Nút Chơi Game
                ctx.fillStyle = "#27AE60";
                ctx.fillRect(60, 210, 280, 60);
                ctx.strokeStyle = "#000";
                ctx.lineWidth = 4;
                ctx.strokeRect(60, 210, 280, 60);
                drawPixelText(t.play, canvas.width / 2, 248, 14);

                // Nút Cửa Hàng
                ctx.fillStyle = "#2980B9";
                ctx.fillRect(60, 290, 280, 60);
                ctx.strokeRect(60, 290, 280, 60);
                drawPixelText(t.shop, canvas.width / 2, 328, 14);

            }} else if (gameState === 'level_select') {{
                drawBackground();
                drawPixelText(t.selectLevel, canvas.width / 2, 42, 17, "center", "#F1C40F");

                // Nút Lùi
                ctx.fillStyle = "#7F8C8D";
                ctx.fillRect(20, 15, 110, 35);
                ctx.strokeStyle = "#000";
                ctx.lineWidth = 3;
                ctx.strokeRect(20, 15, 110, 35);
                drawPixelText(t.back, 75, 38, 10);

                for (let i = 1; i <= 5; i++) {{
                    let lvl = levels[i];
                    ctx.fillStyle = "rgba(0, 0, 0, 0.8)";
                    ctx.fillRect(20, 55 + i * 68, 360, 53);
                    ctx.strokeRect(20, 55 + i * 68, 360, 53);

                    drawPixelText(t.lvlNames[i], 35, 82 + i * 68, 10, "left");
                    drawPixelText(t.target + lvl.targetScore + " | " + t.reward + lvl.reward, 35, 99 + i * 68, 8, "left", "#F1C40F");
                }}

            }} else if (gameState === 'shop') {{
                drawBackground();
                drawPixelText(t.shop, canvas.width / 2, 38, 17, "center", "#F1C40F");
                drawPixelText(t.coins + totalCoins, canvas.width / 2, 63, 11);

                // Nút Lùi
                ctx.fillStyle = "#7F8C8D";
                ctx.fillRect(20, 15, 110, 35);
                ctx.strokeStyle = "#000";
                ctx.lineWidth = 3;
                ctx.strokeRect(20, 15, 110, 35);
                drawPixelText(t.back, 75, 38, 10);

                let keys = Object.keys(skins);
                for (let i = 0; i < keys.length; i++) {{
                    let skinKey = keys[i];
                    let skin = skins[skinKey];
                    let isUnlocked = unlockedSkins.includes(skinKey);
                    let isSelected = (currentSkin === skinKey);

                    ctx.fillStyle = isSelected ? "#27AE60" : "rgba(0, 0, 0, 0.8)";
                    ctx.fillRect(15, 75 + i * 88, 370, 78);
                    ctx.strokeStyle = isSelected ? "#2ECC71" : "#000";
                    ctx.lineWidth = 3;
                    ctx.strokeRect(15, 75 + i * 88, 370, 78);

                    let imgPreview = cleanedSkinCanvases[skinKey] || skinImages[skinKey];
                    if (imgPreview && (imgPreview.complete || imgPreview.width)) {{
                        ctx.imageSmoothingEnabled = false;
                        ctx.drawImage(imgPreview, 25, 86 + i * 88, 65, 42);
                    }} else {{
                        ctx.fillStyle = skin.color;
                        ctx.fillRect(30, 90 + i * 88, 35, 35);
                        ctx.strokeStyle = "#000";
                        ctx.strokeRect(30, 90 + i * 88, 35, 35);
                    }}

                    drawPixelText(skin.name, 102, 106 + i * 88, 10, "left");

                    if (isSelected) {{
                        drawPixelText(t.using, 102, 134 + i * 88, 10, "left", "#2ECC71");
                    }} else if (isUnlocked) {{
                        drawPixelText(t.owned, 102, 134 + i * 88, 10, "left", "#AED6F1");
                    }} else {{
                        drawPixelText(t.price + skin.price, 102, 134 + i * 88, 10, "left", "#F1C40F");
                    }}
                }}

                drawConfirmationModal();

            }} else if (gameState === 'playing' || gameState === 'gameover' || levelCompleted) {{
                drawBackground();

                let lvl = levels[currentLevel];
                for (let i = 0; i < pipes.length; i++) {{
                    drawPixelPipe(pipes[i].x, pipes[i].top, pipes[i].bottom);
                }}

                drawBird();

                drawPixelText("LVL:" + currentLevel + " | " + score + "/" + lvl.targetScore, 15, 30, 10, "left");
                drawPixelText("🪙 " + totalCoins, 385, 30, 10, "right");

                if (gameState === 'gameover') {{
                    ctx.fillStyle = "rgba(0, 0, 0, 0.82)";
                    ctx.fillRect(0, 0, canvas.width, canvas.height);
                    drawPixelText(t.failed, canvas.width / 2, 210, 20, "center", "#E74C3C");
                    drawPixelText(t.retry, canvas.width / 2, 260, 9);
                }}

                if (levelCompleted) {{
                    ctx.fillStyle = "rgba(0, 0, 0, 0.82)";
                    ctx.fillRect(0, 0, canvas.width, canvas.height);
                    drawPixelText(t.completed, canvas.width / 2, 185, 17, "center", "#2ECC71");
                    drawPixelText(t.earned + coinsEarnedThisRun, canvas.width / 2, 230, 11, "center", "#F1C40F");
                    drawPixelText(t.continue, canvas.width / 2, 280, 9);
                }}
            }}
        }}

        function loop() {{
            update();
            draw();
            requestAnimationFrame(loop);
        }}

        loop();
    </script>
</body>
</html>
"""

st.components.v1.html(flappy_bird_html, height=540)
