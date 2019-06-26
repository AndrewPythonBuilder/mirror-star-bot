import logging
import constants, base_w, texts
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, Contact, KeyboardButton, ChatMember, ChatAction, InlineQueryResultArticle, InputTextMessageContent, ParseMode
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters, InlineQueryHandler

import datetime


add = delete_a = robber_t = disc = ph = telegr = discr = mosh = call_c = money = mailing = upgr = False


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
updater = Updater(token=constants.token)
dispatcher = updater.dispatcher

job_queue = updater.job_queue


def start(bot,update):
    message = update.message
    global add, delete_a, robber_t, disc, ph, telegr, discr , mosh , call_c , money,mailing
    if message.chat.id in constants.admins:
        base_w.delete_none_users()
        add = delete_a = robber_t = disc = ph = telegr = mailing = False
        buttons = [['Добавить мошенника','Модераторы'],['Статистика','Рассылка']]
        keyboard = ReplyKeyboardMarkup(buttons, resize_keyboard=True)
        bot.send_message(message.chat.id, 'Привет, кого на этот раз разоблачим?', reply_markup=keyboard)
    elif message.chat.id in base_w.ids_admins():
        buttons = [['Добавить мошенника']]
        add = delete_a = robber_t = disc = ph = telegr = False
        base_w.delete_none_users()
        keyboard = ReplyKeyboardMarkup(buttons, resize_keyboard=True)
        bot.send_message(message.chat.id, 'Выберите действие', reply_markup=keyboard)
    else:
        base_w.new_user(message.chat.id)
        base_w.statistics_plus(message.chat.id)
        discr = mosh = money = call_c = False
        buttons = [['Поиск мошенника🔍','Список мошенников🕵‍♂🕵‍♂🕵‍♂'],['Добавить мошенника🕵‍♂','Заказать возврат денег💲'],['Связаться с нами📞']]
        keyboard = ReplyKeyboardMarkup(buttons, resize_keyboard=True)
        bot.send_message(message.chat.id, texts.hello_t, reply_markup=keyboard)
        print(message.chat.id)

