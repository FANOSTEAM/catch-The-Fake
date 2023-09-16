import qrcode
qr = qrcode.QRCode(version = 1,
                   box_size = 10,
                   border = 5)
qr.add_data("xyzh")
qr.make(fit = True)
img = qr.make_image()
img.save("qr.png")