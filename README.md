# A Sample structure for a project in its prototyping stage

The beginning of a project is an exciting time. We want to be able to experiment with different ideas quickly, and draw conclusions from those experiments that we then use as inspiration for the next ideas.
At this stage, we have probably decided on a research question, and are working on finding the correct answer.
In this template, the research question that we are considering is "how can I produce a low-frequency approximation of a mesh?"

## Goals

When prototyping, our main goal is usually speed (I want to go from an idea in my head to a concluded experiment as quickly as possible, so I can know if the idea is good), but there are some things we want to make sure of:

### Reproducibility 

Consider this common scenario: 

> Alice ran an experiment, and got an interesting result (maybe her idea failed in an unexpected way, or maybe it succeeded!). She is very excited to share this result with her collaborators. While she waits for her next project meeting, she finish some other experiments, and in doing so *inadvertently* changes globally defined variables or the functionality of the main algorithm. When the meeting comes around, she runs the same experiment she was originally excited by, but the result is now different / it no longer compiles / it no longer succeeds. Alice spends the meeting describing what the results of the experiment were instead of deciding on the next steps in the project, and she is forced to spend hours and hours digging in her git history (at best) or her memory (more likely...). Alice is frustrated, and her small, inadvertent change to the algorithm delays the project by a week.

There is a simple fix for this: **separating the main functionality of the project from the experiment code**. This template has two folders: a `src/[projectname]` folder containing the main functionality of the research project (e.g., a function called `src/meshapprox/approximate_mesh.py`), and `scripts/`, which contains the code for different experiments (e.g., `scripts/example_mesh_approximation.py`). Different experiments in `scripts/` are independent of each other, and only rely on the functionality in `src/`. 
Scripts in `scripts/` usually consist of loading some data, calling functions in `src/`, and storing or visualizing results.

Thus, when Alice finds a version of her main function `src/meshapprox/approximate_mesh.py` that succeeds for her experiment `scripts/experiment_bunny_mesh_approximation.py`, she *commits her changes* to `src/` and to `scripts/experiment_bunny_mesh_approximation.py`, and can keep freely working on other scripts in `scripts/` with the certainty that any changes that do not affect `src/` will not affect the output of `scripts/experiment_bunny_mesh_approximation.py` when she wants to replicate her results days later.

### Avoiding the worst bugs

Bugs happen. That's fine. But the *worst* bugs are the ones that lead you to the wrong research conclusions. For example:

> Bob has an idea for an algorithm that he is pretty sure should work. He implements his idea in `src/poissonreconstruction/reconstruct_mesh_from_point_cloud.py`, and tests it in a new experiment `scripts/experiment_3d_room_reconstruction.py`. Surprisingly, the reconstruction accuracy is not as good as he expected. Bob takes this result to his next research meeting: his collaborators are surprised but, after weeks of testing different variations of Bob's idea to similar results, eventually conclude that the entire idea should be discarded and they should instead pivot to a different research strategy (or even problem!) entirely. Months later, Bob realizes that *there was a bug in the function that was calculating the reconstruction accuracy*, which made him think his method was worse than it was. His idea was actually good! But a bug in his evaluation code led his team in entirely different research direction.

