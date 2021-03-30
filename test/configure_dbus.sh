#!/bin/bash

echo "Configuring D-bus environment"
echo 'eval "$(dbus-launch --sh-syntax)"' > /dbus.sh
# Create D-bus keyring directories
mkdir -p ~/.cache
mkdir -p ~/.local/share/keyrings
# Unlock D-bus with empty password
echo 'ps -ef | grep dbus | grep -v grep' >> /dbus.sh
echo 'eval "$(echo | gnome-keyring-daemon --unlock)"' >> /dbus.sh
# Export D-bus variables to working shell to support keyring
echo "export DBUS_SESSION_BUS_ADDRESS" >> /dbus.sh
echo "export GNOME_KEYRING_CONTROL" >> /dbus.sh
echo "export SSH_AUTH_SOCK" >> /dbus.sh

if [[ "$DEBUG" == "true" ]]; then
  echo "bash" >> /dbus.sh
else
  echo "bash -c \"nose2 -v -X --config integration_test.cfg -A 'integration'\"" >> /dbus.sh
fi

chmod 755 /dbus.sh

# shellcheck disable=SC2068
exec $@
