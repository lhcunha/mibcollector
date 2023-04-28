# mibcollector
Have you ever felt the pain of having a list of thousands of SNMP OIDs and having to search for their associated MIB files one by one?
This kind of task can easily lead to weeks of works.
To prevent me and you from such repetitive task, I developed this script that parses a list of OIDs and collects the associated MIB file for each OID.

# Usage
To use the script, simply run the command "python mibcollector.py -f oids.txt", where:
- oids.txt : Is the input file containing the OID list. You can give any name to the file.

The script will then start to process the OIDs one by one. When it is done, you can verify all the collected MIB files on the directory "mib_files/"


# Disclaimer
- The MIB files gathering relies on the website https://www.circitor.fr/ as the datasource (thanks Raymond MERCIER)
- With that said, any unavailability on the website can cause unoperability to the script
