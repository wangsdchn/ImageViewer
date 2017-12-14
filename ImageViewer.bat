::-----隐藏cmd窗口----
@echo off
if "%1" == "h" goto begin
mshta vbscript:createobject("wscript.shell").run("""%~nx0"" h",0)(window.close)&&exit
:begin
REM

::----最小化cmd窗口----
::@echo off
::%1(start /min cmd.exe /c %0 :&exit)

python ImageViewer.py