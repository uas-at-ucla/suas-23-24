sudo date -s "$(wget -qSO- --max-redirect=0 google.com 2>&1 | grep Date: | cut -d' ' -f5-8)Z"
echo "Date set."
process=$(ps aux | grep gphoto2);
output=($(echo "$process" | tr ' ' '\n'))
pid="${output[1]}"
kill -9 $pid
echo "GPhoto2 Conflicting Process Killed"

