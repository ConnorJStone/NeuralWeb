import numpy as npx
from random import randint

class Neuron():
    resettime = 3

    #----- initiallization
    def __init__(self, name, position):
        #print 'Neuron: name: ' + str(name)
        #print 'Neuron: position: ' + str(position)
        self.name = name
        self.threshold = 1
        self.excitation = np.zeros(Neuron.resettime)
        self.state = [False,False]
        self.position = np.array(position)
        self.dendrites = []
        
    #----- Make dendrites
    def AddConnection(self, dendrite):
        for d in self.dendrites:
            if d.GetName() == dendrite.GetName():
                return

        self.dendrites.append(dendrite)

    def Reconnect(self, dendrites):
        self.dendrites = dendrites

    #----- Dendrites
    def ChangeInteraction(self):
        for d in self.dendrites:
            d.ChangeInteraction(randint(0,2))

    def Crosses(self, coefficients):
        for d in self.dendrites:
            if d.Crosses(coefficients):
                return True
        return False

    #----- Reset functions
    def ResetDendriteDidfire(self):
        for d in self.dendrites:
            d.ResetDidfire()

    def ResetExcitation(self):
        self.excitation[-1] -= self.threshold

    def FullReset(self):
        self.state = [False, False]
        self.excitation *= 0 
        for d in self.dendrites:
            d.ResetDidfire()
        
    #----- Main loop                
    def TimeStep(self):
        self.state = [self.state[1],False]
        self.excitation[:-1] = self.excitation[1:]
        self.excitation[-1] = 0

    def SendSignal(self):
        for d in self.dendrites:
            d.SendSignal(1)
            
    def Excite(self,signal):
        self.excitation[-1] += signal

    def Activate(self):
        if np.sum(self.excitation) > self.threshold:
            self.ResetExcitation()
            self.state[1] = True
            return True
        else:
            return False

    def Dopamine(self):
        for d in self.dendrites:
            d.Dopamine()

    def Histamine(self):
        for d in self.dendrites:
            d.Histamine()
            
    def Prune(self):
        survivingdendrittes = []
        for d in self.dendrites:
            if not d.Prune():
                survivingdendrittes.append(d)

        self.dendrites = survivingdendrittes

    #----- Status
    def GetState(self):
        return self.state[0]

    def IsDead(self):
        return len(self.dendrites) < float(self.threshold)/Neuron.resettime

    #----- Input Neuron method
    def SetState(self, newstate):
        self.state[0] = newstate
