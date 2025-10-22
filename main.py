# /sieu_dinh_bot/main.py

import asyncio
import logging
from datetime import datetime, timedelta
import config
from modules.sender import BotSender

# --- PHẦN THÊM MỚI ---
import os
from flask import Flask
from threading import Thread
# --- KẾT THÚC PHẦN THÊM MỚI ---


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# --- PHẦN THÊM MỚI ---
# Tạo một ứng dụng web Flask
app = Flask(__name__)

# Tạo một "route" hay một "endpoint" để UptimeRobot có thể truy cập
@app.route('/')
def home():
    return "I'm alive!"

# Hàm để chạy web server
def run_web_server():
    # Lấy cổng mà Render cung cấp, nếu không có thì mặc định là 10000
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
# --- KẾT THÚC PHẦN THÊM MỚI ---


async def run_session_workflow(sender: BotSender, session_time: datetime):
    # (Giữ nguyên toàn bộ nội dung của hàm này)
    prediction_message_id = None
    try:
        logger.info(f"====== BẮT ĐẦU CA KÉO {session_time.strftime('%H:%M')} ======")
        next_session_time = session_time + timedelta(minutes=config.SESSION_INTERVAL_MINUTES)
        
        await sender.send_start_session(session_time)
        await asyncio.sleep(config.DELAY_STEP_1_TO_2)
        
        await sender.send_table_images()
        
        await asyncio.sleep(config.DELAY_STEP_2_TO_3)
        prediction_message_id = await sender.send_prediction()
        await asyncio.sleep(config.DELAY_STEP_3_TO_4)
        
    except Exception as e:
        logger.error(f"❌ Gặp lỗi nghiêm trọng giữa ca kéo: {e}")
    finally:
        await sender.send_end_session(session_time, next_session_time, prediction_message_id)
        logger.info(f"====== KẾT THÚC CA KÉO {session_time.strftime('%H:%M')} ======\n")

async def main_loop(sender: BotSender):
    # (Giữ nguyên toàn bộ nội dung của hàm này)
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


if __name__ == "__main__":
    if not all([config.TELEGRAM_TOKEN, config.CHAT_ID]):
        logger.critical("❌ Một hoặc nhiều cấu hình (TELEGRAM_TOKEN, CHAT_ID) chưa được thiết lập trong file .env.")
    else:
        try:
            bot_sender = BotSender(config.TELEGRAM_TOKEN, config.CHAT_ID)
            
            # --- PHẦN THAY ĐỔI ---
            # Chạy bot trong một luồng (thread) riêng
            bot_thread = Thread(target=lambda: asyncio.run(main_loop(bot_sender)))
            bot_thread.start()
            
            # Chạy web server trong luồng chính
            run_web_server()
            # --- KẾT THÚC PHẦN THAY ĐỔI ---

        except (KeyboardInterrupt, SystemExit):
            logger.info("🛑 Bot đã dừng hoạt động.")
        except Exception as e:
            logger.critical(f"❌ Bot gặp lỗi không thể phục hồi: {e}")