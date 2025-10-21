import turtle
import colorsys
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk, ImageEnhance
import random, math, time, os
import pygame

# ======== CÀI ĐẶT BAN ĐẦU ========
pygame.mixer.init()

# Tạo cửa sổ turtle và lấy Tk root
turtle.bgcolor("black")
turtle.speed(0)
turtle.hideturtle()

screen = turtle.Screen()
canvas = screen.getcanvas()
root = canvas.winfo_toplevel()

# ======== CHỌN NHẠC MỞ ĐẦU ========
root.update()
print("🎵 Hãy chọn file nhạc mở đầu (hoặc Cancel để bỏ qua)...")
intro_path = filedialog.askopenfilename(
    parent=root,
    title="Chọn nhạc mở đầu",
    filetypes=[("Audio files", "*.mp3 *.wav *.ogg *.flac")]
)
if intro_path and os.path.isfile(intro_path):
    try:
        pygame.mixer.music.load(intro_path)
        pygame.mixer.music.play(-1)
        print("🎶 Đang phát nhạc mở đầu:", os.path.basename(intro_path))
    except Exception as e:
        print("Lỗi phát nhạc mở đầu:", e)
else:
    print("Không chọn nhạc mở đầu hoặc file không tồn tại -> bỏ qua.")

# ======== VẼ HOA ========
NUMBER_OF_PETALS = 16
NUMBER_OF_PETAL_VEINS = 18
hue = 0
for i in range(NUMBER_OF_PETALS):
    for j in range(NUMBER_OF_PETAL_VEINS):
        color = colorsys.hsv_to_rgb(hue, 1, 1)
        turtle.color(color)
        hue += 0.005
        turtle.right(90)
        radius = 150 - j * 6
        turtle.circle(radius, 90)
        turtle.left(90)
        turtle.circle(radius, 90)
        turtle.right(180)
    turtle.circle(40, 24)

print("🌸 Hoa đã vẽ xong — chuẩn bị chọn ảnh...")
# ======== VIẾT CHỮ Ở TÂM HOA ========
# ======== VIẾT CHỮ Ở TÂM HOA VỚI HIỆU ỨNG GÕ TỪNG KÝ TỰ ========
turtle.penup()
turtle.goto(0, 0)  # tâm hoa
turtle.color("#FFD700")  # vàng nhẹ, nổi bật
turtle.hideturtle()

message = " crush ❤️ 20/10"
font_style = ("Arial", 18, "bold")

# Hiệu ứng xuất hiện từng ký tự
display_text = ""
for ch in message:
    display_text += ch
    turtle.clear()  # xóa chữ cũ
    turtle.write(display_text, align="center", font=font_style)
    time.sleep(0.08)  # tốc độ gõ (giảm giá trị để nhanh hơn)

time.sleep(1.5)  # giữ chữ lại 1.5s trước khi tiếp tục


time.sleep(2)  # giữ chữ lại 2 giây trước khi tiếp tục
turtle.hideturtle()

# ======== TẠO CANVAS HIỂN THỊ ẢNH ========
photo_canvas = tk.Canvas(root, width=800, height=800, bg="black", highlightthickness=0)
photo_canvas.place(x=0, y=0)

# ======== CHỌN ẢNH PHÁO HOA ========
root.update()
file_paths = filedialog.askopenfilenames(
    parent=root,
    title="Chọn nhiều ảnh để tạo hiệu ứng pháo hoa",
    filetypes=[("Image files", "*.png *.jpg *.jpeg *.gif")]
)
if not file_paths:
    print("❌ Không có ảnh nào được chọn. Thoát.")
    turtle.done()
    exit()

images = []
for path in file_paths:
    try:
        pil = Image.open(path).resize((60, 60))
        tkimg = ImageTk.PhotoImage(pil, master=root)
        images.append(tkimg)
        print("✅ Đã tải:", os.path.basename(path))
    except Exception as e:
        print("⚠️ Lỗi khi tải ảnh:", e)
if not images:
    print("❌ Không có ảnh nào hợp lệ. Thoát.")
    turtle.done()
    exit()

# ======== CẤU HÌNH NHẠC TRÁI TIM & ẢNH NỀN ========
HEART_MUSIC_PATH = "C:\projectpy\music2.mp3"                # tên file nhạc (đặt cùng thư mục)
HEART_BACKGROUND_PATH = "C:\projectpy\flower1.jpg"          # tên ảnh nền (đặt cùng thư mục) nên cho ảnh crush  đây
bg_image_global = None                       # giữ ảnh nền để không bị GC

explosion_count = 0
MAX_EXPLOSIONS = 5
second_music_played = False

