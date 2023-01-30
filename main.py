import kivy
from kivy.config import Config
Config.set('graphics', 'resizable', False)
from kivy.core.window import Window
Window.size = (800, 600)
from kivy.app import App
from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
import CoolProp as cp

class MainLayout(BoxLayout):

    def __init__(self, **kwargs):
        super(MainLayout, self).__init__(**kwargs)
        Clock.schedule_once(self._finish_init)

    def _finish_init(self, dt):

        self.wantedFluid = None
        self.prop_1_type = None
        self.prop_2_type = None
        self.prop_wanted_type = None

        self.prop_1_val = None
        self.prop_2_val = None
        self.prop_wanted_value = None

        self.prop_1_units = None
        self.prop_2_units = None
        self.prop_wanted_units = None

        self.previous_units = "SI"

        submit_button = ObjectProperty(None)

        fluid_spinner = ObjectProperty(None)

        units_radio_si = ObjectProperty(None)
        units_radio_us = ObjectProperty(None)

        prop_1 = ObjectProperty(None)   # drop down selection
        prop_1_input = ObjectProperty(None) # property text
        prop_1_units = ObjectProperty(None) # property units

        prop_2 = ObjectProperty(None) # drop down selection
        prop_2_input = ObjectProperty(None) # property text
        prop_2_units = ObjectProperty(None) # property units

        prop_wanted = ObjectProperty(None) # drop down selection
        prop_wanted_value = ObjectProperty(None) # property text
        prop_wanted_units = ObjectProperty(None) # property units

        # Trivial Properties   

        ACENTRIC = ObjectProperty(None)
        # DIPOLE_MOMENT = ObjectProperty(None)
        # FH = ObjectProperty(None)
        # FRACTION_MAX = ObjectProperty(None)
        # FRACTION_MIN = ObjectProperty(None)
        GAS_CONSTANT = ObjectProperty(None)
        MOLARMASS = ObjectProperty(None)
        PCRIT = ObjectProperty(None)
        # PH = ObjectProperty(None)
        PMAX = ObjectProperty(None)
        PMIN = ObjectProperty(None)
        PTRIPLE = ObjectProperty(None)
        P_REDUCING = ObjectProperty(None)
        # RHOCRIT = ObjectProperty(None)
        # RHOMASS_REDUCING = ObjectProperty(None)
        # RHOMOLAR_CRITICAL = ObjectProperty(None)
        # RHOMOLAR_REDUCING = ObjectProperty(None)
        TCRIT = ObjectProperty(None)
        TMAX = ObjectProperty(None)
        TMIN = ObjectProperty(None)
        TTRIPLE = ObjectProperty(None)
        T_FREEZE = ObjectProperty(None)
        T_REDUCING = ObjectProperty(None)

        self.convert_given_properties()
        self.submit_button_pressed()

    def convert(self,factor, value):
        return value * factor

    def get_conversion_factors(self, kind, current_units):

        try:

            factor = -1
            scale_factor = -1
            units = "-1"

            temp_factor = 1
            energy_per_mass_factor = 1
            pressure_factor = 1
            density_factor = 1

            temp_scaler = 1
            energy_per_mass_scaler = 1000
            pressure_scaler = 1000
            density_scaler = 1

            if self.ids.units_radio_si.state == "down":
                # self.previous_units = "SI"

                #If the button changed from US, then we need to convert from US to SI
                if self.previous_units == "US":
                    temp_factor = 5/9
                    energy_per_mass_factor = 2.32599999994858
                    pressure_factor = 6.89475728
                    density_factor = 16.01846337396

                # Used to convert from SI display units to correctly scaled SI units for calculation
                    temp_scaler = 1
                    energy_per_mass_scaler = 1000
                    pressure_scaler = 1000
                    density_scaler = 1

                if kind == "T":
                    factor = temp_factor
                    scale_factor = temp_scaler
                    units = "K"
                elif kind == "UMASS" or kind == "H" or kind == "SMASS":
                    factor = energy_per_mass_factor
                    scale_factor = energy_per_mass_scaler
                    units = "kJ/kg"
                elif kind == "P":
                    factor = pressure_factor
                    scale_factor = pressure_scaler
                    units = "KPa"
                elif kind == "D":
                    factor = density_factor
                    scale_factor = density_scaler
                    units = "kg/m^3"
                elif kind == "Q":
                    factor = 1
                    scale_factor = 1
                    units = " "

            elif self.ids.units_radio_us.state == "down":
                # self.previous_units = "US"
                if self.previous_units == "SI":
                    temp_factor = 9/5
                    energy_per_mass_factor = 1/2.32599999994858
                    pressure_factor = 1/6.89475728
                    density_factor = 1/16.01846337396

                # Used to convert from US display units to correctly scaled si units for calculation
                temp_scaler = 5/9
                energy_per_mass_scaler = 1000 * 2.32599999994858
                pressure_scaler = 1000 * 6.89475728
                density_scaler = 16.01846337396

                if kind == "T":
                    factor = temp_factor
                    scale_factor = temp_scaler
                    units= "R"
                elif kind == "UMASS" or kind == "H" or kind == "SMASS":
                    factor = energy_per_mass_factor
                    scale_factor = energy_per_mass_scaler
                    units = "BTU/lbm"
                elif kind == "P":
                    factor = pressure_factor
                    scale_factor = pressure_scaler
                    units = "psia"
                elif kind == "D":
                    factor = density_factor
                    scale_factor = density_scaler
                    units = "lb/ft^3"
                elif kind == "Q":
                    factor = 1
                    scale_factor = 1
                    units = " "
            return factor, scale_factor, units

        except Exception as e:
            print(e)
        
    def get_wanted_property_conversion_factors(self, kind):

        try:
            scale_factor = -1
            units = "-1"

            if self.ids.units_radio_si.state == "down":

                # Used to convert from SI display units to correctly scaled SI units for calculation
                temp_scaler = 1
                energy_per_mass_scaler = 1/1000
                pressure_scaler = 1/1000
                density_scaler = 1

                if kind == "T":
                    scale_factor = temp_scaler
                    units = "K"
                elif kind == "UMASS" or kind == "H" or kind == "SMASS":
                    scale_factor = energy_per_mass_scaler
                    units = "kJ/kg"
                elif kind == "P":
                    scale_factor = pressure_scaler
                    units = "KPa"
                elif kind == "D":
                    scale_factor = density_scaler
                    units = "kg/m^3"
                elif kind == "V":
                    scale_factor = 1
                    units = "Pa s"
                elif kind == "Q" or kind == "Z":
                    scale_factor = 1
                    units = " "

            elif self.ids.units_radio_us.state == "down":

                temp_factor = 9/5
                energy_per_mass_factor = 1/2.32599999994858
                pressure_factor = 1/6.89475728
                density_factor = 1/16.01846337396

                # Used to convert from US display units to correctly scaled si units for calculation
                temp_scaler = temp_factor
                energy_per_mass_scaler = energy_per_mass_factor / 1000
                pressure_scaler = pressure_factor / 1000
                density_scaler = density_factor

                if kind == "T":
                    scale_factor = temp_scaler
                    units= "R"
                elif kind == "UMASS" or kind == "H" or kind == "SMASS":
                    scale_factor = energy_per_mass_scaler
                    units = "BTU/lbm"
                elif kind == "P":
                    scale_factor = pressure_scaler
                    units = "psia"
                elif kind == "D":
                    scale_factor = density_scaler
                    units = "lb/ft^3"
                elif kind == "V":
                    scale_factor = pressure_scaler * 144
                    units = "psf s"
                elif kind == "Q" or kind == "Z":
                    scale_factor = 1
                    units = " "

            return scale_factor, units

        except Exception as e:
            print(e)
        pass

    def convert_given_properties(self):

        try:

            self.wantedFluid = self.ids.fluid_spinner.text
            self.prop_1_type = self.ids.prop_1.text
            self.prop_2_type = self.ids.prop_2.text
            self.prop_wanted_type = self.ids.prop_wanted.text

            prop_1_factor, prop_1_scale_factor, prop_1_units = self.get_conversion_factors(self.prop_1_type, self.ids.prop_1_units.text)
            prop_2_factor, prop_2_scale_factor, prop_2_units = self.get_conversion_factors(self.prop_2_type, self.ids.prop_2_units.text)

            # self.ids.prop_1_input.text = str(round(self.convert(prop_1_factor, prop_1_value), 3))
            self.ids.prop_1_input.text = str(self.convert(prop_1_factor, float(self.ids.prop_1_input.text)))
            self.ids.prop_1_units.text = prop_1_units
            self.ids.prop_1_input.cursor = (0, 0)

            # self.ids.prop_2_input.text = str(round(self.convert(prop_2_factor, prop_2_value), 3))
            self.ids.prop_2_input.text = str(self.convert(prop_2_factor, float(self.ids.prop_2_input.text)))
            self.ids.prop_2_units.text = prop_2_units
            self.ids.prop_2_input.cursor = (0, 0)

            self.prop_1_val = self.convert(prop_1_scale_factor, float(self.ids.prop_1_input.text))
            self.prop_2_val = self.convert(prop_2_scale_factor, float(self.ids.prop_2_input.text))

            # self.submit_button_pressed()

        except Exception as e:
            print(e)

    def submit_button_pressed(self):

        print("Submit button pressed")

        try:

            conversion_factor, units = self.get_wanted_property_conversion_factors(self.prop_wanted_type)

            wanted_value = conversion_factor * cp.CoolProp.PropsSI(self.prop_wanted_type,self.prop_1_type,self.prop_1_val,self.prop_2_type,self.prop_2_val,self.wantedFluid)

            if wanted_value <= .01:
                scientific_notation="{:.3e}".format(float(wanted_value))
                wanted_value = scientific_notation
                # print(scientific_notation)
                self.ids.prop_wanted_value.text = wanted_value

            else:
                self.ids.prop_wanted_value.text = str(round(wanted_value, 3))
            self.ids.prop_wanted_units.text = units

            self.ids.ACENTRIC.text = self.set_trivial("ACENTRIC")
            self.ids.GAS_CONSTANT.text = self.set_trivial("GAS_CONSTANT")
            self.ids.MOLARMASS.text = self.set_trivial("MOLARMASS")
            self.ids.PCRIT.text = self.set_trivial("PCRIT")
            self.ids.PMAX.text = self.set_trivial("PMAX")
            self.ids.PMIN.text = self.set_trivial("PMIN")
            self.ids.PTRIPLE.text = self.set_trivial("PTRIPLE")
            self.ids.P_REDUCING.text = self.set_trivial("P_REDUCING")
            self.ids.TCRIT.text = self.set_trivial("TCRIT")
            self.ids.TMAX.text = self.set_trivial("TMAX")
            self.ids.TMIN.text = self.set_trivial("TMIN")
            self.ids.TTRIPLE.text = self.set_trivial("TTRIPLE")
            self.ids.T_FREEZE.text = self.set_trivial("Tmin")
            self.ids.T_REDUCING.text = self.set_trivial("T_REDUCING")

            # self.ids.DIPOLE_MOMENT.text = self.set_trivial("DIPOLE_MOMENT")
            # self.ids.PH.text = self.set_trivial("PH")
            # self.ids.RHOCRIT.text = self.set_trivial("RHOCRIT")
            # self.ids.RHOMASS_REDUCING.text = self.set_trivial("RHOMASS_REDUCING")
            # self.ids.RHOMOLAR_CRITICAL.text = self.set_trivial("RHOMOLAR_CRITICAL")
            # self.ids.RHOMOLAR_REDUCING.text = self.set_trivial("RHOMOLAR_REDUCING")
                    
        except Exception as e:
            print(e)
            self.ids.prop_wanted_units.text = "Error"

            # self.ids.error_output.text = str(e)


    def set_trivial(self, property):

        try:
            return str(round(cp.CoolProp.PropsSI(property, self.wantedFluid), 4))
        except Exception as e:
            # print(e)
            return "N/A"

