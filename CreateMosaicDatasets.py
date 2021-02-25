import arcpy

listRasterMosaics = [
    "rm_atl01",
    "rm_atl02",
    "rm_atl03",
    "rm_atl04",
    "rm_atl05",
    "rm_atl06",
    "rm_cen01",
]

prj = "PROJCS['WGS_1984_Web_Mercator_Auxiliary_Sphere',GEOGCS['GCS_WGS_1984',DATUM['D_WGS_1984',SPHEROID['WGS_1984',6378137.0,298.257223563]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['Mercator_Auxiliary_Sphere'],PARAMETER['False_Easting',0.0],PARAMETER['False_Northing',0.0],PARAMETER['Central_Meridian',0.0],PARAMETER['Standard_Parallel_1',0.0],PARAMETER['Auxiliary_Sphere_Type',0.0],UNIT['Meter',1.0]]"

for name in listRasterMosaics:
    print("Creating mosaic: {}".format(name))
    
    arcpy.management.CreateMosaicDataset(
        r"C:\Users\pearce.c\Desktop\KAP Testing Env.gdb",
        name, 
        prj,
        None,
        "",
        "NONE",
        None
        )
