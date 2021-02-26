const dbd = require("dbd.js");

const bot = new dbd.Bot({
    token: process.env.TOKEN,
    prefix: "/"
})

bot.status({
    type: "STREAMING",
    text: "Minecraft",
    time: 12,
    url: "https://vk.com/csides"
})

bot.interactionCommand({
    name: "пинг",
    code: `$interactionReply[{title:🏓Понг!}{description:Пинг сервера $ping мс}{color:RED}]`
});
bot.interactionCommand({
    name: "шар",
    code: `
        $interactionReply[{title:«$message»}{description:$randomText[Бесспорно;Предрешено;Никаких сомнений;Определённо да;Можешь быть уверен в этом;Мне кажется — «да»;Вероятнее всего;Хорошие перспективы;Знаки говорят — «да»;Да;Пока не ясно, попробуй снова;Спроси позже;Лучше не рассказывать;Сейчас нельзя предсказать;Сконцентрируйся и спроси опять;Даже не думай;Мой ответ — «нет»;По моим данным — «нет»;Перспективы не очень хорошие;Весьма сомнительно]}{color:RED}];
    `
});
bot.interactionCommand({
    name: "запуск",
    code: `
        $interactionReply[{title:Вывод}{description:$eval[$message;no]}{color:RED}]
        $onlyForIDs[487845696100368384;{title:Вы не владелец бота!}{color:RED}]
    `
});
bot.interactionCommand({
    name: "новость",
    code: `
        $title[Новость]
        $description[$message]
        $color[#7289DA]
        $useChannel[804673463469604865]
        $onlyPerms[admin;$dm Вы не имеете прав админа!]
    `
});
bot.interactionCommand({
    name: "жалоба",
    code: `
        <@&804651446158884894> <@&804676398009679873>
        $title[Жалоба!]
        $description[<@$message[2]> нарушил правило $message[1] со следующим комментарием: $message[3]]
        $color[RED]
        $author[$username;$authorAvatar]
        $useChannel[804670060424724530]
    `
});

bot.interactionCommand({
    name: "rcon",
    code: `$djsEval[
        const Rcon = require("modern-rcon");
        const rcon = new Rcon('95.216.62.180', 28582, '5A8C3CA9757DBD9EE8')
        rcon.connect()
        .then(() => {
            return rcon.send('$message')
        })
        .then(res => {
            d.message.channel.send(res)
        })
        .then(() => {
            return rcon.disconnect()
        });]`
})

bot.onInteractionCreate()


bot.joinCommand({
    channel: "804650873074483200",
    code: `$useChannel[804650873074483200] $username зашел на сервер!`
});

bot.onJoined()
