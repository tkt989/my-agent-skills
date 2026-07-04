# CSVインデックス仕様

## files.csv

```csv
path,module,type,responsibility,importance,depends_on,notes
```

## classes.csv

```csv
class,file,module,responsibility,key_methods,dependencies,importance,notes
```

## symbols.csv

```csv
symbol,kind,file,module,description,exported,importance,notes
```

## modules.csv

```csv
module,path,responsibility,importance,main_files,notes
```

## dependencies.csv

```csv
source,target,dependency_type,description,confidence,notes
```

## flows.csv

```csv
flow,summary,entrypoint,main_modules,importance,related_files,notes
```
