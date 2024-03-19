# Student Fee Management Tkinter-Python Kiosk

## 1. For Windows

1. Click the following link to first install python:<br>
<https://www.python.org/downloads/>

2. Clone this repository:

```bash
cd path\to\desired\directory
git clone https://github.com/kp-1208/Fee-Manager-Tkinter-Kiosk.git
```

3. Now execute the ***win_setup.bat*** file to configure the working environment and install requirements.

```bash
win_setup.bat
```

4. Finally, execute the ***win_main.py*** to run the application.
```bash
win_main.bat
```

## 2. For Linux

1. Clone this repository:

```bash
cd path\to\desired\directory
git clone https://github.com/kp-1208/Fee-Manager-Tkinter-Kiosk.git
```

2. Make the scripts ***linux_setup.sh*** and ***linux_main.sh*** executable using following commands:

```bash
chmod 777 linux_setup.sh
chmod 777 linux_main.sh
```

3. Execute the ***linux_setup.sh*** script to configure environment and install requirements:

```bash
./linux_setup.sh
```

4. Execute the ***linux_main.sh*** script to run the application:

```bash
./linux_main.sh
```
### The File Structure

<pre>
Fee-Manager-Tkinter-Kiosk
   ├── data/
   │   └── fee_details.csv
   ├── reports/
   ├── scripts/
   │   ├── index.py
   │   ├── parameters.py
   │   └── report_generator.py
   ├── static/
   │   ├── header.jpg
   │   ├── logo.png
   │   └── sign.png
   ├── linux_main.sh
   ├── linux_setup.sh
   ├── requirements.txt
   ├── win_main.bat
   └── win_setup.bat
</pre>

