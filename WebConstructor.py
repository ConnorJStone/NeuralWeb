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
        inputneuronlocations.append(np.array(currentlocation))
        if currentlocation[0] + inxdistance < nx-1:
            currentlocation[0] += inxdistance
        else:
            currentlocation[0] = inxdistance/2.0
            currentlocation[1] += inydistance

    for x in range(nx):
        for y in range(ny):
            for z in range(1,nz-1):
                interneuronlocations.append([x,y,z])

    outxdistance, outydistance = IdealRectanglePlacement(nx,ny,noutput)
    currentlocation = [outxdistance/2.0, outydistance/2.0,nz-1]
    for i in range(noutput):
        outputneuronlocations.append(np.array(currentlocation))
        if currentlocation[0] + outxdistance < nx-1:
            currentlocation[0] += outxdistance
        else:
            currentlocation[0] = outxdistance/2.0
            currentlocation[1] += outydistance

    return Web(inputneuronlocations, interneuronlocations, outputneuronlocations, r)

    
def IdealRectanglePlacement(nx, ny, nlocations):
    
    factorablenlocations = int(nlocations+1) if isprime(nlocations) else int(nlocations)
    print 'even location:' + str(factorablenlocations)
    xinitialization = int(nx) if nx > np.sqrt(float(nx)*factorablenlocations/ny) else int(np.sqrt(float(nx)*factorablenlocations/ny))
    print 'X initialization:' + str(xinitialization)
    while (float(factorablenlocations)/xinitialization)%1 != 0:
        xinitialization -= 1

    print xinitialization
    yinitialization = factorablenlocations/xinitialization
    print 'Y initialization: ' + str(yinitialization)
    xdistance = float(nx-1)/xinitialization
    ydistance = float(ny-1)/yinitialization

    print 'xdistance: '+ str(xdistance)
    print 'ydistance: ' + str(ydistance)
    return xdistance, ydistance

def isprime(n):
    for i in xrange(2,int(np.sqrt(n))+1):
        if n%i == 0:
            print 'not prime'
            return False

    print 'prime'
    return True
    

# Create a truncated pyrimid where the input neurons form the closest approximation of a square at the base, and the output neurons form the closest approximation of a square at the top. only the number of input and output neurons is required, the dimensions are determined by the pyramid constraint

# Create a sphere of neurons with the input at the center, and the output on the surface
