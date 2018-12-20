from telegram import Update
from telegram.ext import Filters, BaseFilter
from ..trigger_result import TriggerResult
from .basic_triggers import BaseTrigger


class FilterBasedTrigger(BaseTrigger):
    def __init__(self, filter: BaseFilter):
        self.filter = filter

    def check_trigger(self, update: Update) -> TriggerResult:
        return TriggerResult(should_respond=self.filter(update.message))


class _UserFilterBasedTrigger(FilterBasedTrigger):
    def __init__(self, user_id=None, username=None):
        super().__init__(Filters.user(user_id, username))


class _ChatFilterBasedTrigger(FilterBasedTrigger):
    def __init__(self, chat_id=None, username=None):
        super().__init__(Filters.chat(chat_id, username))


class _LanguageFilterBasedTrigger(FilterBasedTrigger):
    def __init__(self, lang):
        super().__init__(Filters.language(lang))


class FilterTriggers:
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
    entity = FilterBasedTrigger(Filters.entity)
    caption_entity = FilterBasedTrigger(Filters.caption_entity)
    private = FilterBasedTrigger(Filters.private)
    group = FilterBasedTrigger(Filters.group)
    invoice = FilterBasedTrigger(Filters.invoice)
    successful_payment = FilterBasedTrigger(Filters.successful_payment)
    passport_data = FilterBasedTrigger(Filters.passport_data)
    user = _UserFilterBasedTrigger
    chat = _ChatFilterBasedTrigger
    language = _LanguageFilterBasedTrigger
