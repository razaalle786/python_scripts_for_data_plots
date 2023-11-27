import numpy as np, xraylib as xrl, xraylib_np as xrl_np, datetime
from datetime import time


class Element():
    def __init__(self, E, Z):
        self.abundance = 1
        self.E = E
        self.CS_Total = xrl.CS_Total(Z, E)
        self.CS_Photo = xrl.CS_Photo(Z, E)
        self.CS_Compt = xrl.CS_Compt(Z, E)
        self.CS_Rayl = xrl.CS_Rayl(Z, E)
        
        self.Photo_Fraction = self.CS_Photo / self.CS_Total
        self.Compt_Fraction = self.CS_Compt / self.CS_Total
        self.Rayl_Fraction = self.CS_Rayl / self.CS_Total

class Mixture_np():
    def __init__(self, Z, abundance, E):
        self.abundances = abundance
        self.E = E
        self.CS_Total = np.einsum('i,ik->k',abundance,xrl_np.CS_Total(Z, E))
        self.CS_Photo = np.einsum('i,ik->k',abundance,xrl_np.CS_Photo(Z, E))
        self.CS_Compt = np.einsum('i,ik->k',abundance,xrl_np.CS_Compt(Z, E))
        self.CS_Rayl = np.einsum('i,ik->k',abundance,xrl_np.CS_Rayl(Z, E))
        
        #self.Photo_Fraction = self.CS_Photo / self.CS_Total
        #self.Compt_Fraction = self.CS_Compt / self.CS_Total
        #self.Rayl_Fraction = self.CS_Rayl / self.CS_Total

class Radionuclide():
    def __init__(self, xrl_name):
        self.data = xrl.GetRadioNuclideDataByName(xrl_name)
        self.ref_activity = 1e6
        self.activity = 1e6
        self.half_life = 1
        self.emitted_energies = np.concatenate(
            (xrl_np.LineEnergy(np.array((0,self.data['Z'])), 
                               np.array(self.data['XrayLines']))[1],
             self.data['GammaEnergies']))
        self.emitted_intensities = np.concatenate(
            (self.data['XrayIntensities'],self.data['GammaIntensities']))

        self.primary_peak = self.emitted_intensities.argmax()
        self.energies_of_interest = range(self.emitted_energies.__len__())
        
    def set_half_life(self,days):
        self.half_life = datetime.timedelta(days).total_seconds()
    def set_ref_date(self, year, month, day):
        self.ref_date = datetime.date(year,month,day)
        decay_time  = (datetime.date.today() - self.ref_date).total_seconds()
        self.activity = (self.ref_activity
                         * np.exp(-(np.log(2)*decay_time)/self.half_life))
        
class Tc99m():
    def __init__(self):
        self.ref_activity = 1e6
        self.activity = 1e6
        self.half_life = datetime.timedelta(0.250279167).total_seconds()
        
        #Only gamma energies!
        self.emitted_energies = np.array([89.6, 140.511, 142.683])
        self.emitted_intensities = np.array([.0000104, .885, .00023])
        #self.emitted_energies = np.concatenate(
        #    (xrl_np.LineEnergy(np.array((0,self.data['Z'])), 
        #                       np.array(self.data['XrayLines']))[1],
        #     self.data['GammaEnergies']))
        #self.emitted_intensities = np.concatenate(
        #    (self.data['XrayIntensities'],self.data['GammaIntensities']))

        self.primary_peak = self.emitted_intensities.argmax()
        self.energies_of_interest = range(self.emitted_energies.__len__())
        
    def set_half_life(self,days):
        self.half_life = datetime.timedelta(days).total_seconds()
    def set_ref_time(self, yr, mnth, dy, hr, mnt):
        self.ref_time = datetime.datetime(year=yr, month=mnth, day=dy,
                                          hour=hr, minute=mnt)
        decay_time  = (datetime.datetime.now() - self.ref_time).total_seconds()
        self.activity = (self.ref_activity
                         * np.exp(-(np.log(2)*decay_time)/self.half_life))

def rectangular_solid_angle(a,b,d):
    alpha = a/(2*d)
    beta = b/(2*d)
    return 4*np.arctan((alpha*beta)/np.sqrt(1+alpha**2+beta**2))

