const { create, Client } = require('@open-wa/wa-automate');
const puppeteer = require('puppeteer');

(async () => {
  // Inicie o navegador Puppeteer
  const browser = await puppeteer.launch();
  const page = await browser.newPage();

  // Navegue para o site do WhatsApp Web
  await page.goto('https://web.whatsapp.com/');

  // Encontre o elemento do QR code e salve o caminho da imagem
//   const qrCodeElement = await page.waitForSelector('#app > div > div > div.landing-window > div.landing-main > div > div > div > img');
//   const qrCodeImagePath = await qrCodeElement.screenshot({ path: 'qr-code.png' });
//   console.log(`QR code salvo em ${qrCodeImagePath}`);

  // Crie um cliente do WA Automate Node.js
  const client = await create({ puppeteer: { browser } });

  // Registre um evento para imprimir as mensagens recebidas
  client.onMessage((message) => {
    console.log(`Mensagem recebida: ${message.body}`);
  });
})();