class Battery:
    def __init__(self, soc):
        
        self.capacity = 40
        self.soc = soc
        self.max_charge_power = 5
        self.max_discharge_power = 5
        self.efficiency = 0.9
        self.soc_min = 20
        self.soc_max = 90

    def charge(self, solar, demande):

        charge = 0
        surplus = solar - demande
        stored_energy =  self.soc / 100 * self.capacity
        remimnig = self.capacity - stored_energy
        if(solar > demande and self.soc < self.soc_max ):
            if(surplus < self.max_charge_power):
                charge =  surplus * self.efficiency
                if(charge <= remimnig): 
                    self.soc = stored_energy + charge
                    self.soc =  100/self.capacity * self.soc 
            else :
                charge = self.max_charge_power * self.efficiency
                if(charge <= remimnig): 
                    self.soc = stored_energy + charge 
                    self.soc =  100/self.capacity * self.soc

            

    def discharge(self, solar, demande):
        deficit =  demande - solar
        stored_energy =  self.soc / 100 * self.capacity
        minimum_energy = self.capacity  * (self.soc_min/100)
        available = stored_energy - minimum_energy

        if(solar < demande and self.soc > self.soc_min ):
            if(deficit < self.max_discharge_power):
                discharge =  deficit / self.efficiency
                if(discharge <= available): 
                    self.soc = stored_energy - discharge
                    self.soc =  100/self.capacity * self.soc 
                else :
                    discharge = self.max_discharge_power / self.efficiency
                    if discharge <= available :
                        self.soc = stored_energy - discharge 
                        self.soc =  100/self.capacity * self.soc
                    else :
                        discharge = available
                        stored_energy -= discharge
                        self.soc = self.soc_min
