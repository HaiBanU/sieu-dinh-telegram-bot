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


async def main_loop(sender: BotSender):
    logger.info("🚀 Bot đang khởi động và kiểm tra lịch trình...")
    last_day_checked = None
    sent_flags = {}
    last_session_run_time = None

    while True:
        now = datetime.now(config.VN_TZ)
        if now.date() != last_day_checked:
            logger.info(f"☀️  Ngày mới bắt đầu ({now.strftime('%d/%m/%Y')}). Đặt lại trạng thái.")
            sent_flags = {
                'good_morning': False, 'good_night': False,
                'last_rules_sent': None, 'last_schedule_image_hour': -1,
                'last_intro_video_hour': -1, 'last_golden_tip_hour': -1
            }
            last_day_checked = now.date()

        current_hour = now.hour
        is_working_hours = config.SESSION_START_HOUR <= current_hour < config.SESSION_END_HOUR

        if not is_working_hours:
            if current_hour < config.SESSION_START_HOUR and not sent_flags['good_morning']:
                await sender.send_good_morning()
                sent_flags['good_morning'] = True
            elif current_hour >= config.SESSION_END_HOUR and not sent_flags['good_night']:
                await sender.send_good_night()
                sent_flags['good_night'] = True
            if current_hour != sent_flags['last_golden_tip_hour']:
                await sender.send_golden_tip()
                sent_flags['last_golden_tip_hour'] = current_hour
        else:
            if now.minute == 15 and current_hour != sent_flags['last_schedule_image_hour']:
                await sender.send_schedule_image()
                sent_flags['last_schedule_image_hour'] = current_hour
            elif now.minute == 45 and current_hour != sent_flags['last_intro_video_hour']:
                await sender.send_intro_video()
                sent_flags['last_intro_video_hour'] = current_hour
            elif sent_flags['last_rules_sent'] is None or (now - sent_flags['last_rules_sent']) >= timedelta(hours=config.RULES_INTERVAL_HOURS):
                if now.minute % config.SESSION_INTERVAL_MINUTES != 0:
                    await sender.send_group_rules()
                    sent_flags['last_rules_sent'] = now

            current_session_time = now.replace(second=0, microsecond=0)
            if now.minute % config.SESSION_INTERVAL_MINUTES == 0:
                if current_session_time != last_session_run_time:
                    last_session_run_time = current_session_time
                    asyncio.create_task(run_session_workflow(sender, now))

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