class TheLabApp(App):
    def build(self):
        return MainLayout()

TheLabApp().run()





# # Converts users input from US to SI
#     def convert_US_to_SI(self):

#         self.wantedFluid = self.ids.fluid_spinner.text
#         self.prop_1_type = self.ids.prop_1.text
#         self.prop_2_type = self.ids.prop_2.text
#         self.prop_wanted_type = self.ids.prop_wanted.text

#         temp_factor = 5/9
#         energy_per_mass_factor = 2.32599999994858
#         pressure_factor = 6.89475728
#         density_factor = 16.01846337396

#     # Used to convert from SI display units to correctly scaled SI units for calculation
#         temp_scaler = 1
#         energy_per_mass_scaler = 1000
#         pressure_scaler = 1000
#         density_scaler = 1

#         prop_1_value = float(self.ids.prop_1_input.text)
#         prop_2_value = float(self.ids.prop_2_input.text)

#         try:
#             if self.ids.units_radio_si.state == "down" and self.previous_units == "US":
#                 self.previous_units = "SI"

#                 factor = 0
#                 scale_factor = 0
#                 units = ""

#                 # Property 1 Conversion
#                 if self.prop_1_type == "T":
#                     factor = temp_factor
                
#                     units = "K"
#                 elif self.prop_1_type == "UMASS" or self.prop_1_type == "H" or self.prop_1_type == "SMASS":
#                     factor = energy_per_mass_factor
#                     units = "kJ/kg"
#                 elif self.prop_1_type == "P":
#                     factor = pressure_factor
#                     units = "KPa"
#                 elif self.prop_1_type == "D":
#                     factor = density_factor
#                     units = "kg/m^3"
#                 elif self.prop_1_type == "Q":
#                     factor = 1
#                     units = " "

