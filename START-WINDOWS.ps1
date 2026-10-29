$ErrorActionPreference = 'Stop'
Write-Host 'TRUST MARK: starting services. Run this script from the extracted project root.'
if (!(Test-Path 'backend\.env')) { Copy-Item 'backend\.env.example' 'backend\.env'; Write-Host 'Created backend\.env. Edit JWT_SECRET and DEMO_PASSWORD before running.' }
if (!(Test-Path 'ai-service\.env')) { Copy-Item 'ai-service\.env.example' 'ai-service\.env' }
if (!(Test-Path 'frontend\.env')) { Copy-Item 'frontend\.env.example' 'frontend\.env' }
if ((Get-Content 'backend\.env' -Raw) -match 'REPLACE_WITH_RANDOM') { Write-Host 'STOP: Set JWT_SECRET in backend\.env. See README.md'; exit 1 }
if ((Get-Content 'backend\.env' -Raw) -notmatch '(?m)^DEMO_PASSWORD=.{10,}') { Write-Host 'STOP: Add DEMO_PASSWORD (10+ characters) to backend\.env'; exit 1 }
Write-Host 'Install Docker Desktop and run: docker compose up -d'
Write-Host 'First time: cd backend; npm install; npm run seed; cd ..'
Write-Host 'Install Python deps: cd ai-service; python -m pip install -r requirements.txt; cd ..'
Write-Host 'Install frontend deps: cd frontend; npm install; cd ..'
Write-Host 'Opening three terminals...'
Start-Process powershell -ArgumentList '-NoExit','-Command',"Set-Location '$PWD\ai-service'; python -m uvicorn main:app --reload --port 8000"
Start-Process powershell -ArgumentList '-NoExit','-Command',"Set-Location '$PWD\backend'; npm start"
Start-Process powershell -ArgumentList '-NoExit','-Command',"Set-Location '$PWD\frontend'; npm run dev"
Write-Host 'Visit http://localhost:5173'
