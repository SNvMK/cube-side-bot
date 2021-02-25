const dbd = require("dbd.js");

const bot = new dbd.Bot({
    token: process.env.TOKEN,
    prefix: "/"
})


bot.interactionCommand({
    name: "пинг",
    code: `$interactionReply[{title:🏓Понг!}{description:Пинг сервера $ping мс}{color:RED}]`
})


bot.onInteractionCreate()