# garden.zbarcam

Real time Barcode and QR Code scanner for [Kivy](https://github.com/kivy/kivy) the camera and [ZBar](https://github.com/ZBar/ZBar).

## How to use
Simply instanciate `ZBarCam` in your kvlang file and access its `symbols` property.
```
BoxLayout:
    orientation: 'vertical'
    ZBarCam:
        id: zbarcam
    Label:
        size_y: 20
        size_hint_y: None
        text: ", ".join([str(symbol.data) for symbol in zbarcam.symbols])
```

## Install
```
pip install -r requirements/requirements.txt
```
You also need to compile OpenCV2 manually and deploy `cv2.so` to your `site-packages/`.

## Credits
I borrowed a lot of code from [tito/android-zbar-qrcode](https://github.com/tito/android-zbar-qrcode).