# ======== HÀM PHÁT NHẠC TRÁI TIM ========
# ======== HÀM PHÁT NHẠC TRÁI TIM (THÊM GIỌNG NÓI) ========
# ======== HÀM PHÁT NHẠC TRÁI TIM (GIỌNG NÓI + FADE-OUT) ========
def play_heart_music():
    global second_music_played
    if second_music_played:
        return
    second_music_played = True

    voice_path = "C:\projectpy\cc.mp3"   # 🎤 File giọng nói (đặt cùng thư mục)
     # 🎶 Nhạc nền trái tim

    try:
        if os.path.exists(voice_path):
            print("🎤 Đang phát giọng nói:", voice_path)
            pygame.mixer.music.load(voice_path)
            pygame.mixer.music.play()
            voice_sound = pygame.mixer.Sound(voice_path)
            voice_length = voice_sound.get_length()

            # ⏳ Phát gần hết giọng nói rồi mờ dần âm (fade-out)
            fade_duration = 1000  # 1000 ms = 1 giây mờ dần
            time.sleep(max(0, voice_length - (fade_duration / 1000)))
            pygame.mixer.music.fadeout(fade_duration)
            print("🔉 Đang làm mờ dần giọng nói...")
            time.sleep(1.0)  # đợi fade-out hoàn tất
        else:
            print("⚠️ Không tìm thấy file giọng nói:", voice_path)
            time.sleep(1)

        # 🎵 Sau khi giọng nói fade xong -> phát nhạc nền trái tim
        if os.path.exists(HEART_MUSIC_PATH):
            pygame.mixer.music.load(HEART_MUSIC_PATH)
            pygame.mixer.music.play(-1)
            print("🎶 Đang phát nhạc nền trái tim:", HEART_MUSIC_PATH)
        else:
            print("⚠️ Không tìm thấy nhạc nền trái tim:", HEART_MUSIC_PATH)

    except Exception as e:
        print("⚠️ Lỗi khi phát âm thanh:", e)


# ======== HÀM HIỆU ỨNG TRÁI TIM ĐẬP ========
# ======== HÀM HIỆU ỨNG TRÁI TIM ĐẬP (CÓ ÁNH SÁNG) ========
def heart_pulse_loop(particles, heart_points, bg_item=None, pulse_index=[0], brightness=[0.5]):
    if not photo_canvas.winfo_exists():
        return

    center_x, center_y = 400, 400
    scale_values = [1.0, 1.03, 1.06, 1.09, 1.06, 1.03, 1.0]
    scale = scale_values[pulse_index[0]]

    # Tăng giảm sáng theo nhịp đập
    brightness_values = [0.45, 0.5, 0.55, 0.6, 0.55, 0.5, 0.45]
    brightness_level = brightness_values[pulse_index[0]]

    for i, p in enumerate(particles):
        xt, yt = heart_points[i]
        dx = xt - center_x
        dy = yt - center_y
        new_x = center_x + dx * scale
        new_y = center_y + dy * scale
        photo_canvas.coords(p["id"], new_x, new_y)

    # Ánh sáng nền tim đập
    if bg_item:
        try:
            # Làm sáng – tối ảnh nền nhẹ theo nhịp
            bg_img = Image.open(HEART_BACKGROUND_PATH.strip()).resize((800, 800))
            from PIL import ImageDraw, ImageEnhance

            # Tạo mask hình trái tim (tô kín)
            mask = Image.new("L", (800, 800), 0)
            draw = ImageDraw.Draw(mask)
            heart_coords = []
            for i in range(0, 360, 2):
                t = math.radians(i)
                x = 16 * math.sin(t)**3
                y = 13 * math.cos(t) - 5 * math.cos(2*t) - 2 * math.cos(3*t) - math.cos(4*t)
                heart_coords.append((x * 15 + 400, -y * 15 + 400))
            draw.polygon(heart_coords, fill=255)

            enhancer = ImageEnhance.Brightness(bg_img)
            bg_img = enhancer.enhance(brightness_level)
            base = Image.new("RGBA", (800, 800), (0, 0, 0, 0))
            masked_bg = Image.composite(bg_img.convert("RGBA"), base, mask)

            global bg_image_global
            bg_image_global = ImageTk.PhotoImage(masked_bg, master=root)
            photo_canvas.itemconfig(bg_item, image=bg_image_global)
        except Exception as e:
            print("⚠️ Lỗi hiệu ứng sáng tim:", e)

    root.update()
    pulse_index[0] = (pulse_index[0] + 1) % len(scale_values)
    root.after(120, lambda: heart_pulse_loop(particles, heart_points, bg_item, pulse_index))

