import { STATUS_REQS } from "./messageHandler.js";

export default function sendStatus(req, client) {
    const number = req.body ? req.body['number'] : null;
    const status = req.body ? req.body['status'] : '';
    if (client !== undefined && number !== null) {
      const newStatus = status === 'FL' ? STATUS_REQS[0] : STATUS_REQS[1];
      client.sendText(number, newStatus);
    }
}