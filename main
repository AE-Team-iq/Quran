import logging
import json
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# إعداد التسجيل
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# تحميل قاعدة البيانات
with open("suras.json", "r", encoding="utf-8") as file:
    SURAS = json.load(file)

# عدد السور في كل صفحة
SURAS_PER_PAGE = 10


# دالة لعرض السور في صفحة معينة
def format_suras_page(page: int):
    start_index = page * SURAS_PER_PAGE
    end_index = start_index + SURAS_PER_PAGE
    suras_page = SURAS[start_index:end_index]

    formatted_text = "اختر سورة من القرآن:\n"
    for i, sura in enumerate(suras_page, start=1):
        formatted_text += f"{i}. {sura['name']} (استخدم /sura {sura['file_id']})\n"

    return formatted_text


# دالة لبدء البوت
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["page"] = 0  # تخزين رقم الصفحة الحالية
    await update.message.reply_text(
        "السلام عليكم ورحمة الله وبركاته\n"
        "أهلأ وسهلأ بك اخي المسلم في بوت القران الكريم\n"
        "لتنزيل الايات القرانيةالمباركة وبصوت القارئ الشيخ مشاري العفاسي\n"
        " يمكنك اختيار سورة من القرآن.\n"
        "استخدم الأوامر أدناه لاختيار السورة أو التنقل بين الصفحات.\n"
        f"{format_suras_page(0)}\n"
        "استخدم /next للصفحة التالية أو /prev للصفحة السابقة."
    )


# دالة للتنقل إلى الصفحة التالية
async def next_page(update: Update, context: ContextTypes.DEFAULT_TYPE):
    page = context.user_data.get("page", 0)
    if (page + 1) * SURAS_PER_PAGE < len(SURAS):
        context.user_data["page"] = page + 1
        await update.message.reply_text(
            f"{format_suras_page(page + 1)}\n"
            "استخدم /next للصفحة التالية أو /prev للصفحة السابقة."
        )
    else:
        await update.message.reply_text("لا توجد صفحات أخرى.")


# دالة للتنقل إلى الصفحة السابقة
async def prev_page(update: Update, context: ContextTypes.DEFAULT_TYPE):
    page = context.user_data.get("page", 0)
    if page > 0:
        context.user_data["page"] = page - 1
        await update.message.reply_text(
            f"{format_suras_page(page - 1)}\n"
            "استخدم /next للصفحة التالية أو /prev للصفحة السابقة."
        )
    else:
        await update.message.reply_text("أنت في الصفحة الأولى.")


# دالة لإرسال الملف الصوتي
async def send_sura(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        # الحصول على رقم السورة من الأمر
        sura_number = context.args[0]

        # البحث عن السورة في قاعدة البيانات
        sura = next((s for s in SURAS if s["file_id"] == sura_number), None)

        if sura:
            # إرسال الملف الصوتي
            await context.bot.send_audio(
                chat_id=update.message.chat_id,
                audio=sura["audio_url"]
            )
        else:
            await update.message.reply_text("عذرًا، السورة غير موجودة.")
    except (IndexError, ValueError):
        await update.message.reply_text("استخدم الأمر بشكل صحيح: /sura_<رقم السورة>")


# إعداد البوت
def main():
    application = Application.builder().token("7606398917:AAGf3-bpQ572hyNr0zOaemmWS51-hxV9W98").build()

    # إضافة الأوامر
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("next", next_page))
    application.add_handler(CommandHandler("prev", prev_page))
    application.add_handler(CommandHandler("sura", send_sura))

    # بدء البوت
    application.run_polling()


if __name__ == "__main__":
    main()
