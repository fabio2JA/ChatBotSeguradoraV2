export default function sendQrCode(res, qrCode) {
    if (qrCode === null || qrCode === undefined) {
        res.send('restarting');
    } else {
        res.send(qrCode);
    }
}