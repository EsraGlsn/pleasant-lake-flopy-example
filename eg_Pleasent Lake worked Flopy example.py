import numpy as np
import matplotlib; matplotlib.use('TKAgg')
import matplotlib.pyplot as plt
import flopy
import flopy.mf6 as mf6
from flopy.discretization import StructuredGrid
from flopy.utils import Raster
import sfrmaker


model_name = 'pleasant'
workspace = '.'

nper, nlay, nrow, ncol = 1,3,60,70
delr,delc = 40,40
xoffset, yoffset = 554400., 389200.0
epsg =3070


modelgrid = StructuredGrid(
    delr=np.ones(ncol) * delr,
    delc=np.ones(nrow) * delc,
    xoff=xoffset,yoff=yoffset, angrot=0)


br_surf = Raster.load('./data/br_surface.tif')
rs = br_surf.resample_to_grid(
    modelgrid, band=1, method='linear')
np.savetxt('data/botm_002.dat', rs)

top = [{'filename': 'data/top.dat'}]
botm = [{'filename': 'data/botm_000.dat'},
        {'filename': 'data/botm_001.dat'},
        {'filename': 'data/botm_002.dat'}]
# hydraulic conductivity
k = [{'filename': 'data/k_000.dat'},
     {'filename': 'data/k_001.dat'},
     {'filename': 'data/k_002.dat'}]
# vertical hydraulic conductivity
k33 = [{'filename': 'data/k33_000.dat'},
       {'filename': 'data/k33_001.dat'},
       {'filename': 'data/k33_002.dat'}]
# use the model top for starting heads
strt = [top[0]] * nlay
recharge = {
    0: {'filename': 'data/rch_000.dat'}}
irch = [{'filename': 'data/irch.dat'}]
spec_head_perimeter = {
    0: {'filename': 'data/chd_000.dat'}}



#Set up the model in Flopy

sim = mf6.MFSimulation(
    sim_name=model_name, version="mf6",
    exe_name="./bin/win/mf6.exe", sim_ws=workspace)

tdis = mf6.ModflowTdis(
    sim,time_units="days" , nper =1,
    perioddata=[(1.0,1,1.0)]
)

ims = mf6.ModflowIms(
    sim,complexity= "moderate",
    outer_dvclose=0.001
)


#crete the model instance

gwf = mf6.ModflowGwf(
    sim, modelname=model_name,
    save_flows=True)

#output control

oc = mf6.ModflowGwfoc(
    gwf, head_filerecord=f'{gwf.name}.hds',
    budget_filerecord=f'{gwf.name}.cbc',
    saverecord=[('head', 'all'), ("budget", "all")])

#set up the discratization package

dis = mf6.ModflowGwfdis(
    gwf,nlay=nlay,nrow=nrow,ncol=ncol,
    delr=delr, delc=delc,
    top=top,botm=botm, idomain=1)

#locate the model grid

gwf.modelgrid.set_coord_info(
    xoff=xoffset, yoff=yoffset, epsg=epsg)
gwf.modelgrid



#Assign aquifer properties

npf = mf6.ModflowGwfnpf(gwf, icelltype=1,k=k,k33=k33)

#Assign initial conditions

ic= mf6.ModflowGwfic(gwf, strt=strt)

#Assign Boundary Conditions


chd=mf6.ModflowGwfchd(
    gwf, stress_period_data=spec_head_perimeter)
rch = mf6.ModflowGwfrcha(
    gwf, recharge=recharge, irch=irch)

lak = mf6.ModflowGwflak(
    gwf,
    boundnames = True, nlakes = 1,
    connectiondata={
        'filename': 'data/lake_cn.dat'},
    packagedata=[[0, 290.85, 345, 'lake1']],
    perioddata={0: [
        [0, 'evaporation', 0.000715],
        [0, 'rainfall', 0.00209]]},
    surfdep=0.1)

# writing the SFR package
lines = sfrmaker.Lines.from_shapefile(
    shapefile='data/edited_flowlines.shp',
    id_column='id',
    routing_column='toid',
    width1_column='width1',
    width2_column='width2',
    name_column='name',
    attr_length_units='meters'
    )
#remove values of "None" geometry
lines.df = lines.df.drop(lines.df.index[lines.df.geometry == None])
sfrdata = lines.to_sfr(
    model=gwf,
    model_length_units='meters')
sfrdata.set_streambed_top_elevations_from_dem(
    'data/dem40m.tif',
    elevation_units='meters')
sfrdata.assign_layers()
sfr = sfrdata.create_mf6sfr(gwf)

sim.write_simulation()

sim.run_simulation()


from flopy.utils.postprocessing import get_water_table

hds = gwf.output.head().get_data()
wt = get_water_table(hds, hdry=-1e30)

cbc = gwf.output.budget()
lak = cbc.get_data(text='lak', full3D=True)[0]


fig, ax = plt.subplots(figsize=(10, 10))
pmv = flopy.plot.PlotMapView(gwf, ax=ax)
ctr = pmv.contour_array(
    wt, levels=np.arange(290, 315, 1),
    linewidths=1, colors='maroon')
labels = pmv.ax.clabel(
    ctr, inline=True,
    fontsize=8, inline_spacing=1)
vmin, vmax = -100, 100
im = pmv.plot_array(
    lak[0], cmap='rainbow_r',
    vmin=vmin, vmax=vmax)

cb = fig.colorbar(
    im, shrink=0.5, label='Leakage, in m$^3$/day')
ax.set_ylabel("Northing, WTM meters")
ax.set_xlabel("Easting, WTM meters")
ax.set_aspect(1)
plt.tight_layout()
plt.savefig('results.pdf')