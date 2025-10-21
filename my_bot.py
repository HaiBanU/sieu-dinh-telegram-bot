# ==================== PHẦN IMPORT THƯ VIỆN ====================
import telegram
import asyncio
import random
from datetime import datetime, timedelta
import os
# ===============================================================

# ==================== PHẦN CẤU HÌNH (Điền lại thông tin của bạn) ====================
# ĐẶT TOKEN CỦA BẠN LẠI VÀO ĐÂY
TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN')
CHAT_ID = os.environ.get('CHAT_ID')
BOSS_SUPPORT_LINK = '@BossKimLongg'

# --- Tên các file video ---
WARNING_VIDEO_PATH = 'canhbao.mp4'
PREDICTION_VIDEO_PATH = 'dudoan.mp4'
END_VIDEO_PATH = 'ketthuc.mp4'

# --- Thời gian chờ cho tin nhắn nội quy (30 phút) ---
RULES_MESSAGE_INTERVAL = 30 * 60

# --- KHUNG GIỜ HOẠT ĐỘNG CHÍNH (Từ 12h trưa đến 22h tối) ---
HOAT_DONG_BAT_DAU = 12
HOAT_DONG_KET_THUC = 22
# ===================================================================================

# --- KHỞI TẠO BOT ---
try:
    bot = telegram.Bot(token=TELEGRAM_TOKEN)
    print("✅ Bot đã khởi tạo thành công!")
except Exception as e:
    print(f"❌ Lỗi khởi tạo bot: {e}. Hãy kiểm tra lại TELEGRAM_TOKEN.")
    exit()

# --- DANH SÁCH BÀN CHƠI ---
danh_sach_ban = [f"BACCARAT {i}" for i in range(1, 9)] + [f"BACCARAT C0{i}" for i in range(1, 9)]

# --- NỘI DUNG CHO KHUNG GIỜ NGHỈ ---
# (Phần này giữ nguyên, không cần thay đổi)
off_hours_messages = [
    f"""🧠 <b>GÓC KIẾN THỨC: QUẢN LÝ VỐN</b> 🧠\n━━━━━━━━━━━━━━━━━━\nTại sao chúng ta luôn được khuyên đi vốn <b>20%</b>?\n\n1️⃣ <b>An Toàn:</b> Giúp bạn chịu được 1-2 tay không may mắn mà không bị "cháy" tài khoản.\n2️⃣ <b>Bền Vững:</b> Kiếm lợi nhuận nhỏ nhưng đều đặn sẽ tốt hơn là một lần "tất tay" đầy rủi ro.\n3️⃣ <b>Tâm Lý:</b> Vốn được chia nhỏ giúp bạn giữ được cái đầu lạnh để đưa ra quyết định sáng suốt.\n\n👉 <i>Hãy nhớ, đường dài mới biết ngựa hay. Kỷ luật vốn là chìa khóa thành công!</i>""",
    f"""💡 <b>BÍ KÍP SOI CẦU: CẦU BỆT</b> 💡\n━━━━━━━━━━━━━━━━━━\nCầu bệt là một chuỗi kết quả liên tiếp chỉ ra CÁI hoặc CON (ví dụ: CÁI - CÁI - CÁI - CÁI...).\n\n✅ <b>Dấu hiệu:</b> Khi có từ 3-4 tay cùng ra một kết quả, khả năng cao cầu bệt đã hình thành.\n✅ <b>Hành động:</b> Bám theo cầu cho đến khi gãy.\n❌ <b>Sai lầm:</b> Cố gắng "bẻ cầu" quá sớm. Việc này cực kỳ rủi ro.\n\n<i>Chúc anh em áp dụng thành công và gặt hái kết quả!</i>""",
    f"""멘 <b>BÀI HỌC TÂM LÝ: THẮNG KHÔNG KIÊU, BẠI KHÔNG NẢN</b> 멘\n━━━━━━━━━━━━━━━━━━\nThị trường luôn có biến động. Việc thắng hoặc thua một vài phiên là điều hết sức bình thường.\n\n🏆 <b>Khi thắng:</b> Hãy vui mừng nhưng đừng chủ quan. Chốt lãi và bảo toàn lợi nhuận.\n😔 <b>Khi thua:</b> Tuyệt đối không cay cú, không gấp thếp để gỡ. Hãy dừng lại, xem lại chiến lược và chờ đợi cơ hội tiếp theo.\n\n<b>Sự bình tĩnh và kỷ luật mới là người bạn đồng hành tin cậy nhất.</b>""",
    f"""⏰ <b>LỊCH HOẠT ĐỘNG NHÓM</b> ⏰\n━━━━━━━━━━━━━━━━━━\nAnh em lưu ý lịch hoạt động chính thức của đội chúng ta:\n\n🔔 <b>Thời gian kéo lệnh:</b> <b>12:00</b> trưa đến <b>22:00</b> tối hàng ngày.\n💡 <b>Ngoài khung giờ trên:</b> Nhóm sẽ chia sẻ kiến thức, kinh nghiệm và các bài học quản lý vốn.\n\n🆘 <b>Cần hỗ trợ?</b> Liên hệ ngay cho <b>{BOSS_SUPPORT_LINK}</b>.\n\n<i>Chúc anh em một ngày làm việc hiệu quả và nhiều năng lượng!</i>"""
]


