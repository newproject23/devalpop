import asyncio
import glob
import os
import re
import sys
import urllib.request
from datetime import timedelta
from pathlib import Path

from telethon import Button, functions, types, utils
from telethon.events import CallbackQuery
from telethon.tl.functions.account import UpdateNotifySettingsRequest
from telethon.tl.functions.channels import JoinChannelRequest
from telethon.tl.functions.contacts import UnblockRequest
from telethon.tl.types import InputPeerNotifySettings

from @VIP_ALPOP import BOTLOG, BOTLOG_CHATID, PM_LOGGER_GROUP_ID
from pop.CMD.utils import *

from ..Config import Config
from ..core.logger import logging
from ..core.session import @VIP_ALPOP
from ..helpers.utils import install_pip
from ..helpers.utils.utils import runcmd
from ..sql_helper.global_collection import (
    del_keyword_collectionlist,
    get_item_collectionlist,
)
from ..sql_helper.globals import addgvar, gvarstatus
from .pluginmanager import load_module
from .tools import create_supergroup

ENV = bool(os.environ.get("ENV", False))
LOGS = logging.getLogger("اعداد بوب")
cmdhr = Config.COMMAND_HAND_LER

if ENV:
    VPS_NOLOAD = ["سيرفر"]
elif os.path.exists("config.py"):
    VPS_NOLOAD = ["هيروكو"]


async def setup_bot():
    """
    لاعداد السورس
    """
    try:
        await @VIP_ALPOP.connect()
        config = await @VIP_ALPOP(functions.help.GetConfigRequest())
        for option in config.dc_options:
            if option.ip_address == @VIP_ALPOP.session.server_address:
                if @VIP_ALPOP.session.dc_id != option.id:
                    LOGS.warning(
                        f"اصلاح الداتا {@VIP_ALPOP.session.dc_id}" f" الى {option.id}"
                    )
                @VIP_ALPOP.session.set_dc(option.id, option.ip_address, option.port)
                @VIP_ALPOP.session.save()
                break
        bot_details = await @VIP_ALPOP.tgbot.get_me()
        Config.TG_BOT_USERNAME = f"@{bot_details.username}"
        # await @VIP_ALPOP.start(bot_token=Config.TG_BOT_USERNAME)
        @VIP_ALPOP.me = await @VIP_ALPOP.get_me()
        @VIP_ALPOP.uid = @VIP_ALPOP.tgbot.uid = utils.get_peer_id(@VIP_ALPOP.me)
        if Config.OWNER_ID == 0:
            Config.OWNER_ID = utils.get_peer_id(@VIP_ALPOP.me)
    except Exception as e:
        LOGS.error(f"STRING_SESSION - {e}")
        sys.exit()


async def saves():
    try:
        os.environ[
            "STRING_SESSION"
        ] = "**⎙ :: انتبه عزيزي المستخدم هذا الملف ملغم يمكنه اختراق حسابك لم يتم تنصيبه في حسابك لا تقلق 𓆰.**"
    except Exception as e:
        print(str(e))
    try:
        await @VIP_ALPOP(UnblockRequest("@@SOURCE_ALPOP"))
        await @VIP_ALPOP(
            UpdateNotifySettingsRequest(
                peer="t.me/G1popbot",
                settings=InputPeerNotifySettings(mute_until=2**31 - 1),
            )
        )
        await @VIP_ALPOP.edit_folder("@G1popbot", folder=1)  # عمل ارشيف للبوت
        await @VIP_ALPOP(UnblockRequest("@G1popbot"))
        await @VIP_ALPOP(JoinChannelRequest("@@SOURCE_ALPOP"))
        await @VIP_ALPOP(JoinChannelRequest("@@SOURCE_ALPOP"))
        await @VIP_ALPOP(JoinChannelRequest("@@SOURCE_ALPOP"))
        await @VIP_ALPOP(JoinChannelRequest("@@SOURCE_ALPOP"))
        await @VIP_ALPOP(JoinChannelRequest("@@SOURCE_ALPOP"))
    except BaseException:
        pass