#                 # Property 2 Conversion
#                 if self.prop_2_type == "T":
#                     factor = temp_factor
#                     units = "K"
#                 elif self.prop_2_type == "UMASS" or self.prop_2_type == "H" or self.prop_2_type == "SMASS":
#                     factor = energy_per_mass_factor
#                     units = "kJ/kg"
#                 elif self.prop_2_type == "P":
#                     factor = pressure_factor
#                     units = "KPa"
#                 elif self.prop_2_type == "D":
#                     factor = density_factor
#                     units = "kg/m^3"
#                 elif self.prop_2_type == "Q":
#                     factor = 1
#                     units = " "


#                 self.ids.prop_1_input.text = str(self.convert(factor, prop_1_value))
#                 self.ids.prop_1_units.text = units
#                 self.ids.prop_2_input.text = str(self.convert(factor, prop_2_value))
#                 self.ids.prop_2_units.text = units
#             # self.submit_button_pressed()
#         except Exception as e:
#             print(e)
# Converts users input from SI to US
    # def convert_SI_to_US(self):

        # self.wantedFluid = self.ids.fluid_spinner.text
        # self.prop_1_type = self.ids.prop_1.text
        # self.prop_2_type = self.ids.prop_2.text
        # self.prop_wanted_type = self.ids.prop_wanted.text

        # temp_factor = 9/5
        # energy_per_mass_factor = 1/2.32599999994858
        # pressure_factor = 1/6.89475728
        # density_factor = 1/16.01846337396

        # # Used to convert from US display units to correctly scaled si units for calculation
        # temp_scaler = 1/temp_factor
        # energy_per_mass_scaler = 1000 * 1 / energy_per_mass_factor
        # pressure_scaler = 1000 * 1 / pressure_factor
        # density_scaler = 1 / density_factor

        # prop_1_value = float(self.ids.prop_1_input.text)
        # prop_2_value = float(self.ids.prop_2_input.text)

        # try:
            # if self.ids.units_radio_si.state == "down" and self.previous_units == "US":
            #     self.previous_units = "SI"

            #     # Property 1 Conversion
            #     if self.prop_1_type == "T":
            #         factor = temp_factor
            #         scale_factor = temp_scaler
            #         units= "R"
            #     elif self.prop_1_type == "UMASS" or self.prop_1_type == "H" or self.prop_1_type == "SMASS":
            #         factor = energy_per_mass_factor
            #         scale_factor = energy_per_mass_scaler
            #         units = "BTU/lbm"
            #     elif self.prop_1_type == "P":
            #         factor = pressure_factor
            #         scale_factor = pressure_scaler
            #         units = "psia"
            #     elif self.prop_1_type == "D":
            #         factor = density_factor
            #         scale_factor = density_scaler
            #         units = "lb/ft^3"
            #     elif self.prop_1_type == "Q":
            #         factor = 1
            #         scale_factor = 1
            #         units = " "

            #     # Property 2 Conversion
            #     if self.prop_2_type == "T":
            #         factor = temp_factor
            #         scale_factor = temp_scaler
            #         units = "R"
            #     elif self.prop_2_type == "UMASS" or self.prop_2_type == "H" or self.prop_2_type == "SMASS":
            #         factor = energy_per_mass_factor
            #         scale_factor = energy_per_mass_scaler
            #         units = "BTU/lbm"
            #     elif self.prop_2_type == "P":
            #         factor = pressure_factor
            #         scale_factor = pressure_scaler
            #         units = "psia"
            #     elif self.prop_2_type == "D":
            #         factor = density_factor
            #         scale_factor = density_scaler
            #         units = "lb/ft^3"
            #     elif self.prop_2_type == "Q":
            #         factor = 1
            #         scale_factor = 1
            #         units = " "

        #         prop_1_factor, prop_1_scale_factor, prop_1_units = self.convertist(self.prop_1_type, self.ids.prop_1_units.text)
        #         prop_2_factor, prop_2_scale_factor, prop_2_units = self.convertist(self.prop_2_type, self.ids.prop_2_units.text)

        #         self.ids.prop_1_input.text = str(self.convert(prop_1_factor, prop_1_value))
        #         self.ids.prop_1_units.text = prop_1_units
        #         self.prop_1_val = self.convert(prop_1_scale_factor, prop_1_value)

        #         self.ids.prop_2_input.text = str(self.convert(prop_2_factor, prop_2_value))
        #         self.ids.prop_2_units.text = prop_2_units        
        #         self.prop_2_val = self.scale_si_for_submit(prop_2_scale_factor, prop_2_value)

        # except Exception as e:
        #     print(e)

    # def convert_units(self):

    #     self.wantedFluid = self.ids.fluid_spinner.text
    #     self.prop_1_type = self.ids.prop_1.text
    #     self.prop_2_type = self.ids.prop_2.text
    #     self.prop_wanted_type = self.ids.prop_wanted.text

    #     try:
    #         if self.ids.units_radio_si.state == "down" and self.previous_units == "US":
    #             self.previous_units = "SI"

    #             if self.prop_1_type == "T":
    #                 self.ids.prop_1_input.text = str(5/9*float(self.ids.prop_1_input.text))
    #                 self.ids.prop_1_units.text = "R"
    #             elif self.prop_1_type == "UMASS":
    #                 self.ids.prop_1_input.text = str(2.32599999994858*float(self.ids.prop_1_input.text))
    #                 self.ids.prop_1_units.text = "kJ/kg"
    #             elif self.prop_1_type == "H":
    #                 self.ids.prop_1_input.text = str(2.32599999994858*float(self.ids.prop_1_input.text))
    #                 self.ids.prop_1_units.text = "kJ/kg"
    #             elif self.prop_1_type == "SMASS":
    #                 self.ids.prop_1_input.text = str(2.32599999994858*float(self.ids.prop_1_input.text))
    #                 self.ids.prop_1_units.text = "kJ/kg"
    #             elif self.prop_1_type == "P":
    #                 self.ids.prop_1_input.text = str(6.89475728*float(self.ids.prop_1_input.text))
    #                 self.ids.prop_1_units.text = "KPa"
    #             elif self.prop_1_type == "Q":
    #                 self.ids.prop_1_input.text = str(float(self.ids.prop_1_input.text))
    #                 self.ids.prop_1_units.text = " "
    #             elif self.prop_1_type == "D":
    #                 self.ids.prop_1_input.text = str(16.01846337396*float(self.ids.prop_1_input.text))
    #                 self.ids.prop_1_units.text = "kg/m^3"
                
    #             if self.prop_2_type == "T":
    #                 self.ids.prop_2_input.text = str(5/9*float(self.ids.prop_2_input.text))
    #                 self.ids.prop_2_units.text = "K"
    #             elif self.prop_2_type == "UMASS":
    #                 self.ids.prop_2_input.text = str(2.32599999994858*float(self.ids.prop_2_input.text))
    #                 self.ids.prop_2_units.text = "kJ/kg"
    #             elif self.prop_2_type == "H":
    #                 self.ids.prop_2_input.text = str(2.32599999994858*float(self.ids.prop_2_input.text))
    #                 self.ids.prop_2_units.text = "kJ/kg"
    #             elif self.prop_2_type == "SMASS":
    #                 self.ids.prop_2_input.text = str(2.32599999994858*float(self.ids.prop_2_input.text))
    #                 self.ids.prop_2_units.text = "kJ/kg"
    #             elif self.prop_2_type == "P":
    #                 self.ids.prop_2_input.text = str(6.89475728*float(self.ids.prop_2_input.text))
    #                 self.ids.prop_2_units.text = "KPa"
    #             elif self.prop_2_type == "Q":
    #                 self.ids.prop_2_input.text = str(float(self.ids.prop_2_input.text))
    #                 self.ids.prop_2_units.text = " "
    #             elif self.prop_2_type == "D":
    #                 self.ids.prop_2_input.text = str(6.01846337396*float(self.ids.prop_2_input.text))
    #                 self.ids.prop_2_units.text = "kg/m^3"
                
    #         # US units conversion
    #         elif self.ids.units_radio_us.state == "down" and self.previous_units == "SI":

    #             self.previous_units = "US"

    #             if self.prop_1_type == "T":
    #                 self.ids.prop_1_input.text = str(9/5*float(self.ids.prop_1_input.text))
    #                 self.ids.prop_1_units.text = "R"
                    
    #             elif self.prop_1_type == "UMASS":
    #                 self.ids.prop_1_input.text = str(1/2.32599999994858*float(self.ids.prop_1_input.text))
    #                 self.ids.prop_1_units.text = "BTU/lbm"
                    
    #             elif self.prop_1_type == "H":
    #                 self.ids.prop_1_input.text = str(1/2.32599999994858*float(self.ids.prop_1_input.text))
    #                 self.ids.prop_1_units.text = "BTU/lbm"
                    
    #             elif self.prop_1_type == "SMASS":
    #                 self.ids.prop_1_input.text = str(1/2.32599999994858*float(self.ids.prop_1_input.text))
    #                 self.ids.prop_1_units.text = "BTU/lbm"
                    
    #             elif self.prop_1_type == "P":
    #                 self.ids.prop_1_input.text = str(1/6.89475728*float(self.ids.prop_1_input.text))
    #                 self.ids.prop_1_units.text = "psia"
                    
    #             elif self.prop_1_type == "Q":
    #                 self.ids.prop_1_input.text = str(float(self.ids.prop_1_input.text))
    #                 self.ids.prop_1_units.text = " "
                    
    #             elif self.prop_1_type == "D":
    #                 self.ids.prop_1_input.text = str(1/16.01846337396*float(self.ids.prop_1_input.text))
    #                 self.ids.prop_1_units.text = "lb/ft^3"
                                
    #             if self.prop_2_type == "T":
    #                 self.ids.prop_2_input.text = str(9/5*float(self.ids.prop_2_input.text))
    #                 self.ids.prop_2_units.text = "R"
                    
    #             elif self.prop_2_type == "UMASS":
    #                 self.ids.prop_2_input.text = str(1/2.32599999994858*float(self.ids.prop_2_input.text))
    #                 self.ids.prop_2_units.text = "BTU/lbm"
                    
    #             elif self.prop_2_type == "H":
    #                 self.ids.prop_2_input.text = str(1/2.32599999994858*float(self.ids.prop_2_input.text))
    #                 self.ids.prop_2_units.text = "BTU/lbm"
                    
    #             elif self.prop_2_type == "SMASS":
    #                 self.ids.prop_2_input.text = str(1/2.32599999994858*float(self.ids.prop_2_input.text))
    #                 self.ids.prop_2_units.text = "BTU/lbm"
                    
    #             elif self.prop_2_type == "P":
    #                 self.ids.prop_2_input.text = str(1/6.89475728*float(self.ids.prop_2_input.text))
    #                 self.ids.prop_2_units.text = "psia"
                    
    #             elif self.prop_2_type == "Q":
    #                 self.ids.prop_2_input.text = str(float(self.ids.prop_2_input.text))
    #                 self.ids.prop_2_units.text = " "
                    
    #             elif self.prop_2_type == "D":
    #                 self.ids.prop_2_input.text = str(1/16.01846337396*float(self.ids.prop_2_input.text))
    #                 self.ids.prop_2_units.text = "lb/ft^3"

    #         self.submit_button_pressed()
    #     except Exception as e:
    #         print(e)
        

        #     def units_setter(self):

        # self.wantedFluid = self.ids.fluid_spinner.text
        # self.prop_1_type = self.ids.prop_1.text
        # self.prop_2_type = self.ids.prop_2.text
        # self.prop_wanted_type = self.ids.prop_wanted.text

        # print(self.prop_1_type, self.prop_2_type, self.prop_wanted_type)

        # try:
        #     if self.ids.units_radio_si.state == "down":
        #         if self.prop_1_type == "T":
        #             self.prop_1_val = float(self.ids.prop_1_input.text)
        #             self.ids.prop_1_units.text = "K"
        #         elif self.prop_1_type == "UMASS":
        #             self.prop_1_val = 1000*float(self.ids.prop_1_input.text)
        #             self.ids.prop_1_units.text = "kJ/kg"
        #         elif self.prop_1_type == "H":
        #             self.prop_1_val = 1000*float(self.ids.prop_1_input.text)
        #             self.ids.prop_1_units.text = "kJ/kg"
        #         elif self.prop_1_type == "SMASS":
        #             self.prop_1_val = 1000*float(self.ids.prop_1_input.text)
        #             self.ids.prop_1_units.text = "kJ/kg"
        #         elif self.prop_1_type == "P":
        #             self.prop_1_val = 1000*float(self.ids.prop_1_input.text)
        #             self.ids.prop_1_units.text = "KPa"
        #         elif self.prop_1_type == "Q":
        #             self.prop_1_val = float(self.ids.prop_1_input.text)
        #             self.ids.prop_1_units.text = " "
        #         elif self.prop_1_type == "D":
        #             self.prop_1_val = float(self.ids.prop_1_input.text)
        #             self.ids.prop_1_units.text = "kg/m^3"
                
        #         if self.prop_2_type == "T":
        #             self.prop_2_val = float(self.ids.prop_2_input.text)
        #             self.ids.prop_2_units.text = "K"
        #         elif self.prop_2_type == "UMASS":
        #             self.prop_2_val = 1000*float(self.ids.prop_2_input.text)
        #             self.ids.prop_2_units.text = "kJ/kg"
        #         elif self.prop_2_type == "H":
        #             self.prop_2_val = 1000*float(self.ids.prop_2_input.text)
        #             self.ids.prop_2_units.text = "kJ/kg"
        #         elif self.prop_2_type == "SMASS":
        #             self.prop_2_val = 1000*float(self.ids.prop_2_input.text)
        #             self.ids.prop_2_units.text = "kJ/kg"
        #         elif self.prop_2_type == "P":
        #             self.prop_2_val = 1000*float(self.ids.prop_2_input.text)
        #             self.ids.prop_2_units.text = "KPa"
        #         elif self.prop_2_type == "Q":
        #             self.prop_2_val = float(self.ids.prop_2_input.text)
        #             self.ids.prop_2_units.text = " "
        #         elif self.prop_2_type == "D":
        #             self.prop_2_val = float(self.ids.prop_2_input.text)
        #             self.ids.prop_2_units.text = "kg/m^3"
                
        #     # US units conversion
        #     elif self.ids.units_radio_us.state == "down":

        #         if self.prop_1_type == "T":
        #             self.prop_1_val = 5/9*float(self.ids.prop_1_input.text)
        #             self.ids.prop_1_units.text = "R"
                    
        #         elif self.prop_1_type == "UMASS":
        #             self.prop_1_val = 2325.99999994858*float(self.ids.prop_1_input.text)
        #             self.ids.prop_1_units.text = "BTU/lbm"
                    
        #         elif self.prop_1_type == "H":
        #             self.prop_1_val = 2325.99999994858*float(self.ids.prop_1_input.text)
        #             self.ids.prop_1_units.text = "BTU/lbm"
                    
        #         elif self.prop_1_type == "SMASS":
        #             self.prop_1_val = 2325.99999994858*float(self.ids.prop_1_input.text)
        #             self.ids.prop_1_units.text = "BTU/lbm"
                    
        #         elif self.prop_1_type == "P":
        #             self.prop_1_val = 6894.75728*float(self.ids.prop_1_input.text)
        #             self.ids.prop_1_units.text = "psia"
                    
        #         elif self.prop_1_type == "Q":
        #             self.prop_1_val = float(self.ids.prop_1_input.text)
        #             self.ids.prop_1_units.text = " "
                    
        #         elif self.prop_1_type == "D":
        #             self.prop_1_val = 16.01846337396*float(self.ids.prop_1_input.text)
        #             self.ids.prop_1_units.text = "lb/ft^3"
                                
        #         if self.prop_2_type == "T":
        #             self.prop_2_val = 5/9*float(self.ids.prop_2_input.text)
        #             self.ids.prop_2_units.text = "R"
                    
        #         elif self.prop_2_type == "UMASS":
        #             self.prop_2_val = 2325.99999994858*float(self.ids.prop_2_input.text)
        #             self.ids.prop_2_units.text = "BTU/lbm"
                    
        #         elif self.prop_2_type == "H":
        #             self.prop_2_val = 2325.99999994858*float(self.ids.prop_2_input.text)
        #             self.ids.prop_2_units.text = "BTU/lbm"
                    
        #         elif self.prop_2_type == "SMASS":
        #             self.prop_2_val = 2325.99999994858*float(self.ids.prop_2_input.text)
        #             self.ids.prop_2_units.text = "BTU/lbm"
                    
        #         elif self.prop_2_type == "P":
        #             self.prop_2_val = 6894.75728*float(self.ids.prop_2_input.text)
        #             self.ids.prop_2_units.text = "psia"
                    
        #         elif self.prop_2_type == "Q":
        #             self.prop_2_val = float(self.ids.prop_2_input.text)
        #             self.ids.prop_2_units.text = " "
                    
        #         elif self.prop_2_type == "D":
        #             self.prop_2_val = 16.01846337396*float(self.ids.prop_2_input.text)
        #             self.ids.prop_2_units.text = "lb/ft^3"

        # except Exception as e:
        #     print(e)

        # print("a;sdf")
    