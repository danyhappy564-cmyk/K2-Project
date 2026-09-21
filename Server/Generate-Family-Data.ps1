$ErrorActionPreference = 'Stop'
# 이 스크립트는 실제 SPT 서버 DB가 있는 사용자 로컬 PC에서 실행해야 합니다.
# (Generate-Data.ps1과 동일한 이유 — 클라우드/컨테이너 세션에는 게임 DB가 없습니다.)
#
# 목적: 이미 검증된 K2C3 시험 프리셋(Server/data/preset.json)을 베이스로,
# "부품 갈아끼우기"용 K2 / K2C4 프리셋을 만든다. 새로 등록하는 부품 3개
# (핸드가드/개머리판/총열)는 전부 "이미 검증된" 기존 HK416A5 부품
# (mod_handguard=5bb20de5d4351e0035629e59, mod_stock=5bb20e58d4351e00320205d7,
# mod_barrel=5bb20d9cd4351e00334c9d8a)를 복제한 것이다 — Verify-Server.ps1로
# 슬롯 호환이 이미 확인된 부품만 복제하므로, "실제 DB에 있는지 모르는 부품
# ID를 기억으로 추정"하는 위험을 피했다. 이름·설명·일부 수치만 K2/K2C4
# 스펙(README 참고)에 맞게 바꾼다.
#
# 출력 파일은 기존 weapon.json / preset.json / assort.json과 정확히 같은
# 스키마로, 부품/프리셋/상점판매 하나당 파일 하나씩 낸다 (배열로 묶지 않음 —
# K2Mod.cs가 기존 코드와 동일한 방식으로 읽을 수 있게 하기 위함).
#
# 총열/핸드가드/개머리판의 겉모습은 여전히 HK416이다 — 실제 K2 모델(블렌더/
# Unity 작업)이 끝나기 전까지는 이것도 "시험판"이다.

$dbRoot = Join-Path $PSScriptRoot '../../02_Resources/SPT/SPT-4.1.5/SPT_Runtime/SPT_Data/database'
$items = Get-Content (Join-Path $dbRoot 'templates/items.json') -Raw | ConvertFrom-Json -AsHashtable
$handbook = Get-Content (Join-Path $dbRoot 'templates/handbook.json') -Raw | ConvertFrom-Json -AsHashtable

$weaponId = 'd21900000000000000000001'

$handguardBaseId = '5bb20de5d4351e0035629e59'
$stockBaseId = '5bb20e58d4351e00320205d7'
$barrelBaseId = '5bb20d9cd4351e00334c9d8a'

$handguardPlainId = 'd21900000000000000000010'
$stockFixedId = 'd21900000000000000000011'
$barrelShortId = 'd21900000000000000000012'

$k2PresetId = 'd21900000000000000000003'
$k2c4PresetId = 'd21900000000000000000004'

function CategoryOf([string]$tplId) {
    $category = ($handbook.Items | Where-Object { $_.Id -eq $tplId }).ParentId
    if (!$category) { throw "편람 분류를 찾지 못했습니다: $tplId" }
    return $category
}

foreach ($id in @($handguardBaseId, $stockBaseId, $barrelBaseId)) {
    if (!$items.ContainsKey($id)) { throw "기준 부품이 실제 DB에 없습니다(HK416A5 구성이 바뀌었을 수 있음): $id" }
}

$dataDir = Join-Path $PSScriptRoot 'data'

