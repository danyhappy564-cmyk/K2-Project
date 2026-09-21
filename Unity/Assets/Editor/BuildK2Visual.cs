using System;
using System.IO;
using UnityEditor;
using UnityEngine;

public static class BuildK2Visual
{
    private static T SaveAsset<T>(T value,string path) where T:UnityEngine.Object
    {
        var existing=AssetDatabase.LoadAssetAtPath<T>(path);
        if(!existing){AssetDatabase.CreateAsset(value,path);return value;}
        EditorUtility.CopySerialized(value,existing);
        UnityEngine.Object.DestroyImmediate(value);
        return existing;
    }
    [Serializable] public class Input { public Part[] meshes; }
    [Serializable] public class Part
    {
        public string name;
        public float[] positions, normals, uv;
        public int[] indices;
    }
    public static void Build()
    {
        var project = Path.GetFullPath(Path.Combine(Application.dataPath, "../.."));
        var input = JsonUtility.FromJson<Input>(File.ReadAllText(Path.Combine(project,"Assets-Local/UnityInput/k2c3-visual.json")));
        Directory.CreateDirectory("Assets/Generated");
        Directory.CreateDirectory("Assets/Textures");
        foreach (var file in Directory.GetFiles(Path.Combine(project,"Assets-Local/K2C3/textures"),"*.png"))
            File.Copy(file,Path.Combine("Assets/Textures",Path.GetFileName(file)),true);
        AssetDatabase.Refresh();
        var root = new GameObject("K2C3_Visual");
        int triangles = 0;
        foreach (var part in input.meshes)
        {
            var mesh = new Mesh { name=part.name };
            var vertices=new Vector3[part.positions.Length/3];
            var normals=new Vector3[vertices.Length];
            var uv=new Vector2[vertices.Length];
            for(int i=0;i<vertices.Length;i++)
            {
                vertices[i]=new Vector3(part.positions[i*3],part.positions[i*3+1],part.positions[i*3+2]);
                normals[i]=new Vector3(part.normals[i*3],part.normals[i*3+1],part.normals[i*3+2]);
                uv[i]=new Vector2(part.uv[i*2],part.uv[i*2+1]);
            }
            mesh.vertices=vertices;mesh.normals=normals;mesh.uv=uv;mesh.triangles=part.indices;
            mesh.RecalculateBounds();mesh.RecalculateTangents();
            triangles+=part.indices.Length/3;
            mesh=SaveAsset(mesh,"Assets/Generated/"+part.name+".asset");
            var material=new Material(Shader.Find("Standard")){name=part.name};
            material.mainTexture=AssetDatabase.LoadAssetAtPath<Texture2D>("Assets/Textures/"+part.name+"_baseColor.png");
            var normalPath="Assets/Textures/"+part.name+"_normal.png";
            var importer=(TextureImporter)AssetImporter.GetAtPath(normalPath);
            importer.textureType=TextureImporterType.NormalMap;importer.SaveAndReimport();
            material.SetTexture("_BumpMap",AssetDatabase.LoadAssetAtPath<Texture2D>(normalPath));
            material.EnableKeyword("_NORMALMAP");
            // Convert glTF G=roughness/B=metallic to Standard R=metallic/A=smoothness.
            var mr=new Texture2D(2,2,TextureFormat.RGBA32,false,true);
            mr.LoadImage(File.ReadAllBytes(Path.Combine(project,"Assets-Local/K2C3/textures/"+part.name+"_metallicRoughness.png")));
            var pixels=mr.GetPixels32();
            for(int i=0;i<pixels.Length;i++)pixels[i]=new Color32(pixels[i].b,0,0,(byte)(255-pixels[i].g));
            mr.SetPixels32(pixels);mr.Apply();
            var packedPath="Assets/Generated/"+part.name+"_metallic.png";
            File.WriteAllBytes(packedPath,mr.EncodeToPNG());UnityEngine.Object.DestroyImmediate(mr);
            AssetDatabase.ImportAsset(packedPath);
            var packedImporter=(TextureImporter)AssetImporter.GetAtPath(packedPath);
            packedImporter.sRGBTexture=false;packedImporter.SaveAndReimport();
            material.SetTexture("_MetallicGlossMap",AssetDatabase.LoadAssetAtPath<Texture2D>(packedPath));
            material.SetFloat("_GlossMapScale",1);material.EnableKeyword("_METALLICGLOSSMAP");
            material=SaveAsset(material,"Assets/Generated/"+part.name+".mat");
            var child=new GameObject(part.name);child.transform.SetParent(root.transform,false);
            child.AddComponent<MeshFilter>().sharedMesh=mesh;
            child.AddComponent<MeshRenderer>().sharedMaterial=material;
        }
        if(triangles!=12732)throw new Exception("Unexpected triangle count: "+triangles);
        const string prefab="Assets/Generated/k2c3_visual.prefab";
        PrefabUtility.SaveAsPrefabAsset(root,prefab);UnityEngine.Object.DestroyImmediate(root);
        AssetDatabase.SaveAssets();
        var output=Path.Combine(project,"Artifacts/VisualBundle");Directory.CreateDirectory(output);
        var result=BuildPipeline.BuildAssetBundles(output,new[]{new AssetBundleBuild{assetBundleName="k2c3_visual.bundle",assetNames=new[]{prefab}}},BuildAssetBundleOptions.ChunkBasedCompression,BuildTarget.StandaloneWindows64);
        if(result==null)throw new Exception("Bundle build failed");
        Debug.Log("K2_VISUAL_BUILD_OK triangles="+triangles+" output="+output);
    }
}
