import mime from 'mime-types';
import { decryptMedia } from '@open-wa/wa-automate';
import fs from 'fs';
import axios from 'axios';


async function enviarBoasVindas(message, client) {
    await client.sendText(message.from, 'Bem vindo sou seu assistente virtual');
    await client.sendText(message.from, 'Você pode digitar "voltar" a qualquer momento para começar a conversa novamente');
    await client.sendText(message.from, BOT_MESSAGES_KEYS[1]);
}

async function enviarCNH(message, client) {
    await client.sendText(message.from, 'Voce escolheu enviar uma cnh para nosso banco de dados');
    await client.sendText(message.from, BOT_MESSAGES_KEYS[2]);
}

async function enviarDOC(message, client) {
    await client.sendText(message.from, 'Voce escolheu enviar um documento de posse do carro para nosso banco de dados');
    await client.sendText(message.from, BOT_MESSAGES_KEYS[3]);
}

async function enviarImagemCNH(message, client) {
    const url = 'https://f-jacks-orange-space-funicular-ww5p7wvqxwrh955p-8000.preview.app.github.dev/reconhecimento/cnh/bot/'
    await enviarImagem(message, client, url, BOT_MESSAGES_KEYS[2]);

}

async function enviarImagemDOC(message, client) {
    const url = 'https://f-jacks-orange-space-funicular-ww5p7wvqxwrh955p-8000.preview.app.github.dev/reconhecimento/doc/bot/'
    await enviarImagem(message, client, url, BOT_MESSAGES_KEYS[3]);
}

async function enviarImagem(message, client, url, nextMessage) {
    if (!message.mimetype) {
        await client.sendText(message.from, 'ERROR AO ENVIAR IMAGEM');
        await client.sendText(message.from, nextMessage);
        return;
    }

    const filename = `./images/${message.from}%${message.t}.${mime.extension(message.mimetype)}`;
    const mediaData = await decryptMedia(message);

    fs.writeFile(filename, mediaData, function(err) {
        if (err) {
          console.log(err);
        }
        console.log('The file was saved!');
    });

    const file = fs.readFileSync(filename);

    const data = {
        image: file,
        image_type: mime.extension(message.mimetype),
        number: message.from
    };

    axios.post(url, data, {
        headers: {
            'Content-Type': 'multipart/form-data'
        }
    })

    fs.unlink(filename, (err) => {
        if (err) {
          console.error(err);
        }
        
        console.log('File deleted successfully!');
    });
}

const BOT_MESSAGES = {
    'boas vindas': {'_': enviarBoasVindas},
    'Qual serviço você gostaria que fosse feito?\n\n\n(1) Reconhecimento de cnh\n\n(2) Reconhecimento do documento de pose do carro': {
        '1': enviarCNH,
        '2': enviarDOC
    },
    'Por favor envie uma imagem ou pdf da sua cnh': {
        '_': enviarImagemCNH,
        'voltar': enviarBoasVindas
    },
    'Por favor envie uma imagem ou pdf do seu documento': {
        '_': enviarImagemDOC,
        'voltar': enviarBoasVindas
    },
    'Você pode aguadar o status da sua solicitação\n\nou\n\ndigite "outra" para enviar outra cnh': {
        'outra': enviarCNH,
        'voltar': enviarBoasVindas
    },
    'Você pode aguadar o status da sua solicitação\n\nou\n\ndigite "outro" para enviar outro documento de posse do carro': {
        'outro': enviarDOC,
        'voltar': enviarBoasVindas
    }
}

const BOT_MESSAGES_KEYS = Object.keys(BOT_MESSAGES);

const STATUS_REQS = [
    'Status da solicitação de reconhecimento:\n\nFALHA\n\nPor favor tente enviar um arquivo melhor ou contacte o nosso suporte',
    'Status da solicitação de reconhecimento:\n\nSUCESSO\n\nSeu documento foi reconhecido com sucesso e ja consta no nosso banco de dados'
]

export default async function messageHandler(message, client) {
    let activator;

    // const allMessages = await client.loadAndGetAllMessagesInChat(message.from, true)
    // const allMessagesFromMe = allMessages.filter(msg => msg.fromMe === true && BOT_MESSAGES_KEYS.includes(msg.body));

    // console.log(allMessages.length);
    const myLTMessage = await client.getMyLastMessage(message.from);
    const myLastMessage = myLTMessage && BOT_MESSAGES_KEYS.includes(myLTMessage.body) ? myLTMessage.body : 'boas vindas';

    const activators = Object.keys(BOT_MESSAGES[myLastMessage]);


    const msgBody = message.body.toLowerCase().split(' ');

    for (let n = 0; n < activators.length; n++) {
        const activate =  activators[n];
        if (msgBody.includes(activate)) {
            activator = activate;
            break;
        }
        if (activate === '_') {
            activator = "_";
        }
    }

    if (activator === undefined || activator === null) {
        await client.sendText(message.from, myLastMessage);
    } else {
        await BOT_MESSAGES[myLastMessage][activator](message, client);
    }
}

export { STATUS_REQS }
