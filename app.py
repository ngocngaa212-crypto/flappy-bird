import streamlit as st
import base64
import os

st.set_page_config(page_title="The journey of Tom", page_icon="🐱", layout="centered")

st.title("🐱 The journey of Tom")
st.write("Hành trình của Tom - Hình nền chỉ tự động đổi khi bạn vào chơi game!")

def get_image_base64(image_path):
    if os.path.exists(image_path):
        with open(image_path, "rb") as img_file:
            encoded = base64.b64encode(img_file.read()).decode()
            return f"data:image/png;base64,{encoded}"
    return ""

def get_audio_base64(audio_path):
    if os.path.exists(audio_path):
        with open(audio_path, "rb") as audio_file:
            encoded = base64.b64encode(audio_file.read()).decode()
            return f"data:audio/mp3;base64,{encoded}"
    return ""

bg_data_url = get_image_base64("background.png")
bg2_data_url = get_image_base64("background2.png")
normal_data_url = get_image_base64("cat_normal.png") if os.path.exists("cat_normal.png") else get_image_base64("bird.png")

rainbow_data_url = get_image_base64("rainbow_Tom.png")
donut_data_url = get_image_base64("Tom_with_donut.png")
strong_data_url = get_image_base64("super_strong_Tom.png")
angela_data_url = get_image_base64("angela.png")

menu_music_url = get_audio_base64("menu_music.mp3")
play_music_url = get_audio_base64("play_music.mp3")
gameover_music_url = get_audio_base64("gameover_music.mp3")
win_music_url = get_audio_base64("win_music.mp3")
angela_win_music_url = get_audio_base64("angela_win_music.mp3")
click_sound_url = get_audio_base64("click_sound.mp3")

