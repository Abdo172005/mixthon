from telethon.sync import TelegramClient, events
from telethon.tl.functions.account import UpdateProfileRequest
from telethon.errors.rpcerrorlist import MessageNotModifiedError, FloodWaitError
from telethon.tl.types import ChannelParticipantCreator, ChannelParticipantAdmin
from telethon.tl.functions.channels import GetParticipantsRequest
from telethon.tl.functions.channels import InviteToChannelRequest
from telethon.tl.types import InputChannel
from telethon.tl.types import ChannelParticipantsSearch
from datetime import datetime
from telethon.tl.types import Channel, Chat
from telethon.tl.functions.messages import DeleteMessagesRequest
import datetime
import pytz
import asyncio
import os
import pickle
import re
import io
import aiohttp
import random
import shutil
import time

# طلب إدخال api_id و api_hash و رقم الهاتف من المستخدم
api_id = '26184950'
api_hash = '240d7a8db018e9fceffebfe94a26f440'
phone_number = input("أدخل رقم الهاتف: ")

session_name = 'aa_update_session'
response_file = 'responses.pkl'
published_messages_file = 'published_messages.pkl'
muted_users_file = 'muted_users.pkl'
time_update_status_file = 'time_update_status.pkl'
channel_link_file = 'channel_link.pkl'
active_publishing_tasks = {}
image_folder = "image"
if not os.path.exists(image_folder):
    os.makedirs(image_folder)

client = TelegramClient(session_name, api_id, api_hash)
client.start(phone_number)

# قراءة الردود من الملف إذا كان موجودًا، وإلا استخدام قاموس فارغ
if os.path.exists(response_file):
    with open(response_file, 'rb') as f:
        responses = pickle.load(f)
else:
    responses = {}

# Load or initialize the channel link
if os.path.exists(channel_link_file):
    with open(channel_link_file, 'rb') as f:
        channel_link = pickle.load(f)
else:
    channel_link = None

# Load or initialize the time update status
if os.path.exists(time_update_status_file):
    with open(time_update_status_file, 'rb') as f:
        time_update_status = pickle.load(f)
else:
    time_update_status = {'enabled': False}

# Load or initialize the muted_users dictionary
if os.path.exists(muted_users_file):
    with open(muted_users_file, 'rb') as f:
        muted_users = pickle.load(f)
else:
    muted_users = {}

# Load responses and published messages from file or create new files if not exists

if os.path.exists(response_file):
    with open(response_file, 'rb') as f:
        responses = pickle.load(f)
else:
    responses = {}

if os.path.exists(published_messages_file):
    with open(published_messages_file, 'rb') as f:
        published_messages = pickle.load(f)
else:
    published_messages = []

# Define the active timers and countdown messages dictionaries
active_timers = {}
countdown_messages = {}

# اسم الصورة المحلية
image_path = 'local_image.jpg'

# Global variable to store the account name
account_name = None

def insert_emojis(message, emojis):
    random.shuffle(emojis)
    message_list = list(message)
    emoji_positions = []
    
    for emoji in emojis:
        pos = random.choice(range(len(message_list)))
        while pos in emoji_positions:
            pos = random.choice(range(len(message_list)))
        
        emoji_positions.append(pos)
        message_list[pos] = emoji
    
    return ''.join(message_list)

@client.on(events.NewMessage(from_users='me', pattern='.متت'))
async def update_message(event):
    await event.delete()
    message_text = ' ' * 6
    emojis = ['🤣', '😂', '😹', '🤣', '😂', '😹']
    
    message = await event.respond('🤣😂😹🤣😂😹')
    
    last_message = ""
    start_time = asyncio.get_event_loop().time()
    duration = 5  # مدة التحديث (10 ثوانٍ)
    
    while True:
        try:
            current_time = asyncio.get_event_loop().time()
            if current_time - start_time > duration:
                break
            
            emoji_string = insert_emojis(message_text, emojis)
            while emoji_string == last_message:
                emoji_string = insert_emojis(message_text, emojis)
            
            last_message = emoji_string
            await message.edit(emoji_string)
            
            await asyncio.sleep(0)

        except Exception as e:
            print(f"Error updating message: {e}")
            break

@client.on(events.NewMessage(from_users='me', pattern='.انتحار'))
async def suicide_message(event):
    await event.delete()
    
    # إرسال رسالة "جاري الانتحار"
    message = await event.respond("**جاري الانتحار .....**")
    
    # الانتظار لمدة 6 ثوانٍ
    await asyncio.sleep(3)
    
    # تحديث الرسالة إلى النص المطلوب
    final_message = (
        "تم الانتحار بنجاح😂...\n"
        "　　　　　|\n"
        "　　　　　|\n"
        "　　　　　|\n"
        "　　　　　|\n"
        "　　　　　|\n"
        "　　　　　|\n"
        "　　　　　|\n"
        "　　　　　|\n"
        "　／￣￣＼| \n"
        "＜ ´･ 　　 |＼ \n"
        "　|　３　 | 丶＼ \n"
        "＜ 、･　　|　　＼ \n"
        "　＼＿＿／∪ _ ∪) \n"
        "　　　　　 Ｕ Ｕ"
    )
    
    await message.edit(final_message)

def insert_emojis(message, emojis):
    random.shuffle(emojis)
    message_list = list(message)
    emoji_positions = []
    
    for emoji in emojis:
        pos = random.choice(range(len(message_list)))
        while pos in emoji_positions:
            pos = random.choice(range(len(message_list)))
        
        emoji_positions.append(pos)
        message_list[pos] = emoji
    
    return ''.join(message_list)

@client.on(events.NewMessage(from_users='me', pattern='.شرير'))
async def update_message(event):
    await event.delete()
    message_text = ' ' * 6
    emojis = ['😈', '💀', '👿', '🔪', '☠️', '👹']
    
    message = await event.respond('👿💀👹👿🔪☠️')
    
    last_message = ""
    start_time = asyncio.get_event_loop().time()
    duration = 5  # مدة التحديث (10 ثوانٍ)
    
    while True:
        try:
            current_time = asyncio.get_event_loop().time()
            if current_time - start_time > duration:
                break
            
            emoji_string = insert_emojis(message_text, emojis)
            while emoji_string == last_message:
                emoji_string = insert_emojis(message_text, emojis)
            
            last_message = emoji_string
            await message.edit(emoji_string)
            
            await asyncio.sleep(0)

        except Exception as e:
            print(f"Error updating message: {e}")
            break

