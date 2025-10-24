# /sieu_dinh_bot/config.py

import os
import pytz
from dotenv import load_dotenv

load_dotenv()

# --- CẤU HÌNH CƠ BẢN ---
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
CHAT_ID = os.getenv('CHAT_ID')
𝓑𝓞𝓢𝓢_SUPPORT_LINK = '@𝓑𝓞𝓢𝓢MinhHieuu'

# --- MÚI GIỜ ---
VN_TZ = pytz.timezone('Asia/Ho_Chi_Minh')

# --- ĐƯỜNG DẪN FILE ---
VIDEO_DIR = 'videos'
IMAGE_DIR = 'images'

START_SESSION_VIDEO = os.path.join(VIDEO_DIR, 'vao_ca.mp4')
PREDICTION_VIDEO = os.path.join(VIDEO_DIR, 'du_doan.mp4')
END_SESSION_VIDEO = os.path.join(VIDEO_DIR, 'ket_ca.mp4')
INTRO_VIDEO_PATH = os.path.join(VIDEO_DIR, 'chia_von.mp4')
RULES_VIDEO_PATH = os.path.join(VIDEO_DIR, 'noi_quy.mp4')

TABLE_IMAGES_DIR = os.path.join(IMAGE_DIR, 'tables')
SCHEDULE_IMAGE_PATH = os.path.join(IMAGE_DIR, 'khung_gio.jpg')


# --- LỊCH TRÌNH HOẠT ĐỘNG (ĐÃ THAY ĐỔI) ---
# Bot sẽ bắt đầu ca đầu tiên lúc 7h00 sáng
SESSION_START_HOUR = 7 
SESSION_START_MINUTE = 0

# Bot sẽ hoạt động đến hết ca 23:30
SESSION_END_HOUR = 24 
# --- THỜI GIAN ---
SESSION_INTERVAL_MINUTES = 10
RULES_INTERVAL_HOURS = 2
RETRY_DELAY_SECONDS = 3

DELAY_STEP_1_TO_2 = 20
DELAY_STEP_2_TO_3 = 20
DELAY_STEP_3_TO_4 = 30

OFF_HOURS_SLEEP_MINUTES = 60