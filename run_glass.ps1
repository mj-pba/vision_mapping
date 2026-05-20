# Define the necessary paths
$ProjectDir = "2D_optical_vision_mapping"
$EnvDir = "py313"
$PythonScript = ".\src\backend\services\generate_2D_glass_certificate_62207_v3.py"

# Function to check if the environment is active (by checking the prompt or VIRTUAL_ENV)
function IsEnvActive {
    return $env:VIRTUAL_ENV -ne $null
}

# 1. Activate the environment if it's not already active
if (-not (IsEnvActive)) {
    Write-Host "Activating virtual environment..."
    # The activate script must be "dotted" (sourced) to run in the current session
    cd ..
    . .\$EnvDir\Scripts\Activate.ps1
    cd $ProjectDir
} else {
    Write-Host "Virtual environment is already active."
}

# 2. Change to the project directory
# Set-Location $ProjectDir

# 3. Run the Python script
Write-Host "Running Python script..."
python $PythonScript