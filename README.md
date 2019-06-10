# rs97_TextReader
A reader write in python(pygame) specially for rs97 game console

This software is for RetroFW v1.2, and has been test on RS97.

When you exit the reader, it will create a bookmark automatically. But this is happened only when you press POWER button. That`s means, if you lost power accidentally, there is no bookmark!!!

You can use Y button to save bookmark manually.

key map:
-   POWER: exit
-   START: lock and turn off the screen
-   Y:     save bookmark(no notification)

##  Install

-   Copy any file and folder into the game console anywhere you want.
-   Copy a .ttf font file into ./fonts folder, rename it to default.ttf (we don`t provide font by default).
-   delete debug.lock and devicewin.py, these files are using for debug on Windows.
-   Modify ./config/config.cfg if you like. No information at this moment.
-   On game console, run run.dge or create a shortcut with file selector using test.dge

(You can try to set CPU frequence to minimal to extend battery life)

Default config file encoding is UTF-8, that means if your font support, it can display Chinese and other language at the same time.

This is still under development.