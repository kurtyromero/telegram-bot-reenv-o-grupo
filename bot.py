import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

BOT_OWNER_ID = 8168679280  # tu ID NUMÉRICO AQUÍ
GROUPS = set()              # donde se guardarán los grupos

logging.basicConfig(level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Bot activo.")

async def register_group(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    if chat.type in ["group", "supergroup"]:
        GROUPS.add(chat.id)
        await update.message.reply_text("Registrado este grupo para recibir contenido.")
        print("Grupo añadido:", chat.id)

async def receive_from_owner(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.from_user.id != BOT_OWNER_ID:
        return

    for group_id in GROUPS:
        try:
            if update.message.photo:
                await context.bot.send_photo(group_id, update.message.photo[-1].file_id, caption=update.message.caption)
            elif update.message.video:
                await context.bot.send_video(group_id, update.message.video.file_id, caption=update.message.caption)
            elif update.message.text:
                await context.bot.send_message(group_id, update.message.text)
            elif update.message.document:
                await context.bot.send_document(group_id, update.message.document.file_id, caption=update.message.caption)
        except Exception as e:
            print("Error enviando a grupo:", e)

async def main():
    app = ApplicationBuilder().token("8549877239:AAGLYiSKeVMDP1S-ZSoh_S779NRT1QU3BvA").build()

    app.add_handler(MessageHandler(filters.COMMAND, register_group))
    app.add_handler(MessageHandler(filters.ALL, receive_from_owner))

    print("Bot iniciado...")
    await app.run_polling()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
