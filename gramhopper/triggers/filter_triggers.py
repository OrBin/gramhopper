from telegram import Update
from telegram.ext import Filters, BaseFilter
from ..dict_enum import DictEnum
from .trigger_result import TriggerResult
from .basic_triggers import BaseTrigger
from ..users_helper import DEFAULT_USERS_HELPER


class FilterBasedTrigger(BaseTrigger):
    def __init__(self, message_filter: BaseFilter):
        self.filter = message_filter

    def check_trigger(self, update: Update) -> TriggerResult:
        return TriggerResult(should_respond=self.filter(update.message))


class _UserFilterBasedTrigger(FilterBasedTrigger):
    def __init__(self, nickname=None, user_id=None, username=None):
        if nickname is not None:
            super().__init__(Filters.user(DEFAULT_USERS_HELPER.get_user_id_by_nickname(nickname)))
        else:
            super().__init__(Filters.user(user_id, username))


class _ChatFilterBasedTrigger(FilterBasedTrigger):
    def __init__(self, chat_id=None, username=None):
        super().__init__(Filters.chat(chat_id, username))


class _LanguageFilterBasedTrigger(FilterBasedTrigger):
    def __init__(self, lang):
        super().__init__(Filters.language(lang))


class FilterTriggers(DictEnum):
    all = FilterBasedTrigger(Filters.all)
    text = FilterBasedTrigger(Filters.text)
    command = FilterBasedTrigger(Filters.command)
    reply = FilterBasedTrigger(Filters.reply)
    audio = FilterBasedTrigger(Filters.audio)
    document = FilterBasedTrigger(Filters.document)
    animation = FilterBasedTrigger(Filters.animation)
    photo = FilterBasedTrigger(Filters.photo)
    sticker = FilterBasedTrigger(Filters.sticker)
    video = FilterBasedTrigger(Filters.video)
    voice = FilterBasedTrigger(Filters.voice)
    video_note = FilterBasedTrigger(Filters.video_note)
    contact = FilterBasedTrigger(Filters.contact)
    location = FilterBasedTrigger(Filters.location)
    venue = FilterBasedTrigger(Filters.venue)
    status_update = FilterBasedTrigger(Filters.status_update)
    forwarded = FilterBasedTrigger(Filters.forwarded)
    game = FilterBasedTrigger(Filters.game)
    entity = FilterBasedTrigger(Filters.entity)  # Filters.entity is a class
    caption_entity = FilterBasedTrigger(Filters.caption_entity)  # Filters.caption_entity is a class
    private = FilterBasedTrigger(Filters.private)
    group = FilterBasedTrigger(Filters.group)
    invoice = FilterBasedTrigger(Filters.invoice)
    successful_payment = FilterBasedTrigger(Filters.successful_payment)
    passport_data = FilterBasedTrigger(Filters.passport_data)
    user = _UserFilterBasedTrigger
    chat = _ChatFilterBasedTrigger
    language = _LanguageFilterBasedTrigger
