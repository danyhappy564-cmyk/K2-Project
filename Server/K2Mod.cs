using System.Reflection;
using SPTarkov.Common.Models.Logging;
using SPTarkov.DI.Annotations;
using SPTarkov.Server.Core.DI;
using SPTarkov.Server.Core.Helpers.Server;
using SPTarkov.Server.Core.Models.Common;
using SPTarkov.Server.Core.Models.Eft.Common.Tables;
using SPTarkov.Server.Core.Models.Spt.Mod;
using SPTarkov.Server.Core.Models.Spt.Tables;
using SPTarkov.Server.Core.Services.Modding.Custom;
using SPTarkov.Server.Core.Utils;
using Path = System.IO.Path;
using File = System.IO.File;

namespace K2Project;

public record ModMetadata : IModMetadata
{
    public string ModGuid { get; init; } = "com.k2project.server";
    public string Name { get; init; } = "K2C3 - Visual Test";
    public string Author { get; init; } = "C33 / R_F";
    public SemanticVersioning.Version Version { get; init; } = new("0.2.0");
    public SemanticVersioning.Range SptVersion { get; init; } = new("~4.1.6");
    public string License { get; init; } = "All rights reserved";
    public bool HasPrepatcher { get; init; } = false;
    public Dictionary<string, SemanticVersioning.Range>? ModDependencies { get; init; } = [];
    public string? Url { get; init; } = "https://github.com/danyhappy564-cmyk/K2-Project";
    public List<string>? Contributors { get; init; } = ["Codex (server prototype)"];
    public List<string>? Incompatibilities { get; init; } = [];
}

