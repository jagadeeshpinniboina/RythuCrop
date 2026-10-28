$testCases = @(
    @{
        name = "Test 1: Kharif, Low water, Beginner"
        body = @{
            land = 2
            season = "Kharif"
            soil = "Sandy Soil"
            irrigation = "Low water availability"
            goal = "Balanced farming"
            experience = "Beginner"
        }
    },
    @{
        name = "Test 2: Rabi, Good water, Higher yield"
        body = @{
            land = 5
            season = "Rabi"
            soil = "Black Soil"
            irrigation = "Good water availability"
            goal = "Higher yield"
            experience = "Some experience"
        }
    },
    @{
        name = "Test 3: Summer, Rainfed, Lower water use"
        body = @{
            land = 1
            season = "Summer"
            soil = "Red Soil"
            irrigation = "Rainfed"
            goal = "Lower water use"
            experience = "Beginner"
        }
    }
)

$validCrops = @(
    'Arecanut', 'Arhar/Tur', 'Castor seed', 'Coconut', 'Cotton(lint)',
    'Dry chillies', 'Gram', 'Jute', 'Maize', 'Onion', 'Potato', 'Rice',
    'Sugarcane', 'Sunflower', 'Tobacco', 'Turmeric', 'Wheat', 'Bajra',
    'Black pepper', 'Groundnut', 'Soyabean'
)

Write-Host "================================================================================"
Write-Host "FARM PLANNING API ENDPOINT TESTS"
Write-Host "================================================================================"

foreach ($test in $testCases) {
    Write-Host "`n$($test.name)"
    
    try {
        $jsonBody = $test.body | ConvertTo-Json
        $response = Invoke-WebRequest -Uri "http://localhost:5000/farm-plan" -Method POST -ContentType "application/json" -Body $jsonBody -ErrorAction Stop
        $data = $response.Content | ConvertFrom-Json
        
        if ($data.recommended_crops) {
            Write-Host "  Recommended: $($data.recommended_crops -join ', ')"
            
            $invalidCrops = $data.recommended_crops | Where-Object { $_ -notin $validCrops }
            if ($invalidCrops) {
                Write-Host "  ❌ INVALID CROPS: $($invalidCrops -join ', ')"
            } else {
                Write-Host "  ✓ All crops valid"
            }
        } else {
            Write-Host "  ❌ No recommendations returned: $($data.error)"
        }
    } catch {
        Write-Host "  ❌ ERROR: $($_.Exception.Message)"
    }
}

Write-Host "`n================================================================================"
Write-Host "Test complete"
