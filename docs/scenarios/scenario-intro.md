# Intro *!writing in progress!*

First of all, scenarios have a **technical meaning** as a structured integration of all nessessary environmental, land use/cover, agricultural, ecological data, information and assumptions to run a model (here, xPollinator). However, in environmental risk assessment, scenarios have a **regulatory meaning** as a testing system, that has to assure a certain protection level in case the test gets passed. In this role, scenarios have to address a certain **level of conservatism**, hence, need to be **representative** for a range of conditions of a typically large geographic area (e.g., a country).  
Whereas detailed scenarios are applied to derive risk estimates, simple ones are used, e.g., for screening a level of conservatism for large areas.  
Scenarios play a key role in the analysis and definition of effective **risk mitigation** measures. Scenarios can incorporate buffer zones, the use of drift-reducing technology, reduced application rates, or alternative practices to evaluate risk reduction. Beyond the focus on actual pesticide uses, scenarios serve **risk management** approaches targeting generic landscape characteristics which affect species populations, communities and biodiversity: e.g., the composition, managment and structure of cultivated landscapes, and their relationship to their surrounding regions.  
Realistic landscape scenarios can play an important role in **policy alignment**: The definition of Specific Protection Goals (SPGs, e.g., [EFSA 2010](https://doi.org/10.2903/j.efsa.2010.1821), [EFSA 2025](https://doi.org/10.2903/j.efsa.2025.9501)) is based on the ecosystem services concepts. Modern regulatory developments highlight the important role of landscape scenarios and approaches as a way to contextualize SPGs, e.g., for terrestrial organisms. Future risk and risk assessment will develop beyond single-species laboratory tests and incorporate realistic agricultural landscapes, including spatial and temporal heterogeneity, e.g., to capture both direct and indirect effects of pesticides. Risk management decisions should be informed by how pesticides affect organisms in actual European agroecosystems, not abstract worst-cases or averages. Landscape scenarios can ensure that SPGs align with broader environmental protection mandates to EU biodiversity and sustainability goals. So, landscape scenarios serve as a **bridge between scientific modelling and regulatory decision-making**.

## xP Scenarios

### General

According to their technical meaning, scenario definition and requirements depend on the given composition of the xP landscape model (i.e., integrated components and their version). Thus, scenario development has to be adaptive and in line with xP model development.  
[Example scenarios](/scenarios/Example-scenarios-France.md) shipped with xP fit to the given model version and reside in the scenario folder after model download (xPollinator\scenario).  
[Example scenarios](/scenarios/Example-scenarios-France.md) also provide a good starting point for the development of user-defined (new) scenarios.  

Outlook:  
For scenario creation web-based services have been experimentally tested. Such services provide a (simple) GUI via web browser to enable the user to select a geographic location (e.g., via mouse click or by providing coordinates), to set parameters and to get a ready-to-use scenario back. This significally reduces effort and cost for the user and supports consistancy and harmonisation.  
Furthermore, such services can support the study site identification, i.e., the selection of representative scenario locations (and numbers).  

### Scenario Development Aspects

#### Scenario Site Selection

The selection of scenario sites is a crucial part of the scenario development process and depends on the study context, purpose and goals.  
An example for a site selection process is illustrated below. The context is a regulatory risk assessment using the BeeHave model, for the use of an insecticide in apple cultivations in France. In this illustrative example, site selection was a 3-step approach:  

1. At country scale (France), cultivation data consistantly available across France was used to select regions of high apple cropping density. Rationale: Honey bees forage on apple inflorescences. As a managed species, bee keepers like to put their hives in apple cultivation vicinity. Thus, risk of honey bees to get exposed by the use of a PPP in apples is driven by local apple cultivation density, simply: the more apple cultivations the greater the chance of bees to be exposed.  
Bee activity is driven by weather conditions, eg, temperature, sunshine hours. As e.g., the effect of varying sunshine hours to risk is currently not clear, 3 regions of different climate conditions were selected covering climatic variability to increase scenario represenativeness.
1. At regional level, bee forage mapping was built upon a dataset of Land Use/Cover types covering bee forage offering vegetation (eg, rape, apples, wood and road margins, riparian). The LULC layer was derived using off-the-shelf topographic, cropping, hydrographic datasets, cropping statistics and expert knowledge (eg, wood margin). A vulnerability map was derived combining densities of bee forage with potential exposure (pesticide use in apples).
1. Local identification of realistic bee hive spots was done in cooperation with bee keepers: Beekeepers have the experience on where to place bee hives in a given landscape. Such management information adds reality to scenario development. This information was combined with regional vulnerability indices in order to ultimately select apiary sites (conservative, ie, high vulnerability percentile).  

Outlook: xxx

- improve quantitative scenario ranking using a metamodel on beehive development (and exposure) derived from a large number of BEEHAVE simulation runs, screening the parameter space, in combination with a sensitivity analysis. 
- explicitely include temporal (seasonal) bee forage variability and diversity
improve quantitative local vulnerability (risk) indicies using a metamodel on beehive development (and exposure) (see also above)



coverage of conditions, variability , 

![Site Selection](../img/scenario%20selection%20-%20case%20study%20France.png)

![Local Site Selection](../img/Scenario%20Example%20-%20local%20site%20selection.png)

#### Modular Scenario Development

xxx elements

![BeeForage in Landscape](../img/BeeForage%20occurrence%20in%20a%20landscape%20illustration.png)

xxx

![BeeForage Construction Kid](../img/Bee%20forage%20contruction%20kit%20illustration.png)

#### Levels of Detail

The ideal data of local nectar and pollen provisioning by plant species and cummunities, together with the necessary data on environmental conditions is hardly available (and are not needed for a given purpose). Typically, **bee forage occurrence is modeled**, as a composit of data, models and expert judgement. Scale, precision and accurracy of this modelling approach should be adapted to the problem at hand. Transparancy in data preparation, processing and modelling steps is key to acceptability.  
To support transparancy and structure in scenario development, we propose to consider explicit levels of detail, which relate to the purpose of the bee (pollinator) forage modelling:

| Level | Data Acquisition | Description |
| --- | --- | --- |
| 1 | Off-the-shelf data | Basic, wide-coverage datasets (satellite, national/regional products) suitable for large-scale or screening analyses. |
| 2 | Best-available data | Curated and locally verified datasets with additional manual processing or expert review for improved accuracy. |
| 3 | Contemporary data generation | High-resolution, high information depth data collected targeted for the study (e.g., drone mapping, targeted remote sensing). |
| 4 | Field study | Detailed, field mapping and measurements providing high-resolution information about forage, phenology and local environmental conditions. |

#### Base Data

This section introduces some base data, commonly used in scenario development. The information is more intended to give a general overview then to point on specific data as data devepoment and provisioning is very dynamic. We highly recommend to consult web pages, search engines and AI agents (artificial intelligence) for recent information before you start your development or study.  

##### Land Use Land Cover (LULC)

A typical base geodata layer in scenario development is composed from pan‑European and national/topographic sources. The table below summarises common products and their typical availability across Europe and individual countries.

| Dataset / Product | Geographic coverage | Typical spatial resolution / unit | Access / Notes |
| --- | --- | --- | --- |
| CORINE Land Cover (CLC) / Copernicus Land Monitoring | Pan‑Europe (EEA) | Vector polygons, minimum mapping unit ≈25 ha (derived raster products ~100 m) | Open via EEA/Copernicus. Good for consistent, multi‑year land-cover mapping but coarse for parcel-scale studies. |
| Copernicus High Resolution Layers (HRL) | Pan‑Europe (selected layers) | Thematic layers (e.g., forests, grasslands) often at 10–20 m equivalent detail | Open via Copernicus; complements CLC with thematic detail. |
| EU‑DEM / SRTM / national DEMs | Pan‑Europe (EU‑DEM) / global (SRTM) / national high‑res | DEMs at 25 m (EU‑DEM) to 90 m (SRTM); national LiDAR-derived DEMs much finer | EU‑DEM open; national DEMs/LiDAR availability varies by country and region. Use national portals for high‑resolution DEMs. |
| National orthophotos / aerial imagery | Country / regional | Very high resolution (sub‑meter to 1 m) | Typically available from national mapping agencies; often open or low‑cost — invaluable for detailed mapping and manual validation. |
| National crop cover / thematic crop maps (e.g., German Crop Cover Map) | Country (examples: Germany, Netherlands, UK, France) | Varies — from 10 m to parcel level | Produced by national agencies or research groups; quality and update frequency vary by country. Check national portals for access and licensing. |
| IACS / LPIS (administrative parcel data) | National / regional (EU) | Parcel-level declarations (farmers’ subsidy claims) | Highly detailed for crop/use per parcel but often restricted; access requires agreements with national paying agencies. Excellent for parcel-scale scenario building when available. |
| LIDAR / ALS point clouds & derivatives | Regional / national (select countries) | Very high resolution (sub‑meter elevation, vegetation structure) | Increasingly open in many countries (e.g., England, Netherlands, parts of Scandinavia); check national geoportals. Useful for hedges, canopy and microtopography. |
| OpenStreetMap (OSM) & volunteered data | Global (incl. Europe) | Vector features (roads, buildings, landuse polygons) | Open and continuously updated; variable completeness and thematic consistency — useful for topographic features and small‑structure mapping. |


##### Topographic / National base maps (country-level)

This table focuses on national topographic and base-map products (vector/raster), useful for deriving parcels, hedges, buildings and other baseline topographic features. Availability and licensing differ by country; check the national geoportal for access and licence terms.

| Dataset / Product | Country / Coverage | Typical spatial resolution / unit | Access / Notes |
| --- | --- | --- | --- |
| ATKIS (Basis‑DLM) | Germany | Multi-scale vector topographic database; detailed topographic objects (scale-dependent) | Provided by BKG and state mapping agencies; access via national geoportals. Licensing varies. |
| BDTOPO / BD TOPO | France | National vector topographic database (detailed topographic layers) | Provided by IGN; available via Géoportail and data.gouv.fr. |
| BTN (Base Topográfica Nacional) / SIOSE | Spain | BTN: national topographic data; SIOSE: land‑use/land‑cover thematic map | Available via CNIG; BTN for topography, SIOSE for land‑use. Licensing and access on national portals. |
| OS OpenData / OS MasterMap | Great Britain | Vector topographic layers; MasterMap provides parcel/building-level detail (commercial) | OS OpenData products available freely for many uses; MasterMap is commercial — check OS licensing. |
| TOP10NL / TOP10Vector / AHN | Netherlands | TOP10: 1:10k vector topographic data; AHN: national LiDAR-derived elevations | Distributed via PDOK; most datasets openly accessible. |
| BEV / Basis‑DLM | Austria | National vector topographic database and derivatives | Provided by BEV; access via Austrian geoportal. |
| IGM / national topo products | Italy | National topographic maps and derived vector datasets | Provided by IGM and regional geoportals; check national/regional portals for access. |
| National examples (SE, NO, BE, PT, etc.) | Sweden, Norway, Belgium, Portugal, ... | Country-specific vector/raster topographic datasets (scale varies) | Examples: Lantmäteriet (SE), Kartverket (NO), NGI/IGN (BE), IPMA/ICNF portals (PT). Check national geoportals for details. |
| OpenStreetMap (OSM) | Global (incl. Europe) | Vector features (roads, buildings, boundary features) | Open, community-maintained; variable completeness — useful as a fallback or for features missing in national datasets. |


##### Agricultural Data

To support reproducibility and transparency, different statistical and administrative data sources are typically consulted when composing study-area inputs. The table below summarises common agricultural statistics sources across Europe (examples and access notes):

| Source | Geographic coverage | Key content | Access / Notes |
| --- | --- | --- | --- |
| Eurostat (Farm Structure Survey, FSS; agri statistics) | EU / Member States | Farm structure, land used by crop, livestock numbers, farm size classes, basic agricultural indicators | Eurostat data portal (tables by survey/year). Useful for consistent, comparable EU-wide indicators. |
| FADN (Farm Accountancy Data Network) | EU (sample of farms) | Farm-level economic accounts, costs, incomes, farm types | Access via EC DG AGRI / FADN portal; sample-based — good for economic analyses but not exhaustive. |
| National agricultural censuses & surveys (e.g., Germany: Agrarstrukturerhebung / DESTATIS) | Country-level | Detailed farm structure, crop areas, livestock, management practices (national methodology) | Published by national statistical offices (e.g., DESTATIS for Germany). Use for highest national detail and legal definitions. |
| IACS / LPIS (administrative subsidy data) | National / Regional (EU) | Parcel-level declarations, crop types, area per parcel — linked to subsidy claims | Managed by national paying agencies; excellent for parcel-level mapping but access may be restricted or require agreements. |
| National ministries / agencies & sector bodies | Country or regional | Administrative statistics (production, registrations, herd/flock data), advisory reports | Often published on ministry portals; complementary to census data and often more up-to-date. |
| FAO / FAOSTAT | Global (incl. Europe) | Production, trade, input/output statistics, long time series | Good for international comparability and long-term trends; lower spatial detail than national sources. |

A common base information layer, today typically available across countries Land use/cover data provides typically builds the spatial base information on 
CORINE
German Crop Cover Map
EEA

Vegetation mapping and modelling. [European Vegetation Archive (EVA)](https://euroveg.org/eva-database/)

##### Remote Sensing


| Platform | Purpose | Availability | Note |
| --- | --- | --- | --- |
| Satellite, medium-resolution (Landsat 5/7/8/9; Sentinel-1/-2) | Land use/cover mapping, agricultural management (crop types, harvest, ploughing), vegetation development | Landsat archive (since <1990, 30 m); Sentinel since ≈2016 (10 m) | Free, full spatial coverage; mature processing workflows |
| Satellite, high-resolution (<1 m) | LULC and small-structure mapping (hedges, margins), vegetation time series | Operational since ≈2000; archives heterogeneous, tasking available | Commercial providers; good for targeted studies |
| Digital orthophotos (high-resolution, <1 m) | Parcel mapping, LULC, small structures | Widely available since 1990s; national/regional coverage | Low cost, widely used for mapping |
| LIDAR (very high resolution) | 3D structure, hedge and margin geometry, elevation models | Increasing availability since ≈2010 | Partly open data; provides detailed structural information |
| Drones (very high resolution) | Regional high-resolution mapping, vegetation characterisation, habitat mapping | Regional / study-specific deployment; flexible temporal resolution | Ideal for field studies; requires flight planning and permissions |
| Field photography | Local LULC, agricultural and habitat characterisation | Field campaigns / regional | Complementary to remote sensing; often collected by CROs or field teams |

#### BeeForage

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

## References

xxx  
Pritsch  
Westrich "Die Wildbienen Deutschlands"