# 1) 새 부품 3개 (weapon.json과 동일한 스키마, 파일 하나당 부품 하나)
$partDefs = @(
    @{
        File = 'family_part_handguard.json'
        NewId = $handguardPlainId
        BaseId = $handguardBaseId
        NewItemName = 'mod_handguard_k2_plain'
        HandbookPriceRoubles = 8000
        En = @{ shortName='K2 Handguard'; name='K2 Plastic Handguard (no rail, placeholder model)'; description='Represents the original K2 non-rail plastic handguard. Still uses the HK416 rail handguard mesh/stats as a placeholder until the real K2 model is ready.' }
        Kr = @{ shortName='K2 핸드가드'; name='K2 플라스틱 핸드가드 (레일 없음, 임시 외형)'; description='원본 K2의 레일 없는 플라스틱 핸드가드를 대표하는 시험용 부품입니다. 실제 K2 모델이 나오기 전까지는 HK416 레일 핸드가드 외형/수치를 그대로 사용합니다.' }
    },
    @{
        File = 'family_part_stock.json'
        NewId = $stockFixedId
        BaseId = $stockBaseId
        NewItemName = 'mod_stock_k2_fixed'
        HandbookPriceRoubles = 6000
        En = @{ shortName='K2 Stock'; name='K2 Side-Folding Fixed Stock (placeholder model)'; description='Represents the original K2 side-folding fixed stock. Still uses the HK416 telescoping stock mesh/stats as a placeholder until the real K2 model is ready.' }
        Kr = @{ shortName='K2 개머리판'; name='K2 측면 접이식 고정 개머리판 (임시 외형)'; description='원본 K2의 측면 접이식 고정 개머리판을 대표하는 시험용 부품입니다. 실제 K2 모델이 나오기 전까지는 HK416 신축식 개머리판 외형/수치를 그대로 사용합니다.' }
    },
    @{
        File = 'family_part_barrel.json'
        NewId = $barrelShortId
        BaseId = $barrelBaseId
        NewItemName = 'mod_barrel_k2c4_short'
        HandbookPriceRoubles = 10000
        En = @{ shortName='K2C4 Barrel'; name='K2C4 310mm Short Barrel (placeholder model)'; description='Represents the K2C4 short barrel (real length 310mm vs 465mm). Still uses the HK416 barrel mesh/stats as a placeholder — velocity/ergonomics deltas are not final.' }
        Kr = @{ shortName='K2C4 총열'; name='K2C4 310mm 단축 총열 (임시 외형)'; description='K2C4의 310mm 단축 총열(기존 465mm 대비)을 대표하는 시험용 부품입니다. 실제 K2 모델이 나오기 전까지는 HK416 총열 외형/수치를 그대로 사용하며, 탄속/인체공학 보정치는 확정값이 아닙니다.' }
    }
)

foreach ($p in $partDefs) {
    $definition = @{
        itemTplToClone = $p.BaseId
        newId = $p.NewId
        newItemName = $p.NewItemName
        parentId = $items[$p.BaseId]._parent
        handbookParentId = CategoryOf $p.BaseId
        handbookPriceRoubles = $p.HandbookPriceRoubles
        fleaPriceRoubles = $p.HandbookPriceRoubles
        overrideProperties = @{ ExaminedByDefault = $true; CanSellOnRagfair = $false; CanRequireOnRagfair = $false }
        locales = @{ en = $p.En; kr = $p.Kr; 'kr-en' = $p.Kr }
    }
    $definition | ConvertTo-Json -Depth 100 | Set-Content (Join-Path $dataDir $p.File) -Encoding utf8
}

# 2) 이미 검증된 K2C3 프리셋(data/preset.json)을 베이스로 부품 1~2개만 바꿔 K2 / K2C4 프리셋 생성
$k2c3Preset = Get-Content (Join-Path $dataDir 'preset.json') -Raw | ConvertFrom-Json -AsHashtable

