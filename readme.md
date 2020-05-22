# Todo
[ x ] Introduce higher level mxcell concept, then handle user objects which wrap mxcells. We want to continue the 'value' design by stripping the user object off of the outside of the mxcell, then embedding it as the mxcell.value
[ x ] Fix up the factories to handle the gid, sid being in the user object, not the mxcell
[ X ] Implement UserObject and UserObjectFactory
[ ] Move geometry to shapely
[ ] Add convenience functions to edges for directionality

# Running
`python3 -m materialize_threats.parse`

# Sample data
```
 <mxGraphModel dx="1956" dy="1884" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="850" pageHeight="1100" math="0" shadow="0">
  <root>
    <mxCell id="0" />
    <mxCell id="1" parent="0" />
    <UserObject type="entity" label="Browser" id="d7KARgRL_lCWHV6r2neS-26">
      <mxCell style="rounded=0;whiteSpace=wrap;html=1;" parent="1" vertex="1">
        <mxGeometry x="-380" y="-680" width="120" height="60" as="geometry" />
      </mxCell>
    </UserObject>
    <UserObject type="process" label="User logs in&lt;br&gt;POST /login" id="d7KARgRL_lCWHV6r2neS-27">
      <mxCell style="ellipse;whiteSpace=wrap;html=1;aspect=fixed;" parent="1" vertex="1">
        <mxGeometry x="-140" y="-690" width="80" height="80" as="geometry" />
      </mxCell>
    </UserObject>
    <UserObject type="dataStore" label="Database" id="d7KARgRL_lCWHV6r2neS-28">
      <mxCell style="shape=partialRectangle;whiteSpace=wrap;html=1;left=0;right=0;fillColor=none;" parent="1" vertex="1">
        <mxGeometry x="360" y="-680" width="120" height="60" as="geometry" />
      </mxCell>
    </UserObject>
    <mxCell id="d7KARgRL_lCWHV6r2neS-2" value="" style="endArrow=classic;html=1;fontColor=#FF3333;exitX=1;exitY=0.5;exitDx=0;exitDy=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0;" parent="1" source="d7KARgRL_lCWHV6r2neS-26" target="d7KARgRL_lCWHV6r2neS-27" edge="1">
      <mxGeometry width="50" height="50" relative="1" as="geometry">
        <mxPoint x="-290" y="-430" as="sourcePoint" />
        <mxPoint x="-240" y="-480" as="targetPoint" />
      </mxGeometry>
    </mxCell>
    <UserObject type="entity" label="API" id="d7KARgRL_lCWHV6r2neS-7">
      <mxCell style="rounded=0;whiteSpace=wrap;html=1;" parent="1" vertex="1">
        <mxGeometry x="10" y="-680" width="120" height="60" as="geometry" />
      </mxCell>
    </UserObject>
    <mxCell id="d7KARgRL_lCWHV6r2neS-11" value="" style="endArrow=classic;html=1;fontColor=#FF3333;exitX=1;exitY=0.5;exitDx=0;exitDy=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0;" parent="1" source="d7KARgRL_lCWHV6r2neS-27" target="d7KARgRL_lCWHV6r2neS-7" edge="1">
      <mxGeometry width="50" height="50" relative="1" as="geometry">
        <mxPoint x="100" y="-490" as="sourcePoint" />
        <mxPoint x="240" y="-480" as="targetPoint" />
      </mxGeometry>
    </mxCell>
    <UserObject type="process" label="Fetch pw hash" id="d7KARgRL_lCWHV6r2neS-13">
      <mxCell style="ellipse;whiteSpace=wrap;html=1;aspect=fixed;" parent="1" vertex="1">
        <mxGeometry x="210" y="-690" width="80" height="80" as="geometry" />
      </mxCell>
    </UserObject>
    <mxCell id="d7KARgRL_lCWHV6r2neS-15" value="" style="endArrow=classic;html=1;fontColor=#FF3333;exitX=0;exitY=0.5;exitDx=0;exitDy=0;entryX=1;entryY=0.5;entryDx=0;entryDy=0;" parent="1" source="d7KARgRL_lCWHV6r2neS-28" target="d7KARgRL_lCWHV6r2neS-13" edge="1">
      <mxGeometry width="50" height="50" relative="1" as="geometry">
        <mxPoint x="320" y="-670" as="sourcePoint" />
        <mxPoint x="330" y="-610" as="targetPoint" />
      </mxGeometry>
    </mxCell>
    <mxCell id="d7KARgRL_lCWHV6r2neS-18" value="" style="endArrow=classic;html=1;fontColor=#FF3333;exitX=0;exitY=0.5;exitDx=0;exitDy=0;entryX=1;entryY=0.5;entryDx=0;entryDy=0;" parent="1" source="d7KARgRL_lCWHV6r2neS-13" target="d7KARgRL_lCWHV6r2neS-7" edge="1">
      <mxGeometry width="50" height="50" relative="1" as="geometry">
        <mxPoint x="200" y="-661" as="sourcePoint" />
        <mxPoint x="130" y="-661" as="targetPoint" />
      </mxGeometry>
    </mxCell>
    <UserObject type="trust zone" label="Z0" placeholders="1" name="Variable" id="d7KARgRL_lCWHV6r2neS-21">
      <mxCell style="text;html=1;strokeColor=#82b366;fillColor=#d5e8d4;align=center;verticalAlign=middle;whiteSpace=wrap;overflow=hidden;" parent="1" vertex="1">
        <mxGeometry x="-290" y="-680" width="30" height="20" as="geometry" />
      </mxCell>
    </UserObject>
    <UserObject type="trust zone" label="Z0" placeholders="1" name="Variable" id="d7KARgRL_lCWHV6r2neS-3">
      <mxCell style="text;html=1;strokeColor=#82b366;fillColor=#d5e8d4;align=center;verticalAlign=middle;whiteSpace=wrap;overflow=hidden;" vertex="1" parent="1">
        <mxGeometry x="-115" y="-690" width="30" height="20" as="geometry" />
      </mxCell>
    </UserObject>
    <UserObject type="trust zone" label="Z1" placeholders="1" name="Variable" id="d7KARgRL_lCWHV6r2neS-8">
      <mxCell style="text;html=1;strokeColor=#82b366;fillColor=#d5e8d4;align=center;verticalAlign=middle;whiteSpace=wrap;overflow=hidden;fontStyle=0" vertex="1" parent="1">
        <mxGeometry x="10" y="-680" width="30" height="20" as="geometry" />
      </mxCell>
    </UserObject>
    <UserObject type="trust zone" label="Z2" placeholders="1" name="Variable" id="d7KARgRL_lCWHV6r2neS-12">
      <mxCell style="text;html=1;strokeColor=#82b366;fillColor=#d5e8d4;align=center;verticalAlign=middle;whiteSpace=wrap;overflow=hidden;fontStyle=0" vertex="1" parent="1">
        <mxGeometry x="230" y="-690" width="30" height="20" as="geometry" />
      </mxCell>
    </UserObject>
    <UserObject type="trust zone" label="Z9" placeholders="1" name="Variable" id="d7KARgRL_lCWHV6r2neS-14">
      <mxCell style="text;html=1;strokeColor=#82b366;fillColor=#d5e8d4;align=center;verticalAlign=middle;whiteSpace=wrap;overflow=hidden;fontStyle=0" vertex="1" parent="1">
        <mxGeometry x="450" y="-680" width="30" height="20" as="geometry" />
      </mxCell>
    </UserObject>
  </root>
</mxGraphModel>
```
TODO: https://github.com/hbmartin/graphviz2drawio/tree/master/graphviz2drawio/mx