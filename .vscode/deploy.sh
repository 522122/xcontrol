DECKUSER="bazzite"
DECKIP="192.168.10.42"
OUT="$(pwd)/out"
PLUGINNAME="xcontrol"

scp $OUT/xcontrol.zip $DECKUSER@$DECKIP:/tmp/$PLUGINNAME.zip

ssh -t $DECKUSER@$DECKIP "sudo bash -c '\
    rm -rf /home/$DECKUSER/homebrew/plugins/$PLUGINNAME && \
    mkdir -p /home/$DECKUSER/homebrew/plugins/$PLUGINNAME && \
    unzip -o /tmp/$PLUGINNAME.zip -d /home/$DECKUSER/homebrew/plugins && \
    chown -R $DECKUSER /home/$DECKUSER/homebrew/plugins/$PLUGINNAME && \
    rm /tmp/$PLUGINNAME.zip && \
    systemctl restart plugin_loader.service
'"
