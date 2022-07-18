import CoolProp.CoolProp as cp

prop_wanted_type = 'D'
prop_1_type = 'S'
prop_2_type = 'U'
prop_1_val = 100000
prop_2_val = 42800
wantedFluid = "water"


# print(cp.PropsSI(prop_wanted_type, prop_1_type,prop_1_val,prop_2_type,prop_2_val,wantedFluid))
print(cp.PropsSI("DIPOLE_MOMENT", "Water"))