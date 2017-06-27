param (
   [string]$strFolder = "D:\Public"
)

#write-host 'Folder: ' $strFolder

get-acl $strFolder | select -expand access
