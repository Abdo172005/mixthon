import os
import asyncio
import re
from telethon import TelegramClient, events
from telethon.tl.functions.channels import JoinChannelRequest  # استيراد الدالة للانضمام إلى القناة
import yt_dlp as youtube_dl
from colored import fg
import pyfiglet

# إعداد اللون الأخضر للنصوص
green = fg('green')

# طلب معلومات التوثيق من المستخدم
API_ID = input(green + "Enter your API ID: ")
API_HASH = input(green + "Enter your API Hash: ")
PHONE = input(green + "Enter your phone number (with country code): ")
MY_USER_ID = int(input(green + "Enter your User ID: "))

client = TelegramClient('session_name', API_ID, API_HASH)

# متغيرات النشر
publishing = False
message_text = ''
interval_seconds = 0.0
publish_task = None
target_chat_id = None

# دالة "التهكير" المزيفة
async def fake_hacking(event):
    # العثور على الرسالة التي تحتوي على كلمة "تهكير"
    message = event.message

    # تعديل الرسالة الأولية
    await message.edit("💻 جاري التهكير...")

    # التقدم في عملية "التهكير" الوهمية
    progress_steps = [
        "10% ■", "20% ■■", "30% ■■■", "40% ■■■■", "50% ■■■■■",
        "60% ■■■■■■", "70% ■■■■■■■", "80% ■■■■■■■■", "90% ■■■■■■■■■",
        "100% ■■■■■■■■■■"
    ]

    for i, step in enumerate(progress_steps):
        if i < 5:  # من 10% إلى 50%
            await asyncio.sleep(0.5)  # الانتظار لمدة ثانية قبل تعديل الرسالة
        else:  # من 50% إلى 100%
            await asyncio.sleep(0.2)  # الانتظار لمدة نصف ثانية قبل تعديل الرسالة
        await message.edit(f"💻 جاري التهكير... {step}")

    # بعد الوصول إلى 100%، تعديل الرسالة النهائية
    await asyncio.sleep(0.3)
    await message.edit("🎉 تم اختراقك بنجاح! طبعاً مجرد مزحة 😂")

@client.on(events.NewMessage)
async def handler(event):
    global publishing, message_text, interval_seconds, publish_task, target_chat_id

    if event.sender_id == MY_USER_ID:
        # كشف معلومات المستخدم
        if event.message.text.startswith('كشف'):
            command_parts = event.message.text.split()
            if len(command_parts) == 2:
                identifier = command_parts[1]
                try:
                    if identifier.isdigit():
                        user_info = await client.get_entity(int(identifier))
                    else:
                        user_info = await client.get_entity(identifier)

                    first_name = user_info.first_name or 'غير موجود'
                    last_name = user_info.last_name or ''
                    username = user_info.username or 'غير موجود'
                    user_id = user_info.id

                    user_info_message = (
                        f"الاسم: {first_name} {last_name}\n"
                        f"يوزره: @{username}\n"
                        f"الايدي: {user_id}"
                    )
                    await event.reply(user_info_message)
                except Exception as e:
                    await event.reply(f"حدث خطأ: {str(e)}")
            elif event.message.reply_to_msg_id:
                replied_message = await event.get_reply_message()
                user_id = replied_message.sender_id
                try:
                    user_info = await client.get_entity(user_id)
                    first_name = user_info.first_name or 'غير موجود'
                    last_name = user_info.last_name or ''
                    username = user_info.username or 'غير موجود'
                    user_id = user_info.id

                    user_info_message = (
                        f"الاسم: {first_name} {last_name}\n"
                        f"يوزره: @{username}\n"
                        f"الايدي: {user_id}"
                    )
                    await event.reply(user_info_message)
                except Exception as e:
                    await event.reply(f"حدث خطأ: {str(e)}")
            else:
                await event.reply("يرجى الرد على رسالة مستخدم أو إدخال معرف المستخدم للحصول على المعلومات.")

        # التهكير المزيف
        elif 'تهكير' in event.text:
            await fake_hacking(event)

        # تحميل الفيديو عند الأمر 'تحميل'
        elif event.text.startswith('تحميل'):
            url = event.text[len('تحميل'):].strip()
            chat_id = event.chat_id
            await event.reply("جاري تحميل الفيديو...")

            try:
                ydl_opts = {
                    'outtmpl': 'downloaded_video.%(ext)s',
                    'format': 'best',
                }

                with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                    info_dict = ydl.extract_info(url, download=True)
                    video_file = ydl.prepare_filename(info_dict)

                await client.send_file(chat_id, video_file, caption="تم تحميل الفيديو بنجاح!")
                os.remove(video_file)  # إزالة الملف بعد الإرسال

            except Exception as e:
                await event.reply(f"حدث خطأ أثناء تحميل الفيديو: {str(e)}")

        # نشر تلقائي عند الأمر 'نشر'
        elif event.is_private or event.chat_id:
            text = event.text.strip()

            match = re.match(r'نشر\s+(.*)\s+(\d+(\.\d+)?)', text)
            if match:
                try:
                    message_text = match.group(1)
                    seconds = float(match.group(2))
                    if seconds < 0.001:
                        await event.reply('أقل فترة زمنية للنشر هي 0.001 ثانية.')
                        return

                    interval_seconds = seconds
                    publishing = True
                    target_chat_id = event.chat_id
                    await event.reply(f'بدء نشر الرسالة "{message_text}" كل {interval_seconds} ثانية.')

                    # إيقاف النشر السابق إذا كان قيد التشغيل
                    if publish_task and not publish_task.done():
                        publish_task.cancel()

                    # نشر الرسائل بشكل متكرر
                    async def publish_messages():
                        while publishing:
                            try:
                                await client.send_message(target_chat_id, message_text)
                            except Exception as e:
                                await event.reply(f'فشل في إرسال الرسالة: {e}')
                            await asyncio.sleep(interval_seconds)

                    publish_task = asyncio.create_task(publish_messages())

                except ValueError:
                    await event.reply('يجب أن يكون عدد الثواني عددًا صحيحًا أو عشريًا.')

            elif text == 'ايقاف':
                if publishing:
                    publishing = False
                    if publish_task and not publish_task.done():
                        publish_task.cancel()
                    await event.reply('تم إيقاف النشر التلقائي بنجاح.')
                else:
                    await event.reply('النشر التلقائي غير مفعل.')

async def main():
    await client.start(phone=PHONE)

    # الانضمام إلى القناة تلقائيًا بعد تسجيل الدخول
    try:
        await client(JoinChannelRequest('uummh'))
        print(green + "تم الانضمام إلى القناة @uummh بنجاح.")
    except Exception as e:
        print(f"حدث خطأ أثناء محاولة الانضمام إلى القناة: {str(e)}")

    # عرض كلمة "mixthon" بخط كبير وباللون الأخضر
    result = pyfiglet.figlet_format("mixthon", font="slant")  # تعديل الخط
    print(green + result)

    await client.run_until_disconnected()

if __name__ == '__main__':
    client.loop.run_until_complete(main())