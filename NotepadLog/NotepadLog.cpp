/*
Copyright 2021 Bruce Dawson All Rights Reserved.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
*/

#include <stdio.h>
#include <stdarg.h>
#include <Windows.h>

// Debug logging function inspired by this tweet:
// https://twitter.com/BruceDawson0xB/status/1263583135427465224

// NotepadLog() is a debugging logging function that finds an untitled notepad
// document and appends to it. All you have to do is open notepad and your debug
// logging statements will start showing up. It's like OutputDebugString, but
// without the need to attach a debugger.
// Fixes from the original include avoiding buffer overruns and handling the
// unsaved-changes marker (leading '*' character) in notepad.
// Don't leave NotepadLog statements in your shipping binaries or else unwitting
// users will find notepad filled with your debug statements.

static void NotepadLog(char * str, ...)
{
  va_list ap;
  va_start(ap, str);

  char buf[1000];
  vsnprintf_s(buf, _TRUNCATE, str, ap);
  va_end(ap);

  strncat_s(buf, _countof(buf), "\r\n", _TRUNCATE);
  HWND notepad = FindWindow(NULL, "Untitled - Notepad");
  if (!notepad)
    notepad = FindWindow(NULL, "*Untitled - Notepad");
  HWND edit = FindWindowEx(notepad, nullptr, "EDIT", nullptr);
  SendMessage(edit, EM_REPLACESEL, TRUE, (LPARAM)buf);
}

// Test code, prints whatever is in the first argument.
int main(int argc, char* argv[]) {
  NotepadLog("Message: '%s'", argv[1]);
}
