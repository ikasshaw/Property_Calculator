import CoolProp.CoolProp as cp
from CoolProp.Plots import PropertyPlot

# plot = PropertyPlot('Water', 'ph')
# plot.calc_isolines()
# plot.show()    

prop_wanted_type = 'V'
prop_1_type = 'T'
prop_2_type = 'P'
prop_1_val = 293
prop_2_val = 101325
wantedFluid = "air"


print(cp.PropsSI(prop_wanted_type, prop_1_type,prop_1_val,prop_2_type,prop_2_val,wantedFluid))
