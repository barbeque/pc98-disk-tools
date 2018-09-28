if [ "$#" -ne 1 ]; then
	echo "Usage: $0 [*.hdm disk image file]"
else
	hdiutil attach -imagekey diskimage-class=CRawDiskImage "$1"
fi
