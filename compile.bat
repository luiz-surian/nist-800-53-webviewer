@echo off

echo Deleting XLSX files
del /q "C:\Nist\dev\bin\nist800_53_*"
echo ..................................................

echo Clearing Build
del /q "C:\Nist\build"
echo ..................................................

echo Copying Dependencies
robocopy "C:\Nist\dev\bin" "C:\Nist\build\bin" /E
echo ..................................................

echo Building Executable
pyinstaller --onefile --icon=bin/favicon.ico --version-file=file_version_info.txt --name=nist800_53 static_server.py
echo ..................................................

echo Copying Build
robocopy "C:\Nist\dev\dist" "C:\Nist\build" nist800_53.exe
echo ..................................................

echo Compilation Done
pause