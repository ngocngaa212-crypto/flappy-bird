import streamlit as st
import base64
import os

st.set_page_config(page_title="The journey of Tom", page_icon="🐱", layout="centered")

st.title("🐱 The journey of Tom - Pixel Edition")
st.write("Hành trình của Tom - Bảng hướng dẫn hoàn chỉnh chi tiết!")

def get_image_base64(image_path):
    if os.path.exists(image_path):
        with open(image_path, "rb") as img_file:
            encoded = base64.b64encode(img_file.read()).decode()
            return f"data:image/png;base64,{encoded}"
    return ""

# Đọc các file ảnh từ thư mục GitHub
bg_data_url = get_image_base64("background.png")
bg2_data_url = get_image_base64("background2.png")
normal_data_url = get_image_base64("cat_normal.png") if os.path.exists("cat_normal.png") else get_image_base64("bird.png")

rainbow_data_url = get_image_base64("rainbow_Tom.png")
donut_data_url = get_image_base64("Tom_with_donut.png")
strong_data_url = get_image_base64("super_strong_Tom.png")
angela_data_url = get_image_base64("angela.png")

flappy_bird_html = f"""
<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <title>The journey of Tom</title>
    <link href="https://fonts.googleapis.com/css2?family=VT323&display=swap" rel="stylesheet">
    <style>
        body {{
            margin: 0;
            background: #111;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            font-family: 'VT323', monospace;
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

        const bgImage1 = new Image();
        bgImage1.src = "{bg_data_url}";

        const bgImage2 = new Image();
        bgImage2.src = "{bg2_data_url}";

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

        const angelaImage = new Image();
        angelaImage.src = "{angela_data_url}";

        const cleanedSkinCanvases = {{}};
        let cleanedAngelaCanvas = null;

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

        angelaImage.onload = function() {{
            let c = document.createElement('canvas');
            c.width = angelaImage.width;
            c.height = angelaImage.height;
            let tCtx = c.getContext('2d');
            tCtx.drawImage(angelaImage, 0, 0);
            try {{
                let imgData = tCtx.getImageData(0, 0, angelaImage.width, angelaImage.height);
                let data = imgData.data;
                for (let i = 0; i < data.length; i += 4) {{
                    let r = data[i], g = data[i+1], b = data[i+2];
                    if (r < 25 && g < 25 && b < 25) {{
                        data[i + 3] = 0;
                    }}
                }}
                tCtx.putImageData(imgData, 0, 0);
                cleanedAngelaCanvas = c;
            }} catch(e) {{
                cleanedAngelaCanvas = angelaImage;
            }}
        }};

        let currentLang = localStorage.getItem("tom_lang") || "vi";

        const i18n = {{
            "vi": {{
                play: "CHƠI GAME",
                shop: "CỬA HÀNG",
                selectLevel: "CHỌN CẤP ĐỘ",
                back: "<- LÙI",
                coins: "XU: ",
                target: "Mục tiêu: ",
                reward: "Phần thưởng dành cho bạn: ",
                using: "ĐANG DÙNG",
                owned: "ĐÃ SỞ HỮU",
                price: "GIÁ: ",
                confirmTitle: "XÁC NHẬN MUA",
                confirmAsk: "Bạn có chắc muốn mua?",
                buy: "MUA",
                cancel: "HỦY",
                failed: "THẤT BẠI!",
                retry: "Nhấn Space để chọn lại",
                passLevel: "CHÚC MỪNG BẠN ĐÃ VƯỢT ẢI ",
                meetAngelaLine1: "Hoàn thành màn 5 để giúp Tom",
                meetAngelaLine2: "gặp được tình yêu của anh ấy",
                continue: "Nhấn Space để tiếp tục",
                notEnoughCoins: "Bạn không đủ tiền xu!",
                locked: "🔒 BỊ KHÓA",
                unlockedNext: "Đã mở khóa Cấp tiếp theo!",
                guideTitle: "HƯỚNG DẪN CÁCH CHƠI",
                guideStep1: "• Nhấn SPACE hoặc chạm để Tom",
                guideStep2: "  bay lên né các ống nước.",
                guideStep3: "• Đạt điểm mục tiêu để mở màn mới.",
                guideStep4: "• Sau 60 giây, hình nền sẽ đổi.",
                guideStep5: "• Tích xu để đổi các skin của Tom.",
                guideStep6: "• Hoàn thành màn 5 để giúp Tom",
                guideStep7: "  gặp được tình yêu của anh ấy.",
                guideWish: "Chúc bạn chơi game vui vẻ!",
                closeBtn: "ĐÓNG",
                lvlNames: {{
                    1: "CẤP 1: KHỞI ĐẦU",
                    2: "CẤP 2: VƯỢT THÁC",
                    3: "CẤP 3: RỪNG SÂU",
                    4: "CẤP 4: THỬ THÁCH",
                    5: "CẤP 5: GẶP ANGELA"
                }}
            }},
            "en": {{
                play: "PLAY GAME",
                shop: "SKIN SHOP",
                selectLevel: "SELECT LEVEL",
                back: "<- BACK",
                coins: "COINS: ",
                target: "Target: ",
                reward: "Reward for you: ",
                using: "EQUIPPED",
                owned: "OWNED",
                price: "PRICE: ",
                confirmTitle: "CONFIRM PURCHASE",
                confirmAsk: "Are you sure you want to buy?",
                buy: "BUY",
                cancel: "CANCEL",
                failed: "GAME OVER!",
                retry: "Press Space to retry",
                passLevel: "CONGRATULATIONS ON CLEARING LEVEL ",
                meetAngelaLine1: "Completed Level 5 to help Tom",
                meetAngelaLine2: "meet the love of his life",
                continue: "Press Space to continue",
                notEnoughCoins: "Not enough coins!",
                locked: "🔒 LOCKED",
                unlockedNext: "Unlocked Next Level!",
                guideTitle: "GAME GUIDE",
                guideStep1: "• Press SPACE or click to make Tom",
                guideStep2: "  fly up and dodge pipes.",
                guideStep3: "• Reach target scores to unlock levels.",
                guideStep4: "• After 60s, background will change.",
                guideStep5: "• Collect coins to change Tom's skins.",
                guideStep6: "• Complete Level 5 to help Tom",
                guideStep7: "  meet the love of his life.",
                guideWish: "Have fun playing the game!",
                closeBtn: "CLOSE",
                lvlNames: {{
                    1: "LEVEL 1: BEGINNING",
                    2: "LEVEL 2: WATERFALL",
                    3: "LEVEL 3: DEEP FOREST",
                    4: "LEVEL 4: CHALLENGE",
                    5: "LEVEL 5: MEET ANGELA"
                }}
            }}
        }};

        let totalCoins = parseInt(localStorage.getItem("tom_coins")) || 0;
        let unlockedSkins = JSON.parse(localStorage.getItem("tom_skins")) || ["normal"];
        let currentSkin = localStorage.getItem("tom_current_skin") || "normal";
        let unlockedLevel = parseInt(localStorage.getItem("tom_unlocked_level")) || 1;

        const skins = {{
            "normal": {{ name: "normal tom", price: 0, color: "#F4D03F" }},
            "rainbow": {{ name: "rainbow Tom", price: 50, color: "#9B59B6" }},
            "donut": {{ name: "Tom with donut", price: 100, color: "#E75480" }},
            "strong": {{ name: "Super strong Tom", price: 170, color: "#E74C3C" }}
        }};

        let gameState = 'menu';
        let pendingBuySkinKey = null;
        let showGuideModal = false;

        let bird = {{
            x: 30,
            y: 150,
            width: 125,
            height: 75,
            gravity: 0.35, 
            lift: -7.5,     
            velocity: 0
        }};

        let currentLevel = 1;
        const levels = {{
            1: {{ speed: 1.2, gap: 240, spawnRate: 130, targetScore: 10, reward: 15 }},
            2: {{ speed: 1.35, gap: 230, spawnRate: 120, targetScore: 20, reward: 30 }},
            3: {{ speed: 1.5, gap: 220, spawnRate: 110, targetScore: 30, reward: 50 }},
            4: {{ speed: 1.65, gap: 210, spawnRate: 100, targetScore: 40, reward: 80 }},
            5: {{ speed: 1.8, gap: 200, spawnRate: 90, targetScore: 50, reward: 120 }}
        }};

        let pipes = [];
        let frameCount = 0;
        let score = 0;
        let coinsEarnedThisRun = 0;
        let levelCompleted = false;
        let playStartTime = 0;

        function resetGame(level) {{
            currentLevel = level;
            bird.y = 150;
            bird.velocity = 0;
            pipes = [];
            score = 0;
            coinsEarnedThisRun = 0;
            frameCount = 0;
            levelCompleted = false;
            playStartTime = Date.now();
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

            if (gameState === 'menu') {{
                if (mouseX >= 270 && mouseX <= 360 && mouseY >= 15 && mouseY <= 53) {{
                    currentLang = (currentLang === "vi") ? "en" : "vi";
                    localStorage.setItem("tom_lang", currentLang);
                    return;
                }}
                if (mouseX >= 215 && mouseX <= 255 && mouseY >= 15 && mouseY <= 53) {{
                    showGuideModal = true;
                    return;
                }}
            }}

            if (showGuideModal) {{
                if (mouseX >= 130 && mouseX <= 270 && mouseY >= 415 && mouseY <= 460) {{
                    showGuideModal = false;
                }}
                return;
            }}

            if (pendingBuySkinKey) {{
                let t = i18n[currentLang];
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
                        if (i <= unlockedLevel) {{
                            resetGame(i);
                        }}
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
            if (gameState !== 'playing' || pendingBuySkinKey || showGuideModal) return;

            let lvl = levels[currentLevel];
            bird.velocity += bird.gravity;
            bird.y += bird.velocity;

            if (bird.y + bird.height >= canvas.height - 45 || bird.y <= 0) {{
                gameState = 'gameover';
            }}

            if (frameCount % lvl.spawnRate === 0) {{
                spawnPipe();
            }}

            let hitboxPaddingX = 22;
            let hitboxPaddingY = 14;

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

                        if (currentLevel === unlockedLevel && unlockedLevel < 5) {{
                            unlockedLevel++;
                            localStorage.setItem("tom_unlocked_level", unlockedLevel);
                        }}
                    }}
                }}

                if (pipes[i].x + pipes[i].width < 0) {{
                    pipes.splice(i, 1);
                }}
            }}

            frameCount++;
        }}

        function drawBackground() {{
            let activeBg = bgImage1;
            if (gameState === 'playing' && playStartTime > 0) {{
                let elapsedSeconds = (Date.now() - playStartTime) / 1000;
                if (elapsedSeconds >= 60 && bgImage2.complete && bgImage2.naturalWidth !== 0) {{
                    activeBg = bgImage2;
                }}
            }}

            if (activeBg.src !== "" && activeBg.complete && activeBg.naturalWidth !== 0) {{
                ctx.drawImage(activeBg, 0, 0, canvas.width, canvas.height);
            }} else {{
                ctx.fillStyle = "#4FB7DB";
                ctx.fillRect(0, 0, canvas.width, canvas.height);
            }}
        }}

        function drawTomCoinIcon(x, y, radius = 10) {{
            ctx.save();
            ctx.fillStyle = "#D4AC0D";
            ctx.beginPath();
            ctx.arc(x, y, radius, 0, Math.PI * 2);
            ctx.fill();

            ctx.fillStyle = "#F4D03F";
            ctx.beginPath();
            ctx.arc(x, y, radius - 2, 0, Math.PI * 2);
            ctx.fill();

            let scale = radius / 10;
            ctx.fillStyle = "#99A3A4";
            ctx.fillRect(x - 5 * scale, y - 6 * scale, 3 * scale, 3 * scale);
            ctx.fillRect(x + 2 * scale, y - 6 * scale, 3 * scale, 3 * scale);
            ctx.fillRect(x - 5 * scale, y - 3 * scale, 10 * scale, 6 * scale);
            ctx.fillStyle = "#000000";
            ctx.fillRect(x - 3 * scale, y - 2 * scale, 2 * scale, 2 * scale);
            ctx.fillRect(x + 1 * scale, y - 2 * scale, 2 * scale, 2 * scale);
            ctx.fillStyle = "#E74C3C";
            ctx.fillRect(x - 1 * scale, y + 1 * scale, 2 * scale, 1 * scale);
            ctx.restore();
        }}

        function drawPixelText(text, x, y, size, align = "center", textColor = "#FFFFFF") {{
            ctx.font = size + "px 'VT323', monospace";
            ctx.textAlign = align;
            ctx.fillStyle = "#000000";
            ctx.lineWidth = Math.max(3, Math.floor(size / 6));
            ctx.strokeText(text, x, y);
            ctx.fillStyle = textColor;
            ctx.fillText(text, x, y);
        }}

        function drawCleanText(text, x, y, size, align = "center", textColor = "#2C3E50") {{
            ctx.font = size + "px 'VT323', monospace";
            ctx.textAlign = align;
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

        function drawGuideModal() {{
            if (!showGuideModal) return;
            let t = i18n[currentLang];

            ctx.fillStyle = "rgba(0, 0, 0, 0.85)";
            ctx.fillRect(0, 0, canvas.width, canvas.height);

            ctx.fillStyle = "#FFFFFF";
            ctx.fillRect(15, 25, 370, 450);
            ctx.strokeStyle = "#2C3E50";
            ctx.lineWidth = 4;
            ctx.strokeRect(15, 25, 370, 450);

            drawCleanText(t.guideTitle, canvas.width / 2, 60, 28, "center", "#1B4F72");

            let startY = 95;
            let stepGap = 35;
            drawCleanText(t.guideStep1, 25, startY, 20, "left", "#2C3E50");
            drawCleanText(t.guideStep2, 25, startY + stepGap, 20, "left", "#2C3E50");
            drawCleanText(t.guideStep3, 25, startY + stepGap * 2, 20, "left", "#2C3E50");
            drawCleanText(t.guideStep4, 25, startY + stepGap * 3, 20, "left", "#2C3E50");
            drawCleanText(t.guideStep5, 25, startY + stepGap * 4, 20, "left", "#2C3E50");
            drawCleanText(t.guideStep6, 25, startY + stepGap * 5, 20, "left", "#2C3E50");
            drawCleanText(t.guideStep7, 25, startY + stepGap * 6, 20, "left", "#2C3E50");

            drawCleanText(t.guideWish, canvas.width / 2, 390, 22, "center", "#C0392B");

            ctx.fillStyle = "#E74C3C";
            ctx.fillRect(130, 415, 140, 45);
            ctx.strokeStyle = "#000";
            ctx.lineWidth = 2;
            ctx.strokeRect(130, 415, 140, 45);
            drawPixelText(t.closeBtn, 200, 445, 22);
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

            drawPixelText(t.confirmTitle, canvas.width / 2, 105, 26, "center", "#F1C40F");

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

            drawPixelText(t.confirmAsk, canvas.width / 2, 240, 22);
            drawPixelText(skin.name, canvas.width / 2, 270, 24, "center", "#3498DB");
            
            drawPixelText(t.price + skin.price, canvas.width / 2 - 12, 300, 24, "center", "#F1C40F");
            drawTomCoinIcon(canvas.width / 2 + 55, 293, 11);

            ctx.fillStyle = "#27AE60";
            ctx.fillRect(40, 330, 140, 50);
            ctx.strokeStyle = "#000";
            ctx.lineWidth = 3;
            ctx.strokeRect(40, 330, 140, 50);
            drawPixelText(t.buy, 110, 363, 26);

            ctx.fillStyle = "#C0392B";
            ctx.fillRect(220, 330, 140, 50);
            ctx.strokeStyle = "#000";
            ctx.lineWidth = 3;
            ctx.strokeRect(220, 330, 140, 50);
            drawPixelText(t.cancel, 290, 363, 26);
        }}

        function draw() {{
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            let t = i18n[currentLang];

            if (gameState === 'menu') {{
                drawBackground();
                drawPixelText("JOURNEY OF TOM", canvas.width / 2, 115, 32, "center", "#F1C40F");
                
                drawPixelText(t.coins + totalCoins, canvas.width / 2 - 10, 165, 24);
                drawTomCoinIcon(canvas.width / 2 + 52, 157, 11);

                ctx.fillStyle = "#D35400";
                ctx.fillRect(215, 15, 42, 38);
                ctx.strokeStyle = "#FFF";
                ctx.lineWidth = 3;
                ctx.strokeRect(215, 15, 42, 38);
                drawPixelText("📖", 236, 41, 20);

                ctx.fillStyle = "#8E44AD";
                ctx.fillRect(270, 15, 90, 38);
                ctx.strokeStyle = "#FFF";
                ctx.lineWidth = 3;
                ctx.strokeRect(270, 15, 90, 38);
                drawPixelText((currentLang === "vi" ? "🌐 VI" : "🌐 EN"), 315, 40, 18);

                ctx.fillStyle = "#27AE60";
                ctx.fillRect(60, 210, 280, 60);
                ctx.strokeStyle = "#000";
                ctx.lineWidth = 4;
                ctx.strokeRect(60, 210, 280, 60);
                drawPixelText(t.play, canvas.width / 2, 250, 26);

                ctx.fillStyle = "#2980B9";
                ctx.fillRect(60, 290, 280, 60);
                ctx.strokeRect(60, 290, 280, 60);
                drawPixelText(t.shop, canvas.width / 2, 330, 26);

                drawGuideModal();

            }} else if (gameState === 'level_select') {{
                drawBackground();
                drawPixelText(t.selectLevel, canvas.width / 2, 42, 30, "center", "#F1C40F");

                ctx.fillStyle = "#7F8C8D";
                ctx.fillRect(20, 15, 110, 38);
                ctx.strokeStyle = "#000";
                ctx.lineWidth = 3;
                ctx.strokeRect(20, 15, 110, 38);
                drawPixelText(t.back, 75, 40, 20);

                for (let i = 1; i <= 5; i++) {{
                    let lvl = levels[i];
                    let isUnlocked = (i <= unlockedLevel);

                    ctx.fillStyle = isUnlocked ? "rgba(0, 0, 0, 0.8)" : "rgba(50, 50, 50, 0.85)";
                    ctx.fillRect(20, 55 + i * 68, 360, 53);
                    ctx.strokeStyle = isUnlocked ? "#2ECC71" : "#555";
                    ctx.lineWidth = 3;
                    ctx.strokeRect(20, 55 + i * 68, 360, 53);

                    if (isUnlocked) {{
                        drawPixelText(t.lvlNames[i], 35, 80 + i * 68, 22, "left");
                        drawPixelText(t.target + lvl.targetScore + " | Phần thưởng: " + lvl.reward, 35, 100 + i * 68, 16, "left", "#F1C40F");
                        drawTomCoinIcon(325, 93 + i * 68, 8);
                    }} else {{
                        drawPixelText(t.lvlNames[i], 35, 80 + i * 68, 22, "left", "#888");
                        drawPixelText(t.locked, 35, 100 + i * 68, 18, "left", "#E74C3C");
                    }}
                }}

            }} else if (gameState === 'shop') {{
                drawBackground();
                drawPixelText(t.shop, canvas.width / 2, 38, 30, "center", "#F1C40F");
                drawPixelText(t.coins + totalCoins, canvas.width / 2 - 10, 65, 20);
                drawTomCoinIcon(canvas.width / 2 + 48, 58, 10);

                ctx.fillStyle = "#7F8C8D";
                ctx.fillRect(20, 15, 110, 38);
                ctx.strokeStyle = "#000";
                ctx.lineWidth = 3;
                ctx.strokeRect(20, 15, 110, 38);
                drawPixelText(t.back, 75, 40, 20);

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

                    drawPixelText(skin.name, 102, 106 + i * 88, 22, "left");

                    if (isSelected) {{
                        drawPixelText(t.using, 102, 134 + i * 88, 20, "left", "#2ECC71");
                    }} else if (isUnlocked) {{
                        drawPixelText(t.owned, 102, 134 + i * 88, 20, "left", "#AED6F1");
                    }} else {{
                        drawPixelText(t.price + skin.price, 102, 134 + i * 88, 20, "left", "#F1C40F");
                        drawTomCoinIcon(225 + skin.price.toString().length * 10, 127 + i * 88, 8);
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

                drawPixelText("LVL:" + currentLevel + " | " + score + "/" + lvl.targetScore, 15, 30, 22, "left");
                
                drawPixelText(totalCoins.toString(), 360, 30, 22, "right");
                drawTomCoinIcon(375, 23, 10);

                if (gameState === 'gameover') {{
                    ctx.fillStyle = "rgba(0, 0, 0, 0.82)";
                    ctx.fillRect(0, 0, canvas.width, canvas.height);
                    drawPixelText(t.failed, canvas.width / 2, 210, 36, "center", "#E74C3C");
                    drawPixelText(t.retry, canvas.width / 2, 260, 20);
                }}

                if (levelCompleted) {{
                    ctx.fillStyle = "rgba(0, 0, 0, 0.85)";
                    ctx.fillRect(0, 0, canvas.width, canvas.height);

                    if (currentLevel === 5) {{
                        drawPixelText(t.meetAngelaLine1, canvas.width / 2, 75, 22, "center", "#F1C40F");
                        drawPixelText(t.meetAngelaLine2, canvas.width / 2, 100, 22, "center", "#F1C40F");

                        ctx.imageSmoothingEnabled = false;
                        let tomImg = cleanedSkinCanvases[currentSkin] || skinImages[currentSkin];
                        if (tomImg && (tomImg.complete || tomImg.width)) {{
                            ctx.drawImage(tomImg, 90, 130, 100, 60);
                        }}
                        let angelaImgToDraw = cleanedAngelaCanvas || angelaImage;
                        if (angelaImgToDraw && (angelaImgToDraw.complete || angelaImgToDraw.width)) {{
                            ctx.drawImage(angelaImgToDraw, 210, 130, 100, 60);
                        }} else {{
                            ctx.fillStyle = "#FFC0CB";
                            ctx.fillRect(210, 130, 100, 60);
                        }}

                        drawPixelText(t.reward + coinsEarnedThisRun, canvas.width / 2 - 15, 230, 22, "center", "#2ECC71");
                        drawTomCoinIcon(canvas.width / 2 + 115, 223, 10);

                        drawPixelText(t.continue, canvas.width / 2, 290, 22);

                    }} else {{
                        drawPixelText(t.passLevel + currentLevel, canvas.width / 2, 110, 28, "center", "#2ECC71");
                        
                        drawPixelText(t.reward + coinsEarnedThisRun, canvas.width / 2 - 20, 175, 22, "center", "#F1C40F");
                        drawTomCoinIcon(canvas.width / 2 + 105, 168, 10);
                        
                        if (currentLevel < 5) {{
                            drawPixelText(t.unlockedNext, canvas.width / 2, 230, 20, "center", "#3498DB");
                        }}
                        
                        drawPixelText(t.continue, canvas.width / 2, 290, 20);
                    }}
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