function ClonePresetWithSwap([hashtable]$basePreset, [string]$newPresetId, [string]$newName, [hashtable]$swap, [int]$idStart) {
    $clone = $basePreset | ConvertTo-Json -Depth 100 | ConvertFrom-Json -AsHashtable
    $idMap = @{}
    $index = $idStart
    foreach ($item in $clone._items) {
        $idMap[$item._id] = 'd219' + $index.ToString('x20')
        $index++
    }
    foreach ($item in $clone._items) {
        $item._id = $idMap[$item._id]
        if ($item.ContainsKey('parentId')) { $item.parentId = $idMap[$item.parentId] }
        if ($swap.ContainsKey($item._tpl)) { $item._tpl = $swap[$item._tpl] }
    }
    $clone._id = $newPresetId
    $clone._parent = $idMap[$basePreset._parent]
    $clone._name = $newName
    $root = $clone._items | Where-Object { $_._id -eq $clone._parent }
    if (!$root -or $root._tpl -ne $weaponId) { throw "$newName 프리셋 루트 오류" }
    return $clone
}

# 계산된(변수) 키를 해시테이블 리터럴에 바로 넣지 않고 인덱서로 대입한다
# (위 PresetToAssort와 같은 이유 — Generate-Data.ps1의 기존 방식과 통일).
$k2Swap = @{}
$k2Swap[$handguardBaseId] = $handguardPlainId
$k2Swap[$stockBaseId] = $stockFixedId
$k2Preset = ClonePresetWithSwap $k2c3Preset $k2PresetId 'K2 (부품 갈아끼우기 시험)' $k2Swap 0x300

$k2c4Swap = @{}
$k2c4Swap[$barrelBaseId] = $barrelShortId
$k2c4Preset = ClonePresetWithSwap $k2c3Preset $k2c4PresetId 'K2C4 (부품 갈아끼우기 시험)' $k2c4Swap 0x400

function PresetToAssort([hashtable]$preset, [string]$priceTpl, [int]$priceCount, [int]$loyalLevel) {
    $assortItems = $preset._items | ConvertTo-Json -Depth 100 | ConvertFrom-Json -AsHashtable
    $root = $assortItems | Where-Object { $_._id -eq $preset._parent }
    $root.parentId = 'hideout'
    $root.slotId = 'hideout'
    $root.upd = @{ UnlimitedCount = $true; StackObjectsCount = 9999; Repairable = @{ Durability = 100; MaxDurability = 100 } }
    # 계산된 값을 키로 쓰려면 해시테이블 리터럴 안에 바로 못 넣는다(Generate-Data.ps1과
    # 동일한 이유) — 빈 해시테이블을 만들고 인덱서로 대입한다.
    $assort = @{ items = @($assortItems); barter_scheme = @{}; loyal_level_items = @{} }
    $assort.barter_scheme[$preset._parent] = ,@(@{ _tpl = $priceTpl; count = $priceCount })
    $assort.loyal_level_items[$preset._parent] = $loyalLevel
    return $assort
}

$k2Preset | ConvertTo-Json -Depth 100 | Set-Content (Join-Path $dataDir 'family_preset_k2.json') -Encoding utf8
$k2c4Preset | ConvertTo-Json -Depth 100 | Set-Content (Join-Path $dataDir 'family_preset_k2c4.json') -Encoding utf8
(PresetToAssort $k2Preset '5696686a4bdc2da3298b456a' 520 1) | ConvertTo-Json -Depth 100 | Set-Content (Join-Path $dataDir 'family_assort_k2.json') -Encoding utf8
(PresetToAssort $k2c4Preset '5696686a4bdc2da3298b456a' 480 1) | ConvertTo-Json -Depth 100 | Set-Content (Join-Path $dataDir 'family_assort_k2c4.json') -Encoding utf8

Write-Output '부품 갈아끼우기 데이터 생성 완료: 부품 3개(family_part_*.json), 프리셋 2개(K2/K2C4), 상점판매 2개.'
Write-Output 'K2Mod.cs가 서버 시작 시 이 파일들을 자동으로 읽습니다(없으면 조용히 건너뜀 — 기존 K2C3 시험판은 그대로 동작).'
Write-Output '주의: 부품들의 실제 외형은 여전히 HK416입니다. 탄속/인체공학 보정치는 시험용 임시값이며 확정 스펙이 아닙니다.'
