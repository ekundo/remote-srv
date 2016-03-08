DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
echo "$$" > $DIR/remote-srv.pid
until /usr/bin/python $DIR/remote-srv.py; do
	echo "Server crashed with exit code $?.  Respawning.." >&2
	sleep 1
done
