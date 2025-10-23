# /sieu_dinh_bot/modules/messages.py

import random
from datetime import datetime
import config

def get_vietnamese_day_of_week(date_obj):
    """Chuyển đổi ngày trong tuần sang Tiếng Việt."""
    weekdays = {
        'Monday': 'Thứ Hai', 'Tuesday': 'Thứ Ba', 'Wednesday': 'Thứ Tư',
        'Thursday': 'Thứ Năm', 'Friday': 'Thứ Sáu', 'Saturday': 'Thứ Bảy',
        'Sunday': 'Chủ Nhật'
    }
    return weekdays.get(date_obj.strftime('%A'), '')

# --- TIN NHẮN ĐẦU/CUỐI NGÀY ---
def get_good_morning_message():
    now = datetime.now(config.VN_TZ)
    ngay_tieng_viet = get_vietnamese_day_of_week(now)
    ngay_thang_nam = now.strftime('%d/%m/%Y')
    return f"""🌅 <b>𝗖𝗛𝗔̀𝗢 𝗡𝗚𝗔̀Y 𝗠𝗢̛́𝗜 𝗖𝗨̀𝗡𝗚 𝗧𝗘𝗔𝗠</b> 🌅
━━━━━━━━━━━━━━━━━━━━
📅 Hôm nay là: <b>{ngay_tieng_viet}, ngày {ngay_thang_nam}</b>

Chúc toàn bộ anh em trong nhóm 𝗕𝗖𝗥 𝟭 𝗟𝗘̣̂𝗡𝗛 một ngày mới tràn đầy năng lượng, giao dịch thuận lợi và gặt hái nhiều thắng lợi!

⏰ <i>Ca kéo đầu tiên sẽ bắt đầu lúc <b>07:00</b>. Anh em chuẩn bị sẵn sàng nhé!</i>"""

def get_good_night_message():
    return f"""🌙 <b>𝗞𝗘̂́𝗧 𝗧𝗛𝗨́𝗖 𝗡𝗚𝗔̀𝗬 𝗟𝗔̀𝗠 𝗩𝗜𝗘̣̂𝗖</b> 🌙
━━━━━━━━━━━━━━━━━━━━
Một ngày giao dịch đã khép lại. Cảm ơn tất cả anh em đã đồng hành, tuân thủ kỷ luật và cùng nhau chiến đấu.

Dù thắng hay thua, điều quan trọng nhất là chúng ta đã học hỏi và rút ra kinh nghiệm. Hãy nghỉ ngơi thật tốt để lấy lại năng lượng.

❤️ Chúc cả nhà ngủ ngon và hẹn gặp lại vào 7h sáng mai!"""

# --- TIN NHẮN NỘI QUY ---
def get_group_rules_message():
    return f"""📜   <b>𝗡𝗢̣̂𝗜 𝗤𝗨𝗬 𝗩𝗔̀𝗡𝗚 𝗖𝗨̉𝗔 𝗡𝗛𝗢́𝗠</b>   📜
━━━━━━━━━━━━━━━━━━━━
Để xây dựng một cộng đồng vững mạnh và hiệu quả, anh em vui lòng tuân thủ các quy tắc sau:

✅  <b>𝗧𝗨𝗔̂𝗡 𝗧𝗛𝗨̉ 𝗞𝗬̉ 𝗟𝗨𝗔̣̂𝗧:</b> Luôn đi đúng <b>𝟭𝟬% 𝗩𝗢̂́𝗡</b> theo khuyến nghị. Tuyệt đối không tự ý gấp thếp, không "tất tay".

🚫  <b>𝗞𝗛𝗢̂𝗡𝗚 𝗦𝗣𝗔𝗠/𝗟𝗢𝗔̃𝗡𝗚 𝗡𝗛𝗢́𝗠:</b> Không gửi link lạ, quảng cáo, hoặc các nội dung không liên quan đến hoạt động của nhóm.

💡  <b>𝗚𝗜𝗨̛̃ 𝗩𝗨̛̃𝗡𝗚 𝗧𝗔̂𝗠 𝗟𝗬́:</b> Thắng không kiêu, bại không nản. Thị trường luôn có biến động, kỷ luật sẽ giúp chúng ta đi đường dài.

🆘  <b>𝗖𝗔̂̀𝗡 𝗛𝗢̂̃ 𝗧𝗥𝗢̛̣?:</b> Nếu có bất kỳ thắc mắc hay vấn đề gì, hãy liên hệ trực tiếp với Boss qua: <b>{config.BOSS_SUPPORT_LINK}</b>

<i>Cảm ơn sự hợp tác của toàn thể anh em!</i>"""

