# /sieu_dinh_bot/modules/sender.py

import os
import logging
import random
import asyncio
from datetime import datetime
from telegram import Bot, Message
from telegram.error import TelegramError
import config
import modules.messages as messages

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class MediaSendError(Exception):
    """Lỗi tùy chỉnh cho các trường hợp không gửi được media quan trọng."""
    pass

class BotSender:
    def __init__(self, bot_token: str, chat_id: str):
        self.bot = Bot(token=bot_token)
        self.chat_id = chat_id
        logging.info("✅ Bot đã khởi tạo thành công!")

    async def _send_message_with_retry(self, text: str, parse_mode='HTML') -> Message | None:
        for attempt in range(2):
            try:
                message = await self.bot.send_message(self.chat_id, text, parse_mode=parse_mode)
                return message
            except TelegramError as e:
                logging.warning(f"Lỗi gửi tin nhắn (lần {attempt+1}): {e}. Thử lại sau {config.RETRY_DELAY_SECONDS}s...")
                if attempt == 0: await asyncio.sleep(config.RETRY_DELAY_SECONDS)
        logging.error(f"❌ Gửi tin nhắn thất bại sau 2 lần thử.")
        return None

    async def _send_video(self, video_path: str, caption: str, parse_mode='HTML') -> Message:
        for attempt in range(2):
            try:
                with open(video_path, 'rb') as video_file:
                    sent_message = await self.bot.send_video(self.chat_id, video_file, caption=caption, parse_mode=parse_mode)
                logging.info(f"Đã gửi video: {os.path.basename(video_path)}")
                return sent_message
            except FileNotFoundError:
                error_msg = f"KHÔNG TÌM THẤY FILE video: {video_path}"
                logging.error(f"❌ {error_msg}")
                raise MediaSendError(error_msg)
            except TelegramError as e:
                logging.warning(f"Lỗi Telegram khi gửi video (lần {attempt+1}): {e}. Thử lại sau {config.RETRY_DELAY_SECONDS}s...")
                if attempt == 0: await asyncio.sleep(config.RETRY_DELAY_SECONDS)
        
        final_error_msg = f"Gửi video thất bại sau 2 lần thử: {os.path.basename(video_path)}"
        logging.error(f"❌ {final_error_msg}")
        raise MediaSendError(final_error_msg)
    
    async def _send_photo_with_retry(self, photo_path: str, caption: str, parse_mode='HTML'):
        # ... (giữ nguyên hàm này)
        for attempt in range(2):
            try:
                with open(photo_path, 'rb') as photo_file:
                    await self.bot.send_photo(self.chat_id, photo_file, caption=caption, parse_mode=parse_mode)
                logging.info(f"Đã gửi ảnh: {os.path.basename(photo_path)}")
                return True
            except Exception as e:
                logging.warning(f"Lỗi gửi ảnh (lần {attempt+1}): {e}. Thử lại sau {config.RETRY_DELAY_SECONDS}s...")
                if attempt == 0: await asyncio.sleep(config.RETRY_DELAY_SECONDS)

        final_error_msg = f"Gửi ảnh thất bại sau 2 lần thử: {os.path.basename(photo_path)}"
        logging.error(f"❌ {final_error_msg}")
        raise MediaSendError(final_error_msg)

    async def _send_gif_with_retry(self, gif_path: str, caption: str, parse_mode='HTML'):
        # ... (giữ nguyên hàm này)
        for attempt in range(2):
            try:
                with open(gif_path, 'rb') as gif_file:
                    await self.bot.send_animation(self.chat_id, gif_file, caption=caption, parse_mode=parse_mode)
                logging.info(f"Đã gửi GIF: {os.path.basename(gif_path)}")
                return True
            except FileNotFoundError:
                error_msg = f"KHÔNG TÌM THẤY FILE GIF: {gif_path}"
                logging.error(f"❌ {error_msg}")
                raise MediaSendError(error_msg)
            except Exception as e:
                logging.warning(f"Lỗi gửi GIF (lần {attempt+1}): {e}. Thử lại sau {config.RETRY_DELAY_SECONDS}s...")
                if attempt == 0: await asyncio.sleep(config.RETRY_DELAY_SECONDS)
        
        final_error_msg = f"Gửi GIF thất bại sau 2 lần thử: {os.path.basename(gif_path)}"
        logging.error(f"❌ {final_error_msg}")
        raise MediaSendError(final_error_msg)

    # ... (giữ nguyên các hàm send_good_morning, send_good_night, send_group_rules, ...)

    async def send_good_morning(self):
        await self._send_message_with_retry(messages.get_good_morning_message())
        logging.info("☀️  Đã gửi tin nhắn chào buổi sáng.")

    async def send_good_night(self):
        await self._send_message_with_retry(messages.get_good_night_message())
        logging.info("🌙  Đã gửi tin nhắn chúc ngủ ngon.")
    
    # /sieu_dinh_bot/modules/sender.py

