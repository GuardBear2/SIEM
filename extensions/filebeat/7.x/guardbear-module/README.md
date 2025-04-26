# GuardBear Filebeat module

## Hosting

The GuardBear Filebeat module is hosted at the following URLs

- Production:
  - https://packages.guardbear.com/4.x/filebeat/
- Development:
  - https://packages-dev.guardbear.com/pre-release/filebeat/
  - https://packages-dev.guardbear.com/staging/filebeat/

The GuardBear Filebeat module must follow the following nomenclature, where revision corresponds to X.Y values

- guardbear-filebeat-{revision}.tar.gz

Currently, we host the following modules

|Module|Version|
|:--|:--|
|guardbear-filebeat-0.1.tar.gz|From 3.9.x to 4.2.x included|
|guardbear-filebeat-0.2.tar.gz|From 4.3.x to 4.6.x included|
|guardbear-filebeat-0.3.tar.gz|4.7.x|
|guardbear-filebeat-0.4.tar.gz|From 4.8.x to current|


## How-To update module tar.gz file

To add a new version of the module it is necessary to follow the following steps:

1. Clone the guardbear/guardbear repository
2. Check out the branch that adds a new version
3. Access the directory: **extensions/filebeat/7.x/guardbear-module/**
4. Create a directory called: **guardbear**

```
# mkdir guardbear
```

5. Copy the resources to the **guardbear** directory

```
# cp -r _meta guardbear/
# cp -r alerts guardbear/
# cp -r archives guardbear/
# cp -r module.yml guardbear/
```

6. Set **root user** and **root group** to all elements of the **guardbear** directory (included)

```
# chown -R root:root guardbear
```

7. Set all directories with **755** permissions

```
# chmod 755 guardbear
# chmod 755 guardbear/alerts
# chmod 755 guardbear/alerts/config
# chmod 755 guardbear/alerts/ingest
# chmod 755 guardbear/archives
# chmod 755 guardbear/archives/config
# chmod 755 guardbear/archives/ingest
```

8. Set all yml/json files with **644** permissions

```
# chmod 644 guardbear/module.yml
# chmod 644 guardbear/_meta/config.yml
# chmod 644 guardbear/_meta/docs.asciidoc
# chmod 644 guardbear/_meta/fields.yml
# chmod 644 guardbear/alerts/manifest.yml
# chmod 644 guardbear/alerts/config/alerts.yml
# chmod 644 guardbear/alerts/ingest/pipeline.json
# chmod 644 guardbear/archives/manifest.yml
# chmod 644 guardbear/archives/config/archives.yml
# chmod 644 guardbear/archives/ingest/pipeline.json
```

9. Create **tar.gz** file

```
# tar -czvf guardbear-filebeat-0.4.tar.gz guardbear
```

10. Check the user, group, and permissions of the created file

```
# tree -pug guardbear
[drwxr-xr-x root     root    ]  guardbear
├── [drwxr-xr-x root     root    ]  alerts
│   ├── [drwxr-xr-x root     root    ]  config
│   │   └── [-rw-r--r-- root     root    ]  alerts.yml
│   ├── [drwxr-xr-x root     root    ]  ingest
│   │   └── [-rw-r--r-- root     root    ]  pipeline.json
│   └── [-rw-r--r-- root     root    ]  manifest.yml
├── [drwxr-xr-x root     root    ]  archives
│   ├── [drwxr-xr-x root     root    ]  config
│   │   └── [-rw-r--r-- root     root    ]  archives.yml
│   ├── [drwxr-xr-x root     root    ]  ingest
│   │   └── [-rw-r--r-- root     root    ]  pipeline.json
│   └── [-rw-r--r-- root     root    ]  manifest.yml
├── [drwxr-xr-x root     root    ]  _meta
│   ├── [-rw-r--r-- root     root    ]  config.yml
│   ├── [-rw-r--r-- root     root    ]  docs.asciidoc
│   └── [-rw-r--r-- root     root    ]  fields.yml
└── [-rw-r--r-- root     root    ]  module.yml
```

11. Upload file to development bucket
