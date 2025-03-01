import logging
import json
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
import time

# إعداد التسجيل
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# تحميل قاعدة البيانات
with open("suras.json", "r", encoding="utf-8") as file:
    SURAS = json.load(file)

# عدد السور في كل صفحة
SURAS_PER_PAGE = 10

# ملف تخزين المستخدمين
USERS_FILE = "users.json"

# تحميل أو تهيئة قائمة المستخدمين
def load_users():
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    else:
        return []

# حفظ قائمة المستخدمين
def save_users(users):
    with open(USERS_FILE, "w", encoding="utf-8") as file:
        json.dump(users, file, ensure_ascii=False, indent=4)

# دالة لإنشاء لوحة المفاتيح
def create_keyboard(page: int):
    start_index = page * SURAS_PER_PAGE
    end_index = start_index + SURAS_PER_PAGE
    suras_page = SURAS[start_index:end_index]

    keyboard = [
        [InlineKeyboardButton(sura["name"], callback_data=f"sura_{sura['file_id']}")] for sura in suras_page
    ]

    navigation_buttons = []
    if page > 0:
        navigation_buttons.append(InlineKeyboardButton("السابق", callback_data=f"page_{page - 1}"))
    if end_index < len(SURAS):
        navigation_buttons.append(InlineKeyboardButton("التالي", callback_data=f"page_{page + 1}"))

    if navigation_buttons:
        keyboard.append(navigation_buttons)

    return InlineKeyboardMarkup(keyboard)

# دالة لبدء البوت
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # تحميل المستخدمين الحاليين
    users = load_users()
    user_id = update.message.from_user.id
    
    # إضافة المستخدم إذا لم يكن موجودًا
    if user_id not in users:
        users.append(user_id)
        save_users(users)  # حفظ التحديث في الملف

    await update.message.reply_text(
        "السلام عليكم ورحمة الله وبركاته\n"
        "أهلأ وسهلأ بك اخي المسلم في بوت القران الكريم\n"
        "لتنزيل الايات القرانيةالمباركة وبصوت القارئ الشيخ مشاري العفاسي\n"
        " يمكنك اختيار سورة من القرآن.\n"
        "استخدم الأزرار أدناه لاختيار السورة أو التنقل بين الصفحات.",
        reply_markup=create_keyboard(page=0)
    )

# دالة للتعامل مع اختيار السورة
async def choose_sura(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()  # تأكيد استلام الاستجابة
    
    logging.info(f"Received callback data: {query.data}")  # تسجيل البيانات المرسلة
    
    if query.data.startswith("sura_"):
        # الحصول على معرف الملف الصوتي
        file_id = query.data.split("_")[1]
        
        # البحث عن السورة في قاعدة البيانات
        sura = next((s for s in SURAS if s["file_id"] == file_id), None)
        
        if sura:
            # إرسال الملف الصوتي
            await context.bot.send_audio(
                chat_id=query.message.chat_id,
                audio=sura["audio_url"]
            )
        else:
            await query.edit_message_text("عذرًا، الملف الصوتي غير متاح.")
    elif query.data.startswith("page_"):
        # تغيير الصفحة
        page = int(query.data.split("_")[1])
        await query.edit_message_text(
            "اختر سورة من القرآن:",
            reply_markup=create_keyboard(page)
        )

# دالة لعرض عدد المستخدمين
async def user_count(update: Update, context: ContextTypes.DEFAULT_TYPE):
    users = load_users()
    user_count = len(users)
    await update.message.reply_text(f"عدد المستخدمين الذين تفاعلوا مع البوت: {user_count}")

# إعداد البوت
def main():
    BOT_TOKEN = os.getenv("BOT_TOKEN")  # قراءة التوكن من متغيرات البيئة
    application = Application.builder().token(BOT_TOKEN).build()
    
    # إضافة الأوامر
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("usercount", user_count))  # أمر لعرض عدد المستخدمين
    application.add_handler(CallbackQueryHandler(choose_sura))
    
    # بدء البوت
    application.run_polling()
    while True:
        time.sleep(1)

if __name__ == "__main__":
    main()