# ======== HÀM NỔ PHÁO HOA / HIỆU ỨNG TRÁI TIM ========
def explode_images(heart_shape=False):
    global bg_image_global
    particles = []
    num_particles = 30

    if heart_shape:
        print("💖 Hiển thị hình trái tim!")
        play_heart_music()

        # ======= ẢNH NỀN CHỈ TRONG VÙNG TRÁI TIM =======
        bg_item = None
        if os.path.exists(HEART_BACKGROUND_PATH.strip()):
            try:
                from PIL import ImageDraw, ImageEnhance

                bg_img = Image.open(HEART_BACKGROUND_PATH.strip()).resize((800, 800))
                base = Image.new("RGBA", (800, 800), (0, 0, 0, 0))

                # Mask trái tim (tô kín)
                mask = Image.new("L", (800, 800), 0)
                draw = ImageDraw.Draw(mask)
                heart_coords = []
                for i in range(0, 360, 2):
                    t = math.radians(i)
                    x = 16 * math.sin(t)**3
                    y = 13 * math.cos(t) - 5 * math.cos(2*t) - 2 * math.cos(3*t) - math.cos(4*t)
                    heart_coords.append((x * 15 + 400, -y * 15 + 400))
                draw.polygon(heart_coords, fill=255)

                # Làm tối ảnh nền một chút
                enhancer = ImageEnhance.Brightness(bg_img)
                bg_img = enhancer.enhance(0.5)

                masked_bg = Image.composite(bg_img.convert("RGBA"), base, mask)
                bg_image_global = ImageTk.PhotoImage(masked_bg, master=root)
                bg_item = photo_canvas.create_image(400, 400, image=bg_image_global)
                photo_canvas.tag_lower(bg_item)
                print("🌈 Ảnh nền hiển thị trong vùng trái tim:", HEART_BACKGROUND_PATH)
            except Exception as e:
                print("⚠️ Không thể tạo ảnh nền trái tim:", e)
        else:
            print("⚠️ Không tìm thấy ảnh nền:", HEART_BACKGROUND_PATH)

        # ======= TẠO HÌNH TRÁI TIM =======
        heart_points = []
        for i in range(num_particles):
            t = math.pi * 2 * i / num_particles
            x = 16 * math.sin(t)**3
            y = 13 * math.cos(t) - 5 * math.cos(2*t) - 2 * math.cos(3*t) - math.cos(4*t)
            heart_points.append((x * 15 + 400, -y * 15 + 400))

        for i in range(num_particles):
            img = random.choice(images)
            pid = photo_canvas.create_image(400, 400, image=img)
            particles.append({"id": pid, "target": heart_points[i]})

        # Di chuyển ảnh vào vị trí trái tim
        for step in range(60):
            for p in particles:
                x0, y0 = photo_canvas.coords(p["id"])
                xt, yt = p["target"]
                nx = x0 + (xt - x0) * 0.08
                ny = y0 + (yt - y0) * 0.08
                photo_canvas.coords(p["id"], nx, ny)
            root.update()
            time.sleep(0.03)

        # Bắt đầu hiệu ứng tim đập có ánh sáng
                # ======= HIỂN THỊ DÒNG CHỮ TRONG TRÁI TIM =======
        text = "tên crush 💖"
        font_style = ("Segoe Script", 22, "bold")
        text_id = photo_canvas.create_text(400, 400, text="", fill="#C51A1A", font=font_style)

        display_text = ""
        for ch in text:
            display_text += ch
            photo_canvas.itemconfig(text_id, text=display_text)
            root.update()
            time.sleep(0.08)  # tốc độ gõ
        print("✨ Dòng chữ đã hiển thị trong trái tim.")

        heart_pulse_loop(particles, heart_points, bg_item)

    else:
        print("💥 Nổ pháo hoa!")
        for i in range(num_particles):
            img = random.choice(images)
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(3, 8)
            particles.append({
                "id": photo_canvas.create_image(400, 400, image=img),
                "vx": math.cos(angle) * speed,
                "vy": math.sin(angle) * speed
            })

        for t in range(70):
            for p in particles:
                photo_canvas.move(p["id"], p["vx"], p["vy"])
            root.update()
            time.sleep(0.03)

        for p in particles:
            photo_canvas.delete(p["id"])



# ======== XỬ LÝ PHÍM ========
def on_key_press(event):
    global explosion_count
    key = event.keysym.lower()
    if key == "r":
        explosion_count += 1
        if explosion_count < MAX_EXPLOSIONS:
            explode_images()
        else:
            explode_images(heart_shape=True)
            explosion_count = 0

root.bind("<Key>", on_key_press)
    # ===== HIỆU ỨNG NHẤP NHÁY CHỮ THEO NHỊP TIM =====
try:
        # Cường độ sáng chữ dựa theo nhịp đập
        brightness_to_color = [255, 230, 200, 170, 200, 230, 255]
        brightness_val = brightness_to_color[pulse_index[0]]
        hex_color = f"#{brightness_val:02x}{brightness_val:02x}50"
        for item in photo_canvas.find_all():
            if photo_canvas.type(item) == "text":
                photo_canvas.itemconfig(item, fill=hex_color)
except Exception as e:
        print("⚠️ Lỗi hiệu ứng chữ sáng:", e)

root.after(500, explode_images)
turtle.done()
root.mainloop()
