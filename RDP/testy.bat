@echo off
setlocal enabledelayedexpansion

cd sitesets
for %%x in (*) do (     
    set filename=%%x  

    call 
    @echo !filename!
    set newn=!filename:*_=!   
    @echo !newn! 
    set newn=!newn:~0,-9!
    @echo !newn!   
  
    ..\RDP5CL.exe -rdpf !newn!.rdp5 -ssou test_result.txt -ssin sitesets/!filename! -ssap   
)