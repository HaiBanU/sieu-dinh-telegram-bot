# /sieu_dinh_bot/main.py

import asyncio
import logging
from datetime import datetime, timedelta
import config
# --- NÂNG CẤP LOGIC: Import lớp lỗi tùy chỉnh ---
from modules.sender import BotSender, MediaSendError
import os
from flask import Flask
from threading import Thread


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is alive and the web server is running!"


# --- NÂNG CẤP LOGIC: Xử lý lỗi một cách chặt chẽ ---
async def run_session_workflow(sender: BotSender, session_time: datetime):
    prediction_message_id = None
    next_session_time = session_time + timedelta(minutes=config.SESSION_INTERVAL_MINUTES)
    
    try:
        logger.info(f"====== BẮT ĐẦU CA KÉO {session_time.strftime('%H:%M')} ======")
        
        # Các bước trong quy trình có thể tung ra MediaSendError
        await sender.send_start_session(session_time)
        await asyncio.sleep(config.DELAY_STEP_1_TO_2)
        
        await sender.send_table_images()
        await asyncio.sleep(config.DELAY_STEP_2_TO_3)
        
        prediction_message_id = await sender.send_prediction()
        await asyncio.sleep(config.DELAY_STEP_3_TO_4)

    except MediaSendError as e:
        # Đây là phần xử lý thông minh: Nếu có lỗi media, hủy ca và thông báo
        logger.error(f"---!!! HỦY CA KÉO do lỗi MediaSendError: {e} !!!---")
        await sender._send_message_with_retry(
            f"❗️❗️ <b>THÔNG BÁO KHẨN</b> ❗️❗️\n\n"
            f"Rất tiếc, ca kéo <b>{session_time.strftime('%H:%M')}</b> đã gặp sự cố kỹ thuật và không thể tiếp tục.\n\n"
            f"Nguyên nhân: <i>Lỗi không thể gửi tệp media quan trọng.</i>\n\n"
            f"Mong toàn thể anh em thông cảm. Chúng tôi sẽ khắc phục sớm nhất có thể."
        )

    except Exception as e:
        # Bắt các lỗi không xác định khác
        logger.error(f"❌ Gặp lỗi không xác định nghiêm trọng giữa ca kéo: {e}")
    
    finally:
        # Dù thành công hay thất bại, vẫn chạy phần kết thúc để dọn dẹp (gỡ ghim, báo ca tiếp)
        await sender.send_end_session(session_time, next_session_time, prediction_message_id)
        logger.info(f"====== KẾT THÚC CA KÉO {session_time.strftime('%H:%M')} ======\n")
# -------------------------------------------------------------------


# /sieu_dinh_bot/main.py

async def main_loop(sender: BotSender):
    logger.info("🚀 Bot đang khởi động và kiểm tra lịch trình...")
    last_day_checked = None
    sent_flags = {}

    while True:
        now = datetime.now(config.VN_TZ)

        # --- A. Quản lý trạng thái hàng ngày ---
        if now.date() != last_day_checked:
            logger.info(f"☀️  Ngày mới bắt đầu ({now.strftime('%d/%m/%Y')}). Đặt lại trạng thái.")
            sent_flags = {
                'good_night_sent': False,
                'last_rules_sent': None,
                'last_schedule_image_hour': -1,
                'last_intro_video_hour': -1,
                'last_golden_tip_hour': -1,
                'last_session_run_time': None
            }
            last_day_checked = now.date()
            
            # Gửi tin nhắn chào ngày mới ngay khi bước qua ngày mới
            await sender.send_good_morning()

        # --- B. Xác định giờ hoạt động chính (có phiên kéo) ---
        # Bắt đầu từ 6h30 sáng trở đi
        is_session_hours = now.hour > config.SESSION_START_HOUR or \
                           (now.hour == config.SESSION_START_HOUR and now.minute >= config.SESSION_START_MINUTE)

        if is_session_hours:
            # --- LOGIC GIỜ HOẠT ĐỘNG CHÍNH (06:30 - 23:59) ---
            
            # 1. Gửi các tin nhắn định kỳ (lịch, nội quy, video, tip vàng)
            if now.minute == 15 and now.hour != sent_flags['last_schedule_image_hour']:
                await sender.send_schedule_image()
                sent_flags['last_schedule_image_hour'] = now.hour
            # *** THAY ĐỔI: Chuyển logic gửi Tip Vàng vào đây, gửi vào phút 30 mỗi giờ ***
            elif now.minute == 30 and now.hour != sent_flags['last_golden_tip_hour']:
                await sender.send_golden_tip()
                sent_flags['last_golden_tip_hour'] = now.hour
            elif now.minute == 45 and now.hour != sent_flags['last_intro_video_hour']:
                await sender.send_intro_video()
                sent_flags['last_intro_video_hour'] = now.hour
            elif sent_flags['last_rules_sent'] is None or (now - sent_flags['last_rules_sent']) >= timedelta(hours=config.RULES_INTERVAL_HOURS):
                # Chỉ gửi nội quy nếu không trùng với thời gian bắt đầu phiên
                if now.minute % config.SESSION_INTERVAL_MINUTES != 0:
                    await sender.send_group_rules()
                    sent_flags['last_rules_sent'] = now

            # 2. Bắt đầu phiên kéo
            current_session_time = now.replace(second=0, microsecond=0)
            if now.minute % config.SESSION_INTERVAL_MINUTES == 0:
                if sent_flags.get('last_session_run_time') != current_session_time:
                    sent_flags['last_session_run_time'] = current_session_time
                    asyncio.create_task(run_session_workflow(sender, now))
            
            # 3. Gửi tin nhắn Chúc ngủ ngon gần nửa đêm
            if now.hour == 23 and now.minute >= 55 and not sent_flags.get('good_night_sent'):
                await sender.send_good_night()
                sent_flags['good_night_sent'] = True
        
        else:
            # --- LOGIC GIỜ NGHỈ NGƠI (00:00 - 06:29) ---
            # *** THAY ĐỔI: Bot sẽ không gửi tip nữa và ngủ một giấc dài ***
            logger.info(f"Giờ nghỉ ngơi (từ 00:00 đến 06:29). Bot sẽ kiểm tra lại sau {config.OFF_HOURS_SLEEP_MINUTES} phút.")
            await asyncio.sleep(config.OFF_HOURS_SLEEP_MINUTES * 60)
            continue # Bỏ qua sleep ngắn ở cuối và lặp lại

        # Chờ 10 giây trước khi lặp lại trong giờ hoạt động chính
        await asyncio.sleep(10)


# (Phần khởi động bot giữ nguyên như cũ)
if not all([config.TELEGRAM_TOKEN, config.CHAT_ID]):
    logger.critical("❌ Thiếu TELEGRAM_TOKEN hoặc CHAT_ID trong biến môi trường.")
else:
    logger.info("✅ Đã tìm thấy các biến môi trường. Bắt đầu khởi tạo bot...")
    bot_sender = BotSender(config.TELEGRAM_TOKEN, config.CHAT_ID)
    
    bot_thread = Thread(target=lambda: asyncio.run(main_loop(bot_sender)))
    bot_thread.daemon = True
    bot_thread.start()
    logger.info("✅ Luồng bot đã được khởi động.")