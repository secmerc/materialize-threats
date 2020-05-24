# Todo
- [x] Introduce higher level mxcell concept, then handle user objects which wrap mxcells. We want to continue the 'value' design by stripping the user object off of the outside of the mxcell, then embedding it as the mxcell.value
- [x] Fix up the factories to handle the gid, sid being in the user object, not the mxcell
- [x] Implement UserObject and UserObjectFactory
- [ ] Now that we have orphan zone objects, how do we update the entity it belongs to?
- [ ] Determine where/how we'll power graph analysis, is neo4j overkill?
- [ ] Move geometry to shapely
- [ ] Add convenience functions to edges for directionality

# Cloning & Running
```
git clone git@github.com:secmerc/materialize_threats.git
python3 -m materialize_threats.parse
```

# Sample data
```
samples/sample.drawio
```
