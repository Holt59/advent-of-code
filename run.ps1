param([switch]$Test, $day)

$folder = $Test ? "tests" : "inputs"

Get-Content ".\2022\$folder\day$day.txt" | python ".\2022\day$day.py"
