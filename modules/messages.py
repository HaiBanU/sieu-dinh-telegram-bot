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
    return f"""🌅 <b>𝓒𝓗𝓐̀𝓞 𝓝𝓖𝓐̀𝓨 𝓜𝓞̛́𝓘 𝓒𝓤̀𝓝𝓖 𝓣𝓔𝓐𝓜</b> 🌅
━━━━━━━━━━━━━━━━━━━━
📅 Hôm nay là: <b>{ngay_tieng_viet}, ngày {ngay_thang_nam}</b>

Chúc toàn bộ anh em trong nhóm 𝓑𝓒𝓡 𝟏 𝓛𝓔̣̂𝓝𝓗 một ngày mới tràn đầy năng lượng, giao dịch thuận lợi và gặt hái nhiều thắng lợi!

⏰ <i>𝓒𝓐 𝓚𝓔́𝓞 đầu tiên (CA 1) sẽ bắt đầu lúc <b>07:00</b>. Anh em chuẩn bị sẵn sàng nhé!</i>"""

def get_good_night_message():
    return f"""🌙 <b>KẾT THÚC NGÀY LÀM VIỆC</b> 🌙
━━━━━━━━━━━━━━━━━━━━
𝓒𝓐 𝓚𝓔́𝓞 cuối cùng trong ngày đã hoàn tất. Cảm ơn tất cả anh em đã đồng hành và chiến đấu hết mình.

Hãy nghỉ ngơi thật tốt để nạp lại năng lượng. Chúc cả nhà ngủ ngon, chuẩn bị cho một ngày mai giao dịch thành công và rực rỡ hơn!

❤️ Hẹn gặp lại anh em vào 7h sáng mai tại ca đầu tiên!"""

# --- TIN NHẮN NỘI QUY ---
def get_group_rules_message():
    return f"""📜   <b>𝓝𝓞̣̂𝓘 𝓠𝓤𝓨 𝓥𝓐̀𝓝𝓖 𝓒𝓤̉𝓐 𝓝𝓗𝓞́𝓜</b>   📜
━━━━━━━━━━━━━━━━━━━━
Để xây dựng một cộng đồng vững mạnh và hiệu quả, anh em vui lòng tuân thủ các quy tắc sau:

✅  <b>𝗧𝗨𝗔̂𝗡 𝗧𝗛𝗨̉ 𝗞𝗬̉ 𝗟𝗨𝗔̣̂𝗧:</b> Luôn đi đúng <b>𝟭𝟬% 𝗩𝗢̂́𝗡</b> theo khuyến nghị. Tuyệt đối không tự ý gấp thếp, không "tất tay".

🚫  <b>𝗞𝗛𝗢̂𝗡𝗚 𝗦𝗣𝗔𝗠/𝗟𝗢𝗔̃𝗡𝗚 𝗡𝗛𝗢́𝗠:</b> Không gửi link lạ, quảng cáo, hoặc các nội dung không liên quan đến hoạt động của nhóm.

💡  <b>𝗚𝗜𝗨̛̃ 𝗩𝗨̛̃𝗡𝗚 𝗧𝗔̂𝗠 𝗟𝗬́:</b> Thắng không kiêu, bại không nản. Thị trường luôn có biến động, kỷ luật sẽ giúp chúng ta đi đường dài.

🆘  <b>𝗖𝗔̂̀𝗡 𝗛𝗢̂̃ 𝗧𝗥𝗢̛̣?:</b> Nếu có bất kỳ thắc mắc hay vấn đề gì, hãy liên hệ trực tiếp với 𝓑𝓞𝓢𝓢 qua: <b>{config.𝓑𝓞𝓢𝓢_SUPPORT_LINK}</b>

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

# --- NỘI DUNG CÁC BƯỚC TRONG 𝓒𝓐 𝓚𝓔́𝓞 ---

# <<< THAY ĐỔI LỚN TẠI ĐÂY: Thêm `session_number` và logic cho ca 1, ca 100 >>>
def get_start_session_caption(session_time: datetime, session_number: int):
    time_str = session_time.strftime('%H:%M - %d/%m')
    
    # Tin nhắn cho CA 1
    if session_number == 1:
        return f"""🔥🔥  <b>𝓒𝓐 𝓚𝓔́𝓞 {session_number}: {time_str}</b> 
━━━━━━━━━━━━━━━━
🚀 <b>Bắt đầu ngày mới!</b> Chúc toàn thể anh em một ngày giao dịch đại thắng, gặt hái nhiều thành công!

💰💰💰ANH EM TẬP TRUNG, CHUẨN BỊ VÀO CA.💰💰💰
💎💎𝓑𝓞𝓢𝓢💎💎 đang vào sảnh, sẽ báo bàn ngay sau đây..."""

    # Tin nhắn cho CA 100 (ca cuối)
    elif session_number == 100:
        return f"""🔥🔥  <b>𝓒𝓐 𝓚𝓔́𝓞 {session_number} (CA CUỐI): {time_str}</b> 
━━━━━━━━━━━━━━━━
Đây là ca cuối cùng trong ngày, mọi người vào lệnh xong chốt lãi ngủ một giấc thật ngon nhé.
Ngày mai chúng ta lại bắt đầu vào lúc 7h sáng!

💰💰💰VÀO VIỆC NỐT CA CUỐI NÀO.
💎💎𝓑𝓞𝓢𝓢💎💎 đang vào sảnh, sẽ báo bàn ngay sau đây..."""

    # Tin nhắn cho các ca còn lại
    else:
        return f"""🔥🔥  <b>𝓒𝓐 𝓚𝓔́𝓞 {session_number}: {time_str}</b>  
