#!/usr/local/bin/python3

"""
0. This script is a quick Folium extension used to demonstrate offline web maps.

1. Folium is a Python wrapper for Leaflet.js

2. Folium generates .html and JS for you.
    2a. This script supports RASTER basemaps in .mbtiles format. Cheers to Ivan Sanchez Ortega who wrote
        Leaflet.TileLayer.MBTiles.js at https://gitlab.com/IvanSanchez/Leaflet.TileLayer.MBTiles
    2b. This script supports .html creation for offline use. This assumes you have all required .js and .css stored
        locally.
    2c. Data overlays (not the basemap) must be .geojson or .topojson.

3. Sample project file structure is as follows:
    ./your_project_name
        /data
            /geojson    # store .geojson overlays here
            /tiles      # store .mbtiles file or standard /{z}/{x}/{y}.png directory format here
                your_tiles.mbtiles
                /tiles/{z}/{x}/{y}.png
        /offline        # store required .js and .css files here.
                        # Leaflet.TileLayer.MBTiles MUST go here for .mbtiles use
        index.html      # this file is generated after running the script.

4. For basic usage, set up your project like the example in step 3, and then modify variables in main()
    to suit your needs.

5. For custom templates, look at the Folium source code to see how it uses jinja2 Templates.
"""

import os

import folium
from jinja2 import Template


def set_offline(file_path):
    """
    Change folium Map templating to look for required .js and .css locally.
    NOTE: These versions may change in time. You must manage/update them manually.
    :param file_path: str system file path to offline file directory
    :return: None
    """

    # compare to _default_js[...] in folium.py
    # modified to look for required .js in ./offline/
    # change relative path to your offline files
    folium.folium._default_js = [
        ('leaflet',
         f'{os.path.join(file_path, "leaflet.js")}'),
        ('jquery',
         f'{os.path.join(file_path, "jquery-1.12.4.min.js")}'),
        ('bootstrap',
         f'{os.path.join(file_path, "bootstrap.min.js")}'),
        ('awesome_markers',
         f'{os.path.join(file_path, "leaflet.awesome-markers.js")}'),
        ('sql',
         f'{os.path.join(file_path, "sql.js")}'),
        ('sql-wasm',
         f'{os.path.join(file_path, "sql-wasm.js")}'),
        ('sql-asm',
         f'{os.path.join(file_path, "sql-adm.js")}'),
        ('mbtiles',
         f'{os.path.join(file_path, "Leaflet.TileLayer.MBTiles.js")}')
    ]

    # compare to _default_css[...] in folium.py
    # modified to look for required .css in ./offline/
    # change relative path to your offline files
    folium.folium._default_css = [
        ('leaflet_css',
         f'{os.path.join(file_path, "leaflet.css")}'),
        ('bootstrap_css',
         f'{os.path.join(file_path, "bootstrap.min.css")}'),
        ('bootstrap_theme_css',
         f'{os.path.join(file_path, "bootstrap-theme.min.css")}'),
        ('awesome_markers_font_css',
         f'{os.path.join(file_path, "font-awesome.min.css")}'),
        ('awesome_markers_css',
         f'{os.path.join(file_path, "leaflet.awesome-markers.css")}'),
        ('awesome_rotate_css',
         f'{os.path.join(file_path, "leaflet.awesome.rotate.css")}')
    ]


def set_online(file_path):
    """
    Change folium Map templating to include Leaflet.TileLayer.MBTiles.js (offline file) and sql.js.
    :return: None
    """

    folium.folium._default_js = [
        ('leaflet',
         'https://cdn.jsdelivr.net/npm/leaflet@1.5.1/dist/leaflet.js'),
        ('jquery',
         'https://code.jquery.com/jquery-1.12.4.min.js'),
        ('bootstrap',
         'https://maxcdn.bootstrapcdn.com/bootstrap/3.2.0/js/bootstrap.min.js'),
        ('awesome_markers',
         'https://cdnjs.cloudflare.com/ajax/libs/Leaflet.awesome-markers/2.0.2/leaflet.awesome-markers.js'),
        ('sql',
         'https://unpkg.com/sql.js@0.3.2/js/sql.js'),
        ('mbtiles',
         f'{os.path.join(file_path, "Leaflet.TileLayer.MBTiles.js")}')
    ]


def set_mbtiles():
    """
    Change folium TileLayer templating from L.tileLayer to L.tileLayer.mbTiles
    Uses Leaflet.TileLayer.MBTiles.js
    https://gitlab.com/IvanSanchez/Leaflet.TileLayer.MBTiles
    :return: None
    """

    # compare to folium raster_layers TileLayer _template in raster_layers.py
    # modified to use Leaflet.TileLayer.MBTiles.js
    # make sure this dependency is in your "offline" local folder
    folium.raster_layers.TileLayer._template = Template(u"""
        {% macro script(this, kwargs) %}
            var {{ this.get_name() }} = L.tileLayer.mbTiles(
                {{ this.tiles|tojson }},
                {{ this.options|tojson }}
            ).addTo({{ this._parent.get_name() }});
        {% endmacro %}
        """)


def main():
    # ---------- set up script parameters ----------

    # True to use offline .js and .css files. False to use Folium default online behavior.
    offline = True

    # relative path to offline .js and .css files.
    offline_file_path = 'offline'

    # relative path to data directory
    data_file_path = 'data'

    # True to use RASTER .mbtiles format. False to use standard /{z}/{x}/{y}.png directory format
    mbtiles = True

    # names of tiles dir or .mbtiles file
    tile_set = 'your_tiles.mbtiles'  # use single file .mbtiles
    # tile_set = 'tiles/{z}/{x}/{y}.png'  # use dir structure.

    # local path for tiles to pass to folium Map
    tile_path = os.path.join(data_file_path, 'tiles', tile_set)

    # attribution. required for custom tile sets
    attr = "e.g. OpenStreetMap contributors"

    # if using offline resources, override folium .js and .css templates. point to local resources.
    if offline:
        set_offline(offline_file_path)
    else:
        set_online(offline_file_path)

    # if tiles are in .mbtiles format (AS RASTER TILES ONLY), override folium TileLayer template.
    if mbtiles:
        set_mbtiles()

    # ------------------------------------------------

    # make folium Map instance
    m = folium.Map(
        location=[33.718651, -116.218178],  # Indio, California
        tiles=tile_path,  # str system file path to tile location
        attr=attr,  # str attribution displayed in lower right corner of browser window
        min_zoom=0,  # "zoomed out" value. 0 is the most zoomed out
        max_zoom=16,  # "zoomed in" value. 14 is practical for file size/zoom balance.
        zoom_start=4,
        control_scale=True,  # Whether a zoom control is added to the map by default.
    )

    # TODO: Additional code here.

    m.save('index.html')


if __name__ == '__main__':
    main()
