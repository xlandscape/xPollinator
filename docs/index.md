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

### BEEHAVE Model

In its initial version (October 2025) xPollinator integrates BEEHAVEcotox as the component to simulate effects to honey bees.  
BEEHAVEecotox is an extension of the [BeeHave](https://beehave-model.net/) model.  
BEEHAVE is a purpose-built, open-source computer model that simulates the daily development of a honeybee colony together with explicit nectar and pollen foraging across heterogeneous landscapes. It integrates within-hive processes (brood care and colony population dynamics) with foraging behaviour and can represent multiple stressors — such as varroa, weather, forage shortages or pesticide impacts — to study their combined effects on colony health. BEEHAVE is implemented in NetLogo, comes with a user manual and detailed model description, and is available for download at the [BeeHave](https://beehave-model.net/) project site.  
[BEEHAVEecotox](https://github.com/ibacon-GmbH-Modelling/BEEHAVEecotox) is an ecotoxicological extension of BEEHAVE that integrates a mechanistic effect module linking pesticide exposure to colony processes (mortality of foragers, brood, and in-hive bees) and landscape-scale inputs. Implemented in NetLogo, the package includes the NetLogo model code, a landscape extension, example input files (for food sources and pesticide applications), a user manual and technical notes. The BEEHAVEecotox implementation and its landscape extension are described in Preuss et al. (2022); the project sources and documentation are available from the BEEHAVEecotox GitHub repository under a GPL licence.

### Scenarios

Scenarios represent the environmental, land use, agricultural management and ecological conditions. Their definition heavily depends on the problem at hand, i.e., the modelling purpose. The technical requirements for xP scenarios, their concepts and development, as well as example scenarios are summarised in the [scenarios](scenarios/scenario-concepts.md) section.  

## Acknowledgements

The development of the xP landscape model was initiated by Thorsten Schad ([thorsten.schad@landwerk-ev.de](mailto:thorsten.schad@landwerk-ev.de)) and the major development was done by Sascha Bub ([sascha.bub@rptu.de](mailto:sascha.bub@rptu.de)).  
Its realisation was only possible due to the contribution of colleagues listed below and the sponsoring by Bayer AG.  

| Role / Activity | Person |
|---|---|
| Idea and Initiative | Thorsten Schad ([thorsten.schad@landwerk-ev.de](mailto:thorsten.schad@landwerk-ev.de)) |
| Goals&Requiements | Thorsten Schad, Vanessa Roeben (Bayer AG), Thomas Preuss (Bayer AG), Sascha Bub ([sascha.bub@rptu.de](mailto:sascha.bub@rptu.de)) |
| Design | Thorsten Schad, Sascha Bub  |
| Implementation | Sascha Bub, Thorsten Schad |
| Testing | Thorsten Schad |
| Documentation | Thorsten Schad |
| Publication | Sascha Bub, Thorsten Schad, Julian Heinrich |
| Analysis Modules | Thorsten Schad, Julian Heinrich |
| Scenarios | Chris Holmes (Applied Analysis Solutions), Thorsten Schad, Sascha Bub|

## References

[EFSA Bee Guidance](https://efsa.onlinelibrary.wiley.com/doi/10.2903/j.efsa.2021.6607).  
Preuss, T.G., Agatz, A., Goussen, B., Roeben, V., Rumkee, J., Zakharova, L. & Thorbek, P. (2022). The BEEHAVEecotox model - Integrating a mechanistic effect module into the honeybee colony model, Environmental Toxicology and Chemist, 41: 2870- 2882.
