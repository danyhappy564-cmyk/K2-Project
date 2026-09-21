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
        return Task.CompletedTask;
    }
}
