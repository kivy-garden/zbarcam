# garden.zbarcam

Real time Barcode and QR Code scanner using the camera.
It's built on top of [Kivy](https://github.com/kivy/kivy) and [ZBar](https://github.com/ZBar/ZBar).

## How to use
Simply import and instanciate `ZBarCam` in your kvlang file and access its `symbols` property.
```
#:import ZBarCam zbarcam
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
pip install https://github.com/AndreMiras/garden.zbarcam/archive/develop.zip
```
You may also need to compile OpenCV2 manually and deploy `cv2.so` to your `site-packages/`.

## Credits
I borrowed a lot of code from [tito/android-zbar-qrcode](https://github.com/tito/android-zbar-qrcode).
