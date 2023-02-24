# qbSat
(This is just an open source repository of this project. If you're missing something try looking through that google drive folder!)
https://drive.google.com/drive/folders/1lZ9XqQMQym47-QnI0wTRByQIBBrD96q0?usp=share_link
## What is qbSat?
qbSat is a mock CubeSat made to teach students the basics of electronics, programming and aerospace in a fun and engaging way! It is a data recording device in the standard CubeSat 1U form factor (10x10x10cm) with both an infrared and visible light camera along with gas, light, and humidity sensors. With custom software, the qbSat can record hours of video from a high altitude balloon or drone. It also has a a built in web interface to see results in real-time (while in Wi-Fi range) and download your recordings.
## Instructions
To make qbSat as easy to understand as possible, we have two forms of instructions. First, we have a video that goes step by step and we also have a set of blueprints.
Link to the tutorial video: https://drive.google.com/file/d/1Izh1XlA06eLax3tzyeJNxBDGkGyG3-vo/view
![11 x 8 5 QbSat Blueprint](https://user-images.githubusercontent.com/22381811/221193780-92b49793-24f9-4d43-9f08-1b9b5e06ef61.png)
![11 x 8 5 QbSat Blueprint(1)](https://user-images.githubusercontent.com/22381811/221193846-ac492ebb-d552-4794-8656-11733ee3a22d.png)
## Parts List
The qbSat uses entirely COTS (Commerical off the shelf parts). However, due to recent supply chain shortages you may need to find alternate parts.
You must have access to: *An internet connection (only to download software), a  3D printer & filament, a soldering iron & Solder, a phillips head screwdriver, a Windows, Chromebook or Mac computer with Wi-fi and an SD card slot.*
### (Quantity, Name, Price, Where to buy)
- 19 | Short female to male jumper cables | $8.99 [Link](https://www.amazon.com/SinLoon-Breadboard-Arduino-Circuit-40-Pack/dp/B08M3QLL3Q/ref=sr_1_13?keywords=male+to+female+jumper+wires&qid=1643724251&sr=8-13)
- 16 | 6 - 32 Machine Screws | $1.86 [Link](https://www.amazon.com/Prime-Line-9003018-Machine-Phillips-Combination/dp/B074ZWNSFY/ref=sr_1_8?crid=23R9O7Q5KTG2&keywords=Screws&pd_rd_r=c1381165-4449-467e-86ec-1d006f4903be&pd_rd_w=FWSCb&pd_rd_wg=597NE&pf_rd_p=b4950e17-f2f6-494c-bba5-69a9d0aa3887&pf_rd_r=AKS50KGXAZCM7RRYCZG9&pid=kD6IyXH&qid=1644586593&refinements=p_n_feature_twenty-eight_browse-bin%3A19043647011&s=industrial&sprefix=6+-+32+machine+screws%2Caps%2C104&sr=1-8)
- 12 | 4 - 40 Machine Screws | $7.99 [Link](https://www.amazon.com/Available-Machine-Phillips-Stainless-Fastener/dp/B07ZHBXG57/ref=sr_1_8?crid=9K9RSKYNKWYV&keywords=4-40+screws&qid=1643724443&sprefix=4-40+screws%2Caps%2C101&sr=8-8)
- 9 | Long female to male jumper cables | $5.49 [Link](https://www.amazon.com/GenBasic-Piece-Female-Jumper-Wires/dp/B077N5RLHN/ref=sr_1_6?crid=2W70SZSSWARQB&keywords=female+to+male+jumper+wires&qid=1644586108&sprefix=female+to+male+jumper+wires%2Caps%2C144&sr=8-6)
- 8 | M2.5 Screws | $11.49 [Link](https://www.amazon.com/uxcell-Phillips-Fasteners-Laptop-Switch/dp/B08J3BDGKH/ref=sr_1_16?crid=2WNZ0XA8BDVZE&keywords=M2.5%2Bscrews&qid=1643724575&s=electronics&sprefix=m2.5%2Bscrews%2Celectronics%2C93&sr=1-16&th=1)
- 3 | Male to male jumper cables | $6.29 [Link](https://www.amazon.com/DIUSTOU-Breadboard-Jumper-Multicolored-Dupont/dp/B0953K343X/ref=sr_1_13?crid=TUUP6WP4V0QT&keywords=male+to+male+jumper+wires+10+cm&qid=1644586332&sprefix=male+to+male+jumper+wire+10+cm%2Caps%2C72&sr=8-13)
- 1 | 3-pin sliding switches | $7.99 [Link](https://www.amazon.com/dp/B08QJP32CH/ref=cm_sw_r_apan_i_2PSV8M2RC2SVFGTD72B2?_encoding=UTF8&psc=1)
- 1 | Raspberry Pi Camera ribbon cable | $6.29 [Link](https://www.amazon.com/A1-FFCs-Cable-Raspberry-Camera/dp/B07JWBRMNZ/ref=sr_1_3?crid=15WK2J0VWSOD3&keywords=raspberry+pi+camera+ribbon+cable+20cm&qid=1644586963&sprefix=raspberry+pi+camera+ribbon+cable+20cm%2Caps%2C84&sr=8-3)
- 1 | Double sided tape | $6.29 [Link](https://www.amazon.com/Double-Sided-Tape-Pack-Heavy/dp/B0852XL3CC/ref=sr_1_20?keywords=double+sided+tape&qid=1644587100&sprefix=Double+%2Caps%2C124&sr=8-20)
- 1 | Micro SD card (32gb+ recommended, no lower than 16gb)| $9.99 [Link](https://www.amazon.com/dp/B08GY9NYRM/ref=twister_B08KB38516?_encoding=UTF8&psc=1)
- 1 | Micro SD to full size SD card adapter (Optional) | $3.40 [Link](https://www.amazon.com/SanDisk-microSD-Memory-Adapter-MICROSD-ADAPTER/dp/B0047WZOOO/ref=sr_1_4?crid=11GX9Y684YO7X&keywords=micro+sd+card+adapter&qid=1644587247&s=electronics&sprefix=micro+sd+card+adapter%2Celectronics%2C141&sr=1-4)
- 1 | Micro USB Cable | $8.99 [Link](https://www.amazon.com/SUNGUY-3-Pack-Braided-Charging-Galaxy/dp/B07G934SJ9/ref=sr_1_3?crid=PWNNSCUZUVWF&keywords=Micro+USB+cable+1ft+data&qid=1644587294&sprefix=micro+usb+cable+1ft+dat%2Caps%2C92&sr=8-3)
- 1 | Raspberry Pi 3B or 3B+ | $35.00 [Link](https://www.adafruit.com/product/3055)
- 1 | Adafruit Lipo Charger | $19.95 [Link](https://www.adafruit.com/product/2465)
- 1 | Lithium Ion Rechargeable Battery 3.7v 2500mAh | $14.95 [Link](https://www.adafruit.com/product/328)
- 1 | Raspberry Pi Camera Module | $29.95 [Link](https://www.adafruit.com/product/3099)
- 1 | Raspberry Pi NoIR Camera | $29.95 [Link](https://www.adafruit.com/product/3099)
- 1 | Pimoroni Enviro + Air Quality | $59.12 [Link](https://shop.pimoroni.com/products/enviro?variant=31155658457171)
- 1 | Arducam Camera Duplexer | $29.99 [Link](https://www.amazon.com/Arducam-Camera-Adapter-Doubleplexer-Raspberry/dp/B07VD9XLYH/ref=sr_1_7?keywords=arducam&qid=1581185338&sr=8-7)

Total: *$289.02*
