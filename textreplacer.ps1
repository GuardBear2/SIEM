###############################################################################
# CONFIGURATION
###############################################################################
# Change this path to the root directory you want to process.
$rootDir = "D:\GuardBear2\SIEM"

# If you want to do a dry-run (no actual changes), set $whatIf = $true
$whatIf = $false

# Full path to this script (so we can skip modifying it)
$scriptPath = $PSCommandPath

# Create UTF8 encoding without BOM
$utf8NoBom = New-Object System.Text.UTF8Encoding $false

###############################################################################
# 1) RENAME DIRECTORIES THAT CONTAIN "Wazuh"/"WAZUH"/"wazuh" (DEEP->SHALLOW)
###############################################################################
Write-Host "`n--- RENAMING DIRECTORIES ---`n"

# Fetch all directories, sorted by depth descending, 
# so deeper subfolders get renamed before their parents.
$dirs = Get-ChildItem -Path $rootDir -Directory -Recurse |
    Sort-Object {
        $_.FullName.Split([IO.Path]::DirectorySeparatorChar).Count
    } -Descending

foreach ($dir in $dirs) {
    # Make a copy of the directory name for case-sensitive replacements
    $newName = $dir.Name

    # Perform three case-sensitive replacements
    $newName = $newName -creplace "Wazuh","GuardBear"
    $newName = $newName -creplace "WAZUH","GUARDBEAR"
    $newName = $newName -creplace "wazuh","guardbear"

    # If the result is different from the old name, rename the directory
    if ($newName -ne $dir.Name) {
        $newFullPath = Join-Path $dir.Parent.FullName $newName
        Write-Host "Directory rename:" $dir.FullName "->" $newFullPath

        if (-not $whatIf) {
            Try {
                Rename-Item -LiteralPath $dir.FullName -NewName $newName
            }
            Catch {
                Write-Warning "Failed to rename directory '$($dir.FullName)': $($_.Exception.Message)"
            }
        }
    }
}

###############################################################################
# 2) RENAME FILES THAT CONTAIN "Wazuh"/"WAZUH"/"wazuh" IN THEIR FILENAME
###############################################################################
Write-Host "`n--- RENAMING FILES ---`n"

# Get all files
$files = Get-ChildItem -Path $rootDir -File -Recurse

foreach ($file in $files) {
    # Skip the script itself
    if ($file.FullName -eq $scriptPath) {
        Write-Host "Skipping script file:" $file.FullName
        continue
    }

    # Make a copy of the file name for case-sensitive replacements
    $newName = $file.Name

    # Perform three case-sensitive replacements
    $newName = $newName -creplace "Wazuh","GuardBear"
    $newName = $newName -creplace "WAZUH","GUARDBEAR"
    $newName = $newName -creplace "wazuh","guardbear"

    # If the result is different, rename the file
    if ($newName -ne $file.Name) {
        $newFullPath = Join-Path $file.DirectoryName $newName
        Write-Host "File rename:" $file.FullName "->" $newFullPath

        if (-not $whatIf) {
            Try {
                Rename-Item -LiteralPath $file.FullName -NewName $newName
            }
            Catch {
                Write-Warning "Failed to rename file '$($file.FullName)': $($_.Exception.Message)"
            }
        }
    }
}

###############################################################################
# 3) REPLACE TEXT ("Wazuh"/"WAZUH"/"wazuh") -> inside FILE CONTENTS
###############################################################################
Write-Host "`n--- REPLACING TEXT INSIDE FILES ---`n"

# Because we may have renamed files above, re-fetch a fresh file list.
$files = Get-ChildItem -Path $rootDir -File -Recurse

foreach ($file in $files) {
    # Skip the script itself
    if ($file.FullName -eq $scriptPath) {
        Write-Host "Skipping script file:" $file.FullName
        continue
    }

    # Attempt to read the file contents as text
    Try {
        $content = [System.IO.File]::ReadAllText($file.FullName, [System.Text.Encoding]::UTF8)
    }
    Catch {
        # If the file is binary or locked, skip
        Write-Warning "Skipping file '$($file.FullName)' (binary or locked): $($_.Exception.Message)"
        continue
    }

    # Perform three case-sensitive replacements in the file content
    $newContent = $content
    $newContent = $newContent -creplace "Wazuh", "GuardBear"
    $newContent = $newContent -creplace "WAZUH", "GUARDBEAR"
    $newContent = $newContent -creplace "wazuh", "guardbear"

    # If something changed, write it back
    if ($newContent -ne $content) {
        Write-Host "Replacing text in file:" $file.FullName

        if (-not $whatIf) {
            Try {
                [System.IO.File]::WriteAllText($file.FullName, $newContent, $utf8NoBom)
            }
            Catch {
                Write-Warning "Failed to write changes to '$($file.FullName)': $($_.Exception.Message)"
            }
        }
    }
}

Write-Host "`nAll operations complete!"
