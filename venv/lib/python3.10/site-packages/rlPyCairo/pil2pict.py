__all__ = (
        'pil2pict',
        )
headerLen=512
maxLen = 127    #maximum length for raw/rle

#Opcodes
picVersion=0x11
background=0x1b
headerOp=0x0C00
clipRgn=0x01
PackBitsRect=0x98
EndOfPicture=0xFF
MAXCOLORS=256

def pil2pict(cols, rows, pixels, palette, tc=-1):
    from struct import pack as struct_pack
    from io import BytesIO
    npixels = len(pixels)
    colors = len(palette)

    __bs__ = BytesIO()  #where we write the bytes
    def putc(c):
        __bs__.write(c)

    def putFill(n):
        __bs__.write(n*b'\x00')

    def putShort(v):
        __bs__.write(struct_pack('>H',v))

    def putLong(v):
        __bs__.write(struct_pack('>l',v))

    def putRect(s0, s1, s2, s3):
        putShort(s0)
        putShort(s1)
        putShort(s2)
        putShort(s3)

    colors //= 3

    # write the header 
    putFill(headerLen)

    # write picSize and picFrame 
    putShort(0) #will be overridden when we know it
    putRect(0, 0, rows, cols)

    # write version op and version 
    putShort(picVersion)
    putShort(0x02FF)
    putShort(headerOp)
    putLong(-1)
    putRect(72, 0, 72, 0)   #h/v resolutions
    putRect(cols, 0, rows, 0)
    putFill(4)

    # seems to be needed by many PICT2 programs 
    putShort(0x1e)  #DefHilite
    putShort(clipRgn)
    putShort(10)
    putRect(0, 0, rows, cols)
    if tc!=-1:
        putShort(background)
        putShort((((tc>>16)&0xFF)*65535)//255)
        putShort((((tc>>8)&0xFF)*65535)//255)
        putShort(((tc&0xFF)*65535)//255)
        putShort(5)                 #src mode
        putShort(36|64)
        putShort(8)                 #src mode
        putShort(36|64)

    # write picture 
    putShort(PackBitsRect)
    putShort(cols | 0x8000)
    putRect(0, 0, rows, cols)
    putShort(0) # pmVersion 
    putShort(0) # packType 
    putLong(0)  # packSize 
    putRect(72, 0, 72, 0)   # hRes/vRes 
    putShort(0) # pixelType 
    putShort(8) # pixelSize 
    putShort(1) # cmpCount 
    putShort(8) # cmpSize 
    putLong(0)  # planeBytes 
    putLong(0)  # pmTable 
    putLong(0)  # pmReserved 
    putLong(0)  # ctSeed 
    putShort(0) # ctFlags 
    putShort(colors-1)  # ctSize 

    #Write out the colormap
    for i in range(colors):
        putShort(i)
        putShort((palette[3*i]*65535)//255)
        putShort((palette[3*i+1]*65535)//255)
        putShort((palette[3*i+2]*65535)//255)

    putRect(0, 0, rows, cols)       #srcRect
    putRect(0, 0, rows, cols)       #dstRect
    putShort((36|64) if tc!=-1 else 0)          #transfer mode

    #write out the pixel data.
    oc = 0
    d = bytearray()
    r = bytearray()
    r_append = r.append
    r_extend = r.extend
    r_reverse = r.reverse
    cols1 = cols - 1
    if cols>=250:
        putRLen = putShort
        rli = 2
    else:
        putRLen = lambda c: putc(bytes([c]))
        rli = 1

    rtc = lambda c: 257-c   #run to char
    ctc = lambda c: c-1     #count to char

    def endrun():
        nonlocal run, count
        if run < 3:
            while run>0:
                r_append(cb)
                run -= 1
                count += 1
                if count==128:
                    r_append(127)
                    count -= 128
            run = 1
        else:   #cb!=d[k] and r>=3
            if count>0:
                r_append(ctc(count))
            count = 0
            while run>0:
                rep = 128 if run > 128 else run
                r_append(cb)
                r_append(rtc(rep)&0xff)
                run -= rep
            run = 1

    for j in range(rows):
        j0 = j*cols #first byte in our pixel data
        d[:] = bytearray(pixels[j0:j0+cols])
        r[:] = bytearray()
        run = count = 0
        k = cols1   #our pointer
        cb = d[-1]  #current byte
        i = cols1
        while i>=0:
            #work backwards through the columns of this row
            if cb == d[k]:
                run += 1    #just increase the run
            else:
                endrun()
            i -= 1
            cb = d[k]
            k -= 1

        endrun()
        if count>0:
            r_append(ctc(count))

        pc = len(r)
        oc += pc+rli
        putRLen(pc)
        r_reverse()
        __bs__.write(bytes(r))

    if oc & 1: putc(b'\x00')    #pad to even number of bytes
    putShort(EndOfPicture)

    lb = __bs__.tell()
    lp = lb - headerLen
    __bs__.seek(headerLen)
    putShort(lp & 0xffff)   #put picture size at the end of the header
    return __bs__.getvalue()
