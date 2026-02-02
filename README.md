# IceGods Sovereign Store Bot
Digital store for WhatsApp, Facebook, and Instagram accounts.

## Deployment to Render
1. Create a Web Service on Render.
2. Connect your GitHub repo.
3. Add Environment Variables from `.env.example`.
4. Use Build Command: `pip install -r requirements.txt`
5. Use Start Command: `gunicorn main:app`
