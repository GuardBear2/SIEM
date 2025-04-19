## Engine Development Container

This container is used to develop the GuardBear engine. 

Features:
- It has all the necessary dependencies to compile guardbear-engine from source.
- guardbear-engine is installed in the container in cration time.
- vscode settings, task and launch config are included in the container to make it easier to develop with vscode.

## Usage

To build the devContainer from scratch, run the following command:

```bash
curl -o download_devContainer.sh https://raw.githubusercontent.com/guardbear/guardbear/main/src/engine/tools/devContainer/download_devContainer.sh
chmod +x download_devContainer.sh
./download_devContainer.sh -h
```

> [!NOTE]
> Only works on Linux.
