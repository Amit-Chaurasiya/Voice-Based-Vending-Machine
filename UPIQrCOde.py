import pyqrcode
import png

myUPI = "upi://pay?pa=benroman1712345@okicici&pn=Amit%20Chaurasiya&am=1.00&tn=For%20Vending%20Machine&cu=INR"
qrcode = pyqrcode.create(myUPI)

qrcode.png("myUPIid.png",scale=5)