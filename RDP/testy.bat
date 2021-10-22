setlocal
@echo off
cd sitesets
for %%x in (*) do (	
	
    set filename=%%x    
    call :dostuff
    
)
:dostuff
set newn=%filename:*_=%
set finaln=%newn:~0,-4%
@echo %finaln%.rdp5
@echo sitesets/%filename%
..\RDP5CL.exe -rdpf %finaln%.rdp5 -ssou test_result.txt -ssin sitesets/%filename% -ssap