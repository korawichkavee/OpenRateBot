# Ubuntu deployment

```bash
sudo useradd --system --create-home --home /opt/openratebot openratebot
sudo mkdir -p /opt/openratebot
sudo chown -R openratebot:openratebot /opt/openratebot
# clone/copy the repo into /opt/openratebot
cd /opt/openratebot
sudo -u openratebot python3 -m venv .venv
sudo -u openratebot .venv/bin/pip install -r requirements.txt
sudo -u openratebot cp .env.example .env
sudo -u openratebot nano .env
sudo cp deploy/openratebot.service /etc/systemd/system/openratebot.service
sudo systemctl daemon-reload
sudo systemctl enable --now openratebot
sudo systemctl status openratebot
sudo journalctl -u openratebot -f
```

For updates:

```bash
cd /opt/openratebot
sudo -u openratebot git pull
sudo -u openratebot .venv/bin/pip install -r requirements.txt
sudo systemctl restart openratebot
```
