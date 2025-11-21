// Capacitor Camera + ZXing sample
// Paste into your web bundle (or include as a static file) and call captureAndDecode()

import { Camera, CameraResultType, CameraSource } from '@capacitor/camera';

export async function captureAndDecode() {
  try {
    const photo = await Camera.getPhoto({
      resultType: CameraResultType.Uri,
      source: CameraSource.Camera,
      quality: 90
    });

    const imageUrl = photo.webPath || photo.path;
    if (!imageUrl) throw new Error('No image URL from Camera.getPhoto()');

    const img = new Image();
    img.crossOrigin = 'anonymous';
    img.src = imageUrl;

    img.onload = async () => {
      try {
        const codeReader = new ZXing.BrowserMultiFormatReader();
        const result = await codeReader.decodeFromImageElement(img);
        if (result) {
          // handleResult is your existing handler in scanner.js
          if (typeof handleResult === 'function') {
            handleResult(result.text);
          } else {
            console.log('Decoded QR:', result.text);
          }
        }
      } catch (err) {
        console.error('QR decode from image failed', err);
        alert('Could not decode QR code from captured image. Try again.');
      }
    };

    img.onerror = (e) => {
      console.error('Image load failed', e);
      alert('Failed to load captured image.');
    };

  } catch (e) {
    console.error('Camera error', e);
    if (e.name === 'CameraPluginNotInstalled') {
      alert('Camera plugin not installed - run "npx cap sync" and rebuild native project.');
    } else {
      alert('Camera access failed: ' + (e.message || e));
    }
  }
}
