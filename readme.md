```
                              '             .           .
                           o       '   o  .     '   . O
                        '   .   ' .   _____  '    .      .
                         .     .   .mMMMMMMMm.  '  o  '   .
                       '   .     .MMXXXXXXXXXMM.    .   ' 
                      .       . /XX77:::::::77XX\ .   .   .
                         o  .  ;X7:::''''''':::7X;   .  '
                        '    . |::'.:'        '::| .   .  .
                           .   ;:.:.            :;. o   .
                        '     . \'.:            /.    '   .
                           .     `.':.        .'.  '    .
                         '   . '  .`-._____.-'   .  . '  .
                          ' o   '  .   O   .   '  o    '
                           . ' .  ' . '  ' O   . '  '   '
                            . .   '    '  .  '   . '  '
                             . .'..' . ' ' . . '.  . '
                              `.':.'        ':'.'.'
                                `\\_  |     _//'
                                  \(  |\    )/
                                  //\ |_\  /\\
                                 (/ /\(" )/\ \)
                                  \/\ (  ) /\/
                                     |(  )|
                                     | \( \
                                     |  )  \
                                     |      \
                                     |       \
                                     |        `.__,
                                     \_________.-'
It's magic.
```
# Who is this for?
Developers and security practitioners who want to perform graph analysis on data flow diagrams - using SQL. 

The use case for this analysis implemented by materialize_threats determines STRIDE threats impacting specific flows and elements based on trust zone and flow direction.

# What's in the box?
* Draw.io shape library (dfd-materialize.xml)
    * Create diagrams supported for analysis
* materialize_threats python module
    * Parse supported .drawio file into graph representation (nodes, edges) stored in sqlite
    * SQL (ORM) implementation of Rapid Threat Model Prototyping methodology


# Using
## 1. Creating the diagram
* Use draw.io to import the dfd-materialize.xml shape library
* Create a data flow diagram using the shapes
* Save it as a .drawio file in a convenient location

## 2. Enumerating threats
```
git clone git@github.com:secmerc/materialize_threats.git
python3 materialize_threats/materialize.py --filename=/path/to/diagram.drawio
```

# Sample data
Default to sample
```
python3 materialize_threats/materialize.py
```

Specify alternate sample
```
python3 materialize_threats/materialize.py --filename=samples/sample.drawio
```

# Resources for Mxgraph
* https://github.com/jgraph/mxgraph
* https://github.com/jgraph/mxgraph/blob/7af5a44c5b2d8a4d0fc56d3eebc964c3ca8b82de/java/examples/com/mxgraph/examples/Codec.java
* https://github.com/jgraph/mxgraph/blob/51382db43061ac4f30a87c835d17e306378b1af4/java/src/com/mxgraph/io/mxCellCodec.java
* https://github.com/jgraph/mxgraph/blob/51382db43061ac4f30a87c835d17e306378b1af4/java/src/com/mxgraph/io/mxRootChangeCodec.java
* https://github.com/jgraph/mxgraph/blob/51382db43061ac4f30a87c835d17e306378b1af4/java/src/com/mxgraph/model/mxCell.java

