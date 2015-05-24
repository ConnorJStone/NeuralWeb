import numpy as np
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

    def DendritesPlotable(self):
        x = []
        y = []
        z = []
        for d in self.dendrites:
            xt,yt,zt = d.Positions()
            x.append(xt)
            y.append(yt)
            z.append(zt)
        return x,y,z
            
    #----- Reset functions
    def ResetDendriteDidfire(self):
        for d in self.dendrites:
            d.ResetDidfire()

    def ResetExcitation(self):
        self.excitation = np.zeros(Neuron.resettime)
        
    #----- Main loop                
    def TimeStep(self):
        self.state = [self.state[1],False]
        self.excitation[:-1] = self.excitation[1:]
        self.excitation[-1] = 0

    def Activate(self):
        for d in self.dendrites:
            self.excitation[-1] += d.GetSignal()
        if np.sum(self.excitation) > self.threshold:
            self.ResetExcitation()
            self.state[1] = True

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
