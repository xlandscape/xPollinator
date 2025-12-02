# Intro

First of all, scenarios have a **technical meaning** as a structured integration of all nessessary environmental, land use/cover, agricultural, ecological data, information and assumptions to run a model (here, xPollinator). However, in environmental risk assessment, scenarios have a **regulatory meaning** as a testing system, that has to assure a certain protection level in case the test gets passed. In this role, scenarios have to address a certain **level of conservatism**, hence, need to be **representative** for a range of conditions of a typically large geographic area (e.g., a country).  
Whereas detailed scenarios are applied to derive risk estimates, simple ones are used, e.g., for screening a level of conservatism for large areas.  
Scenarios play a key role in the analysis and definition of effective **risk mitigation** measures. Scenarios can incorporate buffer zones, the use of drift-reducing technology, reduced application rates, or alternative practices to evaluate risk reduction. Beyond the focus on actual pesticide uses, scenarios serve **risk management** approaches targeting generic landscape characteristics which affect species populations, communities and biodiversity: e.g., the composition, managment and structure of cultivated landscapes, and their relationship to their surrounding regions.  
Realistic landscape scenarios can play an important role in **policy alignment**: The definition of Specific Protection Goals (SPGs, e.g., [EFSA 2010](https://doi.org/10.2903/j.efsa.2010.1821), [EFSA 2025](https://doi.org/10.2903/j.efsa.2025.9501)) is based on the ecosystem services concepts. Modern regulatory developments highlight the important role of landscape scenarios and approaches as a way to contextualize SPGs, e.g., for terrestrial organisms. Future risk and risk assessment will develop beyond single-species laboratory tests and incorporate realistic agricultural landscapes, including spatial and temporal heterogeneity, e.g., to capture both direct and indirect effects of pesticides. Risk management decisions should be informed by how pesticides affect organisms in actual European agroecosystems, not abstract worst-cases or averages. Landscape scenarios can ensure that SPGs align with broader environmental protection mandates to EU biodiversity and sustainability goals. So, landscape scenarios serve as a **bridge between scientific modelling and regulatory decision-making**.

# xP Scenario Definition

After downloading a scenario folder 
xPollinator\scenario 

# xP Scenario Development

use existing scenarios as templates

# Outlook

## Geographic Region

## Bee Forage 

### LULC

Land use/cover data provides typically builds the spatial base information on 

Vegetation mapping and modelling. [European Vegetation Archive (EVA)](https://euroveg.org/eva-database/)

### BeeForage

The BeeForage component models the occurrence of nectar and pollen in space and time. The outcome is stored in a multidimensional data store.  
The current version (v0.9) uses spatial data on vegetation types (units) and their phenology as base input, together with information on nectar and pollen production by these vegetation types. The core functionality of the BeeForage component is to match (model) nectar and pollen production for each of these vegetation types. In the current version, this is done by a simple lookup tables (with a honey bee focus):  

1. Assigning nectar and pollen production intensity classes (0-4) to vegetation type (by time).  
1. Assigning nectar and pollen production quantities to intensity classes.  

<img src="../img/Vegetation-Phenology illustration.png" alt="xPollinator modular design" width="700"/>  

Lookup table to assign nectar and pollen production intensity classes (0-4) to vegetation type (by time).

<img src="../img/Nectar-Pollen quantification.png" alt="xPollinator modular design" width="1000"/>  

Lookup table to assign nectar and pollen production quantities to intensity classes.

Both lookup tables are based on literature and expert judgement (xxx).  

This initial realisation of the BeeForage-Component can be enhanced and replaced by more sophisticated bee forage modelling, eg, using data-driven/AI or mechanistic models, together with corresponding geoinformation on the underlying vegetation.  
The BeeForage-Component can also be extended to model the occurrence of honeydew, again, if corresponding models, knowledge and data are available (and fit to each other).  

#### Vegetation

In our representation of vegetation (and its phenology), instead of employing an of-the-shelf land use/cover (LULC) dataset, we compose bee forage-providing land use/land cover elements from different sources. This composition is driven by the study purpose and related requirements (eg, level of detail, precision, certainty, scales), data availability, and given ressources. Eg, 

- a LULC base layer (eg, topographic geodata) is used to identify general LULC types (eg, arable, forest, orchards, grasslands, gardens, ruderal) and more bee forage specific types if possible (eg, apple, decidious woods, arable crop types)  
- Specific bee forage providing crop types are identified from satellite imagery (eg, oil seed rape)  
- Likewise, grassland characterisation can be done using satellite imagery based approaches (eg, hayfield, natural, intense sillage)  
- Further bee forage relevant vegetation can be constructed from LULC base layers and literature (eg, riparian, wood margins)  
- High-resolution landscape elements can be added from mapping (eg, hedges, groups of bee forage relevant trees, etc.) 

The user defines PPP uses in a ***Crop Protection Calender***, including application technology, and mitigation measures for reducing exposure (risk). The approach of using a *Crop Protection Calender* is based on agricultural practice, where pest control measures for a crop are typically planned based on experiance, PPP availability and other factors. Crop protection plans are made eg, by official plant protection advisory services, farmers, or PPP producers. Besides reflecting ag practice, the approach of a CPC also addresses modelling practice in risk assessment which typically focus on a certain indication, conducted over long time periods. Beyond these established uses, alternative CPCs can be used to assess the environmental impact of alternative pest control options, or to design new pest control means against established ones, considered as baselines.  

#### Environmental Data

Agri4Cast

### Tiered Approach

xxx Depending on the purpose of bee (pollinator) forage modelling,  

1. off-the-shelf data: covering large geographic regions
1. best-available data, including manual processing
1. contemporary data generation: high-resolution drone mapping
1. field study: best possible landscape mapping, bee forage quantification and modelling

## References

xxx  
Pritsch  
Westrich "Die Wildbienen Deutschlands"

