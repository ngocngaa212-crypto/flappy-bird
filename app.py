import streamlit as st

st.set_page_config(page_title="Flappy Bird Pixel Art", page_icon="🐦", layout="centered")

st.title("🐦 Flappy Bird - Phong cách Pixel Art")
st.write("Nhấn phím **Space** hoặc nhấp chuột vào khung game để chơi!")

flappy_bird_html = """
<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <title>Flappy Bird</title>
    <style>
        body {
            margin: 0;
            background: #111;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            font-family: Arial, sans-serif;
        }
        canvas {
            border: 3px solid #fff;
            box-shadow: 0px 0px 15px rgba(255,255,255,0.3);
        }
    </style>
</head>
<body>
    <canvas id="gameCanvas" width="400" height="500"></canvas>
    <script>
        const canvas = document.getElementById("gameCanvas");
        const ctx = canvas.getContext("2d");

        let bird = {
            x: 50,
            y: 150,
            width: 28,
            height: 24,
            gravity: 0.6,
            lift: -10,
            velocity: 0
        };

        let pipes = [];
        let frameCount = 0;
        let score = 0;
        let isGameOver = false;

        function resetGame() {
            bird.y = 150;
            bird.velocity = 0;
            pipes = [];
            score = 0;
            frameCount = 0;
            isGameOver = false;
        }

        document.addEventListener("keydown", function(e) {
            if (e.code === "Space") {
                if (isGameOver) {
                    resetGame();
                } else {
                    bird.velocity = bird.lift;
                }
            }
        });

        canvas.addEventListener("click", function() {
            if (isGameOver) {
                resetGame();
            } else {
                bird.velocity = bird.lift;
            }
        });

        function spawnPipe() {
            let gap = 130;
            let topHeight = Math.floor(Math.random() * (canvas.height - gap - 120)) + 40;
            pipes.push({
                x: canvas.width,
                top: topHeight,
                bottom: canvas.height - topHeight - gap,
                width: 55,
                passed: false
            });
        }

        function update() {
            if (isGameOver) return;

            bird.velocity += bird.gravity;
            bird.y += bird.velocity;

            if (bird.y + bird.height >= canvas.height - 80 || bird.y <= 0) {
                isGameOver = true;
            }

            if (frameCount % 90 === 0) {
                spawnPipe();
            }

            for (let i = pipes.length - 1; i >= 0; i--) {
                pipes[i].x -= 2.5;

                if (
                    bird.x < pipes[i].x + pipes[i].width &&
                    bird.x + bird.width > pipes[i].x &&
                    (bird.y < pipes[i].top || bird.y + bird.height > canvas.height - pipes[i].bottom - 80)
                ) {
                    isGameOver = true;
                }

                if (!pipes[i].passed && pipes[i].x + pipes[i].width < bird.x) {
                    score++;
                    pipes[i].passed = true;
                }

                if (pipes[i].x + pipes[i].width < 0) {
                    pipes.splice(i, 1);
                }
            }

            frameCount++;
        }

        // Vẽ mây pixel trắng
        function drawCloud(x, y) {
            ctx.fillStyle = "#FFFFFF";
            ctx.fillRect(x, y, 70, 22);
            ctx.fillRect(x + 12, y - 12, 45, 12);
        }

        // Vẽ bụi cây xanh phong cách pixel
        function drawBush(x, y) {
            ctx.fillStyle = "#65C18C";
            ctx.fillRect(x, y, 60, 40);
            ctx.fillRect(x + 15, y - 15, 30, 20);
        }

        function draw() {
            // 1. Nền trời xanh đặc trưng
            ctx.fillStyle = "#4FB7DB";
            ctx.fillRect(0, 0, canvas.width, canvas.height);

            // 2. Các đám mây trên trời
            drawCloud(40, 50);
            drawCloud(240, 80);

            // 3. Thảm cỏ xanh đậm và bụi cây phía dưới
            drawBush(20, canvas.height - 110);
            drawBush(270, canvas.height - 100);

            ctx.fillStyle = "#1B7A63"; // Màu thảm cỏ giống ảnh mẫu
            ctx.fillRect(0, canvas.height - 80, canvas.width, 80);
            ctx.fillStyle = "#26997B";
            ctx.fillRect(0, canvas.height - 80, canvas.width, 14);

            // 4. Ống nước
            ctx.fillStyle = "#558022";
            for (let i = 0; i < pipes.length; i++) {
                ctx.fillRect(pipes[i].x, 0, pipes[i].width, pipes[i].top);
                ctx.fillRect(pipes[i].x, canvas.height - pipes[i].bottom - 80, pipes[i].width, pipes[i].bottom);
            }

            // 5. Chú chim
            ctx.fillStyle = "#F4D03F";
            ctx.fillRect(bird.x, bird.y, bird.width, bird.height);
            ctx.fillStyle = "#FFFFFF";
            ctx.fillRect(bird.x + 18, bird.y + 4, 6, 6);
            ctx.fillStyle = "#000000";
            ctx.fillRect(bird.x + 22, bird.y + 6, 2, 2);

            // 6. Điểm số
            ctx.fillStyle = "white";
            ctx.font = "bold 28px Arial";
            ctx.lineWidth = 4;
            ctx.strokeStyle = "black";
            ctx.strokeText("Điểm: " + score, 20, 40);
            ctx.fillText("Điểm: " + score, 20, 40);

            if (isGameOver) {
                ctx.fillStyle = "rgba(0, 0, 0, 0.7)";
                ctx.fillRect(0, 0, canvas.width, canvas.height);
                ctx.fillStyle = "white";
                ctx.font = "bold 32px Arial";
                ctx.fillText("GAME OVER", 100, 220);
                ctx.font = "16px Arial";
                ctx.fillText("Nhấn chuột hoặc Space để chơi lại", 75, 265);
            }
        }

        function loop() {
            update();
            draw();
            requestAnimationFrame(loop);
        }

        loop();
    </script>
</body>
</html>
"""

st.components.v1.html(flappy_bird_html, height=540)
