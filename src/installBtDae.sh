sudo cp ./btSendDaemon.service /etc/systemd/system/btSendDaemon.service
sudo systemctl stop btSendDaemon.service
sudo systemctl daemon-reload
sudo systemctl enable btSendDaemon.service
sudo systemctl start btSendDaemon.service
sudo systemctl status btSendDaemon.service