# --- KHO LÝ DO SOI CẦU & TIP VÀNG ---
PREDICTION_REASONS = {
    "CÁI": [
        "Nhận thấy tín hiệu 𝗰𝗮̂̀𝘂 𝗯𝗲̣̂𝘁 𝗡𝗵𝗮̀ 𝗖𝗮́𝗶 (CÁI) đang hình thành.",
        "Phân tích cho thấy 𝗰𝗮̂̀𝘂 𝟭-𝟭 đang nghiêng về 𝗖𝗔́𝗜 ở tay này.",
        "𝗗𝘂̛̃ 𝗹𝗶𝗲̣̂𝘂 𝗹𝗼̛́𝗻 báo về xu hướng đang đổ mạnh về 𝗖𝗔́𝗜.",
        "𝗖𝗵𝘂𝘆𝗲̂𝗻 𝗴𝗶𝗮 nhận định tay này nên 𝗯𝗮́𝗺 𝘁𝗵𝗲𝗼 𝗖𝗔́𝗜."
    ],
    "CON": [
        "Tín hiệu cho thấy khả năng cao sẽ 𝗯𝗲̉ 𝗰𝗮̂̀𝘂 𝘀𝗮𝗻𝗴 𝗖𝗢𝗡.",
        "Phân tích 𝗰𝗮̂̀𝘂 𝟭-𝟮 đang ủng hộ mạnh mẽ cho 𝗖𝗢𝗡.",
        "Nhận thấy dấu hiệu 𝗰𝗮̂̀𝘂 đ𝗼̂𝗶 đang chạy về phía 𝗖𝗢𝗡.",
        "Thống kê cho thấy tỷ lệ ra 𝗖𝗢𝗡 ở phiên này đang cao hơn."
    ]
}

GOLDEN_TIPS = [
    "🧠   <b>𝗚𝗢́𝗖 𝗞𝗜𝗘̂́𝗡 𝗧𝗛𝗨̛́𝗖</b>   🧠\n━━━━━━━━━━━━━━━━━━━━\nTại sao không nên gấp thếp khi thua? Vì nó có thể dẫn đến việc mất trắng vốn chỉ trong vài tay. Hãy tuân thủ kỷ luật 10% để đi đường dài!",
    "💡   <b>𝗠𝗘̣𝗢 𝗧𝗔̂𝗠 𝗟𝗬́</b>   💡\n━━━━━━━━━━━━━━━━━━━━\nNếu bạn thua 2 ca liên tiếp, hãy tạm dừng, đi uống một cốc nước và thư giãn. Đừng để cảm xúc chi phối quyết định của bạn.",
    "📚   <b>𝗕𝗔̀𝗜 𝗛𝗢̣𝗖 𝗩𝗢̛̃ 𝗟𝗢̀𝗡𝗚</b>   📚\n━━━━━━━━━━━━━━━━━━━━\nCầu Bệt là gì? Là một chuỗi kết quả CÁI hoặc CON ra liên tiếp từ 4 tay trở lên. Gặp cầu bệt, chiến thuật tốt nhất là 'bám cầu' cho đến khi gãy.",
    "💰   <b>𝗤𝗨𝗔̉𝗡 𝗟𝗬́ 𝗩𝗢̂́𝗡</b>   💰\n━━━━━━━━━━━━━━━━━━━━\nLuôn đặt ra mục tiêu chốt lãi và cắt lỗ trước mỗi phiên. Ví dụ: Lãi 30% thì nghỉ, hoặc lỗ 20% thì dừng. Kỷ luật là chìa khóa thành công!"
]

def get_golden_tip():
    """Lấy một tip vàng ngẫu nhiên."""
    return random.choice(GOLDEN_TIPS)

# --- NỘI DUNG CÁC BƯỚC TRONG CA KÉO ---
def get_start_session_caption(session_time: datetime):
    time_str = session_time.strftime('%H:%M - %d/%m')
    return f"""🔥🔥  <b>𝗖𝗔 𝗞𝗘́𝗢:  {time_str}</b>  🔥🔥
━━━━━━━━━━━━━━━━━━━━
🔥🔥ANH EM TẬP TRUNG, CHUẨN BỊ VÀO CA.🔥🔥
🔥BOSS🔥 đang vào sảnh, sẽ báo bàn ngay sau đây..."""

def get_table_announcement_caption(table_number: int):
    return f"""💎 💎  <b>𝗦𝗔̉𝗡𝗛 𝗖𝗛𝗢̛𝗜: 𝗦𝗘𝗫𝗬 𝗕𝗔𝗖𝗖𝗔𝗥𝗔𝗧</b> 💎  💎
━━━━━━━━━━━━━━━━━━━━
🃏  <b>𝗕𝗔̀𝗡 Đ𝗔̃ 𝗖𝗛𝗢̣𝗡:  BACCATAT {table_number}</b>

<i>Anh em tập trung vào bàn này.
𝗟𝗲̣̂𝗻𝗵 𝗰𝗵𝘂𝘆𝗲̂𝗻 𝗴𝗶𝗮 sẽ được đưa ra sau 20 giây!</i>"""

