From Exon import TOKEN as bot

def markdownV2Escape(str):
    return str.replace(/(_*\[\~>+\-=|{}.!])/g, '\\\$1')

def handle_message(update):
    message = update['message']
    chat_id = message['chat']['id']
    text = message['text']
    if text == '/start' or text == '/hello':
        reply = 'Howdy, how are you doing?'
    else:
        reply = text
    bot.send_message(chat_id=chat_id, text=reply, parse_mode='MarkdownV2')

def handle_inline_query(update):
    query = update['inline_query']
    query_id = query['id']
    query_text = query['query']
    result = {'type': 'article', 'id': '1', 'title': 'Send the message.', 'input_message_content': {'message_text': query_text + ' #afk'}}
    bot.answer_inline_query(inline_query_id=query_id, results=[result])

def dispatch_update(update):
    if 'message' in update:
        handle_message(update)
    elif 'inline_query' in update:
        handle_inline_query(update)

bot.start_polling(dispatch_update)
