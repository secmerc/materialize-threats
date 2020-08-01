```
materialize threats.
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
                                     |wizardsh`.__,_
                                     \_________.-'
It's magic.
```
# Who is this for?
Developers and security practitioners who want to perform 'graph' analysis on data flow diagrams - **using SQL**. 

`materialize threats` ingests draw.io data flow diagrams into a database, represents them like a property graph, then uses SQL to answer questions about them. 

Today, we can answer questions like:

* Which STRIDE based threat classes impact the elements and flows in my diagram?
* What test cases should be considered for this diagram? 

# What's in the box?
* materialize_threats python module
    * Parse .drawio data flow diagrams into graph representation (nodes, edges) stored in a RDMS (sqlite in this demo)
    * SQL (ORM) implementation of [Rapid Threat Model Prototyping methodology](https://github.com/geoffrey-hill-tutamantic/rapid-threat-model-prototyping-docs) used to generate threat classes
* (Optional) Minimal Draw.io shape library (dfd-materialize.xml)
    * Tag trust zones more easily
* Gherkin test plan generator

# How do I use it?
## Demo
![](samples/bookface.gif)

## 1. Creating the diagram
* Use draw.io with the built-in threat modeling shape set, or use ours
* Create a data flow diagram using some guidelines
   * Use processes between entities to describe flows
      * Example: [Entity: Browser] --> (Process: Login) ----> [Entity: API]
   * Identify trust zones using the green 'security control label'
   * Processes inherit trust zones from the upstream entity
* Save it as a .drawio file in a convenient location

### Example
![](samples/bookface.png)

## 2. Enumerating threats
```
git clone git@github.com:secmerc/materialize_threats.git
python3 materialize_threats/materialize.py --filename=/path/to/diagram.drawio
```

## 3. Creating the feature file
Materialize threats will create a Gherkin feature file with boilerplate scenarios and mitigations, along with remediation tips. By default, it uses the diagram filename.

![](samples/bookface_featurefile.png)

# Sample data
```
python3 materialize_threats/materialize.py
```

More samples can be found in the /samples directory
```
python3 materialize_threats/materialize.py --filename=samples/bookface.drawio
```