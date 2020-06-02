## An emulation-based study of the *Age of Information*

This project has been developed by Salman Qavi as part of *CSE 524: Advanced Project* research-based coursework under the supervision and guidance of Professor Samir Das at Stony Brook University during Spring 2020 semester.

The emulation was executed on a MacBook Pro with a 2.4 GHz Intel Core i5 (Turbo Boost up to 4.1 GHz) CPU and 256 L2 and 6 MB L3 caches, 8GB of 2133 MHz LPDDR3 RAM and a 250.7 GB solid state disk. The laptop was running Mac OS Mojave (10.14.6). The CORE and EMANE environments were run on a virtual machine using VirtualBox 6.1 to run 64-bit Ubuntu 20.04 LTS. For the testbed, we used CORE 6.4, EMANE 1.2.6, MGEN 5.02 and Python 3.8.2.

**_Running CORE:_**\
**start daemon**\
```sudo systemctl daemon-reload```\
```sudo systemctl start core-daemon```\
```sudo service core-daemon start```

**start CORE GUI**\
```core-gui```

Updated information for downloading and installation of CORE-GUI: 
https://coreemu.github.io/core/

Updated information for downloading and installation of MGEN:
https://github.com/USNavalResearchLaboratory/mgen

The **MGEN** build expects the "protolib" source tree (or a symbolic link to it) to
be located in the top level of the "mgen" source tree.  For example, to 
download and build on Linux:

```git clone https://github.com/USNavalResearchLaboratory/mgen.git```\
```cd mgen```\
```git clone https://github.com/USNavalResearchLaboratory/protolib.git```\
```cd makefiles```\
```make -f Makefile.linux```


Reference guide on how to use MGEN tool: 
https://github.com/USNavalResearchLaboratory/mgen/blob/master/doc/mgen.pdf

**Setup of the emulated nodes**

![alt text](https://github.com/salmanshokha/age-of-information/blob/master/network_schematics.png?raw=true)
