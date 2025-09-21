from datetime import datetime
from pytz import timezone
from config import Config
from pyrogram.errors import UserNotParticipant
from pyrogram import enums
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

async def send_log(b, u):
    if Config.LOG_CHANNEL is not None:
        try:
            curr = datetime.now(timezone("Asia/Kolkata"))
            date = curr.strftime('%d %B, %Y')
            time = curr.strftime('%I:%M:%S %p')
            await b.send_message(
                Config.LOG_CHANNEL,
                f"**--Nᴇᴡ Uꜱᴇʀ Sᴛᴀʀᴛᴇᴅ Tʜᴇ Bᴏᴛ--**\n\nUꜱᴇʀ: {u.mention}\nIᴅ: `{u.id}`\nUɴ: @{u.username}\n\nDᴀᴛᴇ: {date}\nTɪᴍᴇ: {time}\n\nBy: {b.mention}"
            )
        except Exception as e:
            logger.error(f"Error sending log: {e}")


async def is_subscribed(bot, query):
    try:
        # Check if AUTH_CHANNEL is properly configured
        if not Config.AUTH_CHANNEL:
            logger.warning("AUTH_CHANNEL not configured, skipping subscription check")
            return True
            
        user = await bot.get_chat_member(Config.AUTH_CHANNEL, query.from_user.id)
    except UserNotParticipant:
        return False
    except ValueError as e:
        # Handle invalid peer ID error
        logger.error(f"Invalid peer ID error in is_subscribed: {e}")
        return True  # Allow access if channel config is invalid
    except Exception as e:
        logger.exception(f"Unexpected error in is_subscribed: {e}")
        return True  # Allow access on other errors
    
    return user.status != enums.ChatMemberStatus.BANNED


async def force_sub(bot, cmd):
    try:
        # Check if AUTH_CHANNEL is properly configured
        if not Config.AUTH_CHANNEL:
            logger.warning("AUTH_CHANNEL not configured, skipping force sub")
            return await cmd.continue_propagation()
            
        # Try to create invite link
        try:
            invite_link = await bot.create_chat_invite_link(int(Config.AUTH_CHANNEL))
            invite_url = invite_link.invite_link
        except Exception as e:
            logger.error(f"Error creating invite link: {e}")
            # Fallback to contacting owner if invite link creation fails
            buttons = [[InlineKeyboardButton(
                text="📢 Contact Owner to add you in Channel 📢", 
                url="https://t.me/V_Ditu")]]
            text = "**Please contact the owner to be added to the channel**"
            return await cmd.reply_text(text=text, reply_markup=InlineKeyboardMarkup(buttons))
        
        buttons = [[InlineKeyboardButton(
            text="📢 Join Our Channel 📢", 
            url=invite_url)]]
        text = "**Sᴏʀʀy Dᴜᴅᴇ Yᴏᴜ'ʀᴇ Nᴏᴛ Jᴏɪɴᴇᴅ My Cʜᴀɴɴᴇʟ 😐. Pʟᴇᴀꜱᴇ Jᴏɪɴ Oᴜʀ Uᴩᴅᴀᴛᴇ Cʜᴀɴɴᴇʟ Tᴏ Cᴏɴᴛɪɴᴜᴇ**"

        return await cmd.reply_text(text=text, reply_markup=InlineKeyboardMarkup(buttons))
    
    except Exception as e:
        logger.exception(f"Unexpected error in force_sub: {e}")
        # Allow the user to continue if there's an unexpected error
        return await cmd.continue_propagation()