[Injectable(InjectionType.Singleton, TypePriority = OnLoadOrder.Preload + 2)]
public sealed class K2Mod(CustomItemService customItems, TemplateTable templates,
    GlobalTable globals, TradersTable traders, ModHelper modHelper, JsonUtil json,
    ISptLogger<K2Mod> logger) : IOnLoad
{
    public const string WeaponId = "d21900000000000000000001";
    public const string BaseId = "5bb2475ed4351e00853264e3";

    // 부품 갈아끼우기(K2/K2C4) — Server/Generate-Family-Data.ps1이 생성하는 파일들.
    // 실제 SPT DB가 있는 로컬 PC에서만 생성 가능하므로, 파일이 없으면 조용히
    // 건너뛴다 (기존 K2C3 시험용 무기 1개는 그대로 동작).
    public const string HandguardPlainId = "d21900000000000000000010";
    public const string StockFixedId = "d21900000000000000000011";
    public const string BarrelShortId = "d21900000000000000000012";
    public const string K2PresetId = "d21900000000000000000003";
    public const string K2C4PresetId = "d21900000000000000000004";

    public Task OnLoadAsync(CancellationToken cancellationToken)
    {
        cancellationToken.ThrowIfCancellationRequested();
        var folder = modHelper.GetAbsolutePathToModFolder(Assembly.GetExecutingAssembly());
        T Read<T>(string file) where T : class =>
            json.DeserializeFromFile<T>(Path.Combine(folder, "data", file))
            ?? throw new InvalidDataException($"[K2] 데이터 로드 실패: {file}");

        var definition = Read<NewItemFromCloneDetails>("weapon.json");
        var preset = Read<Preset>("preset.json");
        var assort = Read<TraderAssort>("assort.json");
        if (definition.NewId != new MongoId(WeaponId) || definition.ItemTplToClone != new MongoId(BaseId))
            throw new InvalidDataException("[K2] 무기 정의 ID가 일치하지 않습니다.");
        if (!templates.Items.ContainsKey(new MongoId(BaseId)))
            throw new InvalidDataException("[K2] HK416 원본 데이터가 없습니다.");
        if (templates.Items.ContainsKey(new MongoId(WeaponId)))
            throw new InvalidDataException("[K2] 중복 설치 또는 아이템 ID 충돌입니다.");
        var trader = traders.GetTrader(new MongoId("5935c25fb3acc3127c3d8cd9"))
            ?? throw new InvalidDataException("[K2] 피스키퍼가 없습니다.");
        foreach (var item in assort.Items)
        {
            if (item.Template != new MongoId(WeaponId) && !templates.Items.ContainsKey(item.Template))
                throw new InvalidDataException($"[K2] 부품을 찾을 수 없습니다: {item.Template}");
            if (trader.Assort.Items.Any(existing => existing.Id == item.Id))
                throw new InvalidDataException($"[K2] 상품 ID 충돌: {item.Id}");
        }
        var presetId = new MongoId("d21900000000000000000002");
        if (globals.ItemPresets.ContainsKey(presetId))
            throw new InvalidDataException("[K2] 프리셋 ID 충돌입니다.");
        var result = customItems.CreateItemFromClone(definition, Assembly.GetExecutingAssembly());
        if (!result.Success)
            throw new InvalidOperationException($"[K2] 등록 실패: {string.Join("; ", result.Errors)}");

        globals.ItemPresets[presetId] = preset;
        foreach (var item in assort.Items) trader.Assort.Items.Add(item);
        foreach (var (id, scheme) in assort.BarterScheme) trader.Assort.BarterScheme[id] = scheme;
        foreach (var (id, level) in assort.LoyalLevelItems) trader.Assort.LoyalLevelItems[id] = level;

        var inventory = templates.Items[new MongoId("55d7217a4bdc2d86028b456d")];
        foreach (var slot in inventory.Properties!.Slots!.Where(s => s.Name is "FirstPrimaryWeapon" or "SecondPrimaryWeapon"))
        foreach (var filter in slot.Properties!.Filters!)
            filter.Filter!.Add(new MongoId(WeaponId));

        logger.Info("[K2] K2C3 시험용 무기 등록 완료 — 외형은 K2.Visual 플러그인 필요 / 피스키퍼 1레벨 / 500달러 / 750 RPM");

        // 부품 갈아끼우기(K2/K2C4) 시험 등록. Generate-Family-Data.ps1을 실행한 적이
        // 없으면 파일이 없어서 조용히 건너뛴다 — 위의 K2C3 시험용 무기 1개 등록은
        // 이 블록과 무관하게 이미 끝난 상태다. (지역 함수로 둬서 트레이더 변수의
        // 실제 타입을 다시 적을 필요 없이 그대로 캡처한다.)
        void RegisterFamilyParts()
        {
            var dataDir = Path.Combine(folder, "data");
            var handguardPartPath = Path.Combine(dataDir, "family_part_handguard.json");
            if (!File.Exists(handguardPartPath))
            {
                logger.Info("[K2] family_part_handguard.json 없음 — Server/Generate-Family-Data.ps1 미실행. K2/K2C4 부품 갈아끼우기는 아직 등록되지 않음(K2C3 시험용 무기 1개는 정상 등록됨)");
                return;
            }

            T ReadFamily<T>(string file) where T : class =>
                json.DeserializeFromFile<T>(Path.Combine(dataDir, file))
                ?? throw new InvalidDataException($"[K2] 데이터 로드 실패: {file}");

            var handguardPart = ReadFamily<NewItemFromCloneDetails>("family_part_handguard.json");
            var stockPart = ReadFamily<NewItemFromCloneDetails>("family_part_stock.json");
            var barrelPart = ReadFamily<NewItemFromCloneDetails>("family_part_barrel.json");
            foreach (var part in new[] { handguardPart, stockPart, barrelPart })
            {
                if (templates.Items.ContainsKey(part.NewId))
                    throw new InvalidDataException($"[K2] 부품 ID 충돌: {part.NewId}");
                var partResult = customItems.CreateItemFromClone(part, Assembly.GetExecutingAssembly());
                if (!partResult.Success)
                    throw new InvalidOperationException($"[K2] 부품 등록 실패({part.NewId}): {string.Join("; ", partResult.Errors)}");
            }

            // 주의: mod_barrel/mod_handguard/mod_sight_rear 슬롯은 무기 본체가 아니라
            // 리시버 아이템(mod_reciever, data/preset.json의 5bb20d53d4351e4502010a69)에
            // 달려 있다 — Server/Generate-Data.ps1로 뽑은 실제 HK416A5 기본 프리셋
            // 구조 기준(2026-09-19). 이 리시버는 우리 WeaponId만의 복제본이 아니라
            // HK416A5가 공유하는 원본 템플릿이라서, 여기에 필터를 추가하면 실제
            // HK416A5도 이 시험용 K2 부품을 낄 수 있게 된다 — 지금은 시험 단계라
            // 허용하고 로그로 남긴다.
            const string ReceiverId = "5bb20d53d4351e4502010a69";
            void AllowInSlot(MongoId hostId, string slotName, MongoId newPartId)
            {
                var host = templates.Items[hostId];
                var slot = host.Properties!.Slots!.SingleOrDefault(s => s.Name == slotName)
                    ?? throw new InvalidDataException($"[K2] 슬롯을 찾지 못했습니다: {slotName}");
                foreach (var filter in slot.Properties!.Filters!) filter.Filter!.Add(newPartId);
            }
            AllowInSlot(new MongoId(ReceiverId), "mod_handguard", new MongoId(HandguardPlainId));
            AllowInSlot(new MongoId(WeaponId), "mod_stock", new MongoId(StockFixedId));
            AllowInSlot(new MongoId(ReceiverId), "mod_barrel", new MongoId(BarrelShortId));
            logger.Info("[K2] 참고: mod_handguard/mod_barrel 필터를 공유 리시버 템플릿에 추가함 — 실제 HK416A5도 이 시험용 K2 부품을 장착할 수 있게 됨(의도된 부작용, 시험 단계)");

            var k2Preset = ReadFamily<Preset>("family_preset_k2.json");
            var k2c4Preset = ReadFamily<Preset>("family_preset_k2c4.json");
            if (globals.ItemPresets.ContainsKey(new MongoId(K2PresetId)) || globals.ItemPresets.ContainsKey(new MongoId(K2C4PresetId)))
                throw new InvalidDataException("[K2] K2/K2C4 프리셋 ID 충돌입니다.");
            globals.ItemPresets[new MongoId(K2PresetId)] = k2Preset;
            globals.ItemPresets[new MongoId(K2C4PresetId)] = k2c4Preset;

            var k2Assort = ReadFamily<TraderAssort>("family_assort_k2.json");
            var k2c4Assort = ReadFamily<TraderAssort>("family_assort_k2c4.json");
            foreach (var familyAssort in new[] { k2Assort, k2c4Assort })
            {
                foreach (var item in familyAssort.Items) trader.Assort.Items.Add(item);
                foreach (var (id, scheme) in familyAssort.BarterScheme) trader.Assort.BarterScheme[id] = scheme;
                foreach (var (id, level) in familyAssort.LoyalLevelItems) trader.Assort.LoyalLevelItems[id] = level;
            }

            logger.Info("[K2] 부품 갈아끼우기(K2/K2C4) 등록 완료 — 부품 3개(핸드가드/개머리판/총열), 프리셋 2개. 외형은 여전히 HK416, 서버 데이터만 시험 중");
        }
        RegisterFamilyParts();

        return Task.CompletedTask;
    }
}