There is also a very simple, and only minimally time-consuming, fix for this: **every function used in an experiment should be exhaustively unit-tested**. Every file `src/[functionname].py` (i.e., in the main research algorithm functionality) and in `utility/[functionname].py` (`utility` contains common functions used throughout experiments outside of the main algorithm's functionality) has an equivalent file `test/test_[functionname].py` which exhaustively checks the behavior of the function.
*No function should ever be added to `src/` or `utility/` without a corresponding, exhaustive unit test*.

## Structure

Let's go over each element of this repository:

### `src/[project_name]/`

This is the most important folder, as it contains the main functionality of your research. If you are writing a paper about surface reconstruction, this folder will have a `reconstruct_surface.py` function and all other functions that `reconstruct_surface.py` needs to function (and only those).
The code in this function *should not call or depend on any other piece of code or data anywhere else in the repository*: one should be able to copy-paste this folder and use it as a python module, running `import [project_name]` without any missing local dependencies.

Because almost every other element of the project will depend on this folder, one should very carefully follow rules when handling it:

*When adding functions:*
- One function per file. No more than one function should be defined in each file, except for auxiliary functions that are only used within that file.
- Every added function `src/[project_name]/[function_name].py` must have an associated added unit test `test/[function_name].py`. There will not be that many functions, so dedicate some time to thinking what an exhaustive unit test looks like. If you are writing a project about surface reconstruction, you may want to check that a higher number of samples leads to higher accuracy, and that this behavior is consistent across different inputs. You may also want to check that every possible input parameter combination results in a valid output, and that the parameters are having the intended effect.

*When editing functions:*
- If your change adds a new parameter to an existing `src/[project_name]/[function_name].py`, edit `test/[function_name].py` accordingly to **exhaustively and convincingly** test that the effect of this parameter is the one you expect, including what the default behavior is. A common easy technique if you do not wish to change the default behavior of a function is to choose an input, run the function for that input with no optional parameters, save the output to a file in `data/`, and add a unit test that checks for exact match with the saved output.
- Before committing and pushing a change to `src/`, **re-run every unit test in `test/` and every script in `scripts/`**. Do the tests pass, and are the outputs what you expect? A common issue is that your function API changed, so some of the experiments in `scripts/` no longer run. This is fine: either spend the time updating those old script files, or delete them (ensuring they are in the git history). This is what version control is for, and we should have **no legacy, un-runnable code** in the `scripts/` directory (or anywhere).
- **Properly document** (with commit message and code comments) what the change to your core method's functionality was (e.g., "added support for 3D inputs", "fixed bug blahblah", "new SDF-based method").

### `utility/`

This folder contains functions that are outside the main functionality of your method, but that you will still need to call in many different experiments. For example: evaluation code that checks the accuracy of an input or output, I/O code that reads or writes files, or plotting / visualization code.
The rules for this folder are similar to `src/`: there should be one function per file and every function (except perhaps plotting ones) should have an associated exhaustive unit test in `test/`.
Before pushing a change to `utility/`, one should check that all `scripts/` and `test/` run successfully.

### `test/`

This folder contains unit tests for every function in the project. An easy way of doing this is with the `unittest` library, with which you can run every unit test by calling `python -m unittest` from the repository's root directory. Take a look at the example `test/test_approximate_mesh.py` to see what a template test can look like.

### `scripts/`

These are the only executable files in your project, i.e., the only ones that you will run by calling `python scripts/[name_of_script].py` (all others are imported). This folder is where most of your work happens: you design new experiments, you try new method ideas, you visualize, you debug... All this is done through different files in `scripts/`. To ensure reproducibility while working freely in this folder, here are some things to keep in mind:
- Many of your scripts will produce results (plots, output meshes, etc.) that you want to save. It is helpful to create, for every `scripts/[name_of_script].py`, a corresponding `results/[name_of_script]/`, and programatically ensure that all written files are in this results folder. This will avoid overwriting files with those of newer experiments, and will avoid you not remembering which script led to which result.
- Each script should depend on `src/`, `utility/`, `data/` and external dependencies *only*. Importantly, this means *no script can depend on another script*. If there is some functionality that you wish to use in more than one script, add it to `utility/` or `src/` and write a unit test for it.

### `results/`

This folder contains all files produced by `scripts/`, in folders `results/[name_of_script]` for each `script/[name_of_script].py`. Depending on the specifics of a project, this folder can be hidden from git fully or partly: a good middle-ground is to hide from .git any large `.obj` files but commit low-resolution renders of each output. Every time a change to a `script/` is pushed, the `results/` folder should be updated with the output of that script.

### `data/`

This contains all external data that is needed to run the scripts and unit tests: most often, this is input data in the form of 3D meshes or scenes obtained from the internet. 
Make sure to track the origin of every asset that you did not create yourself, so we can properly credit artists at the end. Unless the asset is obviously public domain, every `data/[asset].[ext]` should be accompanied by a `data/[asset].txt` file referencing its origin.

### `requirements.txt`

Any external library that you need should be listed here, with the version that you have installed in the local machine you are developing in. Nothing is more frustrating than getting a new computer, or sharing your code with someone, and them not being able to run it because of a version mis-match. A well maintained `requirements.txt` fixes this.

## Sample workflow
