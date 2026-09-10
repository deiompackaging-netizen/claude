const http = require('http');
const fs = require('fs');
const path = require('path');

const PORT = process.env.PORT || 3000;

function sendJson(res, status, data) {
  res.writeHead(status, { 'Content-Type': 'application/json' });
  res.end(JSON.stringify(data));
}

function readJson(req) {
  return new Promise((resolve, reject) => {
    let body = '';
    req.on('data', chunk => {
      body += chunk;
      if (body.length > 1000000) req.destroy();
    });
    req.on('end', () => {
      try { resolve(JSON.parse(body || '{}')); }
      catch (e) { reject(e); }
    });
    req.on('error', reject);
  });
}

const server = http.createServer(async (req, res) => {
  if (req.method === 'GET' && req.url === '/') {
    const file = fs.readFileSync(path.join(__dirname, 'public', 'index.html'));
    res.writeHead(200, { 'Content-Type': 'text/html; charset=utf-8' });
    return res.end(file);
  }

  // Demo endpoint: builds the payment request but does NOT charge a card.
  // Connect this endpoint to your authorized payment provider after configuring
  // its official API URL and credentials on your server.
  if (req.method === 'POST' && req.url === '/api/pay') {
    try {
      const input = await readJson(req);
      if (!input.googlePayToken) return sendJson(res, 400, { error: 'Google Pay token is required' });
      if (!input.amount || !input.currency) return sendJson(res, 400, { error: 'Amount and currency are required' });

      const paymentRequest = {
        amount: input.amount,
        currency: String(input.currency).toUpperCase(),
        confirm: true,
        capture_method: 'automatic',
        payment_method: 'wallet',
        payment_method_type: 'google_pay',
        payment_method_data: {
          wallet: {
            google_pay: {
              tokenization_data: {
                type: 'DIRECT',
                token: input.googlePayToken
              }
            }
          }
        }
      };

      // Intentionally return a safe demo response instead of submitting payment.
      return sendJson(res, 200, {
        mode: 'demo',
        message: 'Google Pay payload created successfully. No payment was charged.',
        paymentRequest
      });
    } catch (error) {
      return sendJson(res, 400, { error: 'Invalid request' });
    }
  }

  sendJson(res, 404, { error: 'Not found' });
});

server.listen(PORT, () => console.log(`Google Pay demo running on port ${PORT}`));
