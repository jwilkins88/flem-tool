systemctl --user stop flem
systemctl --user disable flem
rm ~/.config/systemd/user/flem.service
systemctl --user daemon-reload
