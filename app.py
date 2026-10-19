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
                sfxLabel
