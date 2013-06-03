Every day, we get a report from Mindshift detailing the status of our servers in Secaucus. This Python script is designed to reach out to the Exchange server that receives the reports, parse out the data from the .HTML file in the .ZIP archive, and create a CSV containing the data. The idea is to eventually put all the data into a PostGreSQL database and mine the data for trends. 

netDriveMap is simply one windows command that maps the network drive using the correct username and password so the script can access the share. Obviously since it contains my password I won't be including it here, but it's of the form:
net use n: \\domain1\sharename mypassword /USER:domain\username

DataGatheringCSV is the same as the previous Sandbox.py but renames to something more sensible, while DataGatheringSQL forgoes the CSV file entirely and commits the data to the database directly. 