async def send_group_rules(self):
    try:
        # Thay đổi từ gửi GIF sang gửi Video
        await self._send_video(config.RULES_VIDEO_PATH, messages.get_animated_rules_caption())
        logging.info("📜  Đã gửi video nội quy nhóm.")
    except MediaSendError as e:
        logging.error(f"Lỗi khi gửi video nội quy: {e}. Sẽ thử lại sau.")

    async def send_golden_tip(self):
        await self._send_message_with_retry(messages.get_golden_tip())
        logging.info("💡  Đã gửi tip vàng.")
    
    async def send_schedule_image(self):
        caption = "⏰ <b>KHUNG GIỜ LÊN CA HIẾU B.C.R</b> ⏰\n\n<i>Anh em chủ động theo dõi lịch để vào đúng phiên nhé!</i>"
        try:
            await self._send_photo_with_retry(config.SCHEDULE_IMAGE_PATH, caption)
        except MediaSendError as e:
            logging.error(f"Lỗi khi gửi ảnh lịch trình: {e}. Sẽ thử lại sau.")
    
    async def send_intro_video(self):
        caption = "💰 <b>HƯỚNG DẪN CHIA VỐN THEO TIÊU CHUẨN NHÓM</b> 💰\n\n<i>Ai có mức vốn bao nhiêu thì mình có chia lệnh cược sẵn mọi người xem nhé!</i>"
        try:
            await self._send_video(config.INTRO_VIDEO_PATH, caption)
        except MediaSendError as e:
            logging.error(f"Lỗi khi gửi video hướng dẫn: {e}. Sẽ thử lại sau.")

    # <<< THAY ĐỔI 1: Hàm này giờ trả về Message để lấy ID >>>
    async def send_start_session(self, session_time: datetime) -> Message:
        sent_message = await self._send_video(config.START_SESSION_VIDEO, messages.get_start_session_caption(session_time))
        return sent_message

    async def send_table_images(self) -> int:
        chosen_table_number = random.randint(1, 8)
        image_name = f"table{chosen_table_number}.jpg"
        image_path = os.path.join(config.TABLE_IMAGES_DIR, image_name)
        caption = messages.get_table_announcement_caption(chosen_table_number)
        await self._send_photo_with_retry(image_path, caption)
        return chosen_table_number

    # <<< THAY ĐỔI 2: Hàm này không còn ghim tin nhắn, chỉ gửi và trả về ID >>>
    async def send_prediction(self) -> int | None:
        sent_message = None
        try:
            sent_message = await self._send_video(config.PREDICTION_VIDEO, messages.get_prediction_caption())
        except MediaSendError as e:
            logging.warning(f"Lỗi gửi video dự đoán: {e}. Chuyển sang gửi tin nhắn văn bản.")
            fallback_text = messages.get_prediction_text_fallback()
            sent_message = await self._send_message_with_retry(fallback_text)

        if sent_message:
            return sent_message.message_id
        
        logging.error("❌❌ GỬI LỆNH THẤT BẠI: Không thể gửi video lẫn tin nhắn văn bản.")
        return None

    async def send_end_session(self, session_time: datetime, next_session_time: datetime, message_id_to_unpin: int | None):
        if message_id_to_unpin:
            try:
                await self.bot.unpin_chat_message(self.chat_id, message_id_to_unpin)
                logging.info(f"📌  Đã gỡ ghim tin nhắn (ID: {message_id_to_unpin}).")
            except TelegramError as e:
                logging.warning(f"⚠️  Không thể gỡ ghim tin nhắn: {e}")
        try:
            await self._send_video(config.END_SESSION_VIDEO, messages.get_end_session_caption(session_time, next_session_time))
        except MediaSendError:
            await self._send_message_with_retry(messages.get_end_session_caption(session_time, next_session_time))