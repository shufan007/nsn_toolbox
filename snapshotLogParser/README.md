# SnapshotLogParseTool
split snapshot buffer by dump ID, parse each dump block

[Initiation]
----------------------
set source file Path: (should change to your SW path)
SourcePath =  D:\userdata\Lrc_trunk

[Environment Setting up]
----------------------
	python version:  2.7 or newer
		If you want save the parsed messages to xls file,
		make sure those 2 modules 'xlrd' and 'xlwt' being installed 
		you can download them from the net,then install
		@example: install 'xlrd': 	
		  cd to the module path, run: python setup.py install

[Run]
----------------------
run "CodecLogParser.py" to parse the snapshot file.
   *************************** Usage: ***************************
   # Add SourcePath in 'README'
    -input:            
         -[1] SnapShotFile: input file, .bin file or directory with .bin files
               the .bin file in current path or full path
         -[2] start_addr(offset): unpack .bin file from here
             (defult: '0')             
   @example:
        CodecLogParser.py xxx.bin
        CodecLogParser.py RtlDumpBin
        CodecLogParser.py xxx.bin 17f00               
   - output:
        - Out put Location: the same path as input file
        - "xxx_ParseInfo.txt", information parsed from snapshot buffer
        - Parsed Log in directory "xxx_ParsedData"            
   **************************************************************
   
