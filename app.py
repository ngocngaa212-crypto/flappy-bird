import streamlit as st
import base64
import os

st.set_page_config(page_title="Flappy Bird Pixel Art", page_icon="🐦", layout="centered")

st.title("🐦 Flappy Bird - Pixel Art Edition")
st.write("Chế độ dễ hơn, phong cách Pixel cổ điển, phông chữ chữ trắng viền đen!")

def get_image_base64(image_path):
    if os.path.exists(image_path):
        with open(image_path, "rb") as img_file:
            encoded = base64.b64encode(img_file.read()).decode()
            return f"data:image/png;base64,{encoded}"
    return ""

bg_data_url = get_image_base64("background.png")
bird_data_url = get_image_base64("bird.png")

flappy_bird_html = f"""
<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <title>Flappy Bird Pixel</title>
    <!-- Nhập phông chữ Pixel chính hiệu từ Google Fonts -->
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
            image-rendering: pixelated; /* Giữ độ sắc nét phong cách pixel */
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

        const birdImage = new Image();
        birdImage.src = "{bird_data_url}";

        let totalCoins = parseInt(localStorage.getItem("fb_coins")) || 0;
        let unlockedSkins = JSON.parse(localStorage.getItem("fb_skins")) || ["default"];
        let currentSkin = localStorage.getItem("fb_current_skin") || "default";

        const skins = {{
            "default": {{ name: "Chim Tùy Chỉnh", price: 0, color: "#F4D03F" }},
            "ninja": {{ name: "Ninja Đen Bí Ẩn", price: 20, color: "#2E4053" }},
            "superman": {{ name: "Siêu Nhân Đỏ", price: 50, color: "#CB4335" }},
            "golden": {{ name: "Chim Thần Hoàng Kim", price: 100, color: "#F39C12" }}
        }};

        let gameState = 'menu';

        let bird = {{
            x: 50,
            y: 150,
            width: 34,
            height: 28,
            gravity: 0.45,   /* Giảm trọng lực để chim bay nhẹ nhàng hơn (Dễ hơn) */
            lift: -8.5,      /* Lực nhảy vừa phải, dễ kiểm soát */
            velocity: 0
        }};

        let currentLevel = 1;
        // Đã tinh chỉnh lại 5 cấp độ CỰC KỲ DỄ THỞ, khoảng cách ống rộng hơn nhiều
        const levels = {{
            1: {{ name: "Cấp 1: Tập Sự", speed: 1.5, gap: 170, spawnRate: 120, targetScore: 3, reward: 10 }},
            2: {{ name: "Cấp 2: Thử Thách", speed: 1.8, gap: 160, spawnRate: 110, targetScore: 5, reward: 20 }},
            3: {{ name: "Cấp 3: Khó Nhằn", speed: 2.1, gap: 150, spawnRate: 100, targetScore: 8, reward: 35 }},
            4: {{ name: "Cấp 4: Chuyên Gia", speed: 2.4, gap: 140, spawnRate: 90, targetScore: 12, reward: 50 }},
            5: {{ name: "Cấp 5: Bậc Thầy", speed: 2.8, gap: 130, spawnRate: 80, targetScore: 15, reward: 100 }}
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

            if (gameState === 'menu') {{
                if (mouseX >= 80 && mouseX <= 320 && mouseY >= 230 && mouseY <= 285) {{
                    gameState = 'level_select';
                }}
                if (mouseX >= 80 && mouseX <= 320 && mouseY >= 310 && mouseY <= 365) {{
                    gameState = 'shop';
                }}
            }} else if (gameState === 'level_select') {{
                for (let i = 1; i <= 5; i++) {{
                    if (mouseX >= 30 && mouseX <= 370 && mouseY >= (65 + i * 65) && mouseY <= (115 + i * 65)) {{
                        resetGame(i);
                    }}
                }}
                if (mouseX >= 30 && mouseX <= 130 && mouseY >= 15 && mouseY <= 45) {{
                    gameState = 'menu';
                }}
            }} else if (gameState === 'shop') {{
                if (mouseX >= 30 && mouseX <= 130 && mouseY >= 15 && mouseY <= 45) {{
                    gameState = 'menu';
                }}
                let keys = Object.keys(skins);
                for (let i = 0; i < keys.length; i++) {{
                    let skinKey = keys[i];
                    if (mouseX >= 30 && mouseX <= 370 && mouseY >= (95 + i * 80) && mouseY <= (160 + i * 80)) {{
                        if (unlockedSkins.includes(skinKey)) {{
                            currentSkin = skinKey;
                            localStorage.setItem("fb_current_skin", currentSkin);
                        }} else {{
                            let skin = skins[skinKey];
                            if (totalCoins >= skin.price) {{
                                totalCoins -= skin.price;
                                unlockedSkins.push(skinKey);
                                currentSkin = skinKey;
                                localStorage.setItem("fb_coins", totalCoins);
                                localStorage.setItem("fb_skins", JSON.stringify(unlockedSkins));
                                localStorage.setItem("fb_current_skin", currentSkin);
                            }} else {{
                                alert("Bạn không đủ tiền xu!");
                            }}
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
                width: 55,
                passed: false
            }});
        }}

        function update() {{
            if (gameState !== 'playing') return;

            let lvl = levels[currentLevel];
            bird.velocity += bird.gravity;
            bird.y += bird.velocity;

            if (bird.y + bird.height >= canvas.height - 45 || bird.y <= 0) {{
                gameState = 'gameover';
            }}

            if (frameCount % lvl.spawnRate === 0) {{
                spawnPipe();
            }}

            for (let i = pipes.length - 1; i >= 0; i--) {{
                pipes[i].x -= lvl.speed;

                if (
                    bird.x < pipes[i].x + pipes[i].width &&
                    bird.x + bird.width > pipes[i].x &&
                    (bird.y < pipes[i].top || bird.y + bird.height > canvas.height - pipes[i].bottom - 45)
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
                        localStorage.setItem("fb_coins", totalCoins);
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

        // Hàm hỗ trợ vẽ chữ chuẩn phong cách Pixel: Chữ trắng, viền đen nét căng
        function drawPixelText(text, x, y, size, align = "center") {{
            ctx.font = size + "px 'Press Start 2P'";
            ctx.textAlign = align;
            ctx.fillStyle = "#000000"; // Viền đen
            ctx.lineWidth = 4;
            ctx.strokeText(text, x, y);
            ctx.fillStyle = "#FFFFFF"; // Chữ trắng bên trong
            ctx.fillText(text, x, y);
        }}

        function drawPixelPipe(x, topHeight, bottomHeight) {{
            // Vẽ thân ống nước phong cách Pixel
            ctx.fillStyle = "#558022";
            ctx.fillRect(x, 0, 55, topHeight);
            ctx.fillRect(x, canvas.height - bottomHeight - 45, 55, bottomHeight);

            // Viền pixel đậm cho ống nước
            ctx.strokeStyle = "#223311";
            ctx.lineWidth = 3;
            ctx.strokeRect(x, 0, 55, topHeight);
            ctx.strokeRect(x, canvas.height - bottomHeight - 45, 55, bottomHeight);

            // Nắp ống nước phong cách pixel
            ctx.fillStyle = "#73BF2E";
            ctx.fillRect(x - 4, topHeight - 20, 63, 20);
            ctx.strokeRect(x - 4, topHeight - 20, 63, 20);

            ctx.fillRect(x - 4, canvas.height - bottomHeight - 45, 63, 20);
            ctx.strokeRect(x - 4, canvas.height - bottomHeight - 45, 63, 20);
        }}

        function drawBird() {{
            if (currentSkin === 'default' && birdImage.src !== "" && birdImage.complete && birdImage.naturalWidth !== 0) {{
                ctx.drawImage(birdImage, bird.x, bird.y, bird.width, bird.height);
            }} else {{
                ctx.fillStyle = skins[currentSkin].color;
                ctx.fillRect(bird.x, bird.y, bird.width, bird.height);
                // Viền nhân vật pixel
                ctx.strokeStyle = "#000";
                ctx.lineWidth = 2;
                ctx.strokeRect(bird.x, bird.y, bird.width, bird.height);

                ctx.fillStyle = "#FFFFFF";
                ctx.fillRect(bird.x + 20, bird.y + 5, 8, 8);
                ctx.fillStyle = "#000000";
                ctx.fillRect(bird.x + 24, bird.y + 7, 3, 3);
            }}
        }}

        function draw() {{
            ctx.clearRect(0, 0, canvas.width, canvas.height);

            if (gameState === 'menu') {{
                drawBackground();
                drawPixelText("FLAPPY BIRD", canvas.width / 2, 130, 22);
                drawPixelText("🪙: " + totalCoins, canvas.width / 2, 185, 14);

                // Nút Chơi Game
                ctx.fillStyle = "#27AE60";
                ctx.fillRect(80, 230, 240, 55);
                ctx.strokeStyle = "#000";
                ctx.lineWidth = 3;
                ctx.strokeRect(80, 230, 240, 55);
                drawPixelText("CHOI GAME", canvas.width / 2, 265, 12);

                // Nút Shop
                ctx.fillStyle = "#2980B9";
                ctx.fillRect(80, 310, 240, 55);
                ctx.strokeRect(80, 310, 240, 55);
                drawPixelText("CUA HANG", canvas.width / 2, 345, 12);

            }} else if (gameState === 'level_select') {{
                drawBackground();
                drawPixelText("CHON CAP DO", canvas.width / 2, 45, 16);

                // Nút Back
                ctx.fillStyle = "#7F8C8D";
                ctx.fillRect(30, 15, 100, 30);
                ctx.strokeRect(30, 15, 100, 30);
                drawPixelText("<- LUI", 80, 35, 9);

                for (let i = 1; i <= 5; i++) {{
                    let lvl = levels[i];
                    ctx.fillStyle = "rgba(0, 0, 0, 0.75)";
                    ctx.fillRect(30, 65 + i * 65, 340, 48);
                    ctx.strokeRect(30, 65 + i * 65, 340, 48);

                    drawPixelText(lvl.name, 45, 92 + i * 65, 10, "left");
                    
                    ctx.font = "8px 'Press Start 2P'";
                    ctx.fillStyle = "#F1C40F";
                    ctx.fillText("Muc tieu: " + lvl.targetScore + " | Thuong: 🪙" + lvl.reward, 45, 106 + i * 65);
                }}

            }} else if (gameState === 'shop') {{
                drawBackground();
                drawPixelText("CUA HANG", canvas.width / 2, 45, 16);
                drawPixelText("🪙 Xu: " + totalCoins, canvas.width / 2, 75, 10);

                // Nút Back
                ctx.fillStyle = "#7F8C8D";
                ctx.fillRect(30, 15, 100, 30);
                ctx.strokeRect(30, 15, 100, 30);
                drawPixelText("<- LUI", 80, 35, 9);

                let keys = Object.keys(skins);
                for (let i = 0; i < keys.length; i++) {{
                    let skinKey = keys[i];
                    let skin = skins[skinKey];
                    let isUnlocked = unlockedSkins.includes(skinKey);
                    let isSelected = (currentSkin === skinKey);

                    ctx.fillStyle = isSelected ? "#27AE60" : "rgba(0, 0, 0, 0.75)";
                    ctx.fillRect(30, 95 + i * 80, 340, 65);
                    ctx.strokeRect(30, 95 + i * 80, 340, 65);

                    ctx.fillStyle = skin.color;
                    ctx.fillRect(45, 110 + i * 80, 25, 25);
                    ctx.strokeStyle = "#000";
                    ctx.strokeRect(45, 110 + i * 80, 25, 25);

                    drawPixelText(skin.name, 85, 122 + i * 80, 10, "left");

                    ctx.font = "8px 'Press Start 2P'";
                    if (isSelected) {{
                        ctx.fillStyle = "#2ECC71";
                        ctx.fillText("DANG DUNG", 85, 142 + i * 80);
                    }} else if (isUnlocked) {{
                        ctx.fillStyle = "#AED6F1";
                        ctx.fillText("DA SO HUU", 85, 142 + i * 80);
                    }} else {{
                        ctx.fillStyle = "#F1C40F";
                        ctx.fillText("Gia: 🪙 " + skin.price, 85, 142 + i * 80);
                    }}
                }}

            }} else if (gameState === 'playing' || gameState === 'gameover' || levelCompleted) {{
                drawBackground();

                let lvl = levels[currentLevel];
                for (let i = 0; i < pipes.length; i++) {{
                    drawPixelPipe(pipes[i].x, pipes[i].top, pipes[i].bottom);
                }}

                drawBird();

                drawPixelText("LVL: " + currentLevel + " | DIEM: " + score + "/" + lvl.targetScore, 20, 28, 9, "left");
                drawPixelText("🪙 " + totalCoins, 350, 28, 9, "right");

                if (gameState === 'gameover') {{
                    ctx.fillStyle = "rgba(0, 0, 0, 0.8)";
                    ctx.fillRect(0, 0, canvas.width, canvas.height);
                    drawPixelText("THAT BAI!", canvas.width / 2, 210, 20);
                    drawPixelText("Nhan Space de chon lai", canvas.width / 2, 260, 9);
                }}

                if (levelCompleted) {{
                    ctx.fillStyle = "rgba(0, 0, 0, 0.8)";
                    ctx.fillRect(0, 0, canvas.width, canvas.height);
                    drawPixelText("HOAN THANH!", canvas.width / 2, 185, 16);
                    
                    ctx.font = "10px 'Press Start 2P'";
                    ctx.fillStyle = "#F1C40F";
                    ctx.textAlign = "center";
                    ctx.fillText("Thuong: + 🪙 " + coinsEarnedThisRun, canvas.width / 2, 230);
                    
                    drawPixelText("Nhan Space de tiep tuc", canvas.width / 2, 280, 9);
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
