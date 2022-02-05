# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import yandex

# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    import os, telebot

    bot = telebot.TeleBot(os.environ['TELEGRAM_BOT_TOKEN'])
    @bot.message_handler(commands=['start'])
    def start_command(message):
        intro_str = "Вы обратились к конвертеру ссылок \" Yandex <-> Spotify\"!\n" \
                     "Введите ссылку на песню в Яндекс.Музыке или в Spotify в следующих форматах:\n" \
                     "- https://music.yandex.ru/album/номер альбома/track/номер трека\n" \
                     "- https://music.yandex.ru/track/номер трека\n" \
                     "- https://open.spotify.com/track/номер трека"
        bot.send_message(message.chat.id, intro_str)

    @bot.message_handler(content_types=['text'])
    def get_text_messages(message):
        if "yandex" in message.text:
            album_id, track_id = yandex.get_album_and_track_from_yandex_url(message.text)
            if album_id == "" and track_id == "":
                bot.send_message(message.from_user.id, f'Неправильный формат ссылки.')
            else:
                artist, title = yandex.get_artist_and_title_from_yandex(album_id, track_id)
                ext_url = yandex.get_url_from_spotify_by_artist_and_title(artist, title)
                bot.send_message(message.from_user.id, f'{ext_url}')
        elif "spotify" in message.text:
            track_id = yandex.get_album_and_track_from_spotify_url(message.text)
            if track_id == "":
                bot.send_message(message.from_user.id, f'Неправильный формат ссылки.')
            else:
                artist, title = yandex.get_artist_and_title_from_spotify(track_id)
                ext_url = yandex.get_url_from_yandex_by_artist_and_title(artist, title)
                bot.send_message(message.from_user.id, f'{ext_url}')
        else:
            error_str = "Неправильный формат ссылки. Наберите команду \start для подробностей."
            bot.send_message(message.from_user.id, error_str)

    bot.polling(none_stop=True)