# --- CÁC HÀM GỬI TIN NHẮN (Đã có thời gian thực) ---
# (Tất cả các hàm send_warning_message, send_prediction_message, v.v. giữ nguyên)
async def send_warning_message():
    thoi_gian_hien_tai = datetime.now().strftime('%H:%M:%S')
    ten_ban = random.choice(danh_sach_ban)
    captions = [f"""🎉🎉 <b>TÍN HIỆU VIP - CHUẨN BỊ VÀO PHIÊN</b> 🎉🎉\n━━━━━━━━━━━━━━━━━━\n⭐️⭐️ <b>Sảnh:   SEXY BACCARAT</b>\n🃏 <b>Bàn:    {ten_ban}</b>\n\n🕒 <i>Thời gian: {thoi_gian_hien_tai}</i>\n🔔 <i>Tín hiệu sẽ được phát sau <b>30 giây</b>. Toàn đội sẵn sàng!</i>""",f"""🎉🎉 <b>TOÀN ĐỘI TẬP TRUNG - PHIÊN MỚI</b> 🎉🎉\n━━━━━━━━━━━━━━━━━━\n⭐️⭐️ <b>Sảnh:   SEXY BACCARAT</b>\n🃏 <b>Bàn:    {ten_ban}</b>\n\n🕒 <i>Thời gian: {thoi_gian_hien_tai}</i>\n⏳ <i>Chuẩn bị tâm lý và vào vốn trong <b>30 giây</b> tới...</i>""",]
    caption_text = random.choice(captions)
    try:
        with open(WARNING_VIDEO_PATH, 'rb') as video_file:
            await bot.send_video(chat_id=CHAT_ID, video=video_file, caption=caption_text, parse_mode='HTML')
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Đã gửi video BÁO HIỆU.")
    except Exception as e:
        print(f"❌ Lỗi khi gửi video báo hiệu: {e}.")
        await bot.send_message(chat_id=CHAT_ID, text=caption_text, parse_mode='HTML')

