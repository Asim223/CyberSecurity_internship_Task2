drive = "/dev/sdb"          # Example: USB drive or disk image path
fileD = open(drive, "rb")

size = 512                 # Sector size
byte = fileD.read(size)
offs = 0                   # Offset counter
drec = False               # Recovery mode
rcvd = 0                   # Recovered file counter

while byte:
    found = byte.find(b'\xff\xd8\xff\xe0\x00\x10\x4a\x46')
    if found >= 0:
        drec = True
        print("==== Found JPG at location:", hex(found + (size * offs)), "====")

        fileN = open(str(rcvd) + ".jpg", "wb")
        fileN.write(byte[found:])

        while drec:
            byte = fileD.read(size)
            bfind = byte.find(b'\xff\xd9')
            if bfind >= 0:
                fileN.write(byte[:bfind + 2])
                print("==== Wrote JPG to file:", str(rcvd) + ".jpg ====\n")
                fileN.close()
                rcvd += 1
                drec = False
            else:
                fileN.write(byte)

    byte = fileD.read(size)
    offs += 1

fileD.close()
