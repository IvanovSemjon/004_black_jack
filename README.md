# 004_black_jack
Блек-джек, известный также как «двадцать одно», — карточная игра, в которой игроки пытаются набрать количество очков, как можно более близкое к 21, но не больше. В данной программе используются изображения, составленные из текстовых символов, так называемая ASCII-графика. ASCII (American Standard Code for Information Interchange, американский стандартный код обмена информацией) представляет собой таблицу соответствий текстовых символов числовым кодам, она применялась до того, как ее заменила кодировка Unicode1. Игральные карты в этой программе представляют собой пример ASCII-графики:
"""
\___  \___
|A  | |10 |
| ♣ | | ♦ |
|__A| |_10|
"""
# Описание работы
Символов для мастей карт на клавиатуре нет, поэтому нам приходится вызывать chr() для их отображения. Передаваемое в chr() целое число называется кодом символа (code point) кодировки Unicode, оно представляет собой уникальное число, идентифицирующее символ в соответствии со стандартом Unicode. Unicode часто понимают неправильно. Прекрасное введение в Unicode — доклад Неда Бачхелдера (Ned Batchelder) Pragmatic Unicode, or How Do I Stop the Pain?, сделанный на конференции PyCon US 2012. Вы можете найти его по адресу https://youtu.be/sgHbC6udIqc/. В приложении Б приведен полный список символов Unicode, которые можно использовать в программах Python.