async def send_prediction_message():
    thoi_gian_hien_tai = datetime.now().strftime('%H:%M:%S')
    du_doan = random.choice(["CÁI", "CON"])
    message_id_to_pin = None
    cau_CÁI_list = ["Nhận thấy tín hiệu <b>cầu bệt Nhà Cái (CÁI)</b>.","Phân tích cho thấy <b>cầu 1-1</b> đang nghiêng về <b>CÁI</b>.","Dữ liệu báo về <b>xu hướng đang đổ về Cái</b>.","Chuyên gia nhận định tay này <b>bẻ cầu sang CÁI</b>."]
    cau_CON_list = ["Nhận thấy tín hiệu <b>cầu bệt Nhà Con (CON)</b>.","Phân tích cho thấy <b>cầu 1-2</b> đang ủng hộ <b>CON</b>.","Dữ liệu báo về <b>xu hướng đang đổ về Con</b>.","Chuyên gia nhận định tay này <b>bẻ cầu sang CON</b>."]
    if du_doan == "CÁI":
        icon = "🔴🔴"
        ly_do = random.choice(cau_CÁI_list)
    else:
        icon = "🔵🔵"
        ly_do = random.choice(cau_CON_list)
    caption_text = f"""
💲💲💲💲 <b>LỆNH CHÍNH THỨC TỪ CHUYÊN GIA</b> 💲💲💲💲
━━━━━━━━━━━━━━━━━━
🕒 <i>Thời gian ra lệnh: {thoi_gian_hien_tai}</i>
🔍 <i>Phân tích: {ly_do}</i>

🎯🎯 <b>Lựa chọn theo cầu:</b>   <b>{icon} {du_doan} {icon}</b>🎯🎯

💵 <b>Vốn:</b>          <b>20% trên tổng vốn</b>
🏆 <b>Mục tiêu:</b>     <b>Tuân thủ kỷ luật</b>

<i>Chúc anh em bám chắc cầu và chiến thắng!</i>
    """
    try:
        with open(PREDICTION_VIDEO_PATH, 'rb') as video_file:
            sent_message = await bot.send_video(chat_id=CHAT_ID, video=video_file, caption=caption_text, parse_mode='HTML')
            message_id_to_pin = sent_message.message_id
            await bot.pin_chat_message(chat_id=CHAT_ID, message_id=message_id_to_pin, disable_notification=True)
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Đã gửi và GHIM video VÀO LỆNH (Soi cầu).")
        return message_id_to_pin
    except Exception as e:
        print(f"❌ Lỗi khi gửi video vào lệnh: {e}.")
        return None

async def send_end_of_session_message(message_id_to_unpin):
    thoi_gian_hien_tai = datetime.now().strftime('%H:%M:%S')
    thoi_gian_tiep_theo = (datetime.now() + timedelta(minutes=5)).strftime('%H:%M')
    captions = [f"""💲💲 <b>KẾT THÚC PHIÊN - BẢO TOÀN LỢI NHUẬN</b> 💲💲\n━━━━━━━━━━━━━━━━━━\n🕒 <i>Thời gian kết thúc: {thoi_gian_hien_tai}</i>\nToàn đội nghỉ ngơi và quản lý vốn chặt chẽ.\n<b>Kỷ luật tạo nên sự khác biệt.</b>\n\n⏰ Hẹn gặp lại tại phiên tiếp theo lúc <b>~ {thoi_gian_tiep_theo}</b>.""",f"""🔐 <b>PHIÊN GIAO DỊCH ĐÃ ĐÓNG</b> 🔐\n━━━━━━━━━━━━━━━━━━\n🕒 <i>Thời gian đóng phiên: {thoi_gian_hien_tai}</i>\nThắng không kiêu, bại không nản. Chuẩn bị cho cơ hội tiếp theo.\n<b>Luôn tuân thủ kế hoạch.</b>\n\n🕚🕚 Phiên kế tiếp sẽ bắt đầu vào khoảng <b>~ {thoi_gian_tiep_theo}</b>.""",]
    caption_text = random.choice(captions)
    try:
        if message_id_to_unpin:
            await bot.unpin_chat_message(chat_id=CHAT_ID, message_id=message_id_to_unpin)
            print(f"[{datetime.now().strftime('%H:%M:%S')}] Đã GỠ GHIM tin nhắn lệnh cũ.")
        with open(END_VIDEO_PATH, 'rb') as video_file:
            await bot.send_video(chat_id=CHAT_ID, video=video_file, caption=caption_text, parse_mode='HTML')
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Đã gửi video KẾT THÚC PHIÊN.")
    except Exception as e:
        print(f"❌ Lỗi khi gửi thông báo kết thúc: {e}.")