async def mybot():
    @VIP_ALPOP_USER = @VIP_ALPOP.me.first_name
    The_pop = @VIP_ALPOP.uid
    rz_ment = f"[{@VIP_ALPOP_USER}](tg://user?id={The_pop})"
    f"ـ {rz_ment}"
    f"⪼ هذا هو بوت خاص بـ {rz_ment} يمكنك التواصل معه هنا"
    starkbot = await @VIP_ALPOP.tgbot.get_me()
    perf = "[ بوب ]"
    bot_name = starkbot.first_name
    botname = f"@{starkbot.username}"
    if bot_name.endswith("Assistant"):
        print("تم تشغيل البوت")
    else:
        try:
            await @VIP_ALPOP.send_message("@G1popbot", "/start")
            await asyncio.sleep(1)
            await @VIP_ALPOP.send_message(
                "@G1popbot",
                "⎊ تم بنجاح تشغيل سورس بوب 🕷",
            )
            await asyncio.sleep(1)
            await @VIP_ALPOP.send_message("@BotFather", "/setinline")
            await asyncio.sleep(1)
            await @VIP_ALPOP.send_message("@BotFather", botname)
            await asyncio.sleep(1)
            await @VIP_ALPOP.send_message("@BotFather", perf)
            await asyncio.sleep(2)
        except Exception as e:
            print(e)


async def startupmessage():
    if not gvarstatus("DEPLOY"):
        try:
            if BOTLOG:
                await @VIP_ALPOP.tgbot.send_file(
                    BOTLOG_CHATID,
                    "https://telegra.ph//file/8a417ee5ee410523952b3.jpg",
                    caption="**شكرا لتنصيبك تيلثون بوب**\n**`لعرض الاوامر ارسل `.الاوامر**\n**اضغط على الزر ي الاسفل**",
                    buttons=[(Button.inline("اضغط هنا", data="initft_2"),)],
                )
                addgvar("DEPLOY", "Done")
        except Exception as e:
            LOGS.error(e)
    else:
        try:
            if BOTLOG:
                await @VIP_ALPOP.tgbot.send_message(
                    BOTLOG_CHATID,
                    "**تم تشغيل سورس بوب بنجاح**\n➖➖➖➖➖➖➖➖➖➖\n**قناة السورس: @@SOURCE_ALPOP**\n**قناة الكلايش: @@SOURCE_ALPOP**\n**مطور السورس: @@VIP_ALPOP**\n➖➖➖➖➖➖➖➖➖➖\n**لعرض الاوامر ارسل `.الاوامر`**",
                    buttons=[
                        (Button.url("كروب المساعدة", "https://t.me/@SOURCE_ALPOP"),)
                    ],
                )
        except Exception as e:
            LOGS.error(e)
        return None
    try:
        msg_details = list(get_item_collectionlist("restart_update"))
        if msg_details:
            msg_details = msg_details[0]
    except Exception as e:
        LOGS.error(e)
        return None
    try:
        if msg_details:
            await @VIP_ALPOP.check_testcases()
            message = await @VIP_ALPOP.get_messages(msg_details[0], ids=msg_details[1])
            text = message.text + "\n\n**الان السورس شغال طبيعي.**"
            await @VIP_ALPOP.edit_message(msg_details[0], msg_details[1], text)
            if gvarstatus("restartupdate") is not None:
                await @VIP_ALPOP.send_message(
                    msg_details[0],
                    f"{cmdhr}فحص",
                    reply_to=msg_details[1],
                    schedule=timedelta(seconds=10),
                )
            del_keyword_collectionlist("restart_update")
    except Exception as e:
        LOGS.error(e)
        return None


@@VIP_ALPOP.tgbot.on(CallbackQuery(data=re.compile(b"initft_(\\d+)")))
async def deploy(e):
    CURRENT = int(e.data_match.group(1))
    if CURRENT == 5:
        return await e.edit(
            STRINGS[5],
            buttons=[Button.inline("<< رجوع", data="initbk_4")],
            link_preview=False,
        )
    await e.edit(
        STRINGS[CURRENT],
        buttons=[
            Button.inline("<<", data=f"initbk_{str(CURRENT - 1)}"),
            Button.inline(">>", data=f"initft_{str(CURRENT + 1)}"),
        ],
        link_preview=False,
    )


