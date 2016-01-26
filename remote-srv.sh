DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
until /usr/bin/python_root $DIR/remote-srv.py; do
	echo "Server crashed with exit code $?.  Respawning.." >&2
	sleep 1
done
