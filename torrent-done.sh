#! /bin/bash
{

/usr/bin/python /var/lib/transmission-daemon/scripts/torrent-done.py "$TR_TORRENT_DIR" "$TR_TORRENT_NAME" "$TR_TORRENT_ID"

} &
