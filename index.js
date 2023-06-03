const { Client } = require('whatsapp-web.js');
const qrcode = require('qrcode-terminal');
const client = new Client();

let database = {
    wfgame: false,
    selection: false,
    wolf: {
        number: null,
        username: null
    },
    players: [],
    playersData: [],
    killed: [],
    numbers: [],
    night: false,
    lastDiscussion: null,
    discussionEnd: null,
    choosen: []
}

function findMode(arr) {
    if (arr.length === 0) {
      return false;
    }
    const frequencyCounter = {};
    for (let num of arr) {
      frequencyCounter[num] = (frequencyCounter[num] || 0) + 1;
    }
    let maxFrequency = 0;
    for (let key in frequencyCounter) {
      if (frequencyCounter[key] > maxFrequency) {
        maxFrequency = frequencyCounter[key];
      }
    }
    const modes = [];
    for (let key in frequencyCounter) {
      if (frequencyCounter[key] === maxFrequency) {
        modes.push(Number(key));
      }
    }
  
    if (modes.length === Object.keys(frequencyCounter).length) {
      return false;
    }
  
    return modes;
  }

client.on('qr', (qr) => {
    qrcode.generate(qr, function (qrcode) {
    console.log(qrcode);
    });
});

client.on('disconnected', (reason) => {
    console.log('Disconnected, reason: '+ reason)
})

client.on('ready', async () => {
    console.log('Client is ready!');
});

