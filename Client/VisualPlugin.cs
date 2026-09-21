using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Reflection;
using System.Threading.Tasks;
using BepInEx;
using BepInEx.Configuration;
using EFT;
using EFT.InventoryLogic;
using HarmonyLib;
using UnityEngine;

namespace K2Project.Visual;

[BepInPlugin("com.k2project.visual", "K2C3 외형 시험", "0.2.0")]
public sealed class VisualPlugin : BaseUnityPlugin
{
    internal const string WeaponId = "d21900000000000000000001";
    internal static VisualPlugin Instance = null!;
    private Harmony? harmony;
    private AssetBundle? bundle;
    private GameObject? prefab;
    private ConfigEntry<bool> enabledPreview = null!;

    private void Awake()
    {
        Instance = this;
        enabledPreview = Config.Bind("외형 시험", "K2C3 외형 활성화", true,
            "K2 시험용 아이템에 K2C3 외형을 적용합니다. 변경 후 무기를 다시 장착하세요. 전용 조준·재장전은 미완성입니다.");
        try
        {
            var path = Path.Combine(Path.GetDirectoryName(Info.Location)!, "k2c3_visual.bundle");
            bundle = AssetBundle.LoadFromFile(path);
            if (!bundle) throw new InvalidDataException("외형 번들을 불러오지 못했습니다: " + path);
            prefab = bundle.LoadAsset<GameObject>("assets/generated/k2c3_visual.prefab");
            if (!prefab || prefab.GetComponentsInChildren<MeshRenderer>(true).Length != 2)
                throw new InvalidDataException("K2C3 프리팹 또는 메시가 올바르지 않습니다.");
            harmony = new Harmony("com.k2project.visual");
            harmony.PatchAll(typeof(VisualPlugin).Assembly);
            Logger.LogInfo("[K2C3] 외형 번들 준비 완료 — 시험용 K2 아이템에만 적용");
        }
        catch (Exception e) { Logger.LogError("[K2C3] 초기화 실패, 기존 외형 유지: " + e); }
    }

    internal void Apply(Item item, GameObject root)
    {
        var previous = root.GetComponent<K2VisualState>();
        if (previous) previous.Restore();
        if (!enabledPreview.Value || item.TemplateId != WeaponId || !prefab) return;
        // Restrict to the weapon subtree, never the character arm hierarchy.
        var anchors = root.GetComponentsInChildren<Transform>(true)
            .Where(t => t.name == "weapon" && t.parent && t.parent.name == "Weapon_root_anim").ToArray();
        if (anchors.Length == 0) throw new InvalidDataException("총기 기준 본을 찾지 못했습니다: " + root.name);
        var state = previous ? previous : root.AddComponent<K2VisualState>();
        try
        {
            foreach (var anchor in anchors) state.Attach(anchor, prefab!);
            Logger.LogInfo("[K2C3] 외형 적용: " + root.name + " / 총기 본 " + anchors.Length);
        }
        catch { state.Restore(); throw; }
    }

    internal static async Task<GameObject> Finish(Task<GameObject> pending, Item item)
    {
        // Preserve Unity's synchronization context; do not run Unity APIs on a worker.
        var root = await pending;
        if (root)
        {
            try { Instance.Apply(item, root); }
            catch (Exception e) { Instance.Logger.LogError("[K2C3] 외형 적용 실패, 기존 외형 유지: " + e); }
        }
        return root;
    }

    private void OnDestroy()
    {
        harmony?.UnpatchSelf();
        foreach (var state in UnityEngine.Object.FindObjectsOfType<K2VisualState>(true)) state.Restore();
        if (bundle) bundle!.Unload(false);
    }

    [HarmonyPatch]
    private static class CreatePatch
    {
        // The 4.1.5 factory type has an obfuscated name. Match its verified public signature.
        private static MethodBase TargetMethod() => typeof(Item).Assembly.GetTypes()
            .SelectMany(t => t.GetMethods(BindingFlags.Public | BindingFlags.Instance | BindingFlags.DeclaredOnly))
            .Single(m => m.Name == "CreateItemAsync" && m.ReturnType == typeof(Task<GameObject>)
                && m.GetParameters().Length == 6 && m.GetParameters()[0].ParameterType == typeof(Item));
        private static void Postfix(Item __0, ref Task<GameObject> __result) => __result = Finish(__result, __0);
    }
}

public sealed class K2VisualState : MonoBehaviour
{
    private readonly Dictionary<Renderer,bool> hidden = new();
    private readonly List<GameObject> visuals = new();
    public void Attach(Transform anchor, GameObject prefab)
    {
        foreach (var renderer in anchor.GetComponentsInChildren<Renderer>(true))
        {
            if (!(renderer is MeshRenderer) && !(renderer is SkinnedMeshRenderer)) continue;
            // Keep the detachable donor magazine so reloads do not become invisible.
            bool magazine = false;
            for (var t = renderer.transform; t && t != anchor; t = t.parent)
                if (t.name.StartsWith("mod_magazine",StringComparison.Ordinal)) magazine = true;
            if (magazine) continue;
            hidden[renderer] = renderer.forceRenderingOff;
            renderer.forceRenderingOff = true;
        }
        var visual = Instantiate(prefab,anchor,false);
        visuals.Add(visual);
        foreach (var t in visual.GetComponentsInChildren<Transform>(true)) t.gameObject.layer = anchor.gameObject.layer;
    }
    public void Restore()
    {
        foreach (var pair in hidden) if (pair.Key) pair.Key.forceRenderingOff = pair.Value;
        hidden.Clear();
        foreach (var visual in visuals) if (visual) { visual.SetActive(false); Destroy(visual); }
        visuals.Clear();
    }
    // Temporary weapon deactivation is not necessarily a pool return.
    // Keep our data so switching back to the same weapon retains the visual.
    private void OnDisable()
    {
        foreach (var pair in hidden) if (pair.Key) pair.Key.forceRenderingOff = pair.Value;
        foreach (var visual in visuals) if (visual) visual.SetActive(false);
    }
    private void OnEnable()
    {
        foreach (var pair in hidden) if (pair.Key) pair.Key.forceRenderingOff = true;
        foreach (var visual in visuals) if (visual) visual.SetActive(true);
    }
    private void OnDestroy() => Restore();
}
