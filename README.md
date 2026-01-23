 OpenConfig Serial Port Config Generator
Simple script to generate OpenConfig CLI commands to configure serial ports based on Netbox

## Usage

The command takes one main argument, the name of the serial console server in Netbox to generate
the configuration for.  This is passed with `--scs` or `-s`.

A valid read-only Netbox API key is also required, which the user will be prompted for (or they can pass as
an argument with `--key`) 

Example of execution:
```
user@laptop:~/repos/openconfigports$ ./gen_openconfig.py -s scs-c2-eqiad
Netbox API token: 
Wrote config to scs-c2-eqiad.conf
```

## Output

The resulting configuration is written to a local file in the directory the script was run from,
for instance:
```
cmooney@wikilap:~/repos/openconfigports$ head -20 scs-c2-eqiad.conf 
# Serial port configuration for scs-c2-eqiad

config -s config.ports.port1=
config -s config.ports.port1.charsize=8
config -s config.ports.port1.dtrmode=alwayson
config -s config.ports.port1.flowcontrol=None
config -s config.ports.port1.label=ps6-c2-eqiad
config -s config.ports.port1.loglevel=0
config -s config.ports.port1.mode=portmanager
config -s config.ports.port1.parity=None
config -s config.ports.port1.pinout=X2
config -s config.ports.port1.protocol=RS232
config -s config.ports.port1.speed=9600
config -s config.ports.port1.stop=1
config -s config.ports.port1.syslog.facility=Default
config -s config.ports.port1.syslog.priority=Default
config -s config.ports.port1.terminal=vt220

config -s config.ports.port2=
config -s config.ports.port2.charsize=8
<-- remaining output cut -->
```
