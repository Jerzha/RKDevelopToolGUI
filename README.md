# RKDevelopToolGUI (for unix/linux/macos)
Rockchip develop tool by python3 tkinter

## Download
[Download](https://github.com/Jerzha/RKDevelopToolGUI/releases)

## Build
python3 setup.py py2app

# About py2app in MacOS 10.14
* pip list to find py2app version
* pip install --user --ignore-installed py2app==0.7.3 

## Demo
![avatar](/demo/demo1.png)

## FAQ

* About Maskrom & Loader mode

    The begin address in maskrom is 0x0, but loader mode is +4Mb(0x2000) in LBA format
 
* Differences between download loader and upgrade loader
    
    Download loader only available in maskrom mode, and it write boot loader to DDR only. 
    Upgrade loader write boot loader to nand.  
    
* In Maskrom mode

    If has any problem after burning, check do not write parameter in loader mode.
    
* Some command usage
    
    * ./rkdeveloptool rd 3    # reboot from loader to maskrom
    * ./rkdeveloptool rcb     # read format, if success, need to offset 4mb
    * ./rkdeveloptool ppt     # read partition table, if failed, means partition table error
