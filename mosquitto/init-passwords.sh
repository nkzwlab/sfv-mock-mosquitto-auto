#!/bin/sh
set -e

# カンマ区切りをスペース区切りに変換
USERS_LIST=$(echo "$MQTT_USERS" | tr ',' ' ')
PWS_LIST=$(echo "$MQTT_PASSWORDS" | tr ',' ' ')

# passwordfile をクリア
:> /mosquitto/config/passwordfile

# 要素数チェック
USER_COUNT=$(echo "$USERS_LIST" | wc -w)
PW_COUNT=$(echo "$PWS_LIST" | wc -w)
if [ "$USER_COUNT" -ne "$PW_COUNT" ]; then
  echo "ERROR: MQTT_USERS($USER_COUNT) and MQTT_PASSWORDS($PW_COUNT) length mismatch" >&2
  exit 1
fi

# ユーザーごとに対応するパスワードを切り出して追加
i=1
for user in $USERS_LIST; do
  pw=$(echo "$PWS_LIST" | cut -d' ' -f"$i")
  echo "Adding user '$user'..."
  mosquitto_passwd -b /mosquitto/config/passwordfile "$user" "$pw"
  i=$((i + 1))
done

# ブローカー起動
exec mosquitto -c /mosquitto/config/mosquitto.conf