flappy_bird_html = f"""
<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <title>The journey of Tom</title>
    <style>
        body {{
            margin: 0;
            background: #111;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
        }}
        canvas {{
            border: 4px solid #fff;
            box-shadow: 0px 0px 20px rgba(255,255,255,0.4);
            border-radius: 8px;
        }}
    </style>
</head>
<body>
    <audio id="menuMusic" loop src="{menu_music_url}"></audio>
    <audio id="playMusic" loop src="{play_music_url}"></audio>
    <audio id="gameoverMusic" src="{gameover_music_url}"></audio>
    <audio id="winMusic" src="{win_music_url}"></audio>
    <audio id="angelaWinMusic" src="{angela_win_music_url}"></audio>
    <audio id="clickSound" src="{click_sound_url}"></audio>

    <canvas id="gameCanvas" width="400" height="500"></canvas>
    <script>
        const canvas = document.getElementById("gameCanvas");
        const ctx = canvas.getContext("2d");

        const menuMusic = document.getElementById("menuMusic");
        const playMusic = document.getElementById("playMusic");
        const gameoverMusic = document.getElementById("gameoverMusic");
        const winMusic = document.getElementById("winMusic");
        const angelaWinMusic = document.getElementById("angelaWinMusic");
        const clickSound = document.getElementById("clickSound");

        let musicMuted = localStorage.getItem("tom_music_muted") === "true";
        let sfxMuted = localStorage.getItem("tom_sfx_muted") === "true";
        let musicVolume = parseFloat(localStorage.getItem("tom_music_vol")) || 0.5;
        let sfxVolume = parseFloat(localStorage.getItem("tom_sfx_vol")) || 0.5;

        let showAudioModal = false;
        let clickTimer = null;

        function applyVolumes() {{
            menuMusic.volume = musicMuted ? 0 : musicVolume;
            playMusic.volume = musicMuted ? 0 : musicVolume;
            gameoverMusic.volume = musicMuted ? 0 : musicVolume;
            winMusic.volume = musicMuted ? 0 : musicVolume;
            angelaWinMusic.volume = musicMuted ? 0 : musicVolume;
            clickSound.volume = sfxMuted ? 0 : sfxVolume;
        }}

        applyVolumes();

        function playClickEffect() {{
            if (sfxMuted) return;
            if (clickSound.src) {{
                if (clickTimer) clearTimeout(clickTimer);

                clickSound.currentTime = 0;
                clickSound.play().catch(e => console.log("Click sound blocked:", e));

                clickTimer = setTimeout(() => {{
                    clickSound.pause();
                    clickSound.currentTime = 0;
                }}, 1000);
            }}
        }}

        function tryAutoplay() {{
            if (gameState === 'playing') {{
                if (playMusic.src && playMusic.paused) {{
                    playMusic.play().catch(e => console.log("Autoplay waiting for interaction"));
                }}
            }} else if (gameState === 'gameover') {{
                if (gameoverMusic.src && gameoverMusic.paused) {{
                    gameoverMusic.play().catch(e => console.log("Autoplay waiting for interaction"));
                }}
            }} else if (levelCompleted) {{
                if (currentLevel === 5) {{
                    if (angelaWinMusic.src && angelaWinMusic.paused) {{
                        angelaWinMusic.play().catch(e => console.log("Autoplay waiting for interaction"));
                    }}
                }} else {{
                    if (winMusic.src && winMusic.paused) {{
                        winMusic.play().catch(e => console.log("Autoplay waiting for interaction"));
                    }}
                }}
            }} else {{
                if (menuMusic.src && menuMusic.paused) {{
                    menuMusic.play().catch(e => console.log("Autoplay waiting for interaction"));
                }}
            }}
        }}

        window.addEventListener('DOMContentLoaded', tryAutoplay);
        window.addEventListener('load', tryAutoplay);

        function handleUserInteraction() {{
            tryAutoplay();
        }}
        window.addEventListener('click', handleUserInteraction);
        window.addEventListener('keydown', handleUserInteraction);
        window.addEventListener('mousemove', handleUserInteraction, {{ once: true }});

        function updateMusicState() {{
            applyVolumes();

            menuMusic.pause();
            playMusic.pause();
            gameoverMusic.pause();
            winMusic.pause();
            angelaWinMusic.pause();

            if (levelCompleted) {{
                if (currentLevel === 5) {{
                    if (angelaWinMusic.src) {{
                        angelaWinMusic.currentTime = 0;
                        angelaWinMusic.play().catch(e => console.log("Angela win music blocked:", e));
                    }}
                }} else {{
                    if (winMusic.src) {{
                        winMusic.currentTime = 0;
                        winMusic.play().catch(e => console.log("Win music blocked:", e));
                    }}
                }}
            }} else if (gameState === 'playing') {{
                if (playMusic.src) {{
                    playMusic.currentTime = 0;
                    playMusic.play().catch(e => console.log("Play music blocked:", e));
                }}
            }} else if (gameState === 'gameover') {{
                if (gameoverMusic.src) {{
                    gameoverMusic.currentTime = 0;
                    gameoverMusic.play().catch(e => console.log("Gameover music blocked:", e));
                }}
            }} else {{
                if (menuMusic.src) {{
                    menuMusic.play().catch(e => console.log("Menu music blocked:", e));
                }}
            }}
        }}

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
                reward: "Phần thưởng: ",
                using: "ĐANG DÙNG",
                owned: "ĐÃ SỞ HỮU",
                price: "GIÁ: ",
                confirmTitle: "XÁC NHẬN MUA",
                confirmAsk: "Bạn có chắc muốn mua?",
                buy: "MUA",
                cancel: "HỦY",
                failed: "THẤT BẠI!",
                retry: "Nhấn Space để thử lại",
                passLevel: "CHÚC MỪNG VƯỢT ẢI ",
                meetAngelaLine1: "Hoàn thành màn 5 để giúp Tom",
                meetAngelaLine2: "gặp được tình yêu của anh ấy!",
                continue: "Nhấn Space để tiếp tục",
                notEnoughCoins: "Bạn không đủ xu!",
                locked: "🔒 BỊ KHÓA",
                unlockedNext: "Đã mở khóa màn tiếp theo!",
                audioTitle: "CÀI ĐẶT ÂM THANH",
                bgMusicLabel: "Nhạc nền (Music):",
                sfxLabel: "Hiệu ứng (SFX):",
                closeBtn: "ĐÓNG",
                guideTitle: "HƯỚNG DẪN CHƠI",
                guideStep1: "• Nhấn SPACE hoặc chạm để Tom",
                guideStep2: "  bay lên né các ống nước.",
                guideStep3: "• Đạt điểm mục tiêu để mở màn.",
                guideStep4: "• Tích xu để đổi các skin của Tom.",
                guideStep5: "• Hoàn thành màn 5 để giúp Tom",
                guideStep6: "  gặp Angela tình yêu của mình.",
                guideWish: "Chúc bạn chơi game vui vẻ!",
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
                reward: "Reward: ",
                using: "EQUIPPED",
                owned: "OWNED",
                price: "PRICE: ",
                confirmTitle: "CONFIRM PURCHASE",
                confirmAsk: "Are you sure you want to buy?",
                buy: "BUY",
                cancel: "CANCEL",
                failed: "GAME OVER!",
                retry: "Press Space to retry",
                passLevel: "CONGRATULATIONS ON LEVEL ",
                meetAngelaLine1: "Completed Level 5 to help Tom",
                meetAngelaLine2: "meet the love of his life!",
                continue: "Press Space to continue",
                notEnoughCoins: "Not enough coins!",
                locked: "🔒 LOCKED",
                unlockedNext: "Unlocked Next Level!",
                audioTitle: "AUDIO SETTINGS",
                bgMusicLabel: "Background Music:",
                sfxLabel: "Sound Effects (SFX):",
                closeBtn: "CLOSE",
                guideTitle: "GAME GUIDE",
                guideStep1: "• Press SPACE or click to make Tom",
                guideStep2: "  fly up and dodge pipes.",
                guideStep3: "• Reach target scores to unlock levels.",
                guideStep4: "• Collect coins to change Tom's skins.",
                guideStep5: "• Complete Level 5 to help Tom",
                guideStep6: "  meet the love of his life.",
                guideWish: "Have fun playing the game!",
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
            "normal": {{ name: "Normal Tom", price: 0, color: "#F4D03F" }},
            "rainbow": {{ name: "Rainbow Tom", price: 50, color: "#9B59B6" }},
            "donut": {{ name: "Tom with Donut", price: 100, color: "#E75480" }},
            "strong": {{ name: "Super Strong Tom", price: 170, color: "#E74C3C" }}
        }};

        let gameState = 'menu';
        let pendingBuySkinKey = null;
        let showGuideModal = false;

        let bird = {{
            x: 30,
            y: 150,
            width: 125,
            height: 75,
            gravity: 0.28,
            lift: -6.8,
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
            updateMusicState();
        }}

        document.addEventListener("keydown", function(e) {{
            if (e.code === "Space") {{
                if (gameState !== 'playing') {{
                    playClickEffect();
                }}

                if (gameState === 'playing') {{
                    bird.velocity = bird.lift;
                }} else if (gameState === 'gameover' || levelCompleted) {{
                    gameState = 'level_select';
                    updateMusicState();
                }}
            }}
        }});

        canvas.addEventListener("click", function(e) {{
            if (gameState !== 'playing') {{
                playClickEffect();
            }}

            let rect = canvas.getBoundingClientRect();
            let mouseX = e.clientX - rect.left;
            let mouseY = e.clientY - rect.top;

            if (showAudioModal) {{
                if (mouseX >= 130 && mouseX <= 270 && mouseY >= 395 && mouseY <= 440) {{
                    showAudioModal = false;
                }}
                if (mouseX >= 220 && mouseX <= 350 && mouseY >= 140 && mouseY <= 175) {{
                    musicMuted = !musicMuted;
                    localStorage.setItem("tom_music_muted", musicMuted);
                    updateMusicState();
                }}
                if (mouseX >= 180 && mouseX <= 215 && mouseY >= 185 && mouseY <= 220) {{
                    musicVolume = Math.max(0, musicVolume - 0.1);
                    localStorage.setItem("tom_music_vol", musicVolume);
                    updateMusicState();
                }}
                if (mouseX >= 315 && mouseX <= 350 && mouseY >= 185 && mouseY <= 220) {{
                    musicVolume = Math.min(1, musicVolume + 0.1);
                    localStorage.setItem("tom_music_vol", musicVolume);
                    updateMusicState();
                }}
                if (mouseX >= 220 && mouseX <= 350 && mouseY >= 255 && mouseY <= 290) {{
                    sfxMuted = !sfxMuted;
                    localStorage.setItem("tom_sfx_muted", sfxMuted);
                    applyVolumes();
                }}
                if (mouseX >= 180 && mouseX <= 215 && mouseY >= 300 && mouseY <= 335) {{
                    sfxVolume = Math.max(0, sfxVolume - 0.1);
                    localStorage.setItem("tom_sfx_vol", sfxVolume);
                    applyVolumes();
                }}
                if (mouseX >= 315 && mouseX <= 350 && mouseY >= 300 && mouseY <= 335) {{
                    sfxVolume = Math.min(1, sfxVolume + 0.1);
                    localStorage.setItem("tom_sfx_vol", sfxVolume);
                    applyVolumes();
                }}
                return;
            }}

            if (showGuideModal) {{
                if (mouseX >= 130 && mouseX <= 270 && mouseY >= 410 && mouseY <= 455) {{
                    showGuideModal = false;
                }}
                return;
            }}

            if (gameState === 'menu') {{
                if (mouseX >= 160 && mouseX <= 200 && mouseY >= 15 && mouseY <= 53) {{
                    showAudioModal = true;
                    return;
                }}
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
                    updateMusicState();
                }}
                if (mouseX >= 60 && mouseX <= 340 && mouseY >= 290 && mouseY <= 350) {{
                    gameState = 'shop';
                    updateMusicState();
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
                    updateMusicState();
                }}
            }} else if (gameState === 'shop') {{
                if (mouseX >= 20 && mouseX <= 130 && mouseY >= 15 && mouseY <= 50) {{
                    gameState = 'menu';
                    updateMusicState();
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
                updateMusicState();
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
            if (gameState !== 'playing' || pendingBuySkinKey || showGuideModal || showAudioModal) return;

            let lvl = levels[currentLevel];
            bird.velocity += bird.gravity;
            bird.y += bird.velocity;

            if (bird.y + bird.height >= canvas.height - 45 || bird.y <= 0) {{
                gameState = 'gameover';
                updateMusicState();
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
                    updateMusicState();
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
                        updateMusicState();
                    }}
                }}

                if (pipes[i].x + pipes[i].width < 0) {{
                    pipes.splice(i, 1);
                }}
            }}

            frameCount++;
        }}

        // Hàm vẽ hình nền:
        // - Ở ngoài Menu: Cố định là background.png
        // - Khi đang chơi game: Tính theo thời gian chơi (10s nền 1 -> 30s nền 2)
        function drawBackground() {{
            let activeBg = bgImage1;

            if (gameState === 'playing' && playStartTime > 0) {{
                let playedSeconds = Math.floor((Date.now() - playStartTime) / 1000);
                let cycleTime = playedSeconds % 40; // Chu kỳ 40 giây (10s nền 1 -> 30s nền 2)

                if (cycleTime >= 10 && bgImage2.complete && bgImage2.naturalWidth !== 0) {{
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
            ctx.save();
            ctx.font = "bold " + size + "px 'Segoe UI', Roboto, Helvetica, Arial, sans-serif";
            ctx.textAlign = align;
            
            ctx.shadowColor = "rgba(0, 0, 0, 0.75)";
            ctx.shadowBlur = 6;
            ctx.shadowOffsetX = 2;
            ctx.shadowOffsetY = 2;

            ctx.fillStyle = textColor;
            ctx.fillText(text, x, y);
            ctx.restore();
        }}

        function drawCleanText(text, x, y, size, align = "center", textColor = "#1B2631") {{
            ctx.save();
            ctx.font = "600 " + size + "px 'Segoe UI', Roboto, Helvetica, Arial, sans-serif";
            ctx.textAlign = align;
            ctx.fillStyle = textColor;
            ctx.fillText(text, x, y);
            ctx.restore();
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

        function drawAudioModal() {{
            if (!showAudioModal) return;
            let t = i18n[currentLang];

            ctx.fillStyle = "rgba(0, 0, 0, 0.85)";
            ctx.fillRect(0, 0, canvas.width, canvas.height);

            ctx.fillStyle = "#FFFFFF";
            ctx.fillRect(25, 50, 350, 410);
            ctx.strokeStyle = "#2C3E50";
            ctx.lineWidth = 4;
            ctx.strokeRect(25, 50, 350, 410);

            drawCleanText(t.audioTitle, canvas.width / 2, 95, 22, "center", "#1B4F72");

            drawCleanText(t.bgMusicLabel, 40, 135, 16, "left", "#1B2631");
            ctx.fillStyle = musicMuted ? "#C0392B" : "#27AE60";
            ctx.fillRect(220, 140, 130, 38);
            ctx.strokeStyle = "#000"; ctx.lineWidth = 2; ctx.strokeRect(220, 140, 130, 38);
            drawPixelText(musicMuted ? "TẮT (OFF)" : "BẬT (ON)", 285, 165, 15);

            ctx.fillStyle = "#E74C3C"; ctx.fillRect(180, 185, 38, 38); ctx.strokeRect(180, 185, 38, 38);
            drawPixelText("-", 199, 210, 20);
            drawCleanText("Vol: " + Math.round(musicVolume * 100) + "%", 255, 210, 16, "center", "#1B2631");
            ctx.fillStyle = "#27AE60"; ctx.fillRect(315, 185, 38, 38); ctx.strokeRect(315, 185, 38, 38);
            drawPixelText("+", 334, 210, 20);

            drawCleanText(t.sfxLabel, 40, 250, 16, "left", "#1B2631");
            ctx.fillStyle = sfxMuted ? "#C0392B" : "#27AE60";
            ctx.fillRect(220, 255, 130, 38); ctx.strokeRect(220, 255, 130, 38);
            drawPixelText(sfxMuted ? "TẮT (OFF)" : "BẬT (ON)", 285, 280, 15);

            ctx.fillStyle = "#E74C3C"; ctx.fillRect(180, 300, 38, 38); ctx.strokeRect(180, 300, 38, 38);
            drawPixelText("-", 199, 325, 20);
            drawCleanText("Vol: " + Math.round(sfxVolume * 100) + "%", 255, 325, 16, "center", "#1B2631");
            ctx.fillStyle = "#27AE60"; ctx.fillRect(315, 300, 38, 38); ctx.strokeRect(315, 300, 38, 38);
            drawPixelText("+", 334, 325, 20);

            ctx.fillStyle = "#2980B9";
            ctx.fillRect(130, 395, 140, 45);
            ctx.strokeStyle = "#000"; ctx.lineWidth = 2; ctx.strokeRect(130, 395, 140, 45);
            drawPixelText(t.closeBtn, 200, 423, 18);
        }}

        function drawGuideModal() {{
            if (!showGuideModal) return;
            let t = i18n[currentLang];

            ctx.fillStyle = "rgba(0, 0, 0, 0.85)";
            ctx.fillRect(0, 0, canvas.width, canvas.height);

            ctx.fillStyle = "#FFFFFF";
            ctx.fillRect(15, 30, 370, 440);
            ctx.strokeStyle = "#2C3E50";
            ctx.lineWidth = 4;
            ctx.strokeRect(15, 30, 370, 440);

            drawCleanText(t.guideTitle, canvas.width / 2, 70, 22, "center", "#1B4F72");

            let startY = 110;
            let stepGap = 38;
            drawCleanText(t.guideStep1, 25, startY, 17, "left", "#1B2631");
            drawCleanText(t.guideStep2, 25, startY + stepGap, 17, "left", "#1B2631");
            drawCleanText(t.guideStep3, 25, startY + stepGap * 2, 17, "left", "#1B2631");
            drawCleanText(t.guideStep4, 25, startY + stepGap * 3, 17, "left", "#1B2631");
            drawCleanText(t.guideStep5, 25, startY + stepGap * 4, 17, "left", "#1B2631");
            drawCleanText(t.guideStep6, 25, startY + stepGap * 5, 17, "left", "#1B2631");

            drawCleanText(t.guideWish, canvas.width / 2, 385, 18, "center", "#C0392B");

            ctx.fillStyle = "#E74C3C";
            ctx.fillRect(130, 410, 140, 45);
            ctx.strokeStyle = "#000";
            ctx.lineWidth = 2;
            ctx.strokeRect(130, 410, 140, 45);
            drawPixelText(t.closeBtn, 200, 438, 18);
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

            drawPixelText(t.confirmTitle, canvas.width / 2, 105, 22, "center", "#F1C40F");

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

            drawPixelText(t.confirmAsk, canvas.width / 2, 240, 18);
            drawPixelText(skin.name, canvas.width / 2, 270, 20, "center", "#3498DB");
            
            drawPixelText(t.price + skin.price, canvas.width / 2 - 12, 300, 20, "center", "#F1C40F");
            drawTomCoinIcon(canvas.width / 2 + 55, 293, 11);

            ctx.fillStyle = "#27AE60";
            ctx.fillRect(40, 330, 140, 50);
            ctx.strokeStyle = "#000";
            ctx.lineWidth = 3;
            ctx.strokeRect(40, 330, 140, 50);
            drawPixelText(t.buy, 110, 362, 20);

            ctx.fillStyle = "#C0392B";
            ctx.fillRect(220, 330, 140, 50);
            ctx.strokeStyle = "#000";
            ctx.lineWidth = 3;
            ctx.strokeRect(220, 330, 140, 50);
            drawPixelText(t.cancel, 290, 362, 20);
        }}

        function draw() {{
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            let t = i18n[currentLang];

            if (gameState === 'menu') {{
                drawBackground();
                drawPixelText("JOURNEY OF TOM", canvas.width / 2, 115, 28, "center", "#F1C40F");
                
                drawPixelText(t.coins + totalCoins, canvas.width / 2 - 10, 165, 20);
                drawTomCoinIcon(canvas.width / 2 + 52, 157, 11);

                ctx.fillStyle = (musicMuted && sfxMuted) ? "#C0392B" : "#27AE60";
                ctx.fillRect(160, 15, 42, 38);
                ctx.strokeStyle = "#FFF";
                ctx.lineWidth = 3;
                ctx.strokeRect(160, 15, 42, 38);
                drawPixelText("🔊", 181, 41, 18);

                ctx.fillStyle = "#D35400";
                ctx.fillRect(215, 15, 42, 38);
                ctx.strokeStyle = "#FFF";
                ctx.lineWidth = 3;
                ctx.strokeRect(215, 15, 42, 38);
                drawPixelText("📖", 236, 41, 18);

                ctx.fillStyle = "#8E44AD";
                ctx.fillRect(270, 15, 90, 38);
                ctx.strokeStyle = "#FFF";
                ctx.lineWidth = 3;
                ctx.strokeRect(270, 15, 90, 38);
                drawPixelText((currentLang === "vi" ? "🌐 VI" : "🌐 EN"), 315, 40, 16);

                ctx.fillStyle = "#27AE60";
                ctx.fillRect(60, 210, 280, 60);
                ctx.strokeStyle = "#000";
                ctx.lineWidth = 4;
                ctx.strokeRect(60, 210, 280, 60);
                drawPixelText(t.play, canvas.width / 2, 248, 22);

                ctx.fillStyle = "#2980B9";
                ctx.fillRect(60, 290, 280, 60);
                ctx.strokeRect(60, 290, 280, 60);
                drawPixelText(t.shop, canvas.width / 2, 328, 22);

                drawGuideModal();
                drawAudioModal();

            }} else if (gameState === 'level_select') {{
                drawBackground();
                drawPixelText(t.selectLevel, canvas.width / 2, 42, 24, "center", "#F1C40F");

                ctx.fillStyle = "#7F8C8D";
                ctx.fillRect(20, 15, 110, 38);
                ctx.strokeStyle = "#000";
                ctx.lineWidth = 3;
                ctx.strokeRect(20, 15, 110, 38);
                drawPixelText(t.back, 75, 40, 16);

                for (let i = 1; i <= 5; i++) {{
                    let lvl = levels[i];
                    let isUnlocked = (i <= unlockedLevel);

                    ctx.fillStyle = isUnlocked ? "rgba(0, 0, 0, 0.8)" : "rgba(50, 50, 50, 0.85)";
                    ctx.fillRect(20, 55 + i * 68, 360, 53);
                    ctx.strokeStyle = isUnlocked ? "#2ECC71" : "#555";
                    ctx.lineWidth = 3;
                    ctx.strokeRect(20, 55 + i * 68, 360, 53);

                    if (isUnlocked) {{
                        drawPixelText(t.lvlNames[i], 35, 78 + i * 68, 18, "left");
                        drawPixelText(t.target + lvl.targetScore + " | Phần thưởng: " + lvl.reward, 35, 98 + i * 68, 14, "left", "#F1C40F");
                        drawTomCoinIcon(325, 91 + i * 68, 8);
                    }} else {{
                        drawPixelText(t.lvlNames[i], 35, 78 + i * 68, 18, "left", "#888");
                        drawPixelText(t.locked, 35, 98 + i * 68, 15, "left", "#E74C3C");
                    }}
                }}

            }} else if (gameState === 'shop') {{
                drawBackground();
                drawPixelText(t.shop, canvas.width / 2, 38, 24, "center", "#F1C40F");
                drawPixelText(t.coins + totalCoins, canvas.width / 2 - 10, 65, 18);
                drawTomCoinIcon(canvas.width / 2 + 48, 58, 10);

                ctx.fillStyle = "#7F8C8D";
                ctx.fillRect(20, 15, 110, 38);
                ctx.strokeStyle = "#000";
                ctx.lineWidth = 3;
                ctx.strokeRect(20, 15, 110, 38);
                drawPixelText(t.back, 75, 40, 16);

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

                    drawPixelText(skin.name, 102, 106 + i * 88, 18, "left");

                    if (isSelected) {{
                        drawPixelText(t.using, 102, 132 + i * 88, 16, "left", "#2ECC71");
                    }} else if (isUnlocked) {{
                        drawPixelText(t.owned, 102, 132 + i * 88, 16, "left", "#AED6F1");
                    }} else {{
                        drawPixelText(t.price + skin.price, 102, 132 + i * 88, 16, "left", "#F1C40F");
                        drawTomCoinIcon(210 + skin.price.toString().length * 8, 126 + i * 88, 8);
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

                drawPixelText("LVL: " + currentLevel + " | " + score + "/" + lvl.targetScore, 15, 30, 18, "left");
                
                drawPixelText(totalCoins.toString(), 360, 30, 18, "right");
                drawTomCoinIcon(375, 23, 10);

                if (gameState === 'gameover') {{
                    ctx.fillStyle = "rgba(0, 0, 0, 0.85)";
                    ctx.fillRect(0, 0, canvas.width, canvas.height);
                    drawPixelText(t.failed, canvas.width / 2, 210, 32, "center", "#E74C3C");
                    drawPixelText(t.retry, canvas.width / 2, 260, 18);
                }}

                if (levelCompleted) {{
                    ctx.fillStyle = "rgba(0, 0, 0, 0.85)";
                    ctx.fillRect(0, 0, canvas.width, canvas.height);

                    if (currentLevel === 5) {{
                        drawPixelText(t.meetAngelaLine1, canvas.width / 2, 75, 18, "center", "#F1C40F");
                        drawPixelText(t.meetAngelaLine2, canvas.width / 2, 100, 18, "center", "#F1C40F");

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

                        drawPixelText(t.reward + coinsEarnedThisRun, canvas.width / 2 - 15, 230, 18, "center", "#2ECC71");
                        drawTomCoinIcon(canvas.width / 2 + 95, 223, 10);

                        drawPixelText(t.continue, canvas.width / 2, 290, 18);

                    }} else {{
                        drawPixelText(t.passLevel + currentLevel, canvas.width / 2, 110, 22, "center", "#2ECC71");
                        
                        drawPixelText(t.reward + coinsEarnedThisRun, canvas.width / 2 - 20, 175, 18, "center", "#F1C40F");
                        drawTomCoinIcon(canvas.width / 2 + 85, 168, 10);
                        
                        if (currentLevel < 5) {{
                            drawPixelText(t.unlockedNext, canvas.width / 2, 230, 17, "center", "#3498DB");
                        }}
                        
                        drawPixelText(t.continue, canvas.width / 2, 290, 17);
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
