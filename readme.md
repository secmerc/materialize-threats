# Todo
- as much as possible, the objects we use should be wrappers around XML - this means that everyone has self.xml, and all setters/getters abstract xml shit
- once thats the case, storing new metadata onto the xml is pointless - we need to store the metadata wherever it will be useful to the threat analysis framework. as a result, 
- [ ] we should start loading things into neo4j now and do a PoC for STRIDE against the diagram.



- [x] Introduce higher level mxcell concept, then handle user objects which wrap mxcells. We want to continue the 'value' design by stripping the user object off of the outside of the mxcell, then embedding it as the mxcell.value
- [x] Fix up the factories to handle the gid, sid being in the user object, not the mxcell
- [x] Implement UserObject and UserObjectFactory
- [x] Now that we have orphan zone objects, how do we update the entity it belongs to?
- [x] Determine where/how we'll power graph analysis, is neo4j overkill?
- [ ] Move geometry to shapely
- [ ] ~~Add convenience functions to edges for directionality~~
- [ ] store the element type so we can skip over processes during threat detection
- [ ] should we pivot to json based flat storage?

# Cloning & Running
```
git clone git@github.com:secmerc/materialize_threats.git
python3 -m materialize_threats.parse
```

# Sample data
```
samples/sample.drawio
```
