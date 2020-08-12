# Digital_Signature_Maker

A simple Python script to convert your messy Signature Image to clean White background and Transparent backgrond, Signature only Images which can be used on pdf's or anywhere else. 

---

### Installation And Preparation

**Install opencv and numpy**
   
    pip install -r requirements.txt
    
**Get your written signature**

Take photo of your written signature on an unruled clean sheet of paper then transfer it to your computer.

---

## Usage:
    
    python dsm.py [-h] [-a] path_to_image

    positional arguments:
        path_to_image  the path to the signature image

    optional arguments:
        -h, --help     show this help message and exit
        -a, --auto     make signature with default settings and save it

    It saves 2 images one with white background named '$path_to_image' + '_binary.png'
    And other with transparent background named named '$path_to_image' + '_trans.png'

---

### If you don't specify -a argument then:


   #### If you are in Crop mode:
      Drag mouse over the area you want to crop
      If satisfied press 'c' to crop
      If you want to reset press 'r'
      If you don't want to crop press c without selecting the area

  #### When you are in Signature maker mode: 
      Adjust lower threshold bar till only your signature is black and rest is white or close to it
      Then adjust blur bar till it is perfect
      Press 's' to save both images(binary and transparent)
      Or Press 'r' to reset taskbar to default values
      If you don't want to save Then press 'q' or 'x' button on GUI