@client.on(events.NewMessage(from_users='me', pattern='.اضافة مجموعة'))
async def add_group(event):
    try:
        # Get the group ID from the chat where the command was issued
        group_id = event.chat_id
        
        # Save the group ID for future use
        with open('group_id.pkl', 'wb') as f:
            pickle.dump(group_id, f)
        
        # Fetch group details
        group = await client.get_entity(group_id)
        group_name = group.title
        group_type = "قناة" if isinstance(group, Channel) else "مجموعة"

        # Send confirmation message
        await event.reply(f"✅ تم تعيين المجموعة إلى: {group_name} ({group_type})")
    except Exception as e:
        await event.reply(f"❌ حدث خطأ: {str(e)}")

# الدالة للتعامل مع الرسائل الخاصة
@client.on(events.NewMessage(incoming=True))
async def forward_private_message(event):
    # Load the group ID
    if os.path.exists('group_id.pkl'):
        with open('group_id.pkl', 'rb') as f:
            group_id = pickle.load(f)
    else:
        group_id = None

    if event.is_private and not (await event.get_sender()).bot:
        if group_id:
            # Forward the message to the specified group
            await client.forward_messages(group_id, event.message)

            # Send additional information
            sender = await event.get_sender()
            group_name = (await client.get_entity(group_id)).title
            timestamp = time.strftime("%H:%M")
            message_text = event.message.text or "لا يوجد نص للرسالة"
            user_mention = f"@{sender.username}" if sender.username else "لا يوجد معرف مستخدم"

            info_message = (
                f"☭ لديك منشن من العضو: {sender.first_name}\n"  # استخدم اسم المرسل الأول
                f"☭ اسم الجروب: {group_name}\n"
                f"☭ الوقت: {timestamp}\n"
                f"☭ نص الرسالة: {message_text}\n"
                f"☭ اليوزر: {user_mention}"
            )
            await client.send_message(group_id, info_message)
        else:
            await event.reply("")

# الدالة للتعامل مع الرسائل في المجموعات
@client.on(events.NewMessage(incoming=True))
async def forward_group_message(event):
    # Load the group ID
    if os.path.exists('group_id.pkl'):
        with open('group_id.pkl', 'rb') as f:
            group_id = pickle.load(f)
    else:
        group_id = None

    if event.is_group and group_id:
        # Check if the message is a reply
        if event.reply_to_msg_id:
            replied_message = await event.get_reply_message()
            reply_sender = await client.get_entity(replied_message.sender_id)
            bot_id = (await client.get_me()).id

            # Check if the replied message was sent by the bot
            if replied_message.sender_id == bot_id:
                # Forward the reply message to the group
                await client.forward_messages(group_id, event.message)

                # Send additional information
                sender = await event.get_sender()  # المرسل الحالي للرسالة التي تم الرد عليها
                group_name = (await client.get_entity(group_id)).title
                timestamp = time.strftime("%H:%M")
                message_text = event.message.text or "لا يوجد نص للرسالة"
                user_mention = f"@{sender.username}" if sender.username else "لا يوجد معرف مستخدم"

                info_message = (
                    f"☭ لديك منشن من العضو: {sender.first_name}\n"  # استخدم اسم المرسل الأول
                    f"☭ اسم الجروب: {group_name}\n"
                    f"☭ الوقت: {timestamp}\n"
                    f"☭ نص الرسالة: {message_text}\n"
                    f"☭ اليوزر: {user_mention}"
                )
                await client.send_message(group_id, info_message)

@client.on(events.NewMessage(pattern='.ايدي المجموعة'))
async def get_group_id(event):
    if event.chat:
        chat_id = event.chat.id
        await event.reply(f"💡 ID المجموعة: {chat_id}")

# وظيفة لإضافة الرد والصورة أو الرد فقط
@client.on(events.NewMessage(from_users='me', pattern='.add'))
async def add_response(event):
    try:
        photo_path = None

        # إذا كانت الرسالة ترد على رسالة أخرى
        if event.reply_to_msg_id:
            # الحصول على الرسالة التي تم الرد عليها
            replied_message = await client.get_messages(event.chat_id, ids=event.reply_to_msg_id)
            
            # تحقق مما إذا كانت الرسالة تحتوي على صورة
            if replied_message.photo:
                # حفظ الصورة في المجلد
                photo_path = os.path.join(image_folder, f"{event.reply_to_msg_id}.jpg")
                await client.download_media(replied_message, file=photo_path)

        # استخراج الكلمة المفتاحية والرد من الرسالة
        if ' ' in event.raw_text:
            _, args = event.raw_text.split(' ', 1)
            if '(' in args and ')' in args:
                keyword, response = args.split('(', 1)[1].split(')', 1)
                keyword = keyword.strip().lower()
                response = response.strip()

                # حفظ الصورة والرد في القاموس
                responses[keyword] = {
                    'response': response,
                    'photo': photo_path
                }
                
                # حفظ الردود في الملف
                with open(response_file, 'wb') as f:
                    pickle.dump(responses, f)
                
                if photo_path:
                    await event.reply("✅ تم إضافة الرد مع الصورة.")
                else:
                    await event.reply("✅ تم إضافة الرد بدون صورة.")
            else:
                await event.reply("⚠️ يجب استخدام الصيغة الصحيحة: .add (الكلمة المفتاحية) الرد")
        else:
            await event.reply("⚠️ يجب استخدام الصيغة الصحيحة: .add (الكلمة المفتاحية) الرد")

    except Exception as e:
        await event.reply(f"حدث خطأ: {str(e)}")

# وظيفة لإظهار الردود المضافة
@client.on(events.NewMessage(from_users='me', pattern='.الردود'))
async def show_responses(event):
    try:
        if responses:
            message = "📋 الردود المضافة:\n"
            for keyword, data in responses.items():
                photo_status = "مضافة إليه صورة" if data['photo'] else "غير مضافة إليه صورة"
                message += f"🔹 الكلمة المفتاحية: {keyword}\n🔸 الرد: {data['response']} ({photo_status})\n"
            await event.reply(message)
        else:
            await event.reply("❌ لا توجد ردود مضافة حتى الآن.")
    except Exception as e:
        await event.reply(f"حدث خطأ: {str(e)}")

