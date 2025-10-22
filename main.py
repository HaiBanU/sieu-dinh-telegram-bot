# /sieu_dinh_bot/main.py

import asyncio
import logging
from datetime import datetime, timedelta
import config
from modules.sender import BotSender

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

async def run_session_workflow(sender: BotSender, session_time: datetime):
    prediction_message_id = None
    try:
        logger.info(f"====== BẮT ĐẦU CA KÉO {session_time.strftime('%H:%M')} ======")
        next_session_time = session_time + timedelta(minutes=config.SESSION_INTERVAL_MINUTES)
        
        await sender.send_start_session(session_time)
        await asyncio.sleep(config.DELAY_STEP_1_TO_2)
        
        # Vẫn gửi ảnh bàn để thông báo, nhưng không dùng số bàn này để chụp kết quả nữa
        await sender.send_table_images()
        
        await asyncio.sleep(config.DELAY_STEP_2_TO_3)
        prediction_message_id = await sender.send_prediction()
        await asyncio.sleep(config.DELAY_STEP_3_TO_4)
        
    except Exception as e:
        logger.error(f"❌ Gặp lỗi nghiêm trọng giữa ca kéo: {e}")
    finally:
        # Xóa chosen_table_number khỏi lời gọi hàm
        await sender.send_end_session(session_time, next_session_time, prediction_message_id)
        logger.info(f"====== KẾT THÚC CA KÉO {session_time.strftime('%H:%M')} ======\n")

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


if __name__ == "__main__":
    # Cập nhật lại điều kiện kiểm tra, bỏ các biến của casino
    if not all([config.TELEGRAM_TOKEN, config.CHAT_ID]):
        logger.critical("❌ Một hoặc nhiều cấu hình (TELEGRAM_TOKEN, CHAT_ID) chưa được thiết lập trong file .env.")
    else:
        try:
            bot_sender = BotSender(config.TELEGRAM_TOKEN, config.CHAT_ID)
            asyncio.run(main_loop(bot_sender))
        except (KeyboardInterrupt, SystemExit):
            logger.info("🛑 Bot đã dừng hoạt động.")
        except Exception as e:
            logger.critical(f"❌ Bot gặp lỗi không thể phục hồi: {e}")