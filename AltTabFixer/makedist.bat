@setlocal

call "%VS100COMNTOOLS%..\..\VC\vcvarsall.bat"

@rem Move to the directory containing this batch file
cd "%~dp0"
devenv AltTabFixer.sln /build release
xcopy /y Release\*.exe ..\bin
