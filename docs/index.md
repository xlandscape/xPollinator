# Welcome to xPollinator

Welcome to the xPollinator (xP) documentation. This documentation provides an **introduction** and will walk new users through **how to get started** with the xPollinator landscape model, including explanations for **sample scenarios** and their use with the [BEEHAVE model](https://beehave-model.net/).

## Background

Today, **scientific models** make a great contribution to understanding and predicting the consequences of how we cultivate the landscapes we are living in. Based on present knowledge and together with data, models have become a key instrument in decision making.  
An important field is the **risk assessment and management of pesticides**. In Europe (and countries beyond), this includes an assessment of pollinator risk, in particular, for the honey bee ([EFSA Bee Guidance](https://efsa.onlinelibrary.wiley.com/doi/10.2903/j.efsa.2021.6607)). The risk assessment includes the use of models (eg,  [BEEHAVE model](https://beehave-model.net/), [ApisRAM](https://www.efsa.europa.eu/en/supporting/pub/en-9293)) which require landscape scenarios for their operation. Key information of such scenarios is the occurrence of pollinator forage (mainly nectar and pollen).  
Beyond the use of xP in a risk assessment and management context and given its modular and flexible design, xP can be employed in a range of **related research and applied topics**, eg,  

- **landscape design and management, biodiversity enhancements**
- **Holistic view to risk**, multiple stressors analysis, systems-based approach, [EFSA, Bee Guidance](https://efsa.onlinelibrary.wiley.com/doi/10.2903/j.efsa.2021.6607))  
- Risk Assessment **Recovery Option** ([EFSA, Aquatic Guidance](https://www.efsa.europa.eu/en/efsajournal/pub/3290)) 
- **Environmental Impact Reduction** (EIR), eg, *what if* analysis, assessment and documentation of real-world EIR by new plantprotection products and digital environmental safety solutions  
- **Insect decline analysis**: habitat conditions    
- **Monitoring** (design, insights, transfer of results to other regions and times)  
- Solutions for **Integrated Pest Management**: improved integration of the use of chemicals and agricultural practices to reduce environmental impact, comparison of pest control options (eg, weed control)  
- **Specific Protection Goals**: identification of driving factors of populations dynamics for targeted chemical risk assessment endpoints and schemes  
- **Ecosystem Services** ([Millennium Ecosystem Assessment](https://www.millenniumassessment.org/en/index.aspx)): improvend quantitative insights into real-world *Ecosystem Services* for more explicit and transparent cost/benefit risk management. The work on the future of sustainable and regenerative agriculture **requires improved operational instruments** which allow to better understand real-world implications.  
  
## Intro

xPollinator is a landscape model to **simulate bee forage occurrence** in cultivated landscapes (currently nectar and pollen), **pesticide use**, as well as **exposure** of and **effects** on pollinators **in space and time** using real-world **landscape data**.  
Its conceptual basis is [**generic**](#concepts) and open to be used for any pollinator species, whereas initial bee forage parameterisations and scenarios focus on the **honey bee**. xP is based on the **modular landscape modelling framework** [xLandscape](xLandscape/xLandscape-intro.md#xlandscape).
  
Forage supply in the landscape largely determines honey bee activity and so the development of honey bee hives as well as of wild bee colonies. Correspondingly, the spatial and temporal occurrences of forage are essential information to model bee colony development (eg, using [BEEHAVE model](https://beehave-model.net/) or [ApisRAM](https://www.efsa.europa.eu/en/supporting/pub/en-9293)). Thus, dynamic forage representation builds the basis for modelling exposure and effects of honey bees due to contact to pesticides.  
**Bee forage** is typically composed of nectar and pollen. In addition, honeydew provided by insects (typically living on trees and shrubs, i.e. in woodlands) can also provide an important forage ressource (initially not considered, yet such a module can added any time). In cultivated landscapes, nectar and pollen are provided by a variety of crops, natural and semi-natural vegetation, with a correspondingly spatial and temporal variability of intensities and quality attributes (eg, sugar type, content, protein content).  
The entire process of modelling beeforage is of [modular design](#modular-design). This allows, e.g., to use a range of land use/cover data together with forage provision information as input, depending on the specific xP model purpose.  

## Concepts and Design

### Framework and Modularity

**xPollinator is a ready-to-use landscape model** for spatiotemporally explicit modelling of pollinator risk in real-world landscapes. This requires to integrate a range of domains, information, processes and models.  
In its initial version, xP can generate [scenarios](#scenarios) for the [BEEHAVE model](https://beehave-model.net/), simulate spatiotemporally explicit exposure pattern of pesticides via different exposure routes and environmental fate, and can model effects of pesticide exposure to pollinators.  
Its individual **functionalities are represented in modules** (called [components](reference/glossary.md#components)) which are **integrated into the [xLandscape](xLandscape/xLandscape-intro.md#xlandscape) framework** (figure below). Both, the framework and the modularity make xP **flexible to adapt its present capabilities** for a range of purposes of modelling pollinator forage ([Background](#background)), pollinator exposure and effects, different species and for basically any geographic region and extent. Eg, in case a bee forage modeller has data and models to simulate the occurrence of honeydew producers, this can be integrated in the xP landscape model as a new component.  

<img src="img/xPollinator LandscapeModel scheme v01.png" alt="xPollinator model" width="1000"/>  

**xPollinator landscape model**. xP is a modular composition of components using the [xLandscape](xLandscape/xLandscape-intro.md#xlandscape) framework. (Components marked with dashed lines were under discussion in the regulatory scientific community at the time of writing.)

### Bee Forage

Nectar and pollen are predominately produced by **flowering vegetation**. Thus, vegetation type, plant species, their phenology and their specific nectar and pollen production (quantity, quality) is essential data and information. Bee forage is also provided as honeydew, which is produced by different insects (eg, Aphids probably the most well-known honeydew producers and often excrete large quantities, but also scale insects (Coccoidea), leafhoppers (Cicadellidae and others), Adelgids (Adelgidae), plant bugs (Heteroptera), whiteflies (Aleyrodidae), or mealybugs (Pseudococcidae)).  
In line with the fundamental design of xLandscape, modelling pollinator forage is separated in  **fundamental building blocks** (modules), implemented as components and integrated into xP. Accordingly, modelling of bee forage in xP itsself is a modular approach, and individual moduls and be replaced (enhanced) giving improved knowledge. An illustration is shown in the figure below.  

<img src="img/BeeForage modelling process with Beehave scenario.png" alt="xPollinator modular design" width="1000"/>  

**Bee forage modelling sequence**. The explicit steps define xP components (initial focus on vegetation as forage providing landscape element).

In the initital implementation of xP, key components for modelling bee forage are:

- **Land use/land cover** (LULC) information: an assembly of spatial data that represents essential LULC types that provide bee forage. The geodata layer can be modulary composed of any data, information and knowledge that the modeller seems relevant and that can be acquired or generated at reasonable efforts (e.g., using satellite imagery), targeting the goals of the bee forage modelling study at hand.  
- **Vegetation and its phenology**: a module to translate LULC types to vegetation types and their phenology. In its inital realisation, the assignments are realised in tabular format and are based on literature and expert knowledge. This early approach is regarded robust and sufficiently accurate for the initial applications of the xP landscape model. However, this simple realisation can be replaced and improved, e.g., by introducing AI on plant communities and phenology models.  
- **BeeForage(x,t)**: the module to generate actual bee forage occurrence in space and time, i.e., (initially) the provision of nectar and pollen (space, time -> BeeForage(x,t)).
- BeeHave Scenario Parser: a module for the ready-to-use preparation of bee forage scenario as input for a pollinator model (eg, the [BEEHAVE model](https://beehave-model.net/)).

A layered view might support the understanding of data and information layers used in bee forage modelling.  

<img src="img/BeeFOrage-Vegetation-Data layering.png" alt="xPollinator modular design" width="700"/>  

**Data and information layers in bee forage modelling**. (* *Sources* represent forage occurrence other then provided by vegetation, eg, honeydew producers.)  

This modularity enables to basically use any type of data, information and sub-models which are approriate to a specific bee (pollinator) forage modelling purpose. Example data inputs and parameterisations are introduced in the [Scenario](#scenarios) section.

### BeeHave

xxx

### xPollinator Landscape Model

The modular landscape model to for spatiotemporally explicit simulation of bee (pollinator) forage, xPollinator (xP), was built using the **landscape modelling framework** [xLandscape](xLandscape/xLandscape-intro.md#xlandscape). The framework allows to compose individual modules, called *Components* to a landscape models, that operates spatiotemporally explicit.  
The components represent and encapsulate distinct functionality. Any component can be replaced by more or less complex ones.  
Adding components adds functionality. For xP, a version exists that comprises the use of pesticides (PPPs) and the environmental exposure (figure below). Again, each exposure route and process is represented by a specific component (which can be replaced to manage model complexity).  

<img src="img/xP.png" alt="xPollinator modular design" width="700"/>  

Composition of the xPollinator landscape model (v0.9). Its components are introduced in subsections below.

<img src="img/xP & exposure and effects.png" alt="xPollinator modular design" width="700"/>  

Composition of the xPollinator landscape model (v0.9) including components to model PPP use and environmental exposure.

#### BeeForage Component

The BeeForage component models the occurrence of nectar and pollen in space and time. The outcome is stored in a multidimensional data store.  
The current version (v0.9) uses spatial data on vegetation types (units) and their phenology as base input, together with information on nectar and pollen production by these vegetation types. The core functionality of the BeeForage component is to match (model) nectar and pollen production for each of these vegetation types. In the current version, this is done by a simple lookup tables (with a honey bee focus):  

1. Assigning nectar and pollen production intensity classes (0-4) to vegetation type (by time).  
1. Assigning nectar and pollen production quantities to intensity classes.  

<img src="img/Vegetation-Phenology illustration.png" alt="xPollinator modular design" width="700"/>  

Lookup table to assign nectar and pollen production intensity classes (0-4) to vegetation type (by time).

<img src="img/Nectar-Pollen quantification.png" alt="xPollinator modular design" width="1000"/>  

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

### xP Simulation xxx: move to 'get started'

On each time step (eg, day) and field in a simulation, xP checks if there are products to apply. If so, exact application details are determined based on model parameterisation (eg, deterministic or by sampling from  from distributions given by the user) and executed.  


## xPollinator Landscape Model

## Scenarios

## Application

## Acknowledgements
The need and the development of the xP landscape model was initiated by Thorsten Schad (thorsten.schad@landwerk-ev.de). It's realisation was only possibly due to the contribution of colleagues listed below and the sponsoring by Bayer AG.  

<img src="img/Contributions.png" alt="Contributors and Roles" width="800"/> xxx

## References
EFSA Guidance  
BioDT

[EFSA Bee Guidance](https://efsa.onlinelibrary.wiley.com/doi/10.2903/j.efsa.2021.6607)  
Pritsch
Westrich Die Wildbienen Deutschlands
