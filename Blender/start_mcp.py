import bpy, importlib.util
path = r'D:/SPT Dev/01_Workbench/BlenderMCP/blender-mcp/addon.py'
spec = importlib.util.spec_from_file_location('k2_blender_mcp', path)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
module.register()
if not getattr(bpy.types, 'blendermcp_server', None):
    bpy.types.blendermcp_server = module.BlenderMCPServer(port=9876)
if not bpy.types.blendermcp_server.running:
    bpy.types.blendermcp_server.start()
