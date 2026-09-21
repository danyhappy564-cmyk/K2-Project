param([string]$BaseUrl='https://127.0.0.1:6978')
$ErrorActionPreference = 'Stop'
function Read-Spt([string]$Route) {
    $buffer = [IO.MemoryStream]::new()
    $compress = [IO.Compression.ZLibStream]::new($buffer,[IO.Compression.CompressionLevel]::Optimal,$true)
    $bytes = [Text.Encoding]::UTF8.GetBytes('{}')
    $compress.Write($bytes,0,$bytes.Length)
    $compress.Dispose()
    $response=Invoke-WebRequest -Uri "$BaseUrl$Route" -Method Post -Body $buffer.ToArray() -ContentType 'application/json' -SkipCertificateCheck
    $buffer.Dispose()
    if ($response.RawContentLength -eq 0) { throw "빈 응답: $Route" }
    $inputStream=$response.RawContentStream
    $inputStream.Position=0
    $decompress=[IO.Compression.ZLibStream]::new($inputStream,[IO.Compression.CompressionMode]::Decompress)
    $reader=[IO.StreamReader]::new($decompress)
    try { $parsed=$reader.ReadToEnd() | ConvertFrom-Json -AsHashtable -Depth 100 } finally { $reader.Dispose(); $inputStream.Dispose() }
    if ($parsed.err -ne 0) { throw "API 오류: $Route" }
    return $parsed.data
}
$id='d21900000000000000000001'
$items=Read-Spt '/client/items'
if ($items[$id]._props.bFirerate -ne 750) { throw 'K2 연사속도 오류' }
if ($items[$id]._props.Prefab.path -ne $items['5bb2475ed4351e00853264e3']._props.Prefab.path) { throw '임시 외형 오류' }
$globals=Read-Spt '/client/globals'
$preset=$globals.ItemPresets['d21900000000000000000002']
if (!$preset -or $preset._items.Count -ne 12) { throw '기본 프리셋 오류' }
$root=$preset._items | Where-Object {$_._tpl -eq $id}
if (!$root) { throw '무기 루트 없음' }
foreach ($part in $preset._items) {
    if (!$items.ContainsKey($part._tpl)) { throw "없는 부품: $($part._tpl)" }
    if ($part.parentId) {
        $parent=$preset._items | Where-Object {$_._id -eq $part.parentId}
        if (!$parent) { throw '부모 부품 없음' }
        $slot=$items[$parent._tpl]._props.Slots | Where-Object {$_._name -eq $part.slotId}
        if (!$slot) { throw "슬롯 없음: $($part.slotId)" }
        if ($part._tpl -notin $slot._props.filters.Filter) { throw "슬롯 호환 오류: $($part._tpl)" }
    }
}
Write-Output 'PASS: K2 750 RPM, HK416 임시 외형, 프리셋 12개 부품 및 슬롯 호환'