client.on('message_create', async msg => {
    if (database.wfgame === true) {
        if (typeof database.lastDiscussion === 'number' && database.lastDiscussion <= Date.now()) {
            await msg.reply('DISCUSSION TIME!!')
            await msg.reply('Choose the wolf, use the ?wrchoose <username>!')
            database.discussionEnd = Date.now() + 60000
            await msg.reply('1 minute until the discussion end.')
            return;
        }
        if (typeof database.discussionEnd === 'number' && database.discussionEnd <= Date.now()) {
            await msg.reply("DISCUSSION TIMES UP!")
            if (database.choosen.length < 1) {
                await msg.reply("No one ejected, (Noone vote)")
                await msg.reply("NIGHT COMES!!!")
                await msg.reply('Waiting until morning!')
                database.night = true
                database.lastDiscussion = Date.now() + 60000
                return;
            }
            let result = findMode(database.choosen)
            if (result.length > 1) {
                await msg.reply("No one ejected, (tie)")
                await msg.reply("NIGHT COMES!!!")
                await msg.reply('Waiting until morning!')
                database.night = true
                database.lastDiscussion = Date.now() + 60000
                return;
            }
            let wolf = result[0]
            if (database.wolf.username === wolf) {
                await msg.reply('CORRECT! WOLF FOUNDED, THE WOLF WAS ' + wolf)
                await msg.reply('Ending game...')
                database = {
                    wfgame: false,
                    selection: false,
                    wolf: {
                        number: null,
                        username: null
                    },
                    players: [],
                    playersData: [],
                    killed: [],
                    numbers: [],
                    night: false,
                    lastDiscussion: null,
                    discussionEnd: null,
                    choosen: []
                }
                return;
            }
        }
    }
    if (msg.body === '?ping') {
        console.log(msg);
        await msg.reply('pong');
        await msg.react('🥶');
    } else if (msg.body === '?deez') {
        await msg.reply('nut');
    } else if (msg.body === "wa.me/settings" || msg.body === "Wa.me/settings") {
        await msg.delete(true);
    } else if (msg.body.startsWith("?howgay")) {
        if (msg.body.split(' ').length <= 1) {
            let random = Math.floor(Math.random() * 101);
            await msg.reply(`@${msg.author} is ${random}% gay!`)
            return;
        } else {
            let user = msg.body.slice(8);
            let random = Math.floor(Math.random() * 101);
            await msg.reply(`${user} is ${random}% gay!`);
            return;
        }
    } else if (msg.body.startsWith('?8ball')) {
        if (!msg.body.split(' ')[1]) {
            await msg.reply('Please enter your question!')
            return;
        }
        let question = msg.body.slice(7);
        if (question === "apakah mickolay gay") {
            await msg.reply('tentu saja')
            return;
        }
        let responses = [
            "Ya", "Tidak", "Mungkin", "Pastinya", "Sepertinya tidak", "Tentu saja", "Harusnya tidak", "Harusnya", "Tentu saja tidak"
        ]
        let randomResponseNumber = Math.floor(Math.random() * (responses.length + 1))
        await msg.reply(`
Pertanyaan: ${question}
Jawaban: ${responses[randomResponseNumber - 1]}
        `)
    } else if (msg.body.startsWith('?echo')) {
        await msg.reply(msg.body.slice(7))
    } else if (msg.body.startsWith('?kapel')) {
        if (!msg.body.split(' ')[1]) {
            await msg.reply('Please enter your couples!')
            return;
        }
        let couples = msg.body.slice(7)
        if (couples.split(',').length <= 1) {
            await msg.reply('The couples must be 2, split it using comma')
            return
        }
        let couplesArray = couples.split(',')
        let meter = Math.floor(Math.random() * 101)
        await msg.reply(`
${couplesArray[0]} ❤️ ${couplesArray[1]}
*${meter}%*
        `)
    } else if (msg.body.startsWith('?wrcreate')) {
        if (database.wfgame === true) {
            await msg.reply('The game is already start.')
            return;
        }
        if (!msg.body.split(' ')[1]) {
            await msg.reply('You must include your username')
            return;
        }
        database.selection = true;
        database.players.push(msg.body.slice(9).toLowerCase())
        database.playersData.push({
            name: msg.body.slice(9).toLowerCase(),
            number: msg.author
        })
        database.numbers.push(msg.author)
        await msg.reply('Starting the game...')
        await msg.reply('Done. Use ?wrjoin <username> to join')
        await msg.reply('Current players: ' + database.players)
    } else if (msg.body.startsWith('?wrjoin')) {
        if (database.wfgame === true) {
            await msg.reply('The game is already start.')
            return;
        }
        if (database.selection === false) {
            await msg.reply('There is no current game.')
            return;
        }
        if (!msg.body.split(' ')[1]) {
            await msg.reply('You must include your username')
            return;
        }
        let username = msg.body.slice(8).toLowerCase()
        if (database.players.includes(username)) {
            await msg.reply('You already joined the game.')
            return;
        }
        if (database.numbers.includes(msg.author)) {
            await msg.reply('You already joined the game.')
            return;
        }
        database.players.push(msg.body.slice(8).toLowerCase())
        database.playersData.push({
            name: msg.body.slice(8).toLowerCase(),
            number: msg.author
        })
        database.numbers.push(msg.author)
        await msg.reply("You are in the game now.")
        await msg.reply('Current players ' + database.players)
    } else if (msg.body.startsWith('?wrstart')) {
        if (database.wfgame === true) {
            await msg.reply('The game is already start.')
            return;
        }
        if (database.selection === false) {
            await msg.reply('There is no current game.')
            return;
        }
        // if (database.players.length <= 2) {
        //     await msg.reply('At least, werewolf game needs 3 players.')
        //     return;
        // }
        if (!database.numbers.includes(msg.author)) {
            await msg.reply('You\'re not in this game, you must join it first using ?wrjoin <username>')
            return;
        }
        database.wfgame = true
        await msg.reply('Starting a game...')
        await msg.reply('Choosing a wolf.. ')
        let wolf = database.numbers[Math.floor(Math.random() * database.players.length)]
        database.wolf = {
            number: wolf,
            username: database.playersData.find(x => x.number === wolf).name.toLowerCase()
        }
        await msg.reply('Wolf finded. Look at your DMs!')
        client.sendMessage(wolf, "You are the wolf!!")
        await msg.reply('Discussion starting. You can discuss who\'s the wolf from now')
        database.lastDiscussion = Date.now() + 60000
    } else if (msg.body.startsWith('?wrchoose')) {
        if (!msg.body.split(' ')[1]) {
            await msg.reply('You must enter a username. Current players: ' + database.players)
            return;
        }
        let wolfChoose = msg.body.slice(10)
        if (!database.players.includes(wolfChoose.toLowerCase())) {
            await msg.reply('Username not found. Current players: ' + database.players)
            return;
        }
        let number = database.playersData.find(x => x.name === wolfChoose.toLowerCase())
        if (msg.author === number) {
            await msg.reply("Are you stupid?")
            return;
        }
        database.choosen.push(wolfChoose.toLowerCase())
        await msg.reply('Cool, you voted for ' + wolfChoose.toLowerCase())
    } else if (msg.body === "?data") {
        msg.reply(`
Started: ${database.wfgame}
Selection; ${database.selection}
Wolf: ${database.wolf.number}
WolfName: ${database.wolf.username}
Players: ${database.players}
PlayersData: ${database.playersData}
Killed: ${database.killed}
Numbers: ${database.numbers}
Night: ${database.night}
LastDisscussion: ${database.lastDiscussion}
        `)
        msg.reply(msg.author)
        console.log(msg.author)
        console.log(database)
    }
}); 

client.initialize();