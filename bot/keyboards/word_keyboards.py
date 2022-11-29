import logging

from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import types


def after_spell_check_keyboard(init_text, corrected):
    buttons = [[types.InlineKeyboardButton(
                    text="Yes, I meant this.",
                    callback_data='sr_' + corrected)],
                [types.InlineKeyboardButton(
                    text="No, I wrote what I meant.",
                    callback_data='swi_' + init_text)],
                [types.InlineKeyboardButton(
                    text="No, I'll write again",
                    callback_data=corrected)]]

    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def after_spell_check_unknown_keyboard(text):
    logging.info(f'{text=}')
    buttons = [[types.InlineKeyboardButton(
                    callback_data="rem_" + text,
                    text="Yes, remember this."),
               types.InlineKeyboardButton(
                    callback_data="pass",
                    text="No, I'll check it out")]]

    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard
