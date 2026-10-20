import streamlit as st
import base64
import os

st.set_page_config(page_title="The journey of Tom", page_icon="🐱", layout="centered")

st.title("🐱 The journey of Tom")
st.write("Hành trình của Tom - Hãy tận hưởng trò chơi!")

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
                play: "CHOI GAME",
                shop: "CUA HANG",
                selectLevel: "CHON CAP DO",
                back: "<- LUI",
                coins: "XU: ",
                target: "Muc tieu: ",
                reward: "Thuong: ",
                using: "DANG DUNG",
                owned: "DA SO HUU",
                price: "GIA: ",
                confirmTitle: "XAC NHAN MUA",
                confirmAsk: "Ban co chac muon mua?",
                buy: "MUA",
                cancel: "HUY",
                failed: "THAT BAI!",
                retry: "Nhan Space de thu lai",
                passLevel: "VUOT AI ",
                meetAngelaLine1: "Hoan thanh man 5 de giup Tom",
                meetAngelaLine2: "gap duoc tinh yeu cua anh ay!",
                continue: "Nhan Space de tiep tuc",
                notEnoughCoins: "Ban khong du xu!",
                locked: "🔒 KHOA",
                unlockedNext: "Da mo khoa man tiep theo!",
                audioTitle: "CAI DAT AM THANH",
                bgMusicLabel: "Nhac nen:",
                sfxLabel: "Hieu ung:",
                closeBtn: "DONG",
                guideTitle: "HUONG DAN",
                guideStep1: "• Nhan SPACE hoac cham",
                guideStep2: "  de Tom bay len.",
                guideStep3: "• Dat diem de mo man moi.",
                guideStep4: "• Tich xu doi skin cho Tom.",
                guideStep5: "• Hoan thanh man 5 de",
                guideStep6: "  giup Tom gap Angela.",
                guideWish: "Chuc ban choi game vui ve!",
                lvlNames: {{
                    1: "CAP 1: KHOI DAU",
                    2: "CAP 2: VUOT THAC",
                    3: "CAP 3: RUNG SAU",
                    4: "CAP 4: THU THACH",
                    5: "CAP 5: GAP ANGELA"
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
                confirmTitle: "CONFIRM",
                confirmAsk: "Are you sure to buy?",
                buy: "BUY",
                cancel: "CANCEL",
                failed: "GAME OVER!",
                retry: "Press Space to retry",
                passLevel: "LEVEL PASSED ",
                meetAngelaLine1: "Complete Level 5 to help Tom",
                meetAngelaLine2: "meet the love of his life!",
                continue: "Press Space to continue",
                notEnoughCoins: "Not enough coins!",
                locked: "🔒 LOCKED",
                unlockedNext: "Unlocked Next Level!",
                audioTitle: "AUDIO SETTINGS",
                bgMusicLabel: "Music:",
                sfxLabel: "SFX:",
                closeBtn: "CLOSE",
                guideTitle: "GAME GUIDE",
                guideStep1: "• Press SPACE or click",
                guideStep2: "  to make Tom fly up.",
                guideStep3: "• Reach target scores.",
                guideStep4: "• Collect coins for skins.",
                guideStep5: "• Complete Level 5 to",
                guideStep6: "  meet Angela.",
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
            width: 95,   /* Đã thu ngắn chiều dài nhân vật lại từ 125 xuống 95 */
            height: 60,  /* Tỉ lệ chiều cao đi kèm tương ứng */
            gravity: 0.28,
            lift: -6.8,
            velocity: 0
        }};

        let currentLevel = 1;
        const levels = {{
            1: {{ speed: 1.2, gap: 240, spawnRate: 130, targetScore: 10, reward: 15 }},
            2: {{ speed: 1.35, gap: 230, spawnRate: 120, targetScore: 20, reward: 30 }},
            3: {{ speed: 1.5, gap: 220, spawnRate: 110, targetScore: 30, reward: 50 }},
            4: {{ speed: 1.9, gap: 175, spawnRate: 85,  targetScore: 50, reward: 90 }},
            5: {{ speed: 2.2, gap: 155, spawnRate: 75,  targetScore: 65, reward: 150 }}
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

            let hitboxPaddingX = 16;
            let hitboxPaddingY = 10;

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

        function drawBackground() {{
            let activeBg = bgImage1;

            if (gameState === 'playing' && playStartTime > 0) {{
                let playedSeconds = Math.floor((Date.now() - playStartTime) / 1000);
                let cycleTime = playedSeconds % 40;

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
            ctx.font = size + "px 'Press Start 2P', monospace";
            ctx.textAlign = align;
            
            ctx.shadowColor = "rgba(0, 0, 0, 0.85)";
            ctx.shadowBlur = 0;
            ctx.shadowOffsetX = 3;
            ctx.shadowOffsetY = 3;

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
            ctx.fillRect(25, 45, 350, 420);
            ctx.strokeStyle = "#2C3E50";
            ctx.lineWidth = 4;
            ctx.strokeRect(25, 45, 350, 420);

            drawPixelText(t.audioTitle, canvas.width / 2, 85, 14, "center", "#1B4F72");

            drawPixelText(t.bgMusicLabel, 40, 130, 10, "left", "#1B2631");
            ctx.fillStyle = musicMuted ? "#C0392B" : "#27AE60";
            ctx.fillRect(220, 112, 130, 34);
            ctx.strokeStyle = "#000"; ctx.lineWidth = 2; ctx.strokeRect(220, 112, 130, 34);
            drawPixelText(musicMuted ? "TAT" : "BAT", 285, 135, 10);

            ctx.fillStyle = "#E74C3C"; ctx.fillRect(170, 160, 34, 34); ctx.strokeRect(170, 160, 34, 34);
            drawPixelText("-", 187, 183, 14);
            drawPixelText("Vol:" + Math.round(musicVolume * 100) + "%", 275, 183, 10, "center", "#1B2631");
            ctx.fillStyle = "#27AE60"; ctx.fillRect(315, 160, 34, 34); ctx.strokeRect(315, 160, 34, 34);
            drawPixelText("+", 332, 183, 14);

            drawPixelText(t.sfxLabel, 40, 230, 10, "left", "#1B2631");
            ctx.fillStyle = sfxMuted ? "#C0392B" : "#27AE60";
            ctx.fillRect(220, 212, 130, 34); ctx.strokeRect(220, 212, 130, 34);
            drawPixelText(sfxMuted ? "TAT" : "BAT", 285, 235, 10);

            ctx.fillStyle = "#E74C3C"; ctx.fillRect(170, 260, 34, 34); ctx.strokeRect(170, 260, 34, 34);
            drawPixelText("-", 187, 283, 14);
            drawPixelText("Vol:" + Math.round(sfxVolume * 100) + "%", 275, 283, 10, "center", "#1B2631");
            ctx.fillStyle = "#27AE60"; ctx.fillRect(315, 260, 34, 34); ctx.strokeRect(315, 260, 34, 34);
            drawPixelText("+", 332, 283, 14);

            ctx.fillStyle = "#2980B9";
            ctx.fillRect(115, 395, 170, 45);
            ctx.strokeStyle = "#000"; ctx.lineWidth = 2; ctx.strokeRect(115, 395, 170, 45);
            drawPixelText(t.closeBtn, 200, 423, 12);
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

            drawPixelText(t.guideTitle, canvas.width / 2, 70, 14, "center", "#1B4F72");

            let startY = 110;
            let stepGap = 42;
            drawPixelText(t.guideStep1, 25, startY, 9, "left", "#1B2631");
            drawPixelText(t.guideStep2, 25, startY + stepGap, 9, "left", "#1B2631");
            drawPixelText(t.guideStep3, 25, startY + stepGap * 2, 9, "left", "#1B2631");
            drawPixelText(t.guideStep4, 25, startY + stepGap * 3, 9, "left", "#1B2631");
            drawPixelText(t.guideStep5, 25, startY + stepGap * 4, 9, "left", "#1B2631");
            drawPixelText(t.guideStep6, 25, startY + stepGap * 5, 9, "left", "#1B2631");

            drawPixelText(t.guideWish, canvas.width / 2, 380, 9, "center", "#C0392B");

            ctx.fillStyle = "#E74C3C";
            ctx.fillRect(115, 405, 170, 45);
            ctx.strokeStyle = "#000";
            ctx.lineWidth = 2;
            ctx.strokeRect(115, 405, 170, 45);
            drawPixelText(t.closeBtn, 200, 433, 12);
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

            drawPixelText(t.confirmTitle, canvas.width / 2, 105, 14, "center", "#F1C40F");

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
            drawPixelText(skin.name, canvas.width / 2, 265, 11, "center", "#3498DB");
            
            drawPixelText(t.price + skin.price, canvas.width / 2 - 15, 300, 11, "center", "#F1C40F");
            drawTomCoinIcon(canvas.width / 2 + 65, 292, 10);

            ctx.fillStyle = "#27AE60";
            ctx.fillRect(40, 330, 140, 50);
            ctx.strokeStyle = "#000";
            ctx.lineWidth = 3;
            ctx.strokeRect(40, 330, 140, 50);
            drawPixelText(t.buy, 110, 362, 12);

            ctx.fillStyle = "#C0392B";
            ctx.fillRect(220, 330, 140, 50);
            ctx.strokeStyle = "#000";
            ctx.lineWidth = 3;
            ctx.strokeRect(220, 330, 140, 50);
            drawPixelText(t.cancel, 290, 362, 12);
        }}

        function draw() {{
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            let t = i18n[currentLang];

            if (gameState === 'menu') {{
                drawBackground();
                drawPixelText("JOURNEY OF TOM", canvas.width / 2, 115, 16, "center", "#F1C40F");
                
                drawPixelText(t.coins + totalCoins, canvas.width / 2 - 12, 165, 11);
                drawTomCoinIcon(canvas.width / 2 + 65, 158, 10);

                ctx.fillStyle = (musicMuted && sfxMuted) ? "#C0392B" : "#27AE60";
                ctx.fillRect(160, 15, 42, 38);
                ctx.strokeStyle = "#FFF";
                ctx.lineWidth = 3;
                ctx.strokeRect(160, 15, 42, 38);
                drawPixelText("🔊", 181, 41, 14);

                ctx.fillStyle = "#D35400";
                ctx.fillRect(215, 15, 42, 38);
                ctx.strokeStyle = "#FFF";
                ctx.lineWidth = 3;
                ctx.strokeRect(215, 15, 42, 38);
                drawPixelText("📖", 236, 41, 14);

                ctx.fillStyle = "#8E44AD";
                ctx.fillRect(270, 15, 90, 38);
                ctx.strokeStyle = "#FFF";
                ctx.lineWidth = 3;
                ctx.strokeRect(270, 15, 90, 38);
                drawPixelText((currentLang === "vi" ? "VI" : "EN"), 315, 41, 11);

                ctx.fillStyle = "#27AE60";
                ctx.fillRect(60, 210, 280, 60);
                ctx.strokeStyle = "#000";
                ctx.lineWidth = 4;
                ctx.strokeRect(60, 210, 280, 60);
                drawPixelText(t.play, canvas.width / 2, 248, 14);

                ctx.fillStyle = "#2980B9";
                ctx.fillRect(60, 290, 280, 60);
                ctx.strokeRect(60, 290, 280, 60);
                drawPixelText(t.shop, canvas.width / 2, 328, 14);

                drawGuideModal();
                drawAudioModal();

            }} else if (gameState === 'level_select') {{
                drawBackground();
                drawPixelText(t.selectLevel, canvas.width / 2, 42, 13, "center", "#F1C40F");

                ctx.fillStyle = "#7F8C8D";
                ctx.fillRect(20, 15, 100, 38);
                ctx.strokeStyle = "#000";
                ctx.lineWidth = 3;
                ctx.strokeRect(20, 15, 100, 38);
                drawPixelText(t.back, 70, 40, 10);

                for (let i = 1; i <= 5; i++) {{
                    let lvl = levels[i];
                    let isUnlocked = (i <= unlockedLevel);

                    ctx.fillStyle = isUnlocked ? "rgba(0, 0, 0, 0.8)" : "rgba(50, 50, 50, 0.85)";
                    ctx.fillRect(20, 55 + i * 68, 360, 53);
                    ctx.strokeStyle = isUnlocked ? "#2ECC71" : "#555";
                    ctx.lineWidth = 3;
                    ctx.strokeRect(20, 55 + i * 68, 360, 53);

                    if (isUnlocked) {{
                        drawPixelText(t.lvlNames[i], 32, 78 + i * 68, 10, "left");
                        drawPixelText(t.target + lvl.targetScore + " | Thuong: " + lvl.reward, 32, 96 + i * 68, 8, "left", "#F1C40F");
                        drawTomCoinIcon(330, 91 + i * 68, 7);
                    }} else {{
                        drawPixelText(t.lvlNames[i], 32, 78 + i * 68, 10, "left", "#888");
                        drawPixelText(t.locked, 32, 96 + i * 68, 9, "left", "#E74C3C");
                    }}
                }}

            }} else if (gameState === 'shop') {{
                drawBackground();
                drawPixelText(t.shop, canvas.width / 2, 38, 14, "center", "#F1C40F");
                drawPixelText(t.coins + totalCoins, canvas.width / 2 - 12, 65, 10);
                drawTomCoinIcon(canvas.width / 2 + 55, 58, 9);

                ctx.fillStyle = "#7F8C8D";
                ctx.fillRect(20, 15, 100, 38);
                ctx.strokeStyle = "#000";
                ctx.lineWidth = 3;
                ctx.strokeRect(20, 15, 100, 38);
                drawPixelText(t.back, 70, 40, 10);

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

                    drawPixelText(skin.name, 102, 106 + i * 88, 11, "left");

                    if (isSelected) {{
                        drawPixelText(t.using, 102, 130 + i * 88, 9, "left", "#2ECC71");
                    }} else if (isUnlocked) {{
                        drawPixelText(t.owned, 102, 130 + i * 88, 9, "left", "#AED6F1");
                    }} else {{
                        drawPixelText(t.price + skin.price, 102, 130 + i * 88, 9, "left", "#F1C40F");
                        drawTomCoinIcon(215 + skin.price.toString().length * 6, 125 + i * 88, 7);
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

                drawPixelText("LVL:" + currentLevel + " " + score + "/" + lvl.targetScore, 15, 30, 10, "left");
                
                drawPixelText(totalCoins.toString(), 345, 30, 10, "right");
                drawTomCoinIcon(365, 23, 9);

                if (gameState === 'gameover') {{
                    ctx.fillStyle = "rgba(0, 0, 0, 0.85)";
                    ctx.fillRect(0, 0, canvas.width, canvas.height);
                    drawPixelText(t.failed, canvas.width / 2, 210, 18, "center", "#E74C3C");
                    drawPixelText(t.retry, canvas.width / 2, 260, 9);
                }}

                if (levelCompleted) {{
                    ctx.fillStyle = "rgba(0, 0, 0, 0.85)";
                    ctx.fillRect(0, 0, canvas.width, canvas.height);

                    if (currentLevel === 5) {{
                        drawPixelText(t.meetAngelaLine1, canvas.width / 2, 75, 10, "center", "#F1C40F");
                        drawPixelText(t.meetAngelaLine2, canvas.width / 2, 100, 10, "center", "#F1C40F");

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

                        drawPixelText(t.reward + coinsEarnedThisRun, canvas.width / 2 - 15, 230, 10, "center", "#2ECC71");
                        drawTomCoinIcon(canvas.width / 2 + 95, 222, 9);

                        drawPixelText(t.continue, canvas.width / 2, 290, 9);

                    }} else {{
                        drawPixelText(t.passLevel + currentLevel, canvas.width / 2, 110, 12, "center", "#2ECC71");
                        
                        drawPixelText(t.reward + coinsEarnedThisRun, canvas.width / 2 - 20, 175, 11, "center", "#F1C40F");
                        drawTomCoinIcon(canvas.width / 2 + 85, 168, 9);
                        
                        if (currentLevel < 5) {{
                            drawPixelText(t.unlockedNext, canvas.width / 2, 230, 10, "center", "#3498DB");
                        }}
                        
                        drawPixelText(t.continue, canvas.width / 2, 290, 9);
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