# وظيفة للاستجابة للكلمات المفتاحية وإرسال الرد مع الصورة إن وجدت
@client.on(events.NewMessage(incoming=True))
async def respond_to_greeting(event):
    if event.is_private and not (await event.get_sender()).bot:
        message_text = event.raw_text.lower()
        for keyword, data in responses.items():
            if keyword in message_text:
                try:
                    if data['photo']:
                        await client.send_file(event.chat_id, file=data['photo'], caption=data['response'])
                    else:
                        await event.reply(data['response'])
                except Exception as e:
                    await event.reply(f"حدث خطأ: {str(e)}")
                break

async def respond_to_mention(event):
    if event.is_private and not (await event.get_sender()).bot:  # تحقق ما إذا كانت الرسالة خاصة وليست من بوت
        sender = await event.get_sender()
        await event.reply(f"انتظر يجي المطور @{sender.username} ويرد على رسالتك لا تبقه تمنشنه هواي")

client.add_event_handler(respond_to_mention, events.NewMessage(incoming=True, pattern=f'(?i)@{client.get_me().username}'))

def superscript_time(time_str):
    superscript_digits = str.maketrans('0123456789', '𝟬𝟭𝟮𝟯𝟰𝟱𝟲𝟳𝟴𝟵')
    return time_str.translate(superscript_digits)

async def update_username():
    global account_name
    iraq_tz = pytz.timezone('Asia/Baghdad')
    
    # Get the current account name if not set
    if account_name is None:
        me = await client.get_me()
        account_name = re.sub(r' - \d{2}:\d{2}', '', me.first_name)
    
    while True:
        now = datetime.datetime.now(iraq_tz)
        current_time = superscript_time(now.strftime("%I:%M"))
        
        if time_update_status.get('enabled', False):
            new_username = f"{account_name} - {current_time}"
        else:
            new_username = f"{account_name}"
        
        try:
            # Change the username
            await client(UpdateProfileRequest(first_name=new_username))
        except FloodWaitError as e:
            await asyncio.sleep(e.seconds)
        except Exception as e:
            print(f"Error updating username: {e}")
        
        # Calculate the remaining time until the start of the next minute
        seconds_until_next_minute = 60 - now.second
        await asyncio.sleep(seconds_until_next_minute)

# المتغيرات لتخزين معلومات النقل
transfer_group_from = None
transfer_group_to = None

@client.on(events.NewMessage(from_users='me', pattern='.نقل من'))
async def start_transfer(event):
    global transfer_group_from
    if transfer_group_from is not None:
        await event.reply("⚠️ لقد قمت بالفعل بتحديد مجموعة المصدر. استخدم  نقل إلى لإكمال العملية")
        return
    
    transfer_group_from = event.chat_id
    await event.reply("🔄 الأن اذهب إلى المجموعة المراد النقل اليها واستخدم نقل إلى.")

@client.on(events.NewMessage(from_users='me', pattern='.نقل الى'))
async def complete_transfer(event):
    global transfer_group_from, transfer_group_to
    transfer_group_to = event.chat_id
    
    if transfer_group_from is None:
        await event.reply("⚠️ لم يتم تحديد مجموعة المصدر. استخدم /نقل من في المجموعة المراد النقل منها أولاً.")
        return
    
    if transfer_group_from == transfer_group_to:
        await event.reply("⚠️ لا يمكنك نقل الأعضاء إلى نفس المجموعة.")
        transfer_group_from = None
        transfer_group_to = None
        return

    # جلب قائمة الأعضاء من المجموعة المصدر
    try:
        participants = await client.get_participants(transfer_group_from)
        
        # دعوة الأعضاء إلى المجموعة الوجهة
        for participant in participants:
            try:
                await client(InviteToChannelRequest(channel=transfer_group_to, users=[participant.id]))
            except Exception as e:
                print(f"Error inviting {participant.id}: {e}")
        
        await event.reply("✅ تم نقل جميع الأعضاء إلى المجموعة الجديدة.")
    except Exception as e:
        await event.reply(f"⚠️ حدث خطأ أثناء نقل الأعضاء: {e}")
    
    # إعادة تعيين متغيرات النقل
    transfer_group_from = None
    transfer_group_to = None

@client.on(events.NewMessage(from_users='me', pattern='.الغاء النقل'))
async def cancel_transfer(event):
    global transfer_group_from, transfer_group_to
    transfer_group_from = None
    transfer_group_to = None
    await event.reply("❌ تم إلغاء عملية النقل.")

import os

# تعريف المسار الأساسي لحفظ الصور
base_images_dir = os.path.join(os.getcwd(), 'images')

