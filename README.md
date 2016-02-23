# PyMapLib
A Python maps API that enables geospatial data visualization

PyMapLib library is designed as a generic framework for geospatial data visualization. As an effort of the GABBs project (NSF DIBBS), this library provides a simple API to a wealth of GIS capabilities to tool developers. The goal of this project is to make it easy to handle geospatial data and visualization without requiring the developer to have in-depth GIS knowledge, hence making it easier for scientists to share spatial data interactively. 

The PyMapLib provides:

1.	A basic map API, following the Google Map API style, for users to easily create map and overly layers and add to their applications. For handling common software tasks such as data source provider, map tile management, raster and vector data rendering, PyMapLibutilizes PyQGIS, a python binding to QGis Geospatial Information System library, and abstract a wrapping layer from QGis.
2.	A set of map tools to enhance PyMapLib’sinteractive functions. These map tools can be accessed inPyMapLib as optional configurations. A user can set map properties according to specific needs. Features include map control (pan, zoom, select), HTML tip display, map layer management (add layer, remove layer, hide and show layer), map style (set rendering style, symbol style, font, color ramp and etc), map overview, map user action and event (execute customized user function), map value tool (inspect raster value and display with table and plot).
3.	A map widget (using PyMapLib) that can be embedded in third party applications. This is essentially an example application that usesthe PyMapLib API introduced above, and is encapsulatedas a geospatial Map Widget. Developers of third party applications mayimport or embed and configure this Map Widget on-the-fly in their tools, e.g., for displaying map and spatial data layers, without additional programming. 

Background Information

We have worked with a diverse range of use cases, most of which are scientific applications where scientists (not expert programmers) wish to share their geospatial data interactively via open source software. The data types range from vector, raster, delimited text, web map tile, to database sources. Users require frequent interaction with the map, e.g., exploring data values from the input and output. Some may need basicgeospatial data processing or analysis while exploring.We have identified a need for a feature-rich, high performance but light weight maplibrary for HUBzero tool developers. After investigating several potential GIS libraries(including Mapnik), we chose QGis as the geospatial data render engine for PyMapLib, and addedmap tools for additional features in PyMapLib. PyMapLib extended QGis by support more types of geospatial data andcapabilities, such as map style, rendering modes, user defined actions, map tip, and basic geospatial data analyses. In this way, PyMapLib provide a mini GIS system as a backend to empower HUBzero tools. The library package can help bridge the gap between research and implementation, and provide a building block for geospatial data visualization.
Future versions of PyMapLib will support Linux desktop tools (independent of HUBzero), and potentially Windows operating system. 

Visit http://mygeohub.org for more information and get the user manual.
