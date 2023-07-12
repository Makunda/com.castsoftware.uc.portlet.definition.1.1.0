Welcome to the com.castsoftware.uc.portlet.definition wiki!
>Warning: The Extension described in this document is delivered as-is. This Extension is made available by CAST User Community and governed by Open Source License. Please consider all necessary steps to validate and to test the Extension in your environment before using it in production.        
The extension is published under GNU LGPL v3 open source license

 

# Table of content
- [Introduction](#introduction)
- [In what situation should you install this extension?](#situation)
   - [Use Cases](#usecases)
- [CAST AIP versions compatibility](#aipcompatibility)
- [Supported DBMS servers](#supporteddbms)
- [Configuration instructions](#configuration)
- [Operation instructions](#Operation)
   - [Source preparation and analysis configuration instructions](#preparation)
   - [Analysis processing](#analysis)
   - [Checks to be performed upon analysis](#checks)
- [What results can you expect?](#expect)
   - [List of custom objects](#objects)
   - [List of links between custom objects](#links)
   - [Sample graphical view in Enlighten](#graphical)
   - [Sample views in CAST Imaging](#imaging)
- [Known issues](#KnownIssues)
- [Limitations and potential enhancements](#limitations)
- [Release Notes](#rn)

 

<a name="introduction"></a>
# Introduction
This extensions add the definition of Java portlets.
As of now the extension is able to detect the following portlets:

 | Portlet Specification | Supported | Link |
|-----------------------|-----------|------|
| JSR-168               | YES       | http://java.sun.com/xml/ns/portlet/portlet-app_1_0.xsd     |
| JSR-286               | YES       | http://java.sun.com/xml/ns/portlet/portlet-app_2_0.xsd     |
| IBM Portlet           | NO        | "-//IBM//DTD Portlet Application 1.1//EN""portlet_1.1.dtd"     |


<a name="situation"></a>
# In what situation should you install this extension?
When the Java application is using portlets, the extension will detect the portlets and create the corresponding objects and links.
The portlet definition is usually located in the portlet.xml file of the application inside the WEB-INF folder.
But the extension will take into account any .xml file discovered in the application.
 

<a name="aipcompatibility"></a>
# CAST AIP compatibility

 

This extension is compatible with all AIP versions from 8.3.3 to 8.3.50, and will be also in future versions.
It relies on Extension SDK.

 

<a name="supporteddbms"></a>
# Supported DBMS servers (for Quality Rules)  

 

This extension is compatible with the following DBMS servers (hosting the Analysis Service):

 

| CAST AIP release       | CSS3 | CSS4| PG On Linux|
| -----------------------|:----:|:------:|:--------: |
| All supported releases |   ![Supported](https://github.com/CAST-Extend/resourceALT/blob/master/check.png)  |    ![Supported](https://github.com/CAST-Extend/resourceALT/blob/master/check.png)   |    ![Supported](https://github.com/CAST-Extend/resourceALT/blob/master/check.png)    |

 

<a name="configuration"></a>
# Configuration instructions

 

An Analysis Unit needs to be created. To do so: 
- Create a new Analysis Unit in CAST Management Studio or CAST AIP Console
- Set the analysis name
- Select the main_sources package
- Select the "Java Portlet" in the selected language  

unless auto-discovery is activated by adding the following to the code-scanner-config.xml file:

```xml
<discoverer extensionId="com.castsoftware.uc.portlet.definition" dmtId="javaportletfilediscoverer" fileExtensions=".ZEKE;.zeke;" label="ZEKE"/>
```

in section:
```xml
<package packageType="delivery.SourceFilesPackage" extractorType="dmtdevfolderextractor.SourceFolderExtractor" />
```

 

<a name="operation"></a>
# Operation instructions
<a name="preparation"></a>
## Source preparation and analysis configuration instructions

 

Run a normal analysis.   
 

<a name="operation"></a>
# Operation instructions
<a name="preparation"></a>
## Source preparation and analysis configuration instructions

 

Run a normal analysis.   

 

<a name="analysis"></a>
## Analysis processing


 

<a name="checks"></a>
## Checks to be performed upon analysis

You can check how many objects and links have been created, both in the AU log and the ApplicationExtensions log

 

<a name="expect"></a>
# What results can you expect?
Custom objects and links will be created in Analysis Service as follow:

 

<a name="objects"></a>
## List of custom objects
| ID          |                                                                                  icon                                                                                   | Custom object type     | 
| ------------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------:|:-----------------------|
| 2123111     |                                                            <img src="" alt="JSR 168" width="32" height="32">                                                            | JSR-168 Portlet        |
| 2123112     |                                                            <img src="" alt="JSR 168" width="32" height="32">                                                            | JSR-286 Portlet        |

 

<a name="links"></a>
## List of links created by the extension   
| link type       | Caller type | Callee type | Detection pattern (as of v1.0.0)                                | 
| ----------------|:------------|:------------|:----------------------------------------------------------------|
| callLink        | JSR-168     | Java Class  |                                                                 |
| callLink        | JSR-168     | JSP Page    |                                                                 |
| callLink        | JSR-286     | Java Class  |                                                                 |
| callLink        | JSR-286     | JSP Page    |                                                                 |

 


<a name="graphical"></a>
## Sample graphical view in Enlighten

 

TODO: insert a graphical view here

 

<a name="imaging"></a>
## Sample views in CAST Imaging

 

TODO: insert a view

 

<a name="knownIssues"></a>
# Known issues
- none issue known  

 

<a name="limitations"></a>
# Limitations and potential enhancements
- Definition of IBM Portlet
- Spring portlet definition support 
- Portlet Event definition support

 

<a name="rn"></a>
# Release Notes
## Version 1.1.0
First version published   

 