@client.on(events.NewMessage(from_users='me', pattern=r'.تكرار (\d+) (\d+) ?([\s\S]*)'))
@client.on(events.NewMessage(from_users='me', pattern=r'.تك (\d+) (\d+) ?([\s\S]*)'))
@client.on(events.NewMessage(from_users='me', pattern=r'.نشر (\d+) (\d+) ?([\s\S]*)'))
async def start_repeating_process(event):
    try:
        seconds = int(event.pattern_match.group(1))
        repeat_count = int(event.pattern_match.group(2))
        custom_text = event.pattern_match.group(3)
        
        # التحقق من أن الوقت لا يقل عن 40 ثانية
        if seconds < 40:
            await event.reply("⚠️ يجب أن يكون الوقت المحدد لا يقل عن 40 ثانية.")
            return

        process_images_dir = None
        media_files = []

        if event.is_reply:
            message = await event.get_reply_message()
            
            # إنشاء مجلد مؤقت لكل عملية
            process_id = int(time.time())  # استخدام الوقت كمعرف فريد
            process_images_dir = os.path.join(base_images_dir, str(process_id))
            os.makedirs(process_images_dir)

            # التحقق من نوع الرسالة المرد عليها
            if message.media:
                if message.grouped_id:  # الرسالة تحتوي على مجموعة صور
                    messages = await client.get_messages(event.chat_id, min_id=message.id - 10, max_id=message.id + 10)
                    for msg in messages:
                        if msg.grouped_id == message.grouped_id and msg.photo:
                            file_path = os.path.join(process_images_dir, f"image_{msg.id}.jpg")
                            await msg.download_media(file=file_path)
                            media_files.append(file_path)
                else:
                    if message.photo:
                        file_path = os.path.join(process_images_dir, f"image_{message.id}.jpg")
                        await message.download_media(file=file_path)
                        media_files.append(file_path)

            if not media_files and not custom_text:
                await event.reply("⚠️ يجب تحديد نص مخصص أو الرد على صورة.")
                return

        async def task():
            for i in range(repeat_count):
                if media_files:
                    await client.send_file(event.chat_id, media_files, caption=custom_text)
                else:
                    await client.send_message(event.chat_id, custom_text)
                
                await asyncio.sleep(seconds)
            
            # حذف الملفات المرتبطة بالعملية عند الانتهاء
            if process_images_dir and os.path.exists(process_images_dir):
                shutil.rmtree(process_images_dir)
            # إزالة حالة العملية من القاموس
            active_publishing_tasks.pop(event.chat_id, None)

        task = asyncio.create_task(task())
        
        # حفظ المهمة باستخدام معرف المحادثة لتتمكن من إيقافها لاحقًا
        if event.chat_id not in active_publishing_tasks:
            active_publishing_tasks[event.chat_id] = []
        active_publishing_tasks[event.chat_id].append((task, process_images_dir))
        
        # إرسال تأكيد بعد 1 ثانية
        await asyncio.sleep(2)
        confirmation_message = await event.reply(f"سيتم إرسال الرسالة كل {seconds} ثانية لـ {repeat_count} مرات.")

        # حذف رسالة الأمر بعد 1 ثانية
        await asyncio.sleep(1)
        await event.delete()
        await confirmation_message.delete()

    except Exception as e:
        await event.reply(f"⚠️ حدث خطأ: {e}")

@client.on(events.NewMessage(from_users='me', pattern=r'.ايقاف الارسال'))
async def stop_sending(event):
    try:
        if event.chat_id in active_publishing_tasks:
            for task, process_images_dir in active_publishing_tasks[event.chat_id]:
                task.cancel()
                # حذف الملفات المرتبطة بالعملية عند الإيقاف
                if process_images_dir and os.path.exists(process_images_dir):
                    shutil.rmtree(process_images_dir)
            
            del active_publishing_tasks[event.chat_id]

            # إرسال تأكيد بعد 1 ثانية
            confirmation_message = await event.reply("✅ تم إيقاف جميع عمليات النشر الفعّالة.")
            
            # حذف رسالة الإيقاف بعد 1 ثانية
            await asyncio.sleep(1)
            await event.delete()
            
            # حذف رسالة التأكيد بعد 3 ثوانٍ
            await asyncio.sleep(3)
            await confirmation_message.delete()

        else:
            await event.reply("❌ لا توجد عمليات نشر فعّالة لإيقافها.")
    except Exception as e:
        await event.reply(f"⚠️ حدث خطأ: {e}")

# إضافة المفتاح الخاص بك
YOUTUBE_API_KEY = 'AIzaSyBfb8a-Ug_YQFrpWKeTc88zuI6PmHVdzV0'
YOUTUBE_API_URL = 'https://www.googleapis.com/youtube/v3/search'

@client.on(events.NewMessage(from_users='me', pattern=r'.يوتيوب (.+)'))
async def youtube_search(event):
    query = event.pattern_match.group(1)
    
    async with aiohttp.ClientSession() as session:
        async with session.get(YOUTUBE_API_URL, params={
            'part': 'snippet',
            'q': query,
            'key': YOUTUBE_API_KEY,
            'type': 'video',
            'maxResults': 1
        }) as response:
            data = await response.json()
            if data['items']:
                video_id = data['items'][0]['id']['videoId']
                video_url = f"https://www.youtube.com/watch?v={video_id}"
                await event.reply(f"📹 هنا رابط الفيديو الذي تم العثور عليه:\n{video_url}")
            else:
                await event.reply("❌ لم يتم العثور على فيديو يتطابق مع العنوان المطلوب.")

@client.on(events.NewMessage(from_users='me', pattern='.تفعيل الوقت'))
async def enable_time_update(event):
    global time_update_status
    time_update_status['enabled'] = True
    with open(time_update_status_file, 'wb') as f:
        pickle.dump(time_update_status, f)
    reply = await event.reply("✅ تم تفعيل تحديث الاسم مع الوقت.")
    await event.delete()  # حذف الرسالة الأصلية

    await asyncio.sleep(1)
    await reply.delete()  # حذف رسالة التأكيد بعد 3 ثواني

@client.on(events.NewMessage(from_users='me', pattern='.تعطيل الوقت'))
async def disable_time_update(event):
    global time_update_status
    time_update_status['enabled'] = False
    with open(time_update_status_file, 'wb') as f:
        pickle.dump(time_update_status, f)
    
    # إزالة الوقت من اسم الحساب
    if account_name:
        iraq_tz = pytz.timezone('Asia/Baghdad')
        now = datetime.datetime.now(iraq_tz)
        current_name = re.sub(r' - \d{2}:\d{2}', '', account_name)
        new_username = f"{current_name}"
        
        try:
            await client(UpdateProfileRequest(first_name=new_username))
            reply = await event.reply("✅ تم تعطيل تحديث الاسم وإزالة الوقت من الاسم.")
        except Exception as e:
            reply = await event.reply(f"⚠️ حدث خطأ أثناء إزالة الوقت من الاسم: {e}")
    else:
        reply = await event.reply("⚠️ لم يتم تعيين اسم الحساب.")
    
    await event.delete()  # حذف الرسالة الأصلية

    await asyncio.sleep(1)
    await reply.delete()  # حذف رسالة التأكيد بعد 3 ثواني

@client.on(events.NewMessage(from_users='me', pattern='.اضافة قناة (.+)'))
async def add_channel(event):
    global channel_link
    channel_link = event.pattern_match.group(1)
    with open(channel_link_file, 'wb') as f:
        pickle.dump(channel_link, f)
    await event.reply(f"✅ تم تعيين رابط القناة إلى: {channel_link}")
    await event.delete()  # حذف الرسالة الأصلية

