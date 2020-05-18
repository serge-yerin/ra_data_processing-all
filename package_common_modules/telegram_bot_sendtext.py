import requests

def telegram_bot_sendtext(chat_id, bot_message):
    '''
    Sending message through telegram bot
    Input variables:
        bot_message - string of text message to send
    Output variables:
        return - response of the bot with message status (json format)
    '''
    token_file = open('service_data/bot.txt', 'r')
    bot_token = token_file.readline()[:-1]
    token_file.close()

    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + chat_id + '&parse_mode=Markdown&text=' + bot_message

    response = requests.get(send_text)
    return response.json()


if __name__ == '__main__':

    chat_id = '927534685'
    test = telegram_bot_sendtext(chat_id, "Hello there, it's GURT! \n We have observed SUN")