def get_elements_and_offsets(a,b,d,x_segmentation,y_segmentation):
    a_element = a/x_segmentation
    b_element = b/y_segmentation
    
    #subdivide detector face into pixels
    elements_x = np.linspace(0, a, x_segmentation+1, endpoint=True)-(a/2)
    elements_y = np.linspace(0, b, y_segmentation+1, endpoint=True)-(b/2)
    #Find midpoint of each subdivision to use as the pixel coordinates.
    #Only the quadrant 1 coordinates are found, detector is rectangluar so this 
    #quarter *4 represents the full detector.
    elements_x = ((elements_x[1:] + elements_x[:-1]) / 2)[elements_x.size//2:]
    elements_y = ((elements_y[1:] + elements_y[:-1]) / 2)[elements_y.size//2:]
    
    #Get possible combinations to get all element coordinates in quadrant 1
    element_coordinates = np.array(np.meshgrid(elements_x,
                                               elements_y)).T.reshape(-1,2)
    #add fixed z=d dimension
    element_coordinates = np.array((element_coordinates[:,0], 
                                    element_coordinates[:,1], 
                                    np.repeat(d,element_coordinates[:,0].size))).T
    #Get element xy offsets - (x,y) distance from nearest pixel vertex to origin
    element_offsets = np.array(np.meshgrid(elements_x - (a_element/2),
                                               elements_y - (b_element/2))).T.reshape(-1,2)
    return element_coordinates, element_offsets, a_element, b_element

def offset_rectangular_solid_angle(xy_offsets,a,b,d):
    quad_1 = rectangular_solid_angle(2*(xy_offsets[:,0]+a), 
                                     2*(xy_offsets[:,1]+b), d)
    quad_2 = rectangular_solid_angle(2*xy_offsets[:,0], 2*(xy_offsets[:,1]+b), 
                                     d)
    quad_3 = rectangular_solid_angle(2*(xy_offsets[:,0]+a), 2*xy_offsets[:,1], 
                                     d)
    quad_4 = rectangular_solid_angle(2*xy_offsets[:,0], 2*xy_offsets[:,1], d)
    return( quad_1 - quad_2 - quad_3 + quad_4)/4

def path_length_rectangular(a, b, element_coords, d, t):
    vedge = a/(2*element_coords[:,0])
    hedge = b/(2*element_coords[:,1])
    rearface = np.repeat((d+t)/d,element_coords[:,0].size)
    
    int_detector = np.zeros(element_coords.shape)
    v_in_detector = np.zeros(element_coords.shape)
    
    #multiply coordinates by scaling vectors to get coordinates of plane intersection
    int_vedge = np.einsum('ij,j->ji',element_coords.T, vedge)
    int_hedge = np.einsum('ij,j->ji',element_coords.T, hedge)
    int_rearface = np.einsum('ij,j->ji',element_coords.T, rearface)
    
    #Select interaction coordiantes within the detector from each planes interactions
    int_detector = np.where(np.tile((int_rearface <= (a/2,b/2,d+t)).all(1), (3,1)).T,
                            int_rearface, int_detector)
    int_detector = np.where(np.tile((int_vedge <= (a/2,(b/2),d+t)).all(1), (3,1)).T,
                            int_vedge, int_detector)
    int_detector = np.where(np.tile((int_hedge <= (a/2,b/2,d+t)).all(1), (3,1)).T,
                            int_hedge, int_detector)
    
    
    v_in_detector[:,0] = int_detector[:,0] - element_coords[:,0]
    v_in_detector[:,1] = int_detector[:,1] - element_coords[:,1]
    v_in_detector[:,2] = int_detector[:,2] -  d
    
    return np.linalg.norm(v_in_detector, axis=1)

#Lab Test Source Data
Co57_source = Radionuclide('57Co')
Co57_source.ref_activity = 200e6
Co57_source.set_half_life(271.8)
Co57_source.set_ref_date(2019, 12, 15)

Cd109_source = Radionuclide('109Cd')
Cd109_source.ref_activity = 100e6
Cd109_source.set_half_life(462.6)
Cd109_source.set_ref_date(2020, 1, 1)

Am241_source = Radionuclide('241Am')
Am241_source.set_half_life(157861.05)
Am241_source.ref_activity =  12.55e6 #50e6
Am241_source.set_ref_date(2022, 2, 2)

Tc99m_source = Tc99m()
Tc99m_source.ref_activity = 4.8e6
Tc99m_source.set_ref_time(yr=2023,mnth=3,dy=27,hr=11,mnt=15)

#Pick source to look at
source = Co57_source

#detector dimensions and simulation setup in cm
a = 2                   #x dimension of detector face
b = 2                   #y dimension of detector face
t = .1                  #detector thickness
d = 6
                 #source-detector face distance
duration = 1

#Set detector material by defining material elements, abundances and material density
material_Zs = np.array((48,52))
material_abundances = np.array((0.5,0.5))
material_density = 5.85

#Get cross sections of materials elements for each gamma energy in the source
detector = Mixture_np(material_Zs, material_abundances, 
                      source.emitted_energies)

#Pick indices of energies you want to look at
#Need to be careful not to include multiple gammas from the same decay chain
energies_of_interest = source.primary_peak
#energies_of_interest = np.arange(source.emitted_intensities.size)

#Pull detectors CS and peak intensities for the peaks identified
#This step is redundant if all looked at, but makes it easier to thin spectra.
CS_of_interest = np.take(detector.CS_Total, energies_of_interest)
intensities_of_interest = np.take(source.emitted_intensities, energies_of_interest)
#Pick investigation peak - must be subset of energies of interest
investigation_peak = source.primary_peak

#set number of elements for integral
element_number = 500

#Incident gammas on whole detector
incident = rectangular_solid_angle(a, b, d) * source.activity * duration/ (4*np.pi)

#Number of gammas attenunated in detector
element_coordinates, element_offsets, a_element, b_element = get_elements_and_offsets(a, b, d, element_number, element_number)
element_path_lengths = path_length_rectangular(a, b, element_coordinates, d, t)
element_incidents = offset_rectangular_solid_angle(element_offsets,a_element,b_element,d) * source.activity * duration/np.pi

if CS_of_interest.size==1:
    attenuated_gammas = (1 - np.e**(-CS_of_interest*material_density*element_path_lengths)) * (element_incidents * intensities_of_interest)
    total_counts_per_path  = attenuated_gammas
    total_counts = attenuated_gammas.sum()
else:
    attenuated_gammas = ((1-np.e**(-material_density*np.einsum('i,j->ij', CS_of_interest, element_path_lengths)))
                         *np.einsum('i,j->ij', intensities_of_interest, element_incidents))
    total_counts_per_path  = attenuated_gammas.sum(0)
    total_counts = total_counts_per_path.sum()


no_of_frames = 1589

print('SA Fraction * decay number: \t\t',incident)
print('Photons attenuated per second: \t', total_counts)
print("Photons attenuated per frame: \t", (total_counts/(duration*no_of_frames)))
#print('Occupancy per frame: \t\t\t', 5*(total_counts/(duration*50000))/(80*80))
#print('Time for', no_of_frames, 'frames: \t', (no_of_frames/8.5))


'''
#Pixel count density stuff - comment out to increase run speed
elements_per_pixel  = int(element_number/(2*40))
elements_per_quarter = int(element_number/2)
counts_mean_pixel = total_counts/(80*80)
inv_peak_counts_mean_pixel = attenuated_gammas[int(investigation_peak),:].sum()/(80*80)

if CS_of_interest.size==1:
    counts_min_pixel = np.reshape(attenuated_gammas,(elements_per_quarter,elements_per_quarter))[-elements_per_pixel:,-elements_per_pixel:].sum()/4
    counts_max_pixel = np.reshape(attenuated_gammas,(elements_per_quarter,elements_per_quarter))[:elements_per_pixel,:elements_per_pixel].sum()/4
    inv_peak_counts_min_pixel = counts_min_pixel
else:
    counts_min_pixel = np.reshape(attenuated_gammas,(attenuated_gammas.shape[0],elements_per_quarter,elements_per_quarter))[:,-elements_per_pixel:,-elements_per_pixel:].sum(0).sum()/4
    counts_max_pixel = np.reshape(attenuated_gammas,(attenuated_gammas.shape[0],elements_per_quarter,elements_per_quarter))[:,:elements_per_pixel,:elements_per_pixel].sum(0).sum()/4
    inv_peak_counts_min_pixel = np.reshape(attenuated_gammas[int(investigation_peak),:],(elements_per_quarter,elements_per_quarter))[-elements_per_pixel:,-elements_per_pixel:].sum(0).sum()/4
    
print('\n')
print('Time for 4k average pixel count: \t\t\t', 4000/counts_mean_pixel)
print('Time for 4k pixel count in all pixels: \t', 4000/counts_min_pixel)
#print('\n')
print('Time for 4k average pixel count \nfrom investigation peak only: \t\t\t', 4000/inv_peak_counts_mean_pixel)
print('Time for 4k pixel count in all \npixels from investigation peak only: \t\t', 4000/inv_peak_counts_min_pixel)
'''