@client.on(events.NewMessage(from_users='me', pattern= '.ازالة القناة' ))
async def remove_channel(event):
    global channel_link
    channel_link = ''
    with open(channel_link_file, 'wb') as f:
        pickle.dump(channel_link, f)
    reply = await event.reply("❌ تم مسح رابط القناة.")
    await event.delete()  # حذف الرسالة الأصلية
    await asyncio.sleep(3)
    await reply.delete()  # حذف رسالة التأكيد بعد ثانية

async def is_subscribed(user_id):
    if not channel_link:
        return True  # إذا لم يكن هناك قناة محددة، اعتبر أن المستخدم مشترك
    channel_username = re.sub(r'https://t.me/', '', channel_link)
    try:
        offset = 0
        limit = 100
        while True:
            participants = await client(GetParticipantsRequest(
                channel=channel_username,
                filter=ChannelParticipantsSearch(''),
                offset=offset,
                limit=limit,
                hash=0
            ))
            if not participants.users:
                break
            for user in participants.users:
                if user.id == user_id:
                    return True
            offset += len(participants.users)
        return False
    except FloodWaitError as e:
        await asyncio.sleep(e.seconds)
        return await is_subscribed(user_id)
    except Exception as e:
        print(f"Error checking subscription: {e}")
        return False

@client.on(events.NewMessage(incoming=True))
async def respond_to_greeting(event):
    if event.is_private and not (await event.get_sender()).bot:  # تحقق ما إذا كانت الرسالة خاصة وليست من بوت
        sender = await event.get_sender()
        if sender.phone == '42777':
            # السماح بمراسلة الحساب بدون الاشتراك في القناة إذا كان الرقم من Telegram
            return
        if not await is_subscribed(event.sender_id):
            await event.reply(f"لا يمكنك مراسلتي الى بعد الاشتراك في قناتي: {channel_link}")
            await client.delete_messages(event.chat_id, [event.id])
        else:
            message_text = event.raw_text.lower()

@client.on(events.NewMessage(from_users='me', pattern='.del'))
async def delete_message(event):
    # انتظار 2 ثانية قبل حذف رسالة الأمر
    await asyncio.sleep(2)
    await event.delete()
    
    try:
        # استخراج الكلمة المفتاحية من الرسالة
        command, keyword = event.raw_text.split(' ', 1)
        keyword = keyword.lower()
        
        if keyword in responses:
            del responses[keyword]
            # حفظ التغييرات في الملف
            with open(response_file, 'wb') as f:
                pickle.dump(responses, f)
            
            # إرسال رسالة تأكيد حذف الكلمة المفتاحية
            confirmation_message = await event.reply("✅ تم حذف الرد")
            
            # انتظار 2 ثانية ثم حذف رسالة التأكيد
            await asyncio.sleep(2)
            await confirmation_message.delete()
        else:
            warning_message = await event.reply("⚠️ لم يتم العثور على الكلمة المحددة")
            
            # انتظار 2 ثانية ثم حذف رسالة التحذير
            await asyncio.sleep(2)
            await warning_message.delete()
    
    # إذا كانت الصيغة غير صحيحة
    except ValueError:
        error_message = await event.reply("⚠️ استخدم الصيغة: del الكلمة المفتاحية")
        
        # انتظار 2 ثانية ثم حذف رسالة الخطأ
        await asyncio.sleep(2)
        await error_message.delete()

@client.on(events.NewMessage(from_users='me', pattern='.عداد'))
async def countdown_timer(event):
    try:
        # Extract the number of minutes from the message
        command, args = event.raw_text.split(' ', 1)
        minutes = int(args.strip().strip('()'))

        # Check if there's an active timer, cancel it
        if event.chat_id in active_timers:
            active_timers[event.chat_id].cancel()
            del active_timers[event.chat_id]
            # Remove the existing countdown message if it exists
            if event.chat_id in countdown_messages:
                await client.delete_messages(event.chat_id, countdown_messages[event.chat_id])
                del countdown_messages[event.chat_id]

        async def timer_task():
            nonlocal minutes
            total_seconds = minutes * 60
            # Send the initial message about the countdown starting
            countdown_message = await event.reply("**⏳ سيبدأ العد التنازلي بعد 3 ثوانٍ**")

            # Store the message ID for later deletion
            countdown_messages[event.chat_id] = countdown_message.id

            # Wait for 1 second and update the message
            await asyncio.sleep(1)
            await countdown_message.edit("⏳** سيبدأ العد التنازلي بعد 2 ثانيتين**")


            # Wait for the final second before starting the countdown
            await asyncio.sleep(1)
            
            # Update the message to start the countdown
            countdown_message = await countdown_message.edit(f"⏳** سيبدأ العد التنازلي بعد 1 ثانية**")
            
            # Countdown loop
            while total_seconds > 0:
                minutes, seconds = divmod(total_seconds, 60)
                new_text = f"⏳** {minutes:02}:{seconds:02} متبقية**"
                await asyncio.sleep(1)
                total_seconds -= 1

                try:
                    if new_text != countdown_message.text:
                        await countdown_message.edit(new_text)
                except MessageNotModifiedError:
                    pass
            
            await countdown_message.edit("⏳ **الوقت انتهى!**")
            # Optionally remove the countdown message after completion
            # await countdown_message.delete()

        # Start the timer task
        active_timers[event.chat_id] = asyncio.create_task(timer_task())
        
    except (ValueError, IndexError):
        await event.reply("⚠️ استخدم الصيغة الصحيحة: عداد (عدد الدقائق)")

@client.on(events.NewMessage(from_users='me', pattern='.توقيف'))
async def stop_timers(event):
    if event.chat_id in active_timers:
        # Cancel the active timer
        active_timers[event.chat_id].cancel()
        del active_timers[event.chat_id]
        
        # Delete the countdown message if it exists
        if event.chat_id in countdown_messages:
            try:
                await client.delete_messages(event.chat_id, countdown_messages[event.chat_id])
                del countdown_messages[event.chat_id]
            except Exception as e:
                print(f"Error deleting countdown message: {e}")

        # Send the confirmation message
        stop_message = await event.reply("✅ تم إيقاف جميع العدادات التنازلية.")
        
        # Wait 3 seconds before deleting the message
        await asyncio.sleep(3)
        await stop_message.delete()
    else:
        # Send the no active timer message
        no_timer_message = await event.reply("❌ لا توجد عدادات تنازلية نشطة لإيقافها.")
        
        # Wait 3 seconds before deleting the message
        await asyncio.sleep(3)
        await no_timer_message.delete()

