rm -f flem.service || true
cat <<EOF >>./flem.service
[Unit]
Description=FLEM Tool
After=network.service

[Service]
Type=simple
Restart=always
WorkingDirectory=$PWD/src
Environment=PYTHONUNBUFFERED=1
ExecStart=$(which python) -m flem run
KillSignal=SIGINT

[Install]
WantedBy=default.target
EOF

if [ ! -d ~/.config/systemd/user ]; then
    mkdir -p ~/.config/systemd/user
fi

if [ -f ~/.config/systemd/user/flem.service ]; then
    systemctl --user stop flem
fi

cp flem.service ~/.config/systemd/user/
systemctl --user daemon-reload
systemctl --user enable flem
