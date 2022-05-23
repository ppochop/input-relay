In order for the script to work without `sudo`, the executing user needs to have `write` permissions on `/dev/uinput` (`setfacl -m u:<uid>:w`)

then just run `python receiver.py`