@client.on(events.NewMessage(from_users='me', pattern='.الاسم'))
async def set_account_name(event):
    global account_name
    try:
        # Extract the new account name from the message
        command, new_name = event.raw_text.split(' ', 1)
        account_name = new_name.split('(', 1)[1].split(')')[0].strip()
        
        # Update the account name immediately
        iraq_tz = pytz.timezone('Asia/Baghdad')
        now = datetime.datetime.now(iraq_tz)
        current_time = superscript_time(now.strftime("%I:%M"))
        new_username = f"{account_name} - {current_time}"
        
        try:
            await client(UpdateProfileRequest(first_name=new_username))
            await event.reply(f"✅ تم تغيير اسم الحساب إلى {new_username}")
        except FloodWaitError as e:
            await asyncio.sleep(e.seconds)
            await client(UpdateProfileRequest(first_name=new_username))
            await event.reply(f"✅ تم تغيير اسم الحساب إلى {new_username}")
        except Exception as e:
            await event.reply(f"⚠️ حدث خطأ أثناء تغيير الاسم: {e}")
    except ValueError:
        await event.reply("⚠️ استخدم الصيغة:  .الاسم (الاسم الجديد)")

@client.on(events.NewMessage(from_users='me', pattern='.مسح'))
async def delete_messages(event):
    try:
        # استخراج عدد الرسائل المراد حذفها من الرسالة
        command, num_str = event.raw_text.split(' ', 1)
        num_messages = int(num_str.strip('()'))
        
        if num_messages <= 0:
            await event.reply("⚠️ يجب أن يكون عدد الرسائل المراد حذفها أكبر من صفر.")
            return
        
        # الحصول على معرفات الرسائل التي سيتم حذفها
        messages = await client.get_messages(event.chat_id, limit=num_messages)
        message_ids = [msg.id for msg in messages]
        
        if message_ids:
            await client(DeleteMessagesRequest(id=message_ids))
            confirmation_message = await event.reply(f"✅ تم مسح {num_messages} رسالة.")
            
            # الانتظار لمدة 3 ثوانٍ ثم حذف رسالة التأكيد
            await asyncio.sleep(2)
            await client(DeleteMessagesRequest(id=[confirmation_message.id]))
        else:
            await event.reply("⚠️ لم يتم العثور على رسائل للحذف.")
    except (ValueError, IndexError):
        await event.reply("⚠️ استخدم الصيغة: مسح (عدد الرسائل)")
    except Exception as e:
        await event.reply(f"⚠️ حدث خطأ أثناء حذف الرسائل: {e}")

@client.on(events.NewMessage(from_users='me', pattern='.نشر مجموعات'))
async def publish_message(event):
    try:
        # Extract the number of groups and the message from the message
        command, args = event.raw_text.split(' ', 1)
        num_groups, message = args.split('(', 1)[1].split(')')[0], args.split(')', 1)[1].strip()
        num_groups = int(num_groups)
        
        # Fetch groups where the bot is a member
        dialogs = await client.get_dialogs()
        groups = [dialog for dialog in dialogs if dialog.is_group]
        
        if len(groups) < num_groups:
            await event.reply(f"⚠️ عدد المجموعات المتاحة أقل من {num_groups}.")
            return
        
        # Publish the message to the specified number of groups
        published_message_ids = []
        for group in groups[:num_groups]:
            msg = await client.send_message(group, message)
            published_message_ids.append((group.id, msg.id))
        
        # Save the published message details
        published_messages.append({
            'message': message,
            'group_ids': [group.id for group in groups[:num_groups]],
            'message_ids': published_message_ids
        })
        with open(published_messages_file, 'wb') as f:
            pickle.dump(published_messages, f)
        
        await event.reply(f"✅ تم نشر الرسالة في {num_groups} مجموعة.")
    except (ValueError, IndexError):
        await event.reply("⚠️ استخدم الصيغة: نشر (عدد المجموعات) الرسالة")
    except Exception as e:
        await event.reply(f"⚠️ حدث خطأ أثناء نشر الرسالة: {e}")

# تحميل قائمة المستخدمين المكتومين من الملف أو إنشاء قائمة جديدة إذا لم تكن موجودة
if os.path.exists(muted_users_file):
    with open(muted_users_file, 'rb') as f:
        muted_users = pickle.load(f)
else:
    muted_users = set()

# أوامر الكتم والسماح وعرض المكتومين
@client.on(events.NewMessage(from_users='me', pattern='.كتم'))
async def mute_user(event):
    if event.is_private:
        muted_users.add(event.chat_id)
        with open(muted_users_file, 'wb') as f:
            pickle.dump(muted_users, f)
        await event.reply("✅ **تم كتم المستخدم**")
    else:
        await event.reply("⚠️ يمكن استخدام هذا الأمر في المحادثات الخاصة فقط.")

@client.on(events.NewMessage(from_users='me', pattern='.سماح'))
async def unmute_user(event):
    if event.is_private and event.chat_id in muted_users:
        muted_users.remove(event.chat_id)
        with open(muted_users_file, 'wb') as f:
            pickle.dump(muted_users, f)
        await event.reply("✅ تم فك الكتم عن هذا المستخدم.")
    else:
        await event.reply("⚠️ هذا المستخدم ليس في قائمة المكتومين")

@client.on(events.NewMessage(from_users='me', pattern='.المكتومين'))
async def show_muted_users(event):
    if muted_users:
        muted_users_list = "\n".join([str(user_id) for user_id in muted_users])
        await event.reply(f"📋 المستخدمون المكتومون:\n{muted_users_list}")
    else:
        await event.reply("❌ لا يوجد مستخدمون مكتومون حالياً.")

from telethon import functions

