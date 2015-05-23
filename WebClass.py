import numpy as np
from NeuronClass import Neuron
from DendriteClass import Dendrite
from math import sqrt
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

class Web():

    def __init__(self, inputneuronlocations, activeneuronlocations, outputneuronlocations, conectionradius):

        #----- initialization variables
        self.inputneurons = []
        self.activeneurons = []
        self.outputneurons = []

        count = 0
        for IN in inputneuronlocations:
            self.inputneurons.append(Neuron('input'+str(count), IN))
            count += 1
        count = 0
        for AN in activeneuronlocations:
            self.activeneurons.append(Neuron('active'+str(count), AN))
            count += 1
        count = 0
        for ON in outputneuronlocations:
            self.outputneurons.append(Neuron('output'+str(count), ON))
            count += 1

        #----- Create Dendrites
        print 'started making dendrites'
        for IN in self.inputneurons:
            for L2IN in self.inputneurons:
                if 0 < Distance(IN.position, L2IN.position) <= conectionradius:
                    IN.AddConnection(Dendrite(L2IN, IN))
            for AN in self.activeneurons:
                if Distance(IN.position, AN.position) <= conectionradius:
                    IN.AddConnection(Dendrite(AN, IN))
                    AN.AddConnection(Dendrite(IN, AN))
            for ON in self.outputneurons:
                if Distance(IN.position, ON.position) <= conectionradius:
                    IN.AddConnection(Dendrite(ON, IN))
                    ON.AddConnection(Dendrite(IN, ON))

        for AN in self.activeneurons:
            for L2AN in self.activeneurons:
                if 0 < Distance(AN.position, L2AN.position) <= conectionradius:
                    AN.AddConnection(Dendrite(L2AN, AN))
            for ON in self.outputneurons:
                if Distance(AN.position, ON.position) <= conectionradius:
                    AN.AddConnection(Dendrite(ON, AN))
                    ON.AddConnection(Dendrite(AN, ON))

        for ON in self.outputneurons:
            for L2ON in self.outputneurons:
                if 0 < Distance(ON.position, L2ON.position) <= conectionradius:
                    ON.AddConnection(Dendrite(L2ON, ON))

        print 'finished making dendrites'
        self.PlotSelf()

    #----- run initialization
    def Randomize(self):
        for IN in self.inputneurons:
            IN.ChangeInteraction()
        for AN in self.activeneurons:
            AN.ChangeInteraction()
        for ON in self.outputneurons:
            ON.ChangeInteraction()

    #----- main loop
    def Learn(self, inputstate, outputstate):
        keeplearning = True
        count = -1
        self.ResetWeb()
        self.Randomize()
        
        while keeplearning:
            count += 1
            if count > len(self.activeneurons)*20:
                print 'Randomization failed'
                break
            self.TimeStep()
            self.InputActivation(inputstate)
            self.ConnectionActivation()
            keeplearning = self.Reinforcement(outputstate)
            self.Prune()

    #----- main loop elements
    def ResetWeb(self):
        for IN in self.inputneurons:
            IN.ResetDendriteDidfire()
            IN.ResetExcitation()
        for AN in self.activeneurons:
            AN.ResetDendriteDidfire()
            AN.ResetExcitation()
        for ON in self.outputneurons:
            ON.ResetDendriteDidfire()
            ON.ResetExcitation()

    def TimeStep(self):
        for IN in self.inputneurons:
            IN.TimeStep()
        for AN in self.activeneurons:
            AN.TimeStep()
        for ON in self.outputneurons:
            ON.TimeStep()
    
    def InputActivation(self, inputstate):
        if len(inputstate) != len(self.inputneurons):
            raise ValueError('the length of the input state must be the same as the number of input neurons')
            
        for i in range(len(self.inputneurons)):
            if inputstate[i]:
                self.inputneurons[i].SetState(True)

    def ConnectionActivation(self):
        for IN in self.inputneurons:
            IN.Activate()
        for AN in self.activeneurons:
            AN.Activate()
        for ON in self.outputneurons:
            ON.Activate()

    def Reinforcement(self, outputstate):
        allfalse = True
        allcorrect = True
        for i in range(len(self.outputneurons)):
            if self.outputneurons[i].GetState() == True:
                allfalse = False
            if self.outputneurons[i].GetState() != outputstate[i]:
                allcorrect = False
            if not allcorrect and not allfalse:
                break

        if allcorrect:
            print 'all correct!!!!!!!!!!!!!!!!!!!!'
            self.Dopamine()
            return False
        elif not allfalse:
            print 'Got it wrong :('
            self.Histamine()
            return False
        else:
            return True

    #----- main loop reinforcement
    def Dopamine(self):
        for IN in self.inputneurons:
            IN.Dopamine()
        for AN in self.activeneurons:
            AN.Dopamine()
        for ON in self.outputneurons:
            ON.Dopamine()

    def Histamine(self):
        for IN in self.inputneurons:
            IN.Histamine()
        for AN in self.activeneurons:
            AN.Histamine()
        for ON in self.outputneurons:
            ON.Histamine()

    def Prune(self):
        for IN in self.inputneurons:
            IN.Prune()
        for AN in self.activeneurons:
            AN.Prune()
        for ON in self.outputneurons:
            ON.Prune()
            
    #----- Web maintenance
    def PlaneCrossing(self, coefficients):
        for AN in self.activeneurons:
            if AN.Crosses(coefficients):
                return True
        for ON in self.outputneurons:
            if ON.Crosses(coefficients):
                return True
        for IN in self.inputneurons:
            if IN.Crosses(coefficients):
                return True
        
    #----- Web plotting
    def PlotSelf(self, drawconnections = False):
        fig = plt.figure()
        ax = fig.add_subplot(111,projection='3d')
        x = []; y = []; z = []
        for IN in self.inputneurons:
            x.append(IN.position[0])
            y.append(IN.position[1])
            z.append(IN.position[2])
            if not drawconnections:
                continue
            for d in IN.dendrites:
                if d.currentinteraction == 0:
                    colour = 'b'
                elif d.currentinteraction == 1:
                    continue
                elif d.currentinteraction == 2:
                    colour = 'r'
                ax.plot(*d.Positions(),c=colour)
        ax.scatter(x,y,z,c='r',s=100)
        x = []; y = []; z = []
        for AN in self.activeneurons:
            x.append(AN.position[0])
            y.append(AN.position[1])
            z.append(AN.position[2])
            if not drawconnections:
                continue
            for d in AN.dendrites:
                if d.currentinteraction == 0:
                    colour = 'b'
                elif d.currentinteraction == 1:
                    continue
                elif d.currentinteraction == 2:
                    colour = 'r'
                ax.plot(*d.Positions(),c=colour)
        ax.scatter(x,y,z,c='b',s=100)
        x = []; y = []; z = []
        for ON in self.outputneurons:
            x.append(ON.position[0])
            y.append(ON.position[1])
            z.append(ON.position[2])
            if not drawconnections:
                continue
            for d in ON.dendrites:
                if d.currentinteraction == 0:
                    colour = 'b'
                elif d.currentinteraction == 1:
                    continue
                elif d.currentinteraction == 2:
                    colour = 'r'
                ax.plot(*d.Positions(),c=colour)
        ax.scatter(x,y,z,c='k',s=100)
        ax.set_xlabel('X axis')
        ax.set_ylabel('Y axis')
        ax.set_zlabel('Z axis')
        plt.show()
        
def DetermineOutputDimensions(boxdimensions, nlocations):
    
    areaperoutputneuron = boxdimensions[0]*boxdimensions[1]/float(nlocations)
    sideratio = boxdimensions[0]/float(boxdimensions[1])
    distancexdirection = sqrt(areaperoutputneuron/sideratio)
    distanceydirection = areaperoutputneuron/distancexdirection
    #distancexdirection = int(distancexdirection)

    if distanceydirection < 1 :
        distanceydirection = 0
        distancexdirection = boxdimensions[0]/nlocations
    elif distancexdirection < 1:
        distancexdirection = 0
        distanceydirection = boxdimensions[1]/nlocations
    elif boxdimensions[0] < 1 and boxdimensions[1] < 1:
        print 'you fool'

    return distancexdirection, distanceydirection

def Distance(position1, position2):
    return np.sqrt(np.sum((position1 - position2)**2))