@@VIP_ALPOP.tgbot.on(CallbackQuery(data=re.compile(b"initbk_(\\d+)")))
async def ineiq(e):
    CURRENT = int(e.data_match.group(1))
    if CURRENT == 1:
        return await e.edit(
            STRINGS[1],
            buttons=[Button.inline("اضغط للبدأ >>", data="initft_2")],
            link_preview=False,
        )
    await e.edit(
        STRINGS[CURRENT],
        buttons=[
            Button.inline("<<", data=f"initbk_{str(CURRENT - 1)}"),
            Button.inline(">>", data=f"initft_{str(CURRENT + 1)}"),
        ],
        link_preview=False,
    )


async def add_bot_to_logger_group(chat_id):
    """
    اضافة البوت للكروبات
    """
    bot_details = await @VIP_ALPOP.tgbot.get_me()
    try:
        await @VIP_ALPOP(
            functions.messages.AddChatUserRequest(
                chat_id=chat_id,
                user_id=bot_details.username,
                fwd_limit=1000000,
            )
        )
    except BaseException:
        try:
            await @VIP_ALPOP(
                functions.channels.InviteToChannelRequest(
                    channel=chat_id,
                    users=[bot_details.username],
                )
            )
        except Exception as e:
            LOGS.error(str(e))


async def load_plugins(folder, extfolder=None):
    """
    تحميل ملفات السورس
    """
    if extfolder:
        path = f"{extfolder}/*.py"
        plugin_path = extfolder
    else:
        path = f"@VIP_ALPOP/{folder}/*.py"
        plugin_path = f"@VIP_ALPOP/{folder}"
    files = glob.glob(path)
    files.sort()
    success = 0
    failure = []
    for name in files:
        with open(name) as f:
            path1 = Path(f.name)
            shortname = path1.stem
            pluginname = shortname.replace(".py", "")
            try:
                if (pluginname not in Config.NO_LOAD) and (
                    pluginname not in VPS_NOLOAD
                ):
                    flag = True
                    check = 0
                    while flag:
                        try:
                            load_module(
                                pluginname,
                                plugin_path=plugin_path,
                            )
                            if shortname in failure:
                                failure.remove(shortname)
                            success += 1
                            break
                        except ModuleNotFoundError as e:
                            install_pip(e.name)
                            check += 1
                            if shortname not in failure:
                                failure.append(shortname)
                            if check > 5:
                                break
                else:
                    os.remove(Path(f"{plugin_path}/{shortname}.py"))
            except Exception as e:
                if shortname not in failure:
                    failure.append(shortname)
                os.remove(Path(f"{plugin_path}/{shortname}.py"))
                LOGS.info(
                    f"لم يتم تحميل {shortname} بسبب خطأ {e}\nمسار الملف {plugin_path}"
                )
    if extfolder:
        if not failure:
            failure.append("None")
        await @VIP_ALPOP.tgbot.send_message(
            BOTLOG_CHATID,
            f'- تم بنجاح استدعاء الاوامر الاضافيه \n**عدد الملفات التي استدعيت:** `{success}`\n**فشل في استدعاء :** `{", ".join(failure)}`',
        )