# <<< SỬA LỖI TẠI ĐÂY >>>
def get_prediction_caption():
    now = datetime.now(config.VN_TZ)
    du_doan = random.choice(["CÁI", "CON"])
    icon = "🔴" if du_doan == "CÁI" else "🔵"
    ly_do = random.choice(PREDICTION_REASONS[du_doan])
    
    return f"""⚡️⚡️ <b>LỆNH TỪ CHUYÊN GIA</b> ⚡️⚡️
━━━━━━━━━━━━━━━━━━
<i>"{ly_do}"</i>

👉 <b>LỰA CHỌN CUỐI CÙNG:</b>

<b>{icon} {du_doan.upper()} {icon}</b>

━━━━━━━━━━━━━━━━━━
💰 <b>Vào vốn:</b> <b><code>10% TỔNG VỐN</code></b>
🎯 <b>Nguyên tắc:</b> Giữ vững kỷ luật!
<i>(Lệnh ra lúc: {now.strftime('%H:%M:%S')})</i>"""
# <<< KẾT THÚC SỬA LỖI >>>

def get_prediction_text_fallback():
    """Tạo tin nhắn dự đoán dạng văn bản khi gửi video thất bại."""
    now = datetime.now(config.VN_TZ)
    du_doan = random.choice(["CÁI", "CON"])
    icon = "🔴" if du_doan == "CÁI" else "🔵"
    ly_do = random.choice(PREDICTION_REASONS[du_doan])
    
    return f"""⚠️ <b>THÔNG BÁO DỰ PHÒNG (LỖI VIDEO)</b> ⚠️
⚡️⚡️ <b>LỆNH TỪ CHUYÊN GIA</b> ⚡️⚡️
━━━━━━━━━━━━━━━━━━
<i>Phân tích: "{ly_do}"</i>

👉 <b>LỰA CHỌN CUỐI CÙNG:</b>

<b>{icon} {du_doan.upper()} {icon}</b>

━━━━━━━━━━━━━━━━━━
💰 <b>Vào vốn:</b> <b><code>10% TỔNG VỐN</code></b>
🎯 <b>Nguyên tắc:</b> Giữ vững kỷ luật!
<i>(Lệnh ra lúc: {now.strftime('%H:%M:%S')})</i>"""

def get_end_session_caption(session_time: datetime, next_session_time: datetime):
    time_str = session_time.strftime('%H:%M - %d/%m')
    next_time_str = next_session_time.strftime('%H:%M')
    return f"""🏁   <b>𝗞𝗘̂́𝗧 𝗧𝗛𝗨́𝗖 𝗖𝗔 𝗞𝗘́𝗢: {time_str}</b>   🏁
━━━━━━━━━━━━━━━━━━━━
Toàn bộ anh em nghỉ ngơi, bảo toàn lợi nhuận và chuẩn bị cho cơ hội tiếp theo.
<b>Kỷ luật là sức mạnh!</b>

⏰  Hẹn gặp lại anh em tại ca kế tiếp lúc <b>~ {next_time_str}</b>."""

def get_animated_rules_caption():
    """Lấy nội dung caption cho tin nhắn Nội Quy Vàng dạng GIF."""
    return f"""📜   <b>𝗡𝗢̣̂𝗜 𝗤𝗨𝗬 𝗩𝗔̀𝗡𝗚 — ANH EM CẦN ĐỌC</b>   📜
━━━━━━━━━━━━━━━━━━━━━━
<i>Để đảm bảo một sân chơi công bằng và hiệu quả, hãy cùng nhau tuân thủ những nguyên tắc cốt lõi sau:</i>

1️⃣  <b>KỶ LUẬT VỐN:</b> Luôn vào lệnh đúng <b><code>10% TỔNG VỐN</code></b>. Đây là nguyên tắc sống còn để đi đường dài. Tuyệt đối không gấp thếp, không đánh theo cảm tính.

2️⃣  <b>TẬP TRUNG TÍN HIỆU:</b> Chỉ theo lệnh từ chuyên gia. Không chat riêng, không gửi link quảng cáo hay các nội dung làm loãng nhóm trong giờ kéo.

3️⃣  <b>TÂM LÝ VỮNG VÀNG:</b> Thắng bại là chuyện thường tình. Quan trọng là giữ được cái đầu lạnh, không cay cú. Thua 2 ca liên tiếp nên tạm nghỉ.

➡️  Mọi thắc mắc cần hỗ trợ, liên hệ ngay cho <b>{config.BOSS_SUPPORT_LINK}</b> để được giải đáp!

<b>Cảm ơn sự hợp tác của tất cả anh em!</b>"""