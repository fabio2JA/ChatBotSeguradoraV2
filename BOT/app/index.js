import { create, ev } from '@open-wa/wa-automate';
import express from 'express';
import cors from 'cors';

import sendQrCode from './qrCode.js';
import sendStatus from './status.js';
import messageHandler from './messageHandler.js';


var client;
var serverStatus = 'offline';
var qrCode;
global.serverStatus = 'offline';

const app = express();

ev.on('qr.**', async qrcode => {
    global.qrCode = qrcode;
});

app.use(cors({
    origin: '*'
}));
app.use(express.json());

app.get('/', (req, res) => {
    global.qrCode = null;
    global.serverStatus = 'restarting'
    restartService(res);
});

app.get('/server-status/', (req, res) => {
    if (global.serverStatus === 'restarting') {
        sendQrCode(res, global.qrCode);
    } else {
        res.send(global.serverStatus);
    }
});

app.post('/status/', (req, res) => {
    sendStatus(req, global.client);
});

app.listen(3000);

async function restartService(res) {
    if (global.client !== undefined && global.client !== null) {
        await exit();
    }


    setTimeout(() => {
        try {
            create({
                sessionId: "COVID_HELPER",
                multiDevice: true,
                authTimeout: 60,
                blockCrashLogs: true,
                disableSpins: true,
                headless: true,
                hostNotificationLang: 'PT_BR',
                logConsole: false,
                popup: true,
                qrTimeout: 0,
                deleteSessionDataOnLogout: true,
                killClientOnLogout: true,
                useChrome: true,
                multiDevice: false
            }).then(client => start(client));
        } catch (e) {
            global.serverStatus = 'offline';
            res.send("offline");
            return;
        }
    
        res.send("restarting");
    }, 5000);
}

function start(client) {
    global.serverStatus = 'online';

    global.client = client;
    client.onMessage(async message => {
        if (!message.fromMe && !message.isGroupMsg && !message.isGroupJoinRequest && !message.isForwarded) {
            messageHandler(message, client);
        }
    });
}

async function exit() {
    await global.client.logout();
    global.client = null;
}