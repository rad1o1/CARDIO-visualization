'raspivid -o - -t 0 -w 640 -h 480 -fps 24 | cvlc -vvvv stream:///dev/stdin --sout '#standard{access=http,mux=ts,dst=:8080}' :demux=h264 --http-host=169.254.235.60'
