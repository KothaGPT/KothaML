# Workspace Update Process

We plan to do a full workspace image update (all libraries and tools) about every three months. The full update involves manual work. We use a systematic approach to update all tools and libraries.

1. Update core (process) tools and interpreters:

   - Tini: [latest release](https://github.com/krallin/tini/releases/latest)
   - OpenResty: [latest release](https://openresty.org/en/download.html)
   - Miniconda: [latest release](https://repo.continuum.io/miniconda/), [python version](https://anaconda.org/conda-forge/python)
   - Node.js: [latest release](https://nodejs.org/en/download/current/)

2. Update core (gui) tools:

   - TigerVNC: [latest release](https://dl.bintray.com/tigervnc/stable/)
   - noVNC: [latest release](https://github.com/novnc/noVNC/releases/latest)
   - Websockify: [latest release](https://github.com/novnc/websockify/releases/latest)
   - VS Code Server: [latest release](https://github.com/cdr/code-server/releases/latest)
   - Ungit: [latest release](https://www.npmjs.com/package/ungit)
   - FileBrowser: [latest release](https://github.com/filebrowser/filebrowser/releases/latest)

3. Update conda packages:

   - Update to latest release of packages: Jupyter Notebook, JupyterLab, IPython, Tensorflow, PyTorch

4. Update VS-code extensions:

   - Update to latest release of extensions: python, java, prettier, jupyter, code-runner, eslint

5. Update tool installer scripts:

   - Update to latest releases of tools: intellij.sh, pycharm.sh, nteract.sh, r-runtime.sh, sqlectron.sh, zeppelin.sh, robo3t.sh, metabase.sh, fasttext.sh, kubernetes-utils.sh, portainer.sh, rapids-gpu.sh

6. Update `minimmal` and `light` flavor Python libraries:

   - Update requirement files using [piprot](https://github.com/sesh/piprot), [pur](https://github.com/alanhamlett/pip-update-requirements), or [pip-upgrader](https://github.com/simion/pip-upgrader):
     - `piprot ./resources/libraries/requirements-minimal.txt`
     - `piprot ./resources/libraries/requirements-light.txt`
     - [pur](https://github.com/alanhamlett/pip-update-requirements) example: `pur -i -r ./resources/libraries/requirements-minimal.txt`

7. Build and test flavors:

   - Build and test `minimal` flavor via `python build.py --make --flavor=minimal`
   - Build and test `light` flavor via `python build.py --make --flavor=light`
   - Build and test `full` flavor via `python build.py --make --flavor=full`
   - Build and test `gpu` flavor via `python build.py --make --flavor=gpu`

8. Build and push all flavors via `python build.py --deploy --version=<VERSION> --flavor=all`
