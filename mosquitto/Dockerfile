FROM eclipse-mosquitto:2.0

# パスワード初期化スクリプトをコピー
COPY mosquitto/init-passwords.sh /usr/local/bin/init-passwords.sh
RUN chmod +x /usr/local/bin/init-passwords.sh

# ブローカ設定ファイルをコピー
COPY config/mosquitto.conf /mosquitto/config/mosquitto.conf

# スクリプト実行→ブローカー起動
ENTRYPOINT ["/usr/local/bin/init-passwords.sh"]
CMD ["mosquitto"]