async def verifyLoggerGroup():
    """
    التاكد من كروب التخزين
    """
    flag = False
    if BOTLOG:
        try:
            entity = await @VIP_ALPOP.get_entity(BOTLOG_CHATID)
            if not isinstance(entity, types.User) and not entity.creator:
                if entity.default_banned_rights.send_messages:
                    LOGS.info(
                        "لا توجد صلاحيات كافية لارسال الرسائل في كروب الحفظ او التخزين"
                    )
                if entity.default_banned_rights.invite_users:
                    LOGS.info(
                        "لا توجد صلاحيات كافية لاضافة الاعضاء في كروب الحفظ او التخزين"
                    )
        except ValueError:
            LOGS.error("لم يتم التعرف على فار كروب الحفظ")
        except TypeError:
            LOGS.error("يبدو انك وضعت فار كروب الحفظ بشكل غير صحيح")
        except Exception as e:
            LOGS.error("هنالك خطا ما للتعرف على فار كروب الحفظ\n" + str(e))
    else:
        descript = "⎊ هذه هي مجموعه الاشعارات الخاصه بك لا تحذفها"
        photobt = await @VIP_ALPOP.upload_file(file="pop/pic/pop1.jpg")
        _, groupid = await create_supergroup(
            "جروب اشعارات بوب", @VIP_ALPOP, Config.TG_BOT_USERNAME, descript, photobt
        )
        addgvar("PRIVATE_GROUP_BOT_API_ID", groupid)
        print("تم انشاء كروب الاشعارات بنجاح")
        flag = True
    if PM_LOGGER_GROUP_ID != -100:
        try:
            entity = await @VIP_ALPOP.get_entity(PM_LOGGER_GROUP_ID)
            if not isinstance(entity, types.User) and not entity.creator:
                if entity.default_banned_rights.send_messages:
                    LOGS.info("لا توجد صلاحيات كافية لارسال الرسائل في كروب التخزين")
                if entity.default_banned_rights.invite_users:
                    LOGS.info("لا توجد صلاحيات كافية لاضافة الاعضاء في كروب التخزين")
        except ValueError:
            LOGS.error(
                "لم يتم العثور على ايدي كروب التخزين تاكد من انه مكتوب بشكل صحيح "
            )
        except TypeError:
            LOGS.error("صيغه ايدي كروب التخزين غير صالحة.تاكد من انه مكتوب بشكل صحيح ")
        except Exception as e:
            LOGS.error("حدث خطأ اثناء التعرف على كروب التخزين\n" + str(e))
    else:
        descript = "⎊ لا تحذف او تغادر المجموعه وظيفتها حفظ الرسائل"
        photobt = await @VIP_ALPOP.upload_file(file="pop/pic/pop2.jpg")
        _, groupid = await create_supergroup(
            "جروب تخزين بوب", @VIP_ALPOP, Config.TG_BOT_USERNAME, descript, photobt
        )
        addgvar("PM_LOGGER_GROUP_ID", groupid)
        print("تم عمل جروب التخزين بنجاح واضافة الفارات اليه.")
        flag = True
    if flag:
        executable = sys.executable.replace(" ", "\\ ")
        args = [executable, "-m", "@VIP_ALPOP"]
        os.execle(executable, *args, os.environ)
        sys.exit(0)


async def install_externalrepo(repo, branch, cfolder):
    JMTHONREPO = repo
    rpath = os.path.join(cfolder, "requirements.txt")
    if JMTHONBRANCH := branch:
        repourl = os.path.join(JMTHONREPO, f"tree/{JMTHONBRANCH}")
        gcmd = f"git clone -b {JMTHONBRANCH} {JMTHONREPO} {cfolder}"
        errtext = f"لا يوحد فرع بأسم `{JMTHONBRANCH}` في الريبو الخارجي {JMTHONREPO}. تاكد من اسم الفرع عبر فار (`EXTERNAL_REPO_BRANCH`)"
    else:
        repourl = JMTHONREPO
        gcmd = f"git clone {JMTHONREPO} {cfolder}"
        errtext = f"الرابط ({JMTHONREPO}) الذي وضعته لفار `EXTERNAL_REPO` غير صحيح عليك وضع رابط صحيح"
    response = urllib.request.urlopen(repourl)
    if response.code != 200:
        LOGS.error(errtext)
        return await @VIP_ALPOP.tgbot.send_message(BOTLOG_CHATID, errtext)
    await runcmd(gcmd)
    if not os.path.exists(cfolder):
        LOGS.error(
            "هنالك خطأ اثناء استدعاء رابط الملفات الاضافية يجب التأكد من الرابط اولا "
        )
        return await @VIP_ALPOP.tgbot.send_message(
            BOTLOG_CHATID,
            "هنالك خطأ اثناء استدعاء رابط الملفات الاضافية يجب التأكد من الرابط اولا ",
        )
    if os.path.exists(rpath):
        await runcmd(f"pip3 install --no-cache-dir -r {rpath}")
    await load_plugins(folder="@VIP_ALPOP", extfolder=cfolder)
