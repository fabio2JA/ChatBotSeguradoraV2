export default function sendStatus(req, client) {
    const number = req.body ? `${req.body['number']}@c.us` : null;
    const status = req.body ? req.body['status'] : '';
    if (client !== undefined && number !== null) {
      client.sendText(number, status);
    }
}