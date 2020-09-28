import supervisor
import time

print( "listening..." )

while True:
    print( "going on" )
    time.sleep( 1 )
    if supervisor.runtime.serial_bytes_available:
        value = input().strip()
        # Sometimes Windows sends an extra (or missing) newline - ignore them
        if value != "":
            print("RX: {}".format(value))