# --- CÁC HÀM VÀ TÁC VỤ KHÁC ---
# (Tất cả các hàm bên dưới giữ nguyên)
async def send_group_rules():
    message_text = f"""📜 <b>NỘI QUY & QUY ĐỊNH CỦA NHÓM</b> 📜\n━━━━━━━━━━━━━━━━━━\nĐể xây dựng một cộng đồng vững mạnh và hiệu quả, anh em vui lòng tuân thủ các quy tắc sau:\n\n✅ <b>TUÂN THỦ KỶ LUẬT:</b> Luôn đi đúng mức vốn được khuyến nghị. Không tự ý gấp thếp, không "tất tay".\n\n🚫 <b>KHÔNG SPAM/LOÃNG NHÓM:</b> Không gửi link lạ, quảng cáo, hoặc các nội dung không liên quan đến hoạt động của nhóm.\n\n💡 <b>GIỮ VỮNG TÂM LÝ:</b> Thắng không kiêu, bại không nản. Thị trường luôn có biến động, kỷ luật sẽ giúp chúng ta đi đường dài.\n\n🆘 <b>CẦN HỖ TRỢ?:</b> Nếu có bất kỳ thắc mắc hay vấn đề gì, hãy liên hệ trực tiếp với Boss qua link: <b>{BOSS_SUPPORT_LINK}</b>\n\n<i>Cảm ơn sự hợp tác của toàn thể anh em!</i>"""
    try:
        await bot.send_message(chat_id=CHAT_ID, text=message_text, parse_mode='HTML')
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Đã gửi tin nhắn định kỳ: [Nội quy nhóm].")
    except Exception as e:
        print(f"❌ Lỗi khi gửi tin nhắn nội quy: {e}")

async def session_job():
    prediction_message_id = None
    try:
        print("=========================================")
        print(f"Bắt đầu phiên làm việc lúc: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        await send_warning_message()
        await asyncio.sleep(30)
        prediction_message_id = await send_prediction_message()
        await asyncio.sleep(30)
        await send_end_of_session_message(prediction_message_id)
        print("💲💲 Hoàn thành phiên làm việc.💲")
        print("=========================================\n")
    except Exception as e:
        print(f"❌ Gặp lỗi nghiêm trọng trong phiên làm việc: {e}")
        if prediction_message_id:
            try: await bot.unpin_chat_message(chat_id=CHAT_ID, message_id=prediction_message_id)
            except: pass

async def periodic_message_job():
    await asyncio.sleep(10)
    while True:
        try:
            await send_group_rules()
            await asyncio.sleep(RULES_MESSAGE_INTERVAL)
        except Exception as e:
            print(f"❌ Gặp lỗi trong tác vụ gửi tin định kỳ: {e}")
            await asyncio.sleep(60)

async def post_off_hours_content():
    try:
        message_text = random.choice(off_hours_messages)
        await bot.send_message(chat_id=CHAT_ID, text=message_text, parse_mode='HTML')
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Đã gửi nội dung trong giờ nghỉ.")
    except Exception as e:
        print(f"❌ Lỗi khi gửi nội dung giờ nghỉ: {e}")

async def main_loop():
    while True:
        now = datetime.now()
        current_hour = now.hour
        if HOAT_DONG_BAT_DAU <= current_hour < HOAT_DONG_KET_THUC:
            print(f"[{now.strftime('%H:%M:%S')}] Trong khung giờ hoạt động. Chuẩn bị phiên mới.")
            await session_job()
            thoi_gian_cho = 5 * 60
            thoi_gian_bat_dau_tiep_theo = (now + timedelta(seconds=thoi_gian_cho)).strftime('%H:%M:%S')
            print(f"✨ Đã hoàn thành phiên. Phiên tiếp theo sẽ bắt đầu sau 5 phút (lúc ~ {thoi_gian_bat_dau_tiep_theo})")
            await asyncio.sleep(thoi_gian_cho)
        else:
            print(f"[{now.strftime('%H:%M:%S')}] Ngoài khung giờ hoạt động. Sẽ gửi nội dung chia sẻ.")
            await post_off_hours_content()
            sleep_duration = 90 * 60
            next_post_time = (now + timedelta(seconds=sleep_duration)).strftime('%H:%M:%S')
            print(f"Đã gửi tin giờ nghỉ. Tin tiếp theo sẽ được gửi sau 90 phút (lúc ~ {next_post_time}).")
            await asyncio.sleep(sleep_duration)

async def main():
    print("🚀 Bot đang khởi động và kiểm tra lịch trình...")
    await asyncio.gather(
        main_loop(),
        periodic_message_job()
    )

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n🛑 Bot đã dừng hoạt động theo yêu cầu.")
    except Exception as e:
        print(f"\n❌ Bot gặp lỗi nghiêm trọng và đã dừng: {e}")