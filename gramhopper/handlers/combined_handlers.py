from telegram.ext import MessageHandler, Filters, ConversationHandler


REGULAR_STATE = 0


# A message handler that equally allows all of its child-handlers
# to handle any received update
class CombinedMessageHandler(MessageHandler):
    def __init__(self, handlers):
        self.handlers = handlers
        super().__init__(Filters.all, self.handle_all)

    def handle_all(self, bot, update):
        for handler in self.handlers:
            handler.handle(bot, update)
        return REGULAR_STATE


# A conversation handler that equally allows all of its child-handlers
# to handle any received update
class CombinedConversationHandler(ConversationHandler):
    def __init__(self, handlers):
        message_handlers = [CombinedMessageHandler(handlers)]
        super().__init__(entry_points=message_handlers,
                         states={REGULAR_STATE: message_handlers},
                         fallbacks=[])
