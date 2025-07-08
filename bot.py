from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO

BOT_TOKEN = "توکن_خودت_رو_نذار_اینجا"

LOGO_TEXT = "textaminophen__"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("سلام! دلنوشته‌تو بفرست تا برات تصویر بسازم.")

def create_image(text: str) -> BytesIO:
    width, height = 1080, 1080
    img = Image.new('RGB', (width, height), color=(0, 0, 0))
    draw = ImageDraw.Draw(img)

    try:
        font = ImageFont.truetype("arial.ttf", 60)
        font_logo = ImageFont.truetype("arial.ttf", 36)
    except:
        font = ImageFont.load_default()
        font_logo = ImageFont.load_default()

    # دلنوشته رو وسط تصویر بنویس
    lines = text.split('\n')
    y = height // 3
    for line in lines:
        w = draw.textlength(line, font=font)
        draw.text(((width - w)/2, y), line, font=font, fill=(255, 255, 255))
        y += 70

    # لوگو پایین
    w_logo = draw.textlength(LOGO_TEXT, font=font_logo)
    draw.text((width - w_logo - 40, height - 70), LOGO_TEXT, font=font_logo, fill=(180, 180, 180))

    output = BytesIO()
    output.name = 'delneveshte.png'
    img.save(output, 'PNG')
    output.seek(0)
    return output

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    img = create_image(update.message.text)
    await update.message.reply_photo(photo=img)

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_text))
    app.run_polling()

if __name__ == '__main__':
    main()
