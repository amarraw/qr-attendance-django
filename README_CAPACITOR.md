Capacitor wrapper — QR Attendance

This guide shows how to create a native wrapper (Android/iOS) with Capacitor, test with ngrok during development, and use the native Camera plugin to reliably capture images and decode QR codes with ZXing.

Prerequisites
- Node.js and npm
- Java JDK + Android Studio (for Android builds)
- Xcode (on macOS, for iOS builds)
- ngrok (optional, recommended for dev HTTPS)

1) Install Capacitor dependencies
Open PowerShell in project root and run:

```powershell
npm install
# If you didn't run npm install yet, this will install @capacitor/core, @capacitor/cli and @capacitor/camera
```

2) Initialize Capacitor (if not done via script)

```powershell
npx cap init qr_attendance_app com.example.qrattend --web-dir=public
```

Notes:
- `webDir` is `public` by default in this scaffold. For a Django-served app you can optionally point Capacitor to a static build folder.
- For dev you can use an HTTPS tunnel (ngrok) and instruct Capacitor to load that URL (see step 4).

3) Dev with ngrok (recommended)

```powershell
# make Django listen on all interfaces so ngrok can reach it
python manage.py runserver 0.0.0.0:8000
ngrok http 8000
```

Copy the HTTPS URL shown by ngrok (e.g. `https://abcd-12-34-56.ngrok.io`).

4) Configure Capacitor to use dev server (optional)
Edit `capacitor.config.json` and add your ngrok URL under `server.url`:

```json
"server": { "url": "https://abcd-12-34-56.ngrok.io" }
```

This makes the native app load your live site during development.

5) Add platforms and sync

```powershell
npx cap add android
npx cap add ios
npx cap sync
```

6) Open native project and run

```powershell
npx cap open android
# or
npx cap open ios
```

Build and run in Android Studio / Xcode. If you used `server.url` with ngrok, the WebView will load the live site. For production remove server.url and put a static build in `public/`.

7) Camera plugin usage (example)
- Install plugin and sync:

```powershell
npm install @capacitor/camera
npx cap sync
```

- Example capture+decode logic (see `capacitor-camera-sample.js`): it uses `Camera.getPhoto()` to capture an image, then decodes the QR with ZXing `decodeFromImageElement`.

8) Platform permissions
- Android: ensure `android/app/src/main/AndroidManifest.xml` contains:

```xml
<uses-permission android:name="android.permission.CAMERA" />
```

- iOS: add to `Info.plist`:

```xml
<key>NSCameraUsageDescription</key>
<string>Camera required to scan student QR codes</string>
```

9) Notes & tips
- For best reliability on iOS, prefer native capture + decode (use Capacitor Camera + ZXing decode) rather than relying on WebView getUserMedia.
- Use `npx cap copy` and `npx cap sync` after updating web files.
- Replace icons with app icons for Play Store / App Store before publishing.

10) Example quick workflow (dev)

```powershell
# Terminal 1 (django)
python manage.py runserver 0.0.0.0:8000
# Terminal 2 (ngrok)
ngrok http 8000
# Terminal 3
npm install
npx cap init qr_attendance_app com.example.qrattend --web-dir=public
npx cap add android
npx cap add ios
# edit capacitor.config.json server.url to ngrok HTTPS URL
npx cap sync
npx cap open android
```

If you want, I can:
- Set `capacitor.config.json.server.url` for you if you paste your ngrok URL (I'll update the file).
- Add a small "Open on this device" QR generator in the admin panel to make opening the ngrok HTTPS URL on mobile trivial.
- Integrate `capacitor-camera-sample.js` into `attendance_admin/templates/adminpanel/scanner.html` UI (add a "Capture (native)" button visible only when the Capacitor Camera plugin is available).

Which of the above would you like me to do next?
