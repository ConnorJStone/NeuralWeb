import numpy as np

class Dendrite():

    maxstrength = 1000

    def __init__(self, toneuron, fromneuron):
        print 'Dendrite: connection to: ' + str(toneuron.name)
        print 'Dendrite: connection from: ' + str(fromneuron.name)
        #Initialize tracking parameters and store the neuron that it points to
        self.toneuron = toneuron
        self.fromneuron = fromneuron
        self.lock = False
        self.currentinteraction = 0
        self.interactions = [[1,0],[0,0],[-1,0]]
        self.didfire = False

    #----- Neuron info
    def GetSignal(self):
        if self.toneuron.GetState():
            self.didfire = True
            return self.interactions[self.currentinteraction][0]
        else:
            return 0

    def GetName(self):
        return self.toneuron.name

    def Crosses(self, coefficients):
        if self.currentinteraction in [1,2]:
            return False
        planerelative1 = np.sum(coefficients[:3]*self.toneuron.position) + coefficients[3] 
        planerelative2 = np.sum(coefficients[:3]*self.fromneuron.position) + coefficients[3]
        if planerelative1 > 0 and planerelative2 < 0:
            return True
        elif planerelative1 < 0 and planerelative2 > 0:
            return True
        else:
            return False

    def Positions(self):
        return [[self.toneuron.position[0],self.fromneuron.position[0]],[self.toneuron.position[1],self.fromneuron.position[1]],[self.toneuron.position[2],self.fromneuron.position[2]]]
        
    #----- Positive/Negative learning
    def Dopamine(self):#perhaps add scaling constant for how "strong" the dopamine/histamine is
        if self.didfire:
            self.Strengthen()

    def Histamine(self):
        if self.didfire:
            self.Weaken()
            
    def Strengthen(self):
        if self.lock:
            return
        else:
            self.interactions[self.currentinteraction][1] += 10
            if self.interactions[self.currentinteraction][1] >= Dendrite.maxstrength:
                self.lock = True
                print '---------------------Dendrite Locked-------------------------'
                
    def Weaken(self):
        if self.lock:
            return
        else:
            for i in self.interactions:
                if i[0] == self.currentinteraction:
                    i[1] -= 1
                else:
                    i[1] += 0.5

    #----- alter type to see effect
    def ChangeInteraction(self,newinteraction):
        if newinteraction in range(len(self.interactions)):
            if not self.lock:
                self.currentinteraction = newinteraction
        else:
            raise ValueError('This interaction is not possible: ' + str(newinteraction))
            
    def Prune(self):
        return self.interactions[1][1] >= Dendrite.maxstrength


    #----- reset functions
    def ResetDidfire(self):
        self.didfire = False
