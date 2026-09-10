# Google Pay Payment Integration

This starter project shows how to pass an already-created Google Pay token to a server-side payment endpoint without storing the token in source control.

## Security

Never commit a real Google Pay payment token, API key, secret, or private credential to GitHub. Configure secrets as environment variables on the server.

## Token location

The token is expected at:

`payment_method_data.wallet.google_pay.tokenization_data.token`

## Example request shape

```json
{
  "amount": 123,
  "currency": "EUR",
  "confirm": true,
  "capture_method": "automatic",
  "payment_method": "wallet",
  "payment_method_type": "google_pay",
  "payment_method_data": {
    "wallet": {
      "google_pay": {
        "tokenization_data": {
          "type": "DIRECT",
          "token": "${GOOGLE_PAY_TOKEN}"
        }
      }
    }
  }
}
```

The project deliberately does not contain the user's real payment token. Use a secure backend and the payment provider's documented endpoint/credentials to submit the request.
