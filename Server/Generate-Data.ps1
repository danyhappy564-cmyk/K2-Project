$ErrorActionPreference = 'Stop'
$dbRoot = Join-Path $PSScriptRoot '../../02_Resources/SPT/SPT-4.1.5/SPT_Runtime/SPT_Data/database'
$items = Get-Content (Join-Path $dbRoot 'templates/items.json') -Raw | ConvertFrom-Json -AsHashtable
$globals = Get-Content (Join-Path $dbRoot 'globals.json') -Raw | ConvertFrom-Json -AsHashtable
$handbook = Get-Content (Join-Path $dbRoot 'templates/handbook.json') -Raw | ConvertFrom-Json -AsHashtable
$baseId = '5bb2475ed4351e00853264e3'
$weaponId = 'd21900000000000000000001'
$presetId = 'd21900000000000000000002'
if ($items[$baseId]._name -ne 'weapon_hk_416a5_556x45') { throw 'HK416 원본 불일치' }
$basePreset = $globals.ItemPresets.Values | Where-Object { $_._encyclopedia -eq $baseId } | Select-Object -First 1
if (!$basePreset) { throw 'HK416 기본 프리셋 없음' }
$preset = $basePreset | ConvertTo-Json -Depth 100 | ConvertFrom-Json -AsHashtable
$idMap = @{}
$index = 256
foreach ($item in $preset._items) {
    $idMap[$item._id] = 'd219' + $index.ToString('x20')
    $index++
}
foreach ($item in $preset._items) {
    $item._id = $idMap[$item._id]
    if ($item.ContainsKey('parentId')) { $item.parentId = $idMap[$item.parentId] }
    if ($item._tpl -eq $baseId) { $item._tpl = $weaponId }
}
$preset._id = $presetId
$preset._parent = $idMap[$basePreset._parent]
$preset._encyclopedia = $weaponId
$preset._name = 'K2 Prototype (HK416 temporary model)'
$root = $preset._items | Where-Object { $_._id -eq $preset._parent }
if (!$root -or $root._tpl -ne $weaponId) { throw '프리셋 루트 오류' }
$assortItems = $preset._items | ConvertTo-Json -Depth 100 | ConvertFrom-Json -AsHashtable
$assortRoot = $assortItems | Where-Object { $_._id -eq $preset._parent }
$assortRoot.parentId = 'hideout'
$assortRoot.slotId = 'hideout'
$assortRoot.upd = @{ UnlimitedCount=$true; StackObjectsCount=9999; Repairable=@{Durability=100;MaxDurability=100} }
$assort = @{ items=@($assortItems); barter_scheme=@{}; loyal_level_items=@{} }
$assort.barter_scheme[$preset._parent] = ,@(@{_tpl='5696686a4bdc2da3298b456a';count=500})
$assort.loyal_level_items[$preset._parent] = 1
$category = ($handbook.Items | Where-Object { $_.Id -eq $baseId }).ParentId
if (!$category) { throw '편람 분류 없음' }
$definition = @{
    itemTplToClone=$baseId; parentId=$items[$baseId]._parent; newId=$weaponId
    newItemName='weapon_k2_prototype_556x45'; handbookParentId=$category
    handbookPriceRoubles=50000; fleaPriceRoubles=50000
    locales=@{
        en=@{name='Daewoo K2 5.56x45 (Prototype)';shortName='K2 Proto';description='Server prototype. Uses the HK416 model, animations and attachments temporarily. Rate of fire: 750 RPM. Custom K2 model is not included.'}
        kr=@{name='대우정밀 K2 5.56×45 돌격소총 (시험용)';shortName='K2 시험용';description='서버 기능 검증용 K2입니다. 외형·애니메이션·부품은 임시로 HK416을 사용하며 연사속도는 분당 750발입니다. K2 전용 모델은 아직 포함되지 않았습니다.'}
        'kr-en'=@{name='대우정밀 K2 5.56×45 돌격소총 (Prototype)';shortName='K2 시험용';description='서버 기능 검증용 K2입니다. HK416 임시 외형과 부품을 사용하며 연사속도는 분당 750발입니다. K2 전용 모델은 아직 포함되지 않았습니다.'}
    }
    overrideProperties=@{bFirerate=750;ExaminedByDefault=$true;CanSellOnRagfair=$false;CanRequireOnRagfair=$false}
}
$dataDir = Join-Path $PSScriptRoot 'data'
New-Item -ItemType Directory -Path $dataDir -Force | Out-Null
$definition | ConvertTo-Json -Depth 100 | Set-Content (Join-Path $dataDir 'weapon.json') -Encoding utf8
$preset | ConvertTo-Json -Depth 100 | Set-Content (Join-Path $dataDir 'preset.json') -Encoding utf8
$assort | ConvertTo-Json -Depth 100 | Set-Content (Join-Path $dataDir 'assort.json') -Encoding utf8
Write-Output "K2 데이터 생성 완료: 원본 $baseId, 프리셋 부품 $($preset._items.Count)개"
