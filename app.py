import streamlit as st
import base64
import os

st.set_page_config(page_title="Flappy Bird RPG & Shop", page_icon="🐦", layout="centered")

st.title("🐦 Flappy Bird - 5 Cấp Độ & Cửa Hàng Nhân Vật")
st.write("Vượt qua các màn chơi, kiếm tiền xu 🪙 để mở khóa nhân vật!")

# Hàm đọc file ảnh background.png cùng thư mục và chuyển sang Base64
def get_image_base64(image_path):
    if os.path.exists(image_path):
        with open(image_path, "rb") as img_file:
            encoded = base64.b64encode(img_file.read()).decode()
            return f"data:image/png;base64,{encoded}"
    return ""

# Đọc file background.png mà bạn đã tải về và lưu chung thư mục
bg_data_url = get_image_base64("background.png")

flappy_bird_html = f"""
<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <title>Flappy Bird RPG</title>
    <style>
        body {{
            margin: 0;
            background: #111;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            font-family: Arial, sans-serif;
        }}
        canvas {{
            border: 3px solid #fff;
            box-shadow: 0px 0px 15px rgba(255,255,255,0.3);
        }}
    </style>
</head>
<body>
    <canvas id="gameCanvas" width="400" height="500"></canvas>
    <script>
        const canvas = document.getElementById("gameCanvas");
        const ctx = canvas.getContext("2d");

        // Load ảnh nền qua dữ liệu Base64
        const bgImage = new Image();
        bgImage.src = "{bg_data_url}";

        let totalCoins = parseInt(localStorage.getItem("fb_coins")) || 0;
        let unlockedSkins = JSON.parse(localStorage.getItem("fb_skins")) || ["default"];
        let currentSkin = localStorage.getItem("fb_current_skin") || "default";

        const skins = {{
            "default": {{ name: "Chim Vàng Cổ Điển", price: 0, color: "#F4D03F" }},
            "ninja": {{ name: "Ninja Đen Bí Ẩn", price: 20, color: "#2E4053" }},
            "superman": {{ name: "Siêu Nhân Đỏ", price: 50, color: "#CB4335" }},
            "golden": {{ name: "Chim Thần Hoàng Kim", price: 100, color: "#F39C12" }}
        }};

        let gameState = 'menu';

        let bird = {{
            x: 50,
            y: 150,
            width: 28,
            height: 24,
            gravity: 0.6,
            lift: -10,
            velocity: 0
        }};

        let currentLevel = 1;
        const levels = {{
            1: {{ name: "Cấp 1: Tập Sự", speed: 2, gap: 140, spawnRate: 100, targetScore: 5, reward: 10 }},
            2: {{ name: "Cấp 2: Thử Thách", speed: 2.5, gap: 130, spawnRate: 90, targetScore: 10, reward: 20 }},
            3: {{ name: "Cấp 3: Khó Nhằn", speed: 3, gap: 120, spawnRate: 80, targetScore: 15, reward: 35 }},
            4: {{ name: "Cấp 4: Chuyên Gia", speed: 3.5, gap: 110, spawnRate: 70, targetScore: 20, reward: 50 }},
            5: {{ name: "Cấp 5: Bậc Thầy", speed: 4, gap: 100, spawnRate: 60, targetScore: 30, reward: 100 }}
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
                if (mouseX >= 100 && mouseX <= 300 && mouseY >= 240 && mouseY <= 290) {{
                    gameState = 'level_select';
                }}
                if (mouseX >= 100 && mouseX <= 300 && mouseY >= 320 && mouseY <= 370) {{
                    gameState = 'shop';
                }}
            }} else if (gameState === 'level_select') {{
                for (let i = 1; i <= 5; i++) {{
                    if (mouseX >= 50 && mouseX <= 350 && mouseY >= (70 + i * 65) && mouseY <= (120 + i * 65)) {{
                        resetGame(i);
                    }}
                }}
                if (mouseX >= 50 && mouseX <= 150 && mouseY >= 20 && mouseY <= 50) {{
                    gameState = 'menu';
                }}
            }} else if (gameState === 'shop') {{
                if (mouseX >= 50 && mouseX <= 150 && mouseY >= 20 && mouseY <= 50) {{
                    gameState = 'menu';
                }}
                let keys = Object.keys(skins);
                for (let i = 0; i < keys.length; i++) {{
                    let skinKey = keys[i];
                    if (mouseX >= 50 && mouseX <= 350 && mouseY >= (100 + i * 85) && mouseY <= (170 + i * 85)) {{
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
                                alert("Bạn không đủ tiền xu để mua nhân vật này!");
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
            let topHeight = Math.floor(Math.random() * (canvas.height - lvl.gap - 120)) + 40;
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

            if (bird.y + bird.height >= canvas.height - 50 || bird.y <= 0) {{
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
                    (bird.y < pipes[i].top || bird.y + bird.height > canvas.height - pipes[i].bottom - 50)
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

        function draw() {{
            ctx.clearRect(0, 0, canvas.width, canvas.height);

            if (gameState === 'menu') {{
                drawBackground();
                ctx.fillStyle = "white";
                ctx.font = "bold 32px Arial";
                ctx.textAlign = "center";
                ctx.fillText("FLAPPY BIRD", canvas.width / 2, 130);

                ctx.font = "18px Arial";
                ctx.fillText("🪙 Tiền xu: " + totalCoins, canvas.width / 2, 180);

                ctx.fillStyle = "#27AE60";
                ctx.fillRect(100, 240, 200, 50);
                ctx.fillStyle = "white";
                ctx.font = "bold 20px Arial";
                ctx.fillText("CHƠI GAME", canvas.width / 2, 272);

                ctx.fillStyle = "#2980B9";
                ctx.fillRect(100, 320, 200, 50);
                ctx.fillStyle = "white";
                ctx.fillText("CỬA HÀNG NHÂN VẬT", canvas.width / 2, 352);
                ctx.textAlign = "left";

            }} else if (gameState === 'level_select') {{
                drawBackground();
                ctx.fillStyle = "white";
                ctx.font = "bold 24px Arial";
                ctx.textAlign = "center";
                ctx.fillText("CHỌN CẤP ĐỘ", canvas.width / 2, 50);

                ctx.fillStyle = "#7F8C8D";
                ctx.fillRect(50, 20, 100, 30);
                ctx.fillStyle = "white";
                ctx.font = "14px Arial";
                ctx.fillText("⬅ Quay lại", 100, 40);

                for (let i = 1; i <= 5; i++) {{
                    let lvl = levels[i];
                    ctx.fillStyle = "rgba(0, 0, 0, 0.6)";
                    ctx.fillRect(50, 70 + i * 65, 300, 45);

                    ctx.fillStyle = "white";
                    ctx.font = "bold 16px Arial";
                    ctx.fillText(lvl.name, 70, 98 + i * 65);
                    ctx.font = "12px Arial";
                    ctx.fillStyle = "#F1C40F";
                    ctx.fillText("Mục tiêu: " + lvl.targetScore + " điểm | Thưởng: 🪙" + lvl.reward, 200, 98 + i * 65);
                }}
                ctx.textAlign = "left";

            }} else if (gameState === 'shop') {{
                drawBackground();
                ctx.fillStyle = "white";
                ctx.font = "bold 24px Arial";
                ctx.textAlign = "center";
                ctx.fillText("CỬA HÀNG NHÂN VẬT", canvas.width / 2, 50);
                ctx.font = "16px Arial";
                ctx.fillStyle = "#F1C40F";
                ctx.fillText("🪙 Số xu của bạn: " + totalCoins, canvas.width / 2, 80);

                ctx.fillStyle = "#7F8C8D";
                ctx.fillRect(50, 20, 100, 30);
                ctx.fillStyle = "white";
                ctx.font = "14px Arial";
                ctx.fillText("⬅ Quay lại", 100, 40);

                let keys = Object.keys(skins);
                for (let i = 0; i < keys.length; i++) {{
                    let skinKey = keys[i];
                    let skin = skins[skinKey];
                    let isUnlocked = unlockedSkins.includes(skinKey);
                    let isSelected = (currentSkin === skinKey);

                    ctx.fillStyle = isSelected ? "#27AE60" : "rgba(0, 0, 0, 0.6)";
                    ctx.fillRect(50, 100 + i * 85, 300, 70);

                    ctx.fillStyle = skin.color;
                    ctx.fillRect(70, 120 + i * 85, 30, 25);

                    ctx.fillStyle = "white";
                    ctx.font = "bold 16px Arial";
                    ctx.fillText(skin.name, 115, 128 + i * 85);

                    ctx.font = "13px Arial";
                    if (isSelected) {{
                        ctx.fillStyle = "#2ECC71";
                        ctx.fillText("Đang sử dụng", 115, 150 + i * 85);
                    }} else if (isUnlocked) {{
                        ctx.fillStyle = "#AED6F1";
                        ctx.fillText("Đã sở hữu (Nhấn để chọn)", 115, 150 + i * 85);
                    }} else {{
                        ctx.fillStyle = "#F1C40F";
                        ctx.fillText("Giá: 🪙 " + skin.price, 115, 150 + i * 85);
                    }}
                }}
                ctx.textAlign = "left";

            }} else if (gameState === 'playing' || gameState === 'gameover' || levelCompleted) {{
                drawBackground();

                let lvl = levels[currentLevel];
                ctx.fillStyle = "#558022";
                for (let i = 0; i < pipes.length; i++) {{
                    ctx.fillRect(pipes[i].x, 0, pipes[i].width, pipes[i].top);
                    ctx.fillRect(pipes[i].x, canvas.height - pipes[i].bottom - 50, pipes[i].width, pipes[i].bottom);
                }}

                ctx.fillStyle = skins[currentSkin].color;
                ctx.fillRect(bird.x, bird.y, bird.width, bird.height);
                ctx.fillStyle = "#FFFFFF";
                ctx.fillRect(bird.x + 18, bird.y + 4, 6, 6);
                ctx.fillStyle = "#000000";
                ctx.fillRect(bird.x + 22, bird.y + 6, 2, 2);

                ctx.fillStyle = "white";
                ctx.font = "bold 20px Arial";
                ctx.fillText("Cấp: " + currentLevel + " | Điểm: " + score + "/" + lvl.targetScore, 20, 30);
                ctx.fillText("🪙 " + totalCoins, 310, 30);

                if (gameState === 'gameover') {{
                    ctx.fillStyle = "rgba(0, 0, 0, 0.7)";
                    ctx.fillRect(0, 0, canvas.width, canvas.height);
                    ctx.fillStyle = "#E74C3C";
                    ctx.font = "bold 32px Arial";
                    ctx.textAlign = "center";
                    ctx.fillText("THẤT BẠI!", canvas.width / 2, 210);
                    ctx.fillStyle = "white";
                    ctx.font = "16px Arial";
                    ctx.fillText("Nhấn Space hoặc Click để chọn lại cấp độ", canvas.width / 2, 260);
                    ctx.textAlign = "left";
                }}

                if (levelCompleted) {{
                    ctx.fillStyle = "rgba(0, 0, 0, 0.7)";
                    ctx.fillRect(0, 0, canvas.width, canvas.height);
                    ctx.fillStyle = "#2ECC71";
                    ctx.font = "bold 32px Arial";
                    ctx.textAlign = "center";
                    ctx.fillText("HOÀN THÀNH MÀN!", canvas.width / 2, 190);
                    ctx.fillStyle = "#F1C40F";
                    ctx.font = "bold 20px Arial";
                    ctx.fillText("Nhận thưởng: + 🪙 " + coinsEarnedThisRun, canvas.width / 2, 235);
                    ctx.fillStyle = "white";
                    ctx.font = "15px Arial";
                    ctx.fillText("Nhấn Space hoặc Click để tiếp tục", canvas.width / 2, 280);
                    ctx.textAlign = "left";
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
