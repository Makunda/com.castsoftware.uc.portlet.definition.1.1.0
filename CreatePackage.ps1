# Script zipping up the package for the release
# The package is created in the same folder as the script containing all the files and folders; excluding the .ps1 file itself and previous zip files
# The package is named after the folder containing the script and the version number containing in the nuspec file is appended at the end
# The created zipfile extension will be reassigned to nuget package extension

# Get the folder containing the script
$scriptFolder = Split-Path -Parent $MyInvocation.MyCommand.Definition

# Get the folder name
$folderName = Split-Path -Leaf $scriptFolder

# Remove previous zip files with the same name
Remove-Item -Path "$scriptFolder\$folderName.*.zip" -Force
Remove-Item -Path "$scriptFolder\$folderName.*.nupkg" -Force

# Get the version number from the nuspec file
$version = Select-String -Path "$scriptFolder\*.nuspec" -Pattern "<version>(.*)</version>" | % { $_.Matches.Groups[1].Value }

$zipFile = "$scriptFolder\$folderName.$version.zip"
$nupkgFile = "$scriptFolder\$folderName.$version.nupkg"

# Create the zip file
$compress = @{
  Path = $scriptFolder
  CompressionLevel = "Fastest"
  DestinationPath = $zipFile
}
Compress-Archive @compress

# Rename the zip file to nuget package extension
Rename-Item -Path $zipFile -NewName $nupkgFile -Force

 #>