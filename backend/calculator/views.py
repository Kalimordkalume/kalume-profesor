from django.shortcuts import render
from rest_framework.decorators import APIView
from .forms import CreateEnergyForm
from math import trunc
# Create your views here.



class EnergyView(APIView):

    def get(self,request):
        form = CreateEnergyForm()
        return render(request,'calculator_home.html',context={'form':form})
        
        
    def post(self,request):
        form = CreateEnergyForm(request.POST)

        if form.is_valid():
            
            planets_count = form.cleaned_data['planets']
            fusion_level = form.cleaned_data['fusion']
            energy_level = form.cleaned_data['energy']
            commander_status = form.cleaned_data['commander']
            engineer_status = form.cleaned_data['engineer']
            life_form = form.cleaned_data['life_form_type']
            life_level = form.cleaned_data['life_form_level']
            steps = form.cleaned_data['steps']
            result_to_render = self.next_steps(
                desired_steps=steps,
                fusion_level=fusion_level,
                energy_level=energy_level,
                lf_level=life_level,
                lf_type=life_form,
                planets=planets_count,
                engineer_status=engineer_status,
                command_staff_status=commander_status
                )
            
            
            return render(request,'calculator_home.html',{'form':form,'results':result_to_render})

    
    def rythm(self, numerator: float, denominator: float):
        """This function will take two arguments and will calculate its ratio"""
        if denominator == 0:
            return float("inf")
        else:
            return numerator / denominator
    
    
    def next_steps(
        self,desired_steps,fusion_level,energy_level,lf_level,lf_type,planets,engineer_status,command_staff_status
    ):
        resultados = {}
        msgs = []
        for step in range(1, desired_steps + 1):
            production_if_fusion = self.get_energy_production(
                bonus=self.get_energy_bonus(
                    building_level=lf_level,
                    life_form_type=lf_type,
                    engineer_status=engineer_status,
                    commander_status=command_staff_status
                ),
                energy_sources=self.get_fusion_energy(
                    fusion_level=fusion_level + 1,
                    tech_energy_level=energy_level,
                ),
            )
            production_if_tech = self.get_energy_production(
                bonus=self.get_energy_bonus(
                    building_level=lf_level,
                    life_form_type=lf_type,
                    engineer_status=engineer_status,
                    commander_status=command_staff_status
                ),
                energy_sources=self.get_fusion_energy(
                    fusion_level=fusion_level, tech_energy_level=energy_level + 1
                ),
            )
            production_if_life = self.get_energy_production(
                bonus=self.get_energy_bonus(
                    building_level=lf_level + 1,
                    life_form_type=lf_type,
                    engineer_status=engineer_status,
                    commander_status=command_staff_status
                ),
                energy_sources=self.get_fusion_energy(
                    fusion_level=fusion_level, tech_energy_level=energy_level
                ),
            )
            current_production = self.get_energy_production(
                bonus=self.get_energy_bonus(
                    building_level=lf_level,
                    life_form_type=lf_type,
                    engineer_status=engineer_status,
                    commander_status=command_staff_status
                ),
                energy_sources=self.get_fusion_energy(
                    fusion_level=fusion_level, tech_energy_level=energy_level
                ),
            )

            production_difference_if_fusion = abs(
                current_production - production_if_fusion
            )
            production_difference_if_energy_tech = abs(
                current_production - production_if_tech
            )
            production_difference_if_life_form = abs(
                current_production - production_if_life
            )

            next_converted_cost_for_fusion = self.conversor(
                quantity=self.get_fusion_plant_cost(plant_level=fusion_level)
            )
            next_converted_cost_for_energy = self.conversor(
                quantity=self.get_energy_tech_cost(energy_level=energy_level)
            )
            next_converted_cost_for_life_form = self.conversor(
                quantity=self.get_life_form_building_cost(
                    life_form_type=lf_type,building_level=lf_level
                )
            )
            
            next_converted_cost_for_life_form = self.conversor(
                quantity=self.get_life_form_building_cost(lf_type,lf_level)
            )

            fusion_rythm = self.rythm(
                denominator=production_difference_if_fusion,
                numerator=next_converted_cost_for_fusion * planets,
            )
            energy_tech_rythm = self.rythm(
                denominator=production_difference_if_energy_tech,
                numerator=next_converted_cost_for_energy,
            )
            life_form_rythm = self.rythm(
                denominator=production_difference_if_life_form,
                numerator=next_converted_cost_for_life_form * planets,
            )

            # A esta altura el bucle debe saber cuál es la mejor tasa y arrojarla.

            # Updateamos los valores:
            resultados.update({"fusion": fusion_rythm})
            resultados.update({"energy_tech": energy_tech_rythm})
            resultados.update({"life_form": life_form_rythm})

            # Escogemos el mínimo:

            resultado = min(resultados, key=resultados.get)
            
            if resultado == "energy_tech":
                msg = f"Tecno de energía: {energy_level+1}.\n"
                msgs.append(msg)
                energy_level += 1
                print(msg)
                continue
            elif resultado == "fusion":
                msg = f"Planta de fusión: {fusion_level+1}.\n"
                msgs.append(msg)
                fusion_level += 1
                print(msg)
                continue
            else:
                msg = f"LifeForms: {lf_level+1}.\n"
                msgs.append(msg)
                lf_level += 1
                print(msg)
                continue
    
        return msgs
            

    
    def get_energy_bonus(self,life_form_type:str, building_level:int, engineer_status:bool,commander_status:bool):
        
        COMMANDER_BONUS = 0.02
        ENGINEER_BONUS = 0.1
        CHAMBER_BONUS = 0.015
        TRANSFORMER_BONUS = 0.01
        
        bonus = 1
        
        if commander_status:
            bonus += COMMANDER_BONUS
        
        if engineer_status:
            bonus += ENGINEER_BONUS
        
        if life_form_type == '2':
            bonus += CHAMBER_BONUS * building_level
        
        if life_form_type == '4':
            bonus += TRANSFORMER_BONUS * building_level
            
        
        
        return round(bonus,3)
    
    
    
    def get_fusion_energy(self, fusion_level: int, tech_energy_level: int):
        return trunc(
            30 * fusion_level * (0.01 * tech_energy_level + 1.05) ** fusion_level
        )
    
    def get_fusion_plant_cost(self, plant_level: int):
        basic_cost = {"M": 900, "C": 360, "D": 180}
        upgrade_factor = 1.8

        if plant_level < 0:
            raise ValueError(
                f"{plant_level=},no es un argumento válido, ingrese un número mayor a 0."
            )
        elif plant_level == 0:
            return basic_cost
        else:
            metal_cost = trunc((basic_cost.get("M") * upgrade_factor ** (plant_level)))
            crystal_cost = trunc(
                (basic_cost.get("C") * upgrade_factor ** (plant_level))
            )
            deuterium_cost = trunc(
                (basic_cost.get("D") * upgrade_factor ** (plant_level))
            )
            final_dict = {"M": metal_cost, "C": crystal_cost, "D": deuterium_cost}

            return final_dict
    
    def get_energy_tech_cost(self, energy_level: int):
        basic_cost = {"M": 0, "C": 800, "D": 400}
        upgrade_factor = 2

        if energy_level < 0:
            raise ValueError(
                f"{energy_level=},no es un argumento válido, ingrese un número mayor a 0."
            )
        elif energy_level == 0:
            return basic_cost
        else:
            metal_cost = trunc(
                (basic_cost.get("M") * (upgrade_factor ** (energy_level)))
            )
            crystal_cost = trunc(
                (basic_cost.get("C") * (upgrade_factor ** (energy_level)))
            )
            deuterium_cost = trunc(
                (basic_cost.get("D") * (upgrade_factor ** (energy_level)))
            )
            final_dict = {"M": metal_cost, "C": crystal_cost, "D": deuterium_cost}

            return final_dict
        
        
    
    
    def get_life_form_building_cost(self,life_form_type:str,building_level:int):
        
        rock = {"M": 20_000, "C": 15_000, "D": 10_000}
        rock_factor = 1.2
        
        mecha = {"M":35_000, "C":15_000,"D":10_000}
        mecha_factor = 1.5
        
        if life_form_type == '2':
            if building_level == 0:
                return rock
            else:
                metal_cost = trunc(
                    (rock.get("M") * rock_factor ** (building_level - 1))
                    * building_level
                )

                crystal_cost = trunc(
                    (rock.get("C") * rock_factor ** (building_level - 1))
                    * building_level
                )
                deuterium_cost = trunc(
                    (rock.get("D") * rock_factor ** (building_level - 1))
                    * building_level
                )
                final_dict = {"M": metal_cost, "C": crystal_cost, "D": deuterium_cost}
                
                return final_dict
        else:
            if building_level == 0:
                return mecha
            else:
                metal_cost = trunc(
                    (mecha.get("M") * mecha_factor ** (building_level - 1))
                    * building_level
                )

                crystal_cost = trunc(
                    (mecha.get("C") * mecha_factor ** (building_level - 1))
                    * building_level
                )
                deuterium_cost = trunc(
                    (mecha.get("D") * mecha_factor ** (building_level - 1))
                    * building_level
                )
                final_dict = {"M": metal_cost, "C": crystal_cost, "D": deuterium_cost}
                
                return final_dict

                
    def get_energy_production(self, bonus, energy_sources):
        total = trunc(bonus * energy_sources)
        return total
    
    def conversor(self, quantity: dict[str:int]) -> float:
        return quantity["M"] + quantity["C"] * 1.5 + quantity["D"] * 3