def answer_questions(bot, update):
    message = update.message
    if (message.chat.id in constants.admins) or (base_w.is_pro_admin(message.chat.id) == 'on'):
        #----------------------------------admins--------------------------------
        global add, delete_a, robber_t,disc, ph, telegr, mailing, upgr
        if message.text == 'Модераторы':
            buttons = [['Добавить модератора','Список модераторов','Удалить модератора'],['Upgrade модератора✅'],['Домой']]
            keyboard = ReplyKeyboardMarkup(buttons, resize_keyboard=True)
            bot.send_message(message.chat.id, 'Выберите действие', reply_markup=keyboard)

        elif message.text == 'Домой' or message.text == 'Отмена':
            add = delete_a = robber_t =disc = ph = telegr =mailing = upgr = False
            base_w.delete_none_users()
            buttons = [['Добавить мошенника', 'Модераторы'], ['Статистика', 'Рассылка']]
            keyboard = ReplyKeyboardMarkup(buttons, resize_keyboard=True)
            bot.send_message(message.chat.id, 'Привет, кого на этот раз разоблачим?', reply_markup=keyboard)

        elif message.text == 'Добавить модератора':
            buttons = [['Отмена']]
            keyboard = ReplyKeyboardMarkup(buttons, resize_keyboard=True)
            bot.send_message(message.chat.id, 'Перешлите какое-нибудь его сообщение в чат с ботом', reply_markup=keyboard)
            add = True

        elif add == True:
            add  = False
            try:
                id_ = message.forward_from.id
                username = message.forward_from.username
                first_name = message.forward_from.first_name
                base_w.init_admin(id_,username,first_name)
                buttons = [['Домой']]
                keyboard = ReplyKeyboardMarkup(buttons, resize_keyboard=True)
                bot.send_message(message.chat.id, 'Отлично добавлен новый модератор', reply_markup=keyboard)
            except:
                bot.send_message(message.chat.id, 'Произошла ошибка, попробуйте еще раз с самого начала. Убедитесь в правильности данных')
                message.text = 'Домой'
                answer_questions(bot, update)

        elif message.text == 'Список модераторов':
            list_of_admins = base_w.all_admins()
            str_list = ''
            for i in list_of_admins:
                str_list += i + '\n'
            bot.send_message(message.chat.id, str_list)

        elif message.text == 'Удалить модератора':
            list_of_admins = base_w.all_admins()
            buttons = []
            for i in list_of_admins:
                button = [i]
                buttons.append(button)
            buttons.append(['Домой'])
            keyboard = ReplyKeyboardMarkup(buttons, resize_keyboard=True)
            bot.send_message(message.chat.id, 'Выберите модератора, которого хотите удалить', reply_markup=keyboard)
            delete_a = True

        elif delete_a == True:
            delete_a =False
            a = message.text.split('  ')
            try:
                base_w.delete_admin(a[0], a[1])
                bot.send_message(message.chat.id, 'Модератор удален')
                message.text = 'Домой'
                answer_questions(bot, update)
            except:
                pass

        #--------------------------------------ROBBER-----------------------
        elif message.text == 'Добавить мошенника':
            buttons = [['Домой']]
            keyboard = ReplyKeyboardMarkup(buttons, resize_keyboard=True)
            bot.send_message(message.chat.id, 'Перешлите сообщение мошенника в чат с ботом', reply_markup=keyboard)
            robber_t = True

        elif robber_t == True:
            robber_t = False
            try:
                id_ = message.forward_from.id
                username = message.forward_from.username
                base_w.add_robber_id(id_, username)
                base_w.save_nikcname(message.forward_from.first_name)
                bot.send_message(message.chat.id, 'id мошенника сохранено\nПришлите описание(без фото)')
                disc = True
            except:
                bot.send_message(message.chat.id,
                                 'Произошла ошибка, попробуйте еще раз с самого начала. Убедитесь в правильности данных')
                message.text = 'Домой'
                answer_questions(bot, update)

        elif disc == True:
            disc = False
            base_w.save_discription(message.text)
            buttons = [['Далее'],['Домой']]
            keyboard = ReplyKeyboardMarkup(buttons, resize_keyboard=True)
            bot.send_message(message.chat.id, 'Описание сохранено, можете прислать фотографии.\nЕсли их нет, нажмите на кнопку "далее"',
                             reply_markup=keyboard)
            ph = True

        elif ph == True:
            ph = False
            if message.text != 'Далее':
                try:
                    l = ''
                    for i in range(len(message.photo)):
                        l += message.photo[i].file_id + '@#$%$#@'
                    base_w.save_photo(l)
                    buttons = [['Все'],['Домой']]
                    keyboard = ReplyKeyboardMarkup(buttons, resize_keyboard=True)
                    bot.send_message(message.chat.id,
                                     'Ваши фотографии сохранены, скиньте ссылку на telegraph или нажмите "все"',
                                     reply_markup=keyboard)
                    telegr = True
                except:
                    bot.send_message(message.chat.id,
                                     'Произошла ошибка, попробуйте еще раз с самого начала. Убедитесь в правильности данных')
                    message.text = 'Домой'
                    answer_questions(bot, update)
            else:
                buttons = [['Все'], ['Домой']]
                keyboard = ReplyKeyboardMarkup(buttons, resize_keyboard=True)
                bot.send_message(message.chat.id,
                                 'Cкиньте ссылку на telegraph или нажмите "все"',
                                 reply_markup=keyboard)
                telegr = True

        elif telegr == True:
            telegr = False
            if message.text != 'Все':
                base_w.save_telegr(message.text)
            else:
                message.text = 'Статьи нет'
                base_w.save_telegr(message.text)
            buttons = [['Домой']]
            keyboard = ReplyKeyboardMarkup(buttons, resize_keyboard=True)
            bot.send_message(message.chat.id,
                             'Все, готово, мошенник пойман!\nПредлагаю пойти домой!)',
                             reply_markup=keyboard)

        #------------------------------------statistics-----------------------------------
        elif message.text == 'Статистика':
            bot.send_message(message.chat.id, texts.statistics %(len(base_w.statistics_registred()), base_w.statistics_daily()))

        #------------------------------------mailing--------------------------------------
        elif message.text == 'Рассылка':
            buttons = [['Отмена']]
            keyboard = ReplyKeyboardMarkup(buttons, resize_keyboard=True)
            bot.send_message(message.chat.id, 'Следующее ваше сообщение разошлется всем пользователям бота, кроме модераторов и админов\nНажмите "отмена", если хотите вернуться назад',
                             reply_markup=keyboard)
            mailing = True

        elif mailing == True:
            mailing = False
            for i in base_w.statistics_registred():
                try:
                    bot.forward_message(chat_id=i, from_chat_id=message.chat.id, disable_notification=False,
                                        message_id=message.message_id)
                except:
                    pass

        elif message.text == 'Upgrade модератора✅':
            list_of_admins = base_w.all_admins()
            buttons = []
            for i in list_of_admins:
                button = [i]
                buttons.append(button)
            buttons.append(['Домой'])
            keyboard = ReplyKeyboardMarkup(buttons, resize_keyboard=True)
            bot.send_message(message.chat.id, 'Выберите модератора, которого хотите обрадовать, он скоро станет.. админом!', reply_markup=keyboard)
            upgr = True

        elif upgr == True:
            upgr = False
            a = message.text.split('  ')
            try:
                base_w.upgrade_admin(a[0], a[1])
                bot.send_message(message.chat.id, 'Модератор удален')
                message.text = 'Домой'
                answer_questions(bot, update)
            except:
                pass


    #------------------------------------------moderators---------
    elif (message.chat.id in base_w.ids_admins()) and (base_w.is_pro_admin(message.chat.id) == 'off'):
        if message.text == 'Домой' or message.text == 'Отмена':
            add = delete_a = robber_t = disc = ph = telegr = False
            base_w.delete_none_users()
            buttons = [['Добавить мошенника']]
            keyboard = ReplyKeyboardMarkup(buttons, resize_keyboard=True)
            bot.send_message(message.chat.id, 'Привет, кого на этот раз разоблачим?', reply_markup=keyboard)


        elif message.text == 'Добавить мошенника':
            buttons = [['Домой']]
            keyboard = ReplyKeyboardMarkup(buttons, resize_keyboard=True)
            bot.send_message(message.chat.id, 'Перешлите сообщение мошенника в чат с ботом', reply_markup=keyboard)
            robber_t = True

        elif robber_t == True:
            robber_t = False
            try:
                id_ = message.forward_from.id
                username = message.forward_from.username
                base_w.add_robber_id(id_, username)
                base_w.save_nikcname(message.forward_from.first_name)
                bot.send_message(message.chat.id, 'id мошенника сохранено\nПришлите описание(без фото)')
                disc = True
            except:
                bot.send_message(message.chat.id,
                                 'Произошла ошибка, попробуйте еще раз с самого начала. Убедитесь в правильности данных')
                message.text = 'Домой'
                answer_questions(bot, update)

        elif disc == True:
            disc = False
            base_w.save_discription(message.text)
            buttons = [['Далее'],['Домой']]
            keyboard = ReplyKeyboardMarkup(buttons, resize_keyboard=True)
            bot.send_message(message.chat.id, 'Описание сохранено, можете прислать фотографии.\nЕсли их нет, нажмите на кнопку "далее"',
                             reply_markup=keyboard)
            ph = True

        elif ph == True:
            ph = False
            if message.text != 'Далее':
                try:
                    l = ''
                    for i in range(len(message.photo)):
                        l += message.photo[i].file_id + '@#$%$#@'
                    base_w.save_photo(l)
                    buttons = [['Все'],['Домой']]
                    keyboard = ReplyKeyboardMarkup(buttons, resize_keyboard=True)
                    bot.send_message(message.chat.id,
                                     'Ваши фотографии сохранены, скиньте ссылку на telegraph или нажмите "все"',
                                     reply_markup=keyboard)
                    telegr = True
                except:
                    bot.send_message(message.chat.id,
                                     'Произошла ошибка, попробуйте еще раз с самого начала. Убедитесь в правильности данных')
                    message.text = 'Домой'
                    answer_questions(bot, update)
            else:
                buttons = [['Все'], ['Домой']]
                keyboard = ReplyKeyboardMarkup(buttons, resize_keyboard=True)
                bot.send_message(message.chat.id,
                                 'Cкиньте ссылку на telegraph или нажмите "все"',
                                 reply_markup=keyboard)
                telegr = True

        elif telegr == True:
            telegr = False
            if message.text != 'Все':
                base_w.save_telegr(message.text)
            else:
                message.text = 'None'
                base_w.save_telegr(message.text)
            buttons = [['Домой']]
            keyboard = ReplyKeyboardMarkup(buttons, resize_keyboard=True)
            bot.send_message(message.chat.id,
                             'Все, готово, мошенник пойман!\nПредлагаю пойти домой!)',
                             reply_markup=keyboard)

    # ------------------------------------------moderators---------
    # ------------------------------------------users--------------
    else:
        global discr, mosh, money, call_c
        if message.text == 'Поиск мошенника🔍':
            buttons = [[InlineKeyboardButton('Поиск мошенника🔍',switch_inline_query_current_chat = '')]]
            keyboard = InlineKeyboardMarkup(buttons)
            bot.send_message(message.chat.id, 'Для продолжения нажмите на кнопку\n'+texts.search_t, reply_markup=keyboard)
        elif message.text == 'Домой' or  message.text == 'Отмена':
            base_w.statistics_plus(message.chat.id)
            discr = mosh = money = call_c =False
            buttons = [['Поиск мошенника🔍', 'Список мошенников🕵‍♂🕵‍♂🕵‍♂'],
                       ['Добавить мошенника🕵‍♂', 'Заказать возврат денег💲'], ['Связаться с нами📞']]
            keyboard = ReplyKeyboardMarkup(buttons, resize_keyboard=True)
            bot.send_message(message.chat.id, texts.hello_t, reply_markup=keyboard)
        elif message.text == 'Список мошенников🕵‍♂🕵‍♂🕵‍♂':
            all_in = base_w.all_info_robbers()
            strim = ''
            for i in range(5):
                try:
                    one = all_in[i]
                    strim += texts.content_one %(one[0], one[2], one[1], one[3]) + '\n\n'
                except:
                    break
            buttons = [[InlineKeyboardButton('◼️', callback_data='None'),InlineKeyboardButton('     1-5     ', callback_data='None'), InlineKeyboardButton('🔻', callback_data='🔻+2')]]
            keyboard = InlineKeyboardMarkup(buttons)
            bot.send_message(message.chat.id, strim,
                             reply_markup=keyboard)
        elif message.text == 'Добавить мошенника🕵‍♂':
            buttons = [['Домой']]
            keyboard = ReplyKeyboardMarkup(buttons, resize_keyboard=True)
            bot.send_message(message.chat.id, 'Перешлите сообщение мошенника в чат с ботом для определения ID (если есть)',
                             reply_markup=keyboard)
            buttons = [[InlineKeyboardButton('Нет смс от мошенника', callback_data='Нет смс от мошенника')]]
            reply_markup = InlineKeyboardMarkup(buttons)
            bot.send_message(message.chat.id, 'Если не можете, то нажмите на кнопку "Нет смс от мошенника"',
                             reply_markup=reply_markup)
            mosh = True

        elif mosh == True:
            mosh = False
            try:
                for i in base_w.ids_admins():
                    try:
                        bot.forward_message(chat_id=i, from_chat_id=message.chat.id, disable_notification=False, message_id=message.message_id)
                    except:
                        pass
                for i in constants.admins:
                    try:
                        bot.forward_message(chat_id=i, from_chat_id=message.chat.id, disable_notification=False, message_id=message.message_id)
                    except:
                        pass
                textw = 'Желательно все в одном смс.  Наш модератор все проверит, добавит его в бота и выложит на канал.'
                bot.send_message(message.chat.id, 'Пожалуйста, пришлите фото(если оно есть) с описанием мошенничества.'+ textw)
                discr = True
            except:
                bot.send_message(message.chat.id,
                                 'Произошла ошибка, попробуйте еще раз с самого начала. Убедитесь в правильности данных')
                message.text = 'Домой'
                answer_questions(bot, update)

        elif discr == True:
            for i in base_w.ids_admins():
                try:
                    bot.forward_message(chat_id=i, from_chat_id=message.chat.id, disable_notification=False,
                                        message_id=message.message_id)
                except:
                    pass
            for i in constants.admins:
                try:
                    bot.forward_message(chat_id=i, from_chat_id=message.chat.id, disable_notification=False,
                                        message_id=message.message_id)
                except:
                    pass
            if message.text != 'Отправить✅':
                buttons = [['Отправить✅']]
                keyboard = ReplyKeyboardMarkup(buttons, resize_keyboard=True)
                bot.send_message(message.chat.id, 'Вы уверены?', reply_markup=keyboard)

            elif message.text == 'Отправить✅':
                discr = False
                bot.send_message(message.chat.id,
                                 'Спасибо, за то, что помогли нам. После проверки мы добавим мошенника в базу.')
                message.text = 'Домой'
                answer_questions(bot, update)


        elif message.text == 'Заказать возврат денег💲':
            buttons = [['Домой']]
            keyboard = ReplyKeyboardMarkup(buttons, resize_keyboard=True)
            bot.send_message(message.chat.id, texts.money, reply_markup=keyboard)
            money = True

        elif money == True:
            money = False
            for i in base_w.ids_admins():
                try:
                    bot.forward_message(chat_id=i, from_chat_id=message.chat.id, disable_notification=False,
                                        message_id=message.message_id)
                except:
                    pass
            for i in constants.admins:
                try:
                    bot.forward_message(chat_id=i, from_chat_id=message.chat.id, disable_notification=False,
                                        message_id=message.message_id)
                except:
                    pass
            bot.send_message(message.chat.id, 'Наш модератор проверит информацию и мы начнем работу👌')

        elif message.text == 'Связаться с нами📞':
            buttons = [['Отмена']]
            keyboard = ReplyKeyboardMarkup(buttons, resize_keyboard=True)
            bot.send_message(message.chat.id, texts.call_city, reply_markup=keyboard)
            call_c = True

        elif call_c == True:
            call_c = False
            for i in base_w.ids_admins():
                try:
                    bot.forward_message(chat_id=i, from_chat_id=message.chat.id, disable_notification=False,
                                        message_id=message.message_id)
                except:
                    pass
            for i in constants.admins:
                try:
                    bot.forward_message(chat_id=i, from_chat_id=message.chat.id, disable_notification=False,
                                        message_id=message.message_id)
                except:
                    pass
            bot.send_message(message.chat.id, 'Я лично передам твое смс админу и в ближайшее время он с тобой свяжется👥')







