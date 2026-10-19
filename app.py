import streamlit as st

st.set_page_config(page_title="Flappy Bird Streamlit", page_icon="🐦", layout="centered")

st.title("🐦 Flappy Bird trên Streamlit")
st.write("Nhấp chuột vào khung game hoặc nhấn phím **Space** để chú chim bay lên và tránh các ống nước!")

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
            background: #70c5ce;
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
            width: 25,
            height: 25,
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

            if (bird.y + bird.height >= canvas.height || bird.y <= 0) {
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
                    (bird.y < pipes[i].top || bird.y + bird.height > canvas.height - pipes[i].bottom)
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

        function draw() {
            ctx.fillStyle = "#70c5ce";
            ctx.fillRect(0, 0, canvas.width, canvas.height);

            ctx.fillStyle = "#73bf2e";
            for (let i = 0; i < pipes.length; i++) {
                ctx.fillRect(pipes[i].x, 0, pipes[i].width, pipes[i].top);
                ctx.fillRect(pipes[i].x, canvas.height - pipes[i].bottom, pipes[i].width, pipes[i].bottom);
            }

            ctx.fillStyle = "#f8e71c";
            ctx.fillRect(bird.x, bird.y, bird.width, bird.height);

            ctx.fillStyle = "white";
            ctx.font = "bold 24px Arial";
            ctx.fillText("Điểm: " + score, 20, 35);

            if (isGameOver) {
                ctx.fillStyle = "rgba(0, 0, 0, 0.6)";
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
