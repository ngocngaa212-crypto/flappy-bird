import streamlit as st
import base64
import os

st.set_page_config(page_title="The journey of Tom", page_icon="🐱", layout="centered")

st.title("🐱 The journey of Tom - Pixel Edition")
st.write("Hành trình của Tom với Cửa hàng nâng cấp & Hộp thoại xác nhận mua Skin!")

def get_image_base64(image_path):
    if os.path.exists(image_path):
        with open(image_path, "rb") as img_file:
            encoded = base64.b64encode(img_file.read()).decode()
            return f"data:image/png;base64,{encoded}"
    return ""

# Đọc các file ảnh từ thư mục GitHub
bg_data_url = get_image_base64("background.png")
normal_data_url = get_image_base64("cat_normal.png") if os.path.exists("cat_normal.png") else get_image_base64("bird.png")

# Đọc 3 file ảnh skin theo đúng tên file
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
        let pendingBuySkinKey = null; // Trạng thái skin đang chờ xác nhận mua

        let bird = {{
            x: 30,
            y: 150,
            width: 125,   /* Phóng to nhân vật Tom trong game */
            height: 75,
            gravity: 0.42, 
            lift: -8.2,      
            velocity: 0
        }};

        let currentLevel = 1;
        const levels = {{
            1: {{ name: "Cấp 1: Khởi Đầu", speed: 1.5, gap: 200, spawnRate: 120, targetScore: 3, reward: 15 }},
            2: {{ name: "Cấp 2: Vượt Thác", speed: 1.8, gap: 190, spawnRate: 110, targetScore: 5, reward: 30 }},
            3: {{ name: "Cấp 3: Rừng Sâu", speed: 2.1, gap: 180, spawnRate: 100, targetScore: 8, reward: 50 }},
            4: {{ name: "Cấp 4: Thử Thách", speed: 2.4, gap: 170, spawnRate: 90, targetScore: 12, reward: 80 }},
            5: {{ name: "Cấp 5: Đỉnh Cao", speed: 2.8, gap: 160, spawnRate: 80, targetScore: 15, reward: 120 }}
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

            if (pendingBuySkinKey) {{
                // Xử lý click trong bảng thông báo xác nhận
                // Nút ĐỒNG Ý MUA (X: 50-180, Y: 330-375)
                if (mouseX >= 50 && mouseX <= 180 && mouseY >= 330 && mouseY <= 375) {{
                    let skin = skins[pendingBuySkinKey];
                    if (totalCoins >= skin.price) {{
                        totalCoins -= skin.price;
                        unlockedSkins.push(pendingBuySkinKey);
                        currentSkin = pendingBuySkinKey;
                        localStorage.setItem("tom_coins", totalCoins);
                        localStorage.setItem("tom_skins", JSON.stringify(unlockedSkins));
                        localStorage.setItem("tom_current_skin", currentSkin);
                    }} else {{
                        alert("Bạn không đủ tiền xu!");
                    }}
                    pendingBuySkinKey = null;
                }}
                // Nút HỦY (X: 220-350, Y: 330-375)
                else if (mouseX >= 220 && mouseX <= 350 && mouseY >= 330 && mouseY <= 375) {{
                    pendingBuySkinKey = null;
                }}
                return;
            }}

            if (gameState === 'menu') {{
                if (mouseX >= 80 && mouseX <= 320 && mouseY >= 220 && mouseY <= 270) {{
                    gameState = 'level_select';
                }}
                if (mouseX >= 80 && mouseX <= 320 && mouseY >= 295 && mouseY <= 345) {{
                    gameState = 'shop';
                }}
            }} else if (gameState === 'level_select') {{
                for (let i = 1; i <= 5; i++) {{
                    if (mouseX >= 30 && mouseX <= 370 && mouseY >= (60 + i * 65) && mouseY <= (108 + i * 65)) {{
                        resetGame(i);
                    }}
                }}
                if (mouseX >= 30 && mouseX <= 130 && mouseY >= 15 && mouseY <= 45) {{
                    gameState = 'menu';
                }}
            }} else if (gameState === 'shop') {{
                if (mouseX >= 20 && mouseX <= 110 && mouseY >= 15 && mouseY <= 43) {{
                    gameState = 'menu';
                }}
                let keys = Object.keys(skins);
                for (let i = 0; i < keys.length; i++) {{
                    let skinKey = keys[i];
                    if (mouseX >= 20 && mouseX <= 380 && mouseY >= (75 + i * 85) && mouseY <= (147 + i * 85)) {{
                        if (unlockedSkins.includes(skinKey)) {{
                            currentSkin = skinKey;
                            localStorage.setItem("tom_current_skin", currentSkin);
                        }} else {{
                            // Mở popup xác nhận mua
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

        function drawPixelText(text, x, y, size, align = "center") {{
            ctx.font = size + "px 'Press Start 2P'";
            ctx.textAlign = align;
            ctx.fillStyle = "#000000";
            ctx.lineWidth = 4;
            ctx.strokeText(text, x, y);
            ctx.fillStyle = "#FFFFFF";
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

            // Phủ lớp xám mờ màn hình
            ctx.fillStyle = "rgba(0, 0, 0, 0.75)";
            ctx.fillRect(0, 0, canvas.width, canvas.height);

            // Bảng thông báo chính
            ctx.fillStyle = "#2C3E50";
            ctx.fillRect(25, 90, 350, 310);
            ctx.strokeStyle = "#FFFFFF";
            ctx.lineWidth = 4;
            ctx.strokeRect(25, 90, 350, 310);

            drawPixelText("XAC NHAN MUA", canvas.width / 2, 125, 12);

            // Hiển thị hình ảnh Skin siêu to, rõ nét ngay giữa bảng
            let imgPreview = cleanedSkinCanvases[pendingBuySkinKey] || skinImages[pendingBuySkinKey];
            if (imgPreview && (imgPreview.complete || imgPreview.width)) {{
                ctx.imageSmoothingEnabled = false;
                // Khung viền cho hình ảnh
                ctx.fillStyle = "rgba(0,0,0,0.5)";
                ctx.fillRect(140, 145, 120, 75);
                ctx.strokeStyle = "#F1C40F";
                ctx.lineWidth = 2;
                ctx.strokeRect(140, 145, 120, 75);
                ctx.drawImage(imgPreview, 145, 150, 110, 65);
            }}

            drawPixelText("Ban co muc mua:", canvas.width / 2, 248, 8);
            
            ctx.font = "9px 'Press Start 2P'";
            ctx.fillStyle = "#3498DB";
            ctx.textAlign = "center";
            ctx.fillText(skin.name + "?", canvas.width / 2, 270);

            ctx.fillStyle = "#F1C40F";
            ctx.fillText("Gia: 🪙 " + skin.price, canvas.width / 2, 295);

            // Nút ĐỒNG Ý MUA
            ctx.fillStyle = "#27AE60";
            ctx.fillRect(50, 330, 130, 45);
            ctx.strokeStyle = "#000";
            ctx.lineWidth = 2;
            ctx.strokeRect(50, 330, 130, 45);
            drawPixelText("MUA", 115, 358, 10);

            // Nút HỦY
            ctx.fillStyle = "#C0392B";
            ctx.fillRect(220, 330, 130, 45);
            ctx.strokeRect(220, 330, 130, 45);
            drawPixelText("HUY", 285, 358, 10);
        }}

        function draw() {{
            ctx.clearRect(0, 0, canvas.width, canvas.height);

            if (gameState === 'menu') {{
                drawBackground();
                drawPixelText("JOURNEY OF TOM", canvas.width / 2, 110, 15);
                drawPixelText("🪙: " + totalCoins, canvas.width / 2, 170, 14);

                ctx.fillStyle = "#27AE60";
                ctx.fillRect(80, 220, 240, 50);
                ctx.strokeStyle = "#000";
                ctx.lineWidth = 3;
                ctx.strokeRect(80, 220, 240, 50);
                drawPixelText("CHOI GAME", canvas.width / 2, 252, 12);

                ctx.fillStyle = "#2980B9";
                ctx.fillRect(80, 295, 240, 50);
                ctx.strokeRect(80, 295, 240, 50);
                drawPixelText("CUA HANG", canvas.width / 2, 327, 12);

            }} else if (gameState === 'level_select') {{
                drawBackground();
                drawPixelText("CHON CAP DO", canvas.width / 2, 40, 15);

                ctx.fillStyle = "#7F8C8D";
                ctx.fillRect(30, 15, 100, 30);
                ctx.strokeRect(30, 15, 100, 30);
                drawPixelText("<- LUI", 80, 35, 9);

                for (let i = 1; i <= 5; i++) {{
                    let lvl = levels[i];
                    ctx.fillStyle = "rgba(0, 0, 0, 0.75)";
                    ctx.fillRect(30, 60 + i * 65, 340, 48);
                    ctx.strokeRect(30, 60 + i * 65, 340, 48);

                    drawPixelText(lvl.name, 45, 87 + i * 65, 9, "left");
                    
                    ctx.font = "7px 'Press Start 2P'";
                    ctx.fillStyle = "#F1C40F";
                    ctx.fillText("Muc tieu:" + lvl.targetScore + " | Thuong:🪙" + lvl.reward, 45, 101 + i * 65);
                }}

            }} else if (gameState === 'shop') {{
                drawBackground();
                drawPixelText("CUA HANG SKIN", canvas.width / 2, 35, 14);
                drawPixelText("🪙 Xu: " + totalCoins, canvas.width / 2, 60, 9);

                ctx.fillStyle = "#7F8C8D";
                ctx.fillRect(20, 15, 90, 28);
                ctx.strokeRect(20, 15, 90, 28);
                drawPixelText("<- LUI", 65, 33, 8);

                let keys = Object.keys(skins);
                for (let i = 0; i < keys.length; i++) {{
                    let skinKey = keys[i];
                    let skin = skins[skinKey];
                    let isUnlocked = unlockedSkins.includes(skinKey);
                    let isSelected = (currentSkin === skinKey);

                    ctx.fillStyle = isSelected ? "#27AE60" : "rgba(0, 0, 0, 0.75)";
                    ctx.fillRect(20, 75 + i * 85, 360, 72);
                    ctx.strokeRect(20, 75 + i * 85, 360, 72);

                    // Xem trước hình ảnh Skin trong Cửa Hàng (Hiển thị to & rõ hơn)
                    let imgPreview = cleanedSkinCanvases[skinKey] || skinImages[skinKey];
                    if (imgPreview && (imgPreview.complete || imgPreview.width)) {{
                        ctx.imageSmoothingEnabled = false;
                        ctx.drawImage(imgPreview, 28, 85 + i * 85, 60, 38);
                    }} else {{
                        ctx.fillStyle = skin.color;
                        ctx.fillRect(35, 90 + i * 85, 30, 30);
                        ctx.strokeStyle = "#000";
                        ctx.strokeRect(35, 90 + i * 85, 30, 30);
                    }}

                    drawPixelText(skin.name, 98, 104 + i * 85, 8, "left");

                    ctx.font = "7px 'Press Start 2P'";
                    if (isSelected) {{
                        ctx.fillStyle = "#2ECC71";
                        ctx.fillText("DANG DUNG", 98, 128 + i * 85);
                    }} else if (isUnlocked) {{
                        ctx.fillStyle = "#AED6F1";
                        ctx.fillText("DA SO HUU", 98, 128 + i * 85);
                    }} else {{
                        ctx.fillStyle = "#F1C40F";
                        ctx.fillText("Gia: 🪙 " + skin.price, 98, 128 + i * 85);
                    }}
                }}

                // Vẽ Bảng xác nhận mua nếu người chơi bấm chọn skin chưa mua
                drawConfirmationModal();

            }} else if (gameState === 'playing' || gameState === 'gameover' || levelCompleted) {{
                drawBackground();

                let lvl = levels[currentLevel];
                for (let i = 0; i < pipes.length; i++) {{
                    drawPixelPipe(pipes[i].x, pipes[i].top, pipes[i].bottom);
                }}

                drawBird();

                drawPixelText("LVL:" + currentLevel + " | DIEM:" + score + "/" + lvl.targetScore, 15, 28, 8, "left");
                drawPixelText("🪙" + totalCoins, 385, 28, 8, "right");

                if (gameState === 'gameover') {{
                    ctx.fillStyle = "rgba(0, 0, 0, 0.8)";
                    ctx.fillRect(0, 0, canvas.width, canvas.height);
                    drawPixelText("THAT BAI!", canvas.width / 2, 210, 20);
                    drawPixelText("Nhan Space de chon lai", canvas.width / 2, 260, 8);
                }}

                if (levelCompleted) {{
                    ctx.fillStyle = "rgba(0, 0, 0, 0.8)";
                    ctx.fillRect(0, 0, canvas.width, canvas.height);
                    drawPixelText("HOAN THANH!", canvas.width / 2, 185, 15);
                    
                    ctx.font = "9px 'Press Start 2P'";
                    ctx.fillStyle = "#F1C40F";
                    ctx.textAlign = "center";
                    ctx.fillText("Thuong: + 🪙 " + coinsEarnedThisRun, canvas.width / 2, 230);
                    
                    drawPixelText("Nhan Space de tiep tuc", canvas.width / 2, 280, 8);
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
