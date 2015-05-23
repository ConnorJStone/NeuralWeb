from WebClass import Web
import numpy as np

# Create a rectangular prism with input neurons at the base, and output neurons at the top
def Rectangle(ninput, noutput, nx, ny, nz, r):

    inputneuronlocations = []
    interneuronlocations = []
    outputneuronlocations = []

    inxdistance, inydistance = IdealRectanglePlacement(nx,ny,ninput)
    currentlocation = [inxdistance/2.0, inydistance/2.0,0]
    for i in range(ninput):
        inputneuronlocations.append(currentlocation)
        if currentlocation[0] + inxdistance < nx:
            currentlocation[0] += inxdistance
        else:
            currentlocation[1] += inydistance

    for x in range(nx):
        for y in range(ny):
            for z in range(1,nz-1):
                interneuronlocations.append([x,y,z])

    outxdistance, outydistance = IdealRectanglePlacement(nx,ny,noutput)
    currentlocation = [outxdistance/2.0, outydistance/2.0,nz-1]
    for i in range(noutput):
        outputneuronlocations.append(currentlocation)
        if currentlocation[0] + outxdistance < nx:
            currentlocation[0] += outxdistance
        else:
            currentlocation[1] += outydistance

    return Web(inputneuronlocations, interneuronlocations, outputneuronlocations, r)

    
def IdealRectanglePlacement(nx, ny, nlocations):
    
    evenlocations = int(nlocations) if nlocations%2 == 0 else int(nlocations+1)
    xinitialization = int(nx) if nx > np.sqrt(float(nx)*evenlocations/ny) else int(np.sqrt(float(nx)*evenlocations/ny))
    
    while (float(evenlocations)/xinitialization)%1 != 0:
        xinitialization -= 1

    yinitialization = evenlocations/xinitialization
    xdistance = float(nx-1)/xinitialization
    ydistance = float(ny-1)/yinitialization

    return xdistance, ydistance
    

# Create a truncated pyrimid where the input neurons form the closest approximation of a square at the base, and the output neurons form the closest approximation of a square at the top. only the number of input and output neurons is required, the dimensions are determined by the pyramid constraint

# Create a sphere of neurons with the input at the center, and the output on the surface
