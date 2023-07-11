# Copy the package to the output directory C:\ProgramData\CAST\CustomExtensions
# The package is copied to the output directory only if the package is not already present in the output directory
# The previous version is kept, expect if the package is already present in the output directory


# Get the folder containing the script
$scriptFolder = Split-Path -Parent $MyInvocation.MyCommand.Definition

# Get the folder name
$folderName = Split-Path -Leaf $scriptFolder

# Get the version number from the nuspec file
$version = Select-String -Path "$scriptFolder\*.nuspec" -Pattern "<version>(.*)</version>" | % { $_.Matches.Groups[1].Value }

# Get the first element of the array containing the version number
$version = $version[0]

# Get the output directory
$outputDirectory = "C:\ProgramData\CAST\CAST\Extensions"

# Remove the previous version of the package from the output directory
Remove-Item -Path "$outputDirectory\$folderName.$version" -Recurse -Force -ErrorAction SilentlyContinue

# List the number of the files in the input directory
$files = Get-ChildItem -Path "$scriptFolder" -Recurse -Force -ErrorAction SilentlyContinue

# Print the number of files in the input directory
Write-Host "Number of files in the input directory: $($files.Count)"

# Copy the package to the output directory with the version number appended
Copy-Item -Path "$scriptFolder" -Destination "$outputDirectory\$folderName.$version" -Recurse -Force

# List the number of the files in the output directory
$files = Get-ChildItem -Path "$outputDirectory\$folderName.*" -Recurse -Force -ErrorAction SilentlyContinue

# Print the number of files in the output directory
Write-Host "Number of files in the output directory: $($files.Count)"
 #>