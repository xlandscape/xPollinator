# Intro

## Get xPollinator

### Option 1: Clone from GitHub

If you just want to inspect or try xPollinator, the easiest way is to get the code directly from GitHub. Below are short, practical steps for a scientific modeller who knows basic IT but is not a Git expert. Choose either the GUI approach (Download ZIP or GitHub Desktop) or the PowerShell/command-line route.

- Prerequisites:
  - Install Git for Windows (<https://git-scm.com/download/win>) if you plan to use PowerShell/command-line.
  - Optionally create a free GitHub account if you want to use GitHub Desktop or contribute changes.

1) Quick — download a ZIP (no git required)
    - Open the repository page in your browser: <https://github.com/xlandscape/xPollinator>
    - Click the green **Code** button and choose **Download ZIP**.
    - Unzip the downloaded file to a folder of your choice, then open it with your editor (e.g., Visual Studio Code).

2) GUI — use GitHub Desktop (recommended if you prefer a graphical client)
    - Install GitHub Desktop (<https://desktop.github.com/>) and sign in with your GitHub account.
    - In the app choose File → Clone repository → URL and paste: <https://github.com/xlandscape/xPollinator.git>
    - Choose a local folder and click **Clone**.

3) Windows Command Prompt / Command-line (quick & reproducible)
    - Open the Windows Command Prompt (cmd.exe) and run these commands:

```bat
REM clone the main repo (HTTPS)
git clone https://github.com/xlandscape/xPollinator.git

REM go into the project folder
cd xPollinator

REM (optional) check out the develop branch which typically contains the latest development work
git fetch --all
git checkout develop

REM open the project folder in Explorer (Windows)
start .

REM (optional) open the project in Visual Studio Code (if installed and in PATH)
code .
```

Notes on authentication and HTTPS vs SSH:

- Public repositories like xPollinator can be cloned via HTTPS without a GitHub account.
- If you prefer SSH and have an SSH key set up, you can clone with the SSH URL instead (`git@github.com:xlandscape/xPollinator.git`).

After cloning: the repository contains documentation, the component source (if applicable) and links to example scenarios. To try the demo scenario referenced in this documentation, also clone the example landscape repository `xPollinatorDemo` (<https://github.com/xlandscape/xPollinatorDemo>) — that repo contains ready-to-run templates and scenarios used in the docs.

Cloning steps vary based on the application being used, eg. [Sourcetree](https://support.atlassian.com/bitbucket-cloud/docs/clone-a-git-repository/) or [Visual Studio Code](https://learn.microsoft.com/en-us/azure/developer/javascript/how-to/with-visual-studio-code/clone-github-repository?tabs=activity-bar). Contact Sascha Bub ([sascha.bub@rptu.de](mailto:sascha.bub@rptu.de)) or Thorsten Schad ([thorsten.schad@landwerk-ev.de](mailto:thorsten.schad@landwerk-ev.de)) in case of problems.  

After cloning the repository, a user will have everything necessary to start using xPollinator including sample scenarios and parametrization files.  

### Option 2: Download xPollinator.zip

To avoid technical steps of closing a GitHub repository, the most resent version(s) of xPollinator are offered as a zip-file for direct download ()'xcopy-readyness').  
xxx here:  

## xP Parameterisation and Configuration

As every landscape derived from the xLandscape framework, xP distinguishes a *parameterisation* from a *configuration* level. xxx  

- ***Parameterisation*** is offered to the (standard) model user as *.xrun* files located at the model root directory. xxx yaml  
- ***Configuration***  

xxx The file *template.xrun* *mc.xml* contains information about the components that are used in the  xPollinator model.  

Example ***.xrun*** file:

``` xml
<Parameters>
  <SimID>TestRun</SimID>
  <Project>scenario/Tarn-et-Garonne-small</Project>
  <NumberBeeHaveTimesteps>365</NumberBeeHaveTimesteps>
  <BeeHaveMapCenterPointX>127406.9408</BeeHaveMapCenterPointX>
  <BeeHaveMapCenterPointY>5482559.8501</BeeHaveMapCenterPointY>
</Parameters>
```

## Running xPollinator

To start xPollinator using the sample scenario, **drag *template.xrun* onto *__start_\_.bat***. This will start an xPollinator run using the demo scenario. Output of the model run can be found in the newly created *\run\Test_Run_xPollinator\mcs\\[mc run ID]\store\arr.dat*.

> [!IMPORTANT]  
> **SimIDs need to be unique**. xPollinator will create a folder for each run using the SimID defined in *template.xrun*. The SimID cannot be the same as a folder already contained in the run folder. If you want to run a simulation with the same SimID you need to delete this folder first.

xxx  
We are fully aware that XML is not the ideal **user interface**. The development of a **graphical user interface (GUI)** is planned.  

## Viewing and Analyzing the Output

### HDFView  

[xLandscape](xLandscape/xLandscape-intro.md) makes use of multidimensional data stores. At present, [HDF](xLandscape/xLandscape-intro.md#multidimensional-data-store) is being used.  

To view the raw output of xPollinator, open *\run\Rummen-demo-scenario\mcs\\[mc run ID]\store\arr.dat* with a HDF5 file viewer such as [HDFView](https://portal.hdfgroup.org/downloads/index.html). Expand the xPollinator folder.

<img src="img/hdf5-file-structure.PNG" alt="Screenshot of output file structure" width="280"/>

Right click on an item and click "Open" to view its attributes and data.

### Jupyter Notebooks

The ***analysis* folder** contains Jupyter notebooks which can analyze and visualize the output of xPollinator. *requirements.txt* lists python packages necessary to run the Jupyter notebooks in this folder.

#### *xBF_write_csv.ipynb*

xxx  
*xBF_write_csv.ipynb* (version 2.0) **writes the contents of *arr.dat* to a csv file**. User parameters:

`xcrop_arrdat_path` : *C:\path\to\arr.dat*

`output_path` : *C:\path\to\output_file.csv*

In the last cell, comment or uncomment any of the following lines to change the columns written to the csv.

``` py
dfs.append(pandas.DataFrame(application_dates, columns=["ApplicationDates"]))
dfs.append(pandas.DataFrame(application_dates_day_month, columns=["ApplicationDayMonth"]))
dfs.append(pandas.DataFrame(applied_features_data, columns=["FeatureID"]))
dfs.append(pandas.DataFrame([feature_id_type_dict.get(x) for x in applied_features_data], columns=["FeatureLULC"]))
dfs.append(pandas.DataFrame(application_rates_data, columns=["ApplicationRates(g/ha)"]))
dfs.append(pandas.DataFrame(decode_PPP, columns=["AppliedPPP"]))
dfs.append(pandas.DataFrame(geom_project_area_ha, columns=["AppliedArea(ha)"]))
dfs.append(pandas.DataFrame(application_rates_data * geom_project_area_ha, columns=["AppliedMass(g)"]))
dfs.append(pandas.DataFrame(drift_reduction_data, columns=["TechnologyDriftReductions"]))
```
