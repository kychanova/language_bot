Данный бот предназначен для изучения английского
языка. При вызове команды /send_article бот парсит 
статью (пока только с сайта The Conversation); 
суммаризует её. Поскольку в этом проекте очень
важно соблюдение грамматических норм, была выбрана
экстрактивная суммаризация. Также очень важна 
скорость, по этой причине существующие модели
на основе BERTa не подошли и был использован
TextRank. 

На основе суммаризованной статьи формируются 
вопросы. Для этого была дообучена модель
T5-BASE с новым префиксом: "questgen:". Модель 
дообучена на SQUADe, поэтому для формирования 
ответов (в целях проверки дальнейших ответов
пользователя) была использована стандартная 
модель на основе BERT без дообучения.

Бот написан на бета версии библиотеки aiogram 3.0