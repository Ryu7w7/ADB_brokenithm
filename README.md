# This application is developed to streamline the integration of Brokenithm with USB devices.
The application offers two key features: 
- The 'Detect Devices' option assists in setting up adb reverse.
- The 'Start Brokenithm Server' option opens the server interface configured with TCP for reduced latency when connected via USB.

![image](https://github.com/user-attachments/assets/e0044069-cff9-46cb-a41d-cbd4c6bf2d2d)

Simply ensure that USB debugging is enabled on your device to complete the process successfully!

# Important
You need custom IO DLL [brokenithm](https://gitea.tendokyu.moe/Dniel97/Brokenithm-Evolved/releases/tag/v0.4.0) and extract it inside App/bin
and configure your segatools.ini

```
; -----------------------------------------------------------------------------
; Custom IO settings
; -----------------------------------------------------------------------------

[aimeio]
; To use a custom card reader IO DLL enter its path here.
; Leave empty if you want to use Segatools built-in keyboard input.
path=aime_brokenithm.dll

[chuniio]
; Uncomment this if you have custom chuniio implementation comprised of a single 32bit DLL.
; (will use chu2to3 engine internally)
;path=

; Uncomment this if you have custom chuniio implementation.
; x86 chuniio to path32, x64 to path64. Both are necessary.
path32=brokenithm_x86.dll
path64=brokenithm_x64.dll
```


# Sources 
- [Brokenithm-Evolved](https://gitea.tendokyu.moe/Dniel97/Brokenithm-Evolved)
- [Brokenithm-Server](https://github.com/tindy2013/Brokenithm-Android-Server)
- [ADB_Debug_Bridge](https://developer.android.com/tools/adb)