active_ratib_timers = {}
active_bakhsheesh_timers = {}
active_sarqa_timers = {}

@client.on(events.NewMessage(from_users='me', pattern='.راتب وعد'))
async def enable_ratib_wad(event):
    await event.delete()
    reply = await event.respond("تم تفعيل أمر راتب وعد")
    await asyncio.sleep(1)
    await reply.delete()

    if event.chat_id not in active_ratib_timers:
        async def send_ratib():
            while True:
                await client.send_message(event.chat_id, "راتب")
                await asyncio.sleep(660)  # 11 دقيقة

        active_ratib_timers[event.chat_id] = asyncio.create_task(send_ratib())

@client.on(events.NewMessage(from_users='me', pattern='.ايقاف راتب وعد'))
async def disable_ratib_wad(event):
    await event.delete()

    if event.chat_id in active_ratib_timers:
        active_ratib_timers[event.chat_id].cancel()
        del active_ratib_timers[event.chat_id]
    
    reply = await event.respond("تم إيقاف أمر راتب وعد")
    await asyncio.sleep(2)
    await reply.delete()

@client.on(events.NewMessage(from_users='me', pattern='.بخشيش وعد'))
async def enable_bakhsheesh_wad(event):
    await event.delete()
    reply = await event.respond("تم تفعيل أمر بخشيش وعد")
    await asyncio.sleep(2)
    await reply.delete()

    if event.chat_id not in active_bakhsheesh_timers:
        async def send_bakhsheesh():
            while True:
                await client.send_message(event.chat_id, "بخشيش")
                await asyncio.sleep(660)  # 11 دقيقة

        active_bakhsheesh_timers[event.chat_id] = asyncio.create_task(send_bakhsheesh())

@client.on(events.NewMessage(from_users='me', pattern='.ايقاف بخشيش وعد'))
async def disable_bakhsheesh_wad(event):
    await event.delete()

    if event.chat_id in active_bakhsheesh_timers:
        active_bakhsheesh_timers[event.chat_id].cancel()
        del active_bakhsheesh_timers[event.chat_id]
    
    reply = await event.respond("تم إيقاف أمر بخشيش وعد")
    await asyncio.sleep(2)
    await reply.delete()

@client.on(events.NewMessage(from_users='me', pattern='.سرقة وعد(?: (\d+))?'))
async def enable_sarqa_wad(event):
    await event.delete()

    if event.pattern_match.group(1):
        user_id = int(event.pattern_match.group(1))

        if user_id not in active_sarqa_timers:
            reply = await event.respond("تم تفعيل أمر سرقة وعد")
            await asyncio.sleep(2)
            await reply.delete()

            async def send_sarqa():
                while True:
                    try:
                        async for message in client.iter_messages(event.chat_id, from_user=user_id, limit=1):
                            await client.send_message(event.chat_id, "زرف", reply_to=message.id)
                        await asyncio.sleep(660)  # 11 دقيقة
                    except Exception as e:
                        print(f"Error: {e}")
                        break

            active_sarqa_timers[user_id] = asyncio.create_task(send_sarqa())
    else:
        reply = await event.respond("يرجى كتابة ايدي الشخص مع الامر!")
        await asyncio.sleep(2)
        await reply.delete()

@client.on(events.NewMessage(from_users='me', pattern='.ايقاف سرقة وعد'))
async def disable_sarqa_wad(event):
    await event.delete()

    if event.chat_id in active_sarqa_timers:
        active_sarqa_timers[event.chat_id].cancel()
        del active_sarqa_timers[event.chat_id]
    
    reply = await event.respond("تم إيقاف أمر سرقة وعد")
    await asyncio.sleep(2)
    await reply.delete()

@client.on(events.NewMessage(from_users='me', pattern='.الاوامر'))
async def show_commands(event):
    commands_text = """
⋖⊶◎⊷⌯❪ 𝙎𝙊𝙐𝙍𝙎𝙀 𝙈𝘼 ❫⌯⊶◎⊷⋗

: ⦑ قائمة اوامر سـورس 𝙈𝘼 ⦒

( .م1 ) اوامر الخاص

( .م2 ) اوامر الردود

( .م3 ) اوامر نشر التلقائي

( .م4 ) اوامر الحساب

( .م5 ) اوامر التسلية

( .م6 ) اوامر وعد

( .م7 ) اوامر اليوتيوب

( .م8 ) اوامر نقل الاعضاء

المطور : @z1_xa

⋖⊶◎⊷⌯❪ 𝙎𝙊𝙐𝙍𝙎𝙀 𝙈𝘼 ❫⌯⊶◎⊷⋗
"""
    await event.reply(commands_text)

@client.on(events.NewMessage(from_users='me', pattern='.م1'))
async def show_m1_commands(event):
    m1_text = """
⋖⊶◎⊷⌯❪ 𝙎𝙊𝙐𝙍𝙎𝙀 𝙈𝘼 ❫⌯⊶◎⊷⋗

☭ • كتم

☭ • سماح

☭ • المكتومين

☭ • اضافة قناة (رابط القناة)

☭ • ازالة القناة

المطور : @z1_xa

⋖⊶◎⊷⌯❪ 𝙎𝙊𝙐𝙍𝙎𝙀 𝙈𝘼 ❫⌯⊶◎⊷⋗
"""
    await event.reply(m1_text)

@client.on(events.NewMessage(from_users='me', pattern='.م2'))
async def show_m2_commands(event):
    m2_text = """
⋖⊶◎⊷⌯❪ 𝙎𝙊𝙐𝙍𝙎𝙀 𝙈𝘼 ❫⌯⊶◎⊷⋗

☭ • add (الكلمة المفتاحية) الرد

☭ • del الكلمة المفتاحية

☭ • الردود

المطور : @z1_xa

⋖⊶◎⊷⌯❪ 𝙎𝙊𝙐𝙍𝙎𝙀 𝙈𝘼 ❫⌯⊶◎⊷⋗
"""
    await event.reply(m2_text)

