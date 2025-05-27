strCommand = "cmd /c scrcpy.exe --video-bit-rate 16M --turn-screen-off --stay-awake --show-touches"

For Each Arg In WScript.Arguments
    strCommand = strCommand & " """ & replace(Arg, """", """""""""") & """"
Next

CreateObject("Wscript.Shell").Run strCommand, 0, false
