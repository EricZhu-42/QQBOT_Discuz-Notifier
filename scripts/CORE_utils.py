# -*- coding: utf-8 -*-
import asyncio
import json
import random
import time

from mirai import (At, Face, Friend, FriendMessage, Group, GroupMessage,
                   Member, MessageChain, Mirai, Plain)
from mirai.face import QQFaces

# =================================

DEBUG = False

# =================================

with open("./config.json", "r", encoding='utf-8') as f:
    _js = json.loads(f.read())

MIRAI_API_HTTP_LOCATE = _js['MIRAI_API_HTTP_LOCATE']
AUTH_KEY              = _js['AUTH_KEY']

BOT_QQ_ID             = _js['BOT_QQ_ID']
MASTER_QQ_ID          = _js['MASTER_QQ_ID']

HEARTBEAT_GROUP_ID    = _js['HEARTBEAT_GROUP_ID']

STEAM_GROUP_ID        = _js['STEAM_GROUP_ID']
RR_GROUP_ID           = _js['RR_GROUP_ID']

app = Mirai(f"mirai://{MIRAI_API_HTTP_LOCATE}?authKey={AUTH_KEY}&qq={BOT_QQ_ID}")