def inline_caps(bot, update):
    query = update.inline_query.query
    if not query:
        return
    else:
        results = []

        if '@' not in query:
            nicks = base_w.search_by_name(str(query))
            for i in nicks:
                content = texts.content %(i[2], i[1], i[3], i[5])
                results.append(InlineQueryResultArticle(id=i[2], title=i[2], input_message_content=InputTextMessageContent(content), description=i[2]))
        else:
            nicks = base_w.search_by_un(str(query))
            for i in nicks:
                content = texts.content % (i[2], i[1], i[3], i[5])
                results.append(InlineQueryResultArticle(id=i[2], title=i[2],
                                                        input_message_content=InputTextMessageContent(content),
                                                        description=i[2]))

        try:
            if results != []:
                bot.answer_inline_query(update.inline_query.id, results)
            else:
                results.append(InlineQueryResultArticle(id='None', title='None', input_message_content=InputTextMessageContent('Ничего не найдено\n/start'), description='Ничего не найдено'))
                bot.answer_inline_query(update.inline_query.id, results)
        except:
            pass



def button_ans(bot, update):
    query = update.callback_query
    if '🔻' in str(query.data):
        list_is = int(str(query.data).split('+')[1])
        all_in = base_w.all_info_robbers()
        strim = ''
        for i in range(5):
            try:
                one = all_in[i + (5 * (list_is-1))]
                strim += texts.content_one % (one[0], one[2], one[1], one[3]) + '\n\n'
            except:
                break

        if strim != '':
            buttons = [[InlineKeyboardButton('🔺', callback_data='🔺+' + str(list_is-1)),
                        InlineKeyboardButton('     %s-%s     ' % (str((list_is * 5 - 4)), str((list_is) * 5)),
                                             callback_data='None'),
                        InlineKeyboardButton('🔻', callback_data='🔻+' + str(list_is + 1))]]
            keyboard = InlineKeyboardMarkup(buttons)
            bot.edit_message_text(message_id=query.message.message_id, chat_id=query.message.chat.id, text=strim,
                                  reply_markup=keyboard)
        else:
            buttons = [[InlineKeyboardButton('🔺', callback_data='🔺+' + str(list_is - 1))]]
            keyboard = InlineKeyboardMarkup(buttons)
            strim = 'Больше мошенников пока нет'
            bot.edit_message_text(message_id=query.message.message_id, chat_id=query.message.chat.id, text=strim,
                                  reply_markup=keyboard)


    elif '🔺' in str(query.data):
        list_is = int(str(query.data).split('+')[1])
        if list_is != 1:
            all_in = base_w.all_info_robbers()
            strim = ''
            for i in range(5):
                try:
                    one = all_in[i + 5 * (list_is-1)]
                    strim += texts.content_one % (one[0], one[2], one[1], one[3]) + '\n\n'
                except:
                    break

            if strim != '':
                buttons = [[InlineKeyboardButton('🔺', callback_data='🔺+' + str(list_is-1)),
                            InlineKeyboardButton('     %s-%s     ' % (str(((list_is-1) * 5) + 1), str((list_is) * 5)),
                                                 callback_data='None'),
                            InlineKeyboardButton('🔻', callback_data='🔻+' + str(list_is + 1))]]
                keyboard = InlineKeyboardMarkup(buttons)
                bot.edit_message_text(message_id=query.message.message_id, chat_id=query.message.chat.id, text=strim,
                                      reply_markup=keyboard)
            else:
                buttons = [[InlineKeyboardButton('🔺', callback_data='🔺+' + str(list_is - 1))]]
                keyboard = InlineKeyboardMarkup(buttons)
                strim = 'Больше мошенников пока нет'
                bot.edit_message_text(message_id=query.message.message_id, chat_id=query.message.chat.id, text=strim,
                                      reply_markup=keyboard)
        else:
            all_in = base_w.all_info_robbers()
            strim = ''
            for i in range(5):
                try:
                    one = all_in[i]
                    strim += texts.content_one % (one[0], one[2], one[1], one[3]) + '\n\n'
                except:
                    break
            buttons = [[InlineKeyboardButton('◼️', callback_data='None'),
                        InlineKeyboardButton('     1-5     ', callback_data='None'),
                        InlineKeyboardButton('🔻', callback_data='🔻+2')]]
            keyboard = InlineKeyboardMarkup(buttons)
            bot.edit_message_text(message_id=query.message.message_id, chat_id=query.message.chat.id, text=strim,
                                  reply_markup=keyboard)

    elif str(query.data) == 'Нет смс от мошенника':
        global mosh,discr
        mosh = False

        textw = 'Чтобы добавить мошенника, пришли его имя, юзернейм (если есть), описание мошенничества и пруфы в виде фото. Желательно все в одном смс.  Наш модератор все проверит, добавит его в бота и выложит на канал.'
        bot.send_message(query.message.chat.id, textw)
        discr = True


def daily_job(bot, update, job_queue):
    t = datetime.time(00,00,00,00)
    job_queue.run_daily(base_w.clear_stat(),t,days=tuple(range(6)))

updater.dispatcher.add_handler(CommandHandler('clearstat', daily_job, pass_job_queue=True))
inline_caps_handler = InlineQueryHandler(inline_caps)
dispatcher.add_handler(inline_caps_handler)
start_handler = CommandHandler('start', start)
answer_handler = MessageHandler(Filters.all, answer_questions)
updater.dispatcher.add_handler(CallbackQueryHandler(button_ans))
dispatcher.add_handler(start_handler)
dispatcher.add_handler(answer_handler)
updater.start_polling(timeout=5, clean=True)