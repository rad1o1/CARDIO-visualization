'raspivid -o - -t 0 -w 640 -h 480 -fps 24 | cvlc -vvvv stream:///dev/stdin --sout '#standard{access=http,mux=ts,dst=:8080}' :demux=h264 --http-host=169.254.235.60'
import subprocess


command = ["raspivid -o - -t 0 -w 1920 -h 1080 -fps 30", "| cvlc -vvvv stream:///dev/stdin --sout '#standard{access=http,mux=ts,dst=:8080}' :demux=h264 --http-host=169.254.235.60"]
result = subprocess.run(command, capture_output=True, text=True)
# Print the output
print("Output:", result.stdout)
print("Error:", result.stderr)
print("Return code:", result.returncode)