# Archicad Connect

## Info

Archicad Python and JSON API Connection Test [archiconnect]

- Version: `27.1.2.0`
- Created by GAG
- https://borsh.pro


## Overview

Connects to Archicad Python JSON API and shows Archicad host info.
Executes commands without parameters.


## Usage

```sh
./archiconnect.py ADDRESS PORT COMMAND
```

Where:

- ADDRESS
	- Network name or IP address of Archicad host.
	- Default address: 127.0.0.1

- PORT
	- Port of Archicad host.
	- Default ports range: 19723—19744

- COMMAND
	- Custom Archicad API command to execute.
	- Accepted commands without parameters:
		- GetActivePenTables
		- GetAllClassificationSystems
		- GetAllElements
		- GetAllPropertyNames
		- GetClassificationSystemIds
		- GetProductInfo
		- GetPublisherSetNames
		- IsAlive

## Usage examples

```sh
./archiconnect.py localhost 19723
./archiconnect.py 127.0.0.1 19723 GetAllClassificationSystems
```

## Sample output

```
Connecting to 127.0.0.1:19723 …

Is alive: True
Host version: Archicad 27 3001 INT
```