━━━━━━━━━━━━━━━━
💰💰💰𝓐𝓝𝓗 𝓔𝓜 𝓣𝓐̣̂𝓟 𝓣𝓡𝓤𝓝𝓖, 𝓒𝓗𝓤𝓐̂̉𝓝 𝓑𝓘̣ 𝓥𝓐̀𝓞 𝓒𝓐.
💎💎𝓑𝓞𝓢𝓢💎💎 đang vào sảnh, sẽ báo bàn ngay sau đây..."""


def get_table_announcement_caption(table_number: int):
    return f"""💎 💎  <b>𝗦𝗔̉𝗡𝗛 𝗖𝗛𝗢̛𝗜: 𝗦𝗘𝗫𝗬 𝘽𝘼𝘾𝘾𝘼𝙍𝘼𝙏</b> 
━━━━━━━━━━━━━━━━
🃏  <b>𝗕𝗔̀𝗡 Đ𝗔̃ 𝗖𝗛𝗢̣𝗡:  𝘽𝘼𝘾𝘾𝘼𝙍𝘼𝙏 {table_number}</b>

<i>Anh em tập trung vào bàn này.
𝗟𝗲̣̂𝗻𝗵 𝗰𝗵𝘂𝘆𝗲̂𝗻 𝗴𝗶𝗮 sẽ được đưa ra sau 20 giây!</i>"""

def get_prediction_caption():
    now = datetime.now(config.VN_TZ)
    du_doan = random.choice(["CÁI", "CON"])
    icon = "🔴" if du_doan == "CÁI" else "🔵"
    ly_do = random.choice(PREDICTION_REASONS[du_doan])
    
    return f"""⚡️⚡️ <b>LỆNH TỪ CHUYÊN GIA</b> 
━━━━━━━━━━━━━━
<i>"{ly_do}"</i>

👉 <b>𝙇𝙐̛̣𝘼 𝘾𝙃𝙊̣𝙉 𝘾𝙐𝙊̂́𝙄 𝘾𝙐̀𝙉𝙂:</b>

<b>{icon} {du_doan.upper()} {icon}</b>

━━━━━━━━━━━━━━
💰 <b>Vào vốn:</b> <b><code>𝟏𝟎% 𝓣𝓞̂̉𝓝𝓖 𝓥𝓞̂́𝓝</code></b>
🎯 <b>Nguyên tắc:</b> Giữ vững kỷ luật!
<i>(Lệnh ra lúc: {now.strftime('%H:%M:%S')})</i>"""

def get_prediction_text_fallback():
    """Tạo tin nhắn dự đoán dạng văn bản khi gửi video thất bại."""
    now = datetime.now(config.VN_TZ)
    du_doan = random.choice(["CÁI", "CON"])
    icon = "🔴" if du_doan == "CÁI" else "🔵"
    ly_do = random.choice(PREDICTION_REASONS[du_doan])
    
    return f"""⚠️ <b>THÔNG BÁO DỰ PHÒNG (LỖI VIDEO)</b> ⚠️
⚡️⚡️ <b>LỆNH TỪ CHUYÊN GIA</b> ⚡️⚡️
━━━━━━━━━━━━━━
<i>Phân tích: "{ly_do}"</i>

👉 <b>LỰA CHỌN CUỐI CÙNG:</b>

<b>{icon} {du_doan.upper()} {icon}</b>

━━━━━━━━━━━━━━
💰 <b>Vào vốn:</b> <b><code>10% TỔNG VỐN</code></b>
🎯 <b>Nguyên tắc:</b> Giữ vững kỷ luật!
<i>(Lệnh ra lúc: {now.strftime('%H:%M:%S')})</i>"""

def get_end_session_caption(session_time: datetime, next_session_time: datetime):
    time_str = session_time.strftime('%H:%M - %d/%m')
    next_time_str = next_session_time.strftime('%H:%M')
    return f"""🏁   <b>𝓚𝓔̂́𝓣 𝓣𝓗𝓤́𝓒 𝓒𝓐 𝓚𝓔́𝓞: {time_str}</b>   🏁
━━━━━━━━━━━━━━━
Toàn bộ anh em nghỉ ngơi, bảo toàn lợi nhuận và chuẩn bị cho cơ hội tiếp theo.
<b>Kỷ luật là sức mạnh!</b>

⏰  Hẹn gặp lại anh em tại ca kế tiếp lúc <b>~ {next_time_str}</b>."""

def get_animated_rules_caption():
    """Lấy nội dung caption cho video Nội Quy Vàng."""
    return f"""📜<b>𝓝𝓞̣̂𝓘 𝓠𝓤𝓨 𝓥𝓐̀𝓝𝓖 — 𝓐𝓝𝓗 𝓔𝓜 𝓒𝓐̂̀𝓝 𝓧𝓔𝓜 𝓚𝓨̃</b>📜
━━━━━━━━━━━━━━━
<i>Để đảm bảo một sân chơi công bằng và hiệu quả, anh em vui lòng xem kỹ video và tuân thủ các nguyên tắc của nhóm.</i>

🆘 Mọi thắc mắc cần hỗ trợ, liên hệ ngay cho <b>{config.𝓑𝓞𝓢𝓢_SUPPORT_LINK}</b> để được giải đáp!"""