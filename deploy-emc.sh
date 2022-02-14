#!/bin/sh

print_help()
{
	echo "Usage:"
	echo "deploy-emc.sh [path] [command]"
	echo "path - path to aphy release folder;"
	echo "command - systemctl command, will be applied to aphy-host-emc.service after it's creation;"
	echo -e "\nExample:"
	echo "deploy-emc.sh ./ enable"
}

if [ "$(id -u)" -ne 0 ]; then
	echo "You need to run this script as root"
	exit 1
fi

if [ -z "$1" ] || [ -z "$2" ]; then
	echo "Incorrect usage of script"
	print_help
	exit 2
fi

if [ ! -x "$1/aphy_host" ]; then
	if [ -f "$1/aphy_host" ]; then
		chmod +x "$1/aphy_host"
		if [ "$?" -ne 0 ]; then
			echo "Failed to make $1/aphy_host executable"
			exit 3
		fi
	else
		echo "$1/aphy_host doesn't exist"
		exit 4
	fi
fi

if [ ! -f "$1/aphy-host-emc.service" ]; then
	echo "$1/aphy-host-emc.service doesn't exist"
	exit 5
fi

cp -f "$1/aphy_host" /usr/sbin/
if [ "$?" -ne 0 ]; then
	echo "Failed to copy $1/aphy_host to /usr/sbin/"
	exit 6
fi

cp -f "$1/aphy-host-emc.service" /etc/systemd/system
if [ "$?" -ne 0 ]; then
	echo "Failed to copy $1/aphy-host-emc.service to /etc/systemd/system"
	exit 7
fi

systemctl $2 aphy-host-emc.service
if [ "$?" -ne 0 ]; then
	echo "Failed to run command: systemctl $2 aphy-host-emc.service"
	exit 8
fi

echo "Done"