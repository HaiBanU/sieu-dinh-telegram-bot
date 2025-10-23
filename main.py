# /sieu_dinh_bot/main.py

import asyncio
import logging
from datetime import datetime, timedelta
import config
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

async def run_session_workflow(sender: BotSender, session_time: datetime):
    # Thay vì ghim tin nhắn dự đoán, ta sẽ ghim tin nhắn bắt đầu ca
    message_id_to_pin = None
    next_session_time = session_time + timedelta(minutes=config.SESSION_INTERVAL_MINUTES)
    
    try:
        logger.info(f"====== BẮT ĐẦU CA KÉO {session_time.strftime('%H:%M')} ======")
        
        # Bước 1: Gửi video vào ca và lấy ID
        start_session_message = await sender.send_start_session(session_time)
        message_id_to_pin = start_session_message.message_id
        
        # Ghim tin nhắn này
        try:
            await sender.bot.pin_chat_message(sender.chat_id, message_id_to_pin, disable_notification=True)
            logger.info(f"📌  Đã ghim tin nhắn 'Vào ca' (ID: {message_id_to_pin}).")
        except Exception as e:
            logger.error(f"❌ Lỗi khi ghim tin nhắn 'Vào ca': {e}")

        await asyncio.sleep(config.DELAY_STEP_1_TO_2)
        
        # Các bước sau giữ nguyên
        await sender.send_table_images()
        await asyncio.sleep(config.DELAY_STEP_2_TO_3)
        
        # Hàm này giờ chỉ gửi lệnh, không ghim nữa
        await sender.send_prediction()
        await asyncio.sleep(config.DELAY_STEP_3_TO_4)

    except MediaSendError as e:
        logger.error(f"---!!! HỦY CA KÉO do lỗi MediaSendError: {e} !!!---")
        await sender._send_message_with_retry(
            f"❗️❗️ <b>THÔNG BÁO KHẨN</b> ❗️❗️\n\n"
            f"Rất tiếc, ca kéo <b>{session_time.strftime('%H:%M')}</b> đã gặp sự cố kỹ thuật và không thể tiếp tục.\n\n"
            f"Nguyên nhân: <i>Lỗi không thể gửi tệp media quan trọng.</i>\n\n"
            f"Mong toàn thể anh em thông cảm. Chúng tôi sẽ khắc phục sớm nhất có thể."
        )

    except Exception as e:
        logger.error(f"❌ Gặp lỗi không xác định nghiêm trọng giữa ca kéo: {e}")
    
    finally:
        # Cuối ca, gỡ ghim tin nhắn 'Vào ca'
        await sender.send_end_session(session_time, next_session_time, message_id_to_pin)
        logger.info(f"====== KẾT THÚC CA KÉO {session_time.strftime('%H:%M')} ======\n")

async def main_loop(sender: BotSender):
    logger.info("🚀 Bot đang khởi động và kiểm tra lịch trình...")
    last_day_checked = None
    sent_flags = {}

    while True:
        now = datetime.now(config.VN_TZ)

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
            
            await sender.send_good_morning()

        is_session_hours = now.hour > config.SESSION_START_HOUR or \
                           (now.hour == config.SESSION_START_HOUR and now.minute >= config.SESSION_START_MINUTE)

        if is_session_hours:
            if now.minute == 15 and now.hour != sent_flags['last_schedule_image_hour']:
                await sender.send_schedule_image()
                sent_flags['last_schedule_image_hour'] = now.hour
            elif now.minute == 30 and now.hour != sent_flags['last_golden_tip_hour']:
                await sender.send_golden_tip()
                sent_flags['last_golden_tip_hour'] = now.hour
            elif now.minute == 45 and now.hour != sent_flags['last_intro_video_hour']:
                await sender.send_intro_video()
                sent_flags['last_intro_video_hour'] = now.hour
            elif sent_flags['last_rules_sent'] is None or (now - sent_flags['last_rules_sent']) >= timedelta(hours=config.RULES_INTERVAL_HOURS):
                if now.minute % config.SESSION_INTERVAL_MINUTES != 0:
                    await sender.send_group_rules()
                    sent_flags['last_rules_sent'] = now

            current_session_time = now.replace(second=0, microsecond=0)
            if now.minute % config.SESSION_INTERVAL_MINUTES == 0:
                if sent_flags.get('last_session_run_time') != current_session_time:
                    sent_flags['last_session_run_time'] = current_session_time
                    asyncio.create_task(run_session_workflow(sender, now))
            
            # <<< THAY ĐỔI THỜI GIAN GỬI TIN NHẮN NGỦ NGON TẠI ĐÂY >>>
            # Sẽ gửi lúc 23:40, sau khi ca cuối cùng (23:30) kết thúc.
            if now.hour == 23 and now.minute == 40 and not sent_flags.get('good_night_sent'):
                await sender.send_good_night()
                sent_flags['good_night_sent'] = True
        
        else:
            logger.info(f"Giờ nghỉ ngơi (từ 00:00 đến {config.SESSION_START_HOUR-1}:59). Bot sẽ kiểm tra lại sau {config.OFF_HOURS_SLEEP_MINUTES} phút.")
            await asyncio.sleep(config.OFF_HOURS_SLEEP_MINUTES * 60)
            continue

        await asyncio.sleep(10)


if not all([config.TELEGRAM_TOKEN, config.CHAT_ID]):
    logger.critical("❌ Thiếu TELEGRAM_TOKEN hoặc CHÁT_ID trong biến môi trường.")
else:
    logger.info("✅ Đã tìm thấy các biến môi trường. Bắt đầu khởi tạo bot...")
    bot_sender = BotSender(config.TELEGRAM_TOKEN, config.CHAT_ID)
    
    bot_thread = Thread(target=lambda: asyncio.run(main_loop(bot_sender)))
    bot_thread.daemon = True
    bot_thread.start()
    logger.info("✅ Luồng bot đã được khởi động.")