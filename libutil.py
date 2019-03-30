
import numpy as np
import xarray as xr


def area_rad_to_km(area_rad):
    """
    convert area in rad^2 to km^2
    """
    r_earth = 6.37122e3 # SHR_CONST_REARTH, in km 
    circ = 2*np.pi*r_earth

    foo = xr.ufuncs.sqrt(area_rad.copy())
    foo *= r_earth
    area_km = foo**2
    return area_km



def print_CPL_icemask_areas(ds, 
                            area_xg='domg_aream', area_xl='doml_aream',
                            fldname_xg='g2x_Sg_icemask', fldname_xl='x2l_Sg_icemask'):
    """
    given a coupler history file, opened as Xarray dataset, 
    print both the LAND and GLC icemask extent in km^2
    
    By default, take the cell area from the mapping file
    """
    glc_area = ds[area_xg].squeeze()
    lnd_area = ds[area_xl].squeeze()

    # convert area to km^2
    glc_area_km = area_rad_to_km(glc_area) 
    lnd_area_km = area_rad_to_km(lnd_area)

    # icemask
    xgIceMask = ds[fldname_xg].squeeze()
    xlIceMask = ds[fldname_xl].squeeze()
    
    tot_cplg = (xgIceMask.to_masked_array() * glc_area_km.values).sum()
    tot_cpll = (xlIceMask.to_masked_array() * lnd_area_km.values).sum()
    print('CPL-G, :', tot_cplg)
    print('CPL-L, :', tot_cpll) 
    print('ratio CPL-L / CPL-G :', tot_cpll/tot_cplg)

    
def print_CPL_glaciercover_areas(ds,
                            area_xg='domg_aream', area_xl='doml_aream',
                            fldname_xg='g2x_Sg_ice_covered', fldname_xl='x2l_Sg_ice_covered'):
    """
    given a coupler history file, opened as Xarray dataset, 
    print both the LAND and GLC glacier cover extent in km^2
    
    By default, take the cell area from the mapping file
    """
    glc_area = ds[area_xg].squeeze()
    lnd_area = ds[area_xl].squeeze()

    # convert area to km^2
    glc_area_km = area_rad_to_km(glc_area) 
    lnd_area_km = area_rad_to_km(lnd_area)
    
    # xg 
    xgIceCov = ds[fldname_xg].squeeze()
    
    # xl
    xlIceCov = np.ma.zeros(lnd_area.shape)
    varname_pattern = fldname_xl + '{ec:02d}' # EC variable

    for i in range(1,11): # loop over ECs
        varname = varname_pattern.format(ec=i)
        xlIceCov += ds[varname].squeeze().to_masked_array()
        
    tot_cplg = (xgIceCov.to_masked_array() * glc_area_km.values).sum()
    tot_cpll = (xlIceCov * lnd_area_km.values).sum()
    print('CPL-G, :', tot_cplg)
    print('CPL-L, :', tot_cpll)
    print('ratio CPL-L / CPL-G :', tot_cpll/tot_cplg)