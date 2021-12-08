Task default -depends Build

Task Restore {
    Exec { python -m pip install --upgrade build twine }
}

Task Rebuild {
    $readme = $(Get-Childitem "README.md")[0]

    Set-Location src
    Write-Output "📦 Build main"

    Copy-Item $readme ./README.md
    Exec { python -m build -o ../dist }
    Remove-Item ./README.md
    
    Set-Location ..
}

Task Build -depends Restore, Rebuild

Task Deploy -depends Build {
    Exec { python -m twine upload --skip-existing --repository pypi "dist/*" }
}

Task Install {

    Write-Output "🛠 Install dependencies"
    if ([System.Runtime.InteropServices.RuntimeInformation]::IsOSPlatform([System.Runtime.InteropServices.OSPlatform]::Linux)) {
        Exec { sudo apt-get update >/dev/null }
    }
    elseif ([System.Runtime.InteropServices.RuntimeInformation]::IsOSPlatform([System.Runtime.InteropServices.OSPlatform]::OSX)) {
    }
    elseif ([System.Runtime.InteropServices.RuntimeInformation]::IsOSPlatform([System.Runtime.InteropServices.OSPlatform]::Windows)) {
    }

    Write-Output "🛠 Install main"

    Set-Location ./dist
    Exec { python -m pip install $(Get-Childitem "codesim-*.whl")[0] }

    Set-Location ..
}

Task Uninstall {
    Write-Output "⚒ Uninstall main"

    Set-Location ./dist
    Exec { python -m pip uninstall $(Get-Childitem "codesim*.whl")[0] -y }

    Set-Location ..
}

Task Demo {
    Write-Output "⏳ 1️⃣ Version ⏳"
    Exec { codesim --version }
    Write-Output "⏳ 2️⃣ Help ⏳"
    Exec { codesim --help }
}

Task DataTest {
    foreach ($file1 in Get-Childitem "./test/*.c") {
        foreach ($file2 in Get-Childitem "./test/*.c") {
            Write-Output "Compare $file1 $file2"
            Write-Output "Time: $($(Measure-Command { Exec { codesim $file1 $file2 -vvv } | Out-Default}).TotalSeconds)"
        }
    }
}

Task LocalTest {
    Set-Location ./src
    foreach ($file1 in Get-Childitem "../test/*.c") {
        foreach ($file2 in Get-Childitem "../test/*.c") {
            Write-Output "Compare $file1 $file2"
            Write-Output "Time: $($(Measure-Command { Exec { python -m codesim $file1 $file2 } | Out-Default}).TotalSeconds)"
        }
    }
    Set-Location ..
}

Task Test -depends Install, Demo, DataTest, Uninstall

Task Clean {
    Remove-Item -Recurse ./dist
    foreach ($egg in Get-Childitem -Recurse *.egg-info) {
        Write-Output "🗑 Remove $egg"
        Remove-Item -Recurse $egg
    }
}

Task Format {
    autopep8 -r --in-place ./src

    foreach ($file in Get-Childitem "./src/**/*.py" -Recurse) {
        isort $file
    }
}