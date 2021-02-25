const dbd = require("dbd.js");

const bot = new dbd.Bot({
    token: process.env.TOKEN,
    prefix: "/"
})
bot.status({
    type: "STREAMING",
    text: "летсплей",
    time: 12,
    url: "https://vk.com/csides"
})

bot.command({
    name: "add_eval",
    code: `$createSlashCommand[$guildID;запуск;Запуск кода(только для SNVMK);код:Код для запуска:true:3]`
})
bot.onMessage()
bot.interactionCommand({
    name: "пинг",
    code: `$interactionReply[{title:🏓Понг!}{description:Пинг сервера $ping мс}{color:RED}]`
})
bot.interactionCommand({
    name: "шар",
    code: `
        $interactionReply[{title:«$message»}{description:$randomText[Бесспорно;Предрешено;Никаких сомнений;Определённо да;Можешь быть уверен в этом;Мне кажется — «да»;Вероятнее всего;Хорошие перспективы;Знаки говорят — «да»;Да;Пока не ясно, попробуй снова;Спроси позже;Лучше не рассказывать;Сейчас нельзя предсказать;Сконцентрируйся и спроси опять;Даже не думай;Мой ответ — «нет»;По моим данным — «нет»;Перспективы не очень хорошие;Весьма сомнительно]}{color:RED}];
    `
})
bot.interactionCommand({
    name: "запуск",
    code: `$interactionReply[{title:Вывод}{description:$eval[$message;yes]}{color:RED}]`
})

bot.onInteractionCreate()


bot.joinCommand({
    channel: "804650873074483200",
    code: `$sendWebhook[804724673677623326;Hnby6pAeIAX4qXJ3UPApsOfOobcdEjDd9XsceD7xnxPN2miGZFa0axMCGlhC3TCX4r8n;Зашёл на сервер;{username:$username};{avatar:$authorAvatar}]`
})

bot.onJoined()