@client.on(events.NewMessage(from_users='me', pattern='.م3'))
async def show_m3_commands(event):
    m3_text = """
⋖⊶◎⊷⌯❪ 𝙎𝙊𝙐𝙍𝙎𝙀 𝙈𝘼 ❫⌯⊶◎⊷⋗

☭ • تك ، تكرار ، نشر (عدد الدقائق) (عدد مرات النشر) الرسالة'

☭ • ايقاف الارسال

☭ • نشر مجموعات (عدد المجموعات) الرسالة

المطور : @z1_xa

⋖⊶◎⊷⌯❪ 𝙎𝙊𝙐𝙍𝙎𝙀 𝙈𝘼 ❫⌯⊶◎⊷⋗
"""
    await event.reply(m3_text)

@client.on(events.NewMessage(from_users='me', pattern='.م4'))
async def show_m4_commands(event):
    m4_text = """
⋖⊶◎⊷⌯❪ 𝙎𝙊𝙐𝙍𝙎𝙀 𝙈𝘼 ❫⌯⊶◎⊷⋗

☭ • تفعيل الوقت ، ايقاف الوقت

☭ • عداد (عدد الدقائق)

☭ • توقيف

☭ • name (الاسم الجديد)

☭ • مسح (عدد الرسائل)

☭ • ايدي المجموعة

☭ •اضافة مجموعة

المطور : @z1_xa

⋖⊶◎⊷⌯❪ 𝙎𝙊𝙐𝙍𝙎𝙀 𝙈𝘼 ❫⌯⊶◎⊷⋗
"""
    await event.reply(m4_text)

@client.on(events.NewMessage(from_users='me', pattern='.م5'))
async def show_m5_commands(event):
    m5_text = """
⋖⊶◎⊷⌯❪ 𝙎𝙊𝙐𝙍𝙎𝙀 𝙈𝘼 ❫⌯⊶◎⊷⋗

☭ • متت

☭ • انتحار

☭ • شرير

☭ • غبي

المطور : @z1_xa

⋖⊶◎⊷⌯❪ 𝙎𝙊𝙐𝙍𝙎𝙀 𝙈𝘼 ❫⌯⊶◎⊷⋗
"""
    await event.reply(m5_text)

@client.on(events.NewMessage(from_users='me', pattern='.م6'))
async def show_m6_commands(event):
    m6_text = """
⋖⊶◎⊷⌯❪ 𝙎𝙊𝙐𝙍𝙎𝙀 𝙈𝘼 ❫⌯⊶◎⊷⋗

☭ • راتب وعد

☭ • ايقاف راتب وعد

☭ • بخشيش وعد

☭ • ايقاف بخشيش وعد

☭ • سرقة وعد (ايدي شخص)

☭ • ايقاف سرقة وعد

المطور : @z1_xa

⋖⊶◎⊷⌯❪ 𝙎𝙊𝙐𝙍𝙎𝙀 𝙈𝘼 ❫⌯⊶◎⊷⋗
"""
    await event.reply(m6_text)

@client.on(events.NewMessage(from_users='me', pattern='.غبي'))
async def dumb_brain(event):
    try:
        # Delete the original command message
        await event.delete()

        # Initial message content
        message_texts = [
            "YOᑌᖇ ᗷᖇᗩIᑎ ➡️ 🧠\n\n🧠         <(^_^ <)🗑",
            "YOᑌᖇ ᗷᖇᗩIᑎ ➡️ 🧠\n\n🧠       <(^_^ <)  🗑",
            "YOᑌᖇ ᗷᖇᗩIᑎ ➡️ 🧠\n\n🧠     <(^_^ <)  🗑",
            "YOᑌᖇ ᗷᖇᗩIᑎ ➡️ 🧠\n\n🧠   <(^_^ <)  🗑",
            "YOᑌᖇ ᗷᖇᗩIᑎ ➡️ 🧠\n\n🧠 <(^_^ <)  🗑",
            "YOᑌᖇ ᗷᖇᗩIᑎ ➡️ 🧠\n\n  (> ^_^)>🧠       🗑",
            "YOᑌᖇ ᗷᖇᗩIᑎ ➡️ 🧠\n\n    (> ^_^)>🧠     🗑",
            "YOᑌᖇ ᗷᖇᗩIᑎ ➡️ 🧠\n\n        (> ^_^)>🧠 🗑",
            "YOᑌᖇ ᗷᖇᗩIᑎ ➡️ 🧠\n\n           (> ^_^)>🗑",
            "YOᑌᖇ ᗷᖇᗩIᑎ ➡️ 🧠\n\n           <(^_^ <)🗑"
        ]

        # Send the initial message
        message = await client.send_message(event.chat_id, message_texts[0])

        # Update the message content every second
        for text in message_texts[1:]:
            await asyncio.sleep(1)
            await message.edit(text)
            
    except Exception as e:
        await client.send_message(event.chat_id, f"⚠️ حدث خطأ: {e}")

@client.on(events.NewMessage(from_users='me', pattern='.م7'))
async def show_m7_commands(event):
    m7_text = """
⋖⊶◎⊷⌯❪ 𝙎𝙊𝙐𝙍𝙎𝙀 𝙈𝘼 ❫⌯⊶◎⊷⋗

☭ • يوتيوب (عنوان الفيديو)

المطور : @z1_xa

⋖⊶◎⊷⌯❪ 𝙎𝙊𝙐𝙍𝙎𝙀 𝙈𝘼 ❫⌯⊶◎⊷⋗
"""
    await event.reply(m7_text)

@client.on(events.NewMessage(from_users='me', pattern='.م8'))
async def show_m8_commands(event):
    m8_text = """
⋖⊶◎⊷⌯❪ 𝙎𝙊𝙐𝙍𝙎𝙀 𝙈𝘼 ❫⌯⊶◎⊷⋗

☭ • نقل من

☭ • نقل الى

☭ •الغاء النقل

المطور : @z1_xaبm

⋖⊶◎⊷⌯❪ 𝙎𝙊𝙐𝙍𝙎𝙀 𝙈𝘼 ❫⌯⊶◎⊷⋗
"""
    await event.reply(m8_text)

# حذف الرسائل من المستخدمين المكتومين
@client.on(events.NewMessage(incoming=True))
async def delete_muted_user_messages(event):
    if event.is_private and event.chat_id in muted_users:
        await client.delete_messages(event.chat_id, [event.id])
    

async def main():
    await client.start()
    await update_username()

with client:
    client.loop.run_until_complete(main())