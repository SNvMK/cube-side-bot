const dbd = require("dbd.js");

const bot = new dbd.Bot({
    token: process.env.TOKEN,
    prefix: "/"
})
bot.status({
    type: "STREAMING",
    text: "летсплей",
    url: "https://vk.com/csides"
})


bot.interactionCommand({
    name: "пинг",
    code: `$interactionReply[{title:🏓Понг!}{description:Пинг сервера $ping мс}{color:RED}]`
})

bot.interactionCommand({
    name: "шар",
    code: `
        $interactionReply[{title:«$message»};{description:$randomText[Бесспорно;Предрешено;Никаких сомнений;Определённо да;Можешь быть уверен в этом;Мне кажется — «да»;Вероятнее всего;Хорошие перспективы;Знаки говорят — «да»;Да;Пока не ясно, попробуй снова;Спроси позже;Лучше не рассказывать;Сейчас нельзя предсказать;Сконцентрируйся и спроси опять;Даже не думай;Мой ответ — «нет»;По моим данным — «нет»;Перспективы не очень хорошие;Весьма сомнительно]}{color:RED}];
    `
})


bot.onInteractionCreate()