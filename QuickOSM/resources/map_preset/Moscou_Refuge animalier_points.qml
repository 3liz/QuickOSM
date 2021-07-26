<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis version="3.16.7-Hannover" styleCategories="Symbology|Actions">
  <renderer-v2 enableorderby="0" forceraster="0" type="singleSymbol" symbollevels="0">
    <symbols>
      <symbol clip_to_extent="1" force_rhr="0" name="0" alpha="1" type="marker">
        <layer locked="0" pass="0" class="SimpleMarker" enabled="1">
          <prop k="angle" v="0"/>
          <prop k="color" v="219,30,42,255"/>
          <prop k="horizontal_anchor_point" v="1"/>
          <prop k="joinstyle" v="bevel"/>
          <prop k="name" v="triangle"/>
          <prop k="offset" v="0,0"/>
          <prop k="offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="offset_unit" v="MM"/>
          <prop k="outline_color" v="128,17,25,255"/>
          <prop k="outline_style" v="solid"/>
          <prop k="outline_width" v="0.4"/>
          <prop k="outline_width_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="outline_width_unit" v="MM"/>
          <prop k="scale_method" v="diameter"/>
          <prop k="size" v="4"/>
          <prop k="size_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="size_unit" v="MM"/>
          <prop k="vertical_anchor_point" v="1"/>
          <data_defined_properties>
            <Option type="Map">
              <Option value="" name="name" type="QString"/>
              <Option name="properties"/>
              <Option value="collection" name="type" type="QString"/>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
    </symbols>
    <rotation/>
    <sizescale/>
  </renderer-v2>
  <blendMode>0</blendMode>
  <featureBlendMode>0</featureBlendMode>
  <attributeactions>
    <defaultAction value="{00000000-0000-0000-0000-000000000000}" key="Canvas"/>
    <actionsetting capture="0" notificationMessage="" id="{55c22a50-a641-45f9-a337-4b0f0a582bc7}" name="Navigateur OSM" shortTitle="Navigateur OSM" isEnabledOnlyWhenEditable="0" type="5" action="http://www.openstreetmap.org/browse/[% &quot;osm_type&quot; %]/[% &quot;osm_id&quot; %]" icon="">
      <actionScope id="Field"/>
      <actionScope id="Canvas"/>
      <actionScope id="Feature"/>
    </actionsetting>
    <actionsetting capture="0" notificationMessage="" id="{4df20cfa-6686-4c7e-a086-490dd9dcbeda}" name="JOSM" shortTitle="JOSM" isEnabledOnlyWhenEditable="0" type="1" action="from QuickOSM.core.actions import Actions;Actions.run(&quot;josm&quot;,&quot;[% &quot;full_id&quot; %]&quot;)" icon="C:\Users\monts\AppData\Roaming\QGIS\QGIS3\profiles\Dev\python\plugins\QuickOSM\resources\icons\josm_icon.svg">
      <actionScope id="Field"/>
      <actionScope id="Canvas"/>
      <actionScope id="Feature"/>
    </actionsetting>
    <actionsetting capture="0" notificationMessage="" id="{a34a1fcb-08e1-4df5-8201-9617e32f8557}" name="Éditeur de l'utilisateur par défaut" shortTitle="Éditeur de l'utilisateur par défaut" isEnabledOnlyWhenEditable="0" type="5" action="http://www.openstreetmap.org/edit?[% &quot;osm_type&quot; %]=[% &quot;osm_id&quot; %]" icon="">
      <actionScope id="Field"/>
      <actionScope id="Canvas"/>
      <actionScope id="Feature"/>
    </actionsetting>
    <actionsetting capture="0" notificationMessage="" id="{b4383d9c-6b27-470e-b621-97491f69f45f}" name="Reload the query in a new file" shortTitle="Reload the query in a new file" isEnabledOnlyWhenEditable="0" type="1" action="from QuickOSM.core.actions import Actions;Actions.run_reload(layer_name=&quot;amenity_animal_shelter_Moscou&quot;)" icon="">
      <actionScope id="Layer"/>
    </actionsetting>
  </attributeactions>
  <layerGeometryType>0</layerGeometryType>
</qgis>
