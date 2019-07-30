# nf-core/denovohybrid: Usage

## Table of contents

<!-- Install Atom plugin markdown-toc-auto for this ToC to auto-update on save -->
<!-- TOC START min:2 max:3 link:true asterisk:true update:true -->
* [Table of contents](#table-of-contents)
* [Introduction](#introduction)
* [Running the pipeline](#running-the-pipeline)
  * [Updating the pipeline](#updating-the-pipeline)
  * [Reproducibility](#reproducibility)
* [Main arguments](#main-arguments)
  * [`-profile`](#-profile)
  * [`--input`](#--input)
  * [`--mode`](#--singleend)
    * [`unicycler`](#unicycler)
    * [`miniasm`](#miniasm)
    * [`wtdbg2 `](#wtdbg2)
    * [`all`](#all)
* [Sample specific parameters]
  * [`--genomeSize`](#--genomeSize)
  * [`--minContigLength`](#--minContigLength)
  * [`--targetShortReadCov / --targetLongReadCov`](#--targetshortreadcov_/_targetlongreadcov)
* [Job resources](#job-resources)
  * [Automatic resubmission](#automatic-resubmission)
  * [Custom resource requests](#custom-resource-requests)
* [AWS Batch specific parameters](#aws-batch-specific-parameters)
  * [`--awsqueue`](#--awsqueue)
  * [`--awsregion`](#--awsregion)
* [Other command line parameters](#other-command-line-parameters)
  * [`--outdir`](#--outdir)
  * [`--email`](#--email)
  * [`-name`](#-name)
  * [`-resume`](#-resume)
  * [`-c`](#-c)
  * [`--custom_config_version`](#--custom_config_version)
  * [`--custom_config_base`](#--custom_config_base)
  * [`--max_memory`](#--max_memory)
  * [`--max_time`](#--max_time)
  * [`--max_cpus`](#--max_cpus)
  * [`--plaintext_email`](#--plaintext_email)
  * [`--monochrome_logs`](#--monochrome_logs)
  * [`--multiqc_config`](#--multiqc_config)
<!-- TOC END -->


## Introduction
Nextflow handles job submissions on SLURM or other environments, and supervises running the jobs. Thus the Nextflow process must run until the pipeline is finished. We recommend that you put the process running in the background through `screen` / `tmux` or similar tool. Alternatively you can run nextflow within a cluster job submitted your job scheduler.

It is recommended to limit the Nextflow Java virtual machines memory. We recommend adding the following line to your environment (typically in `~/.bashrc` or `~./bash_profile`):

```bash
NXF_OPTS='-Xms1g -Xmx4g'
```

<!-- TODO nf-core: Document required command line parameters to run the pipeline-->

## Running the pipeline
The typical command for running the pipeline is as follows:

```bash
nextflow run nf-core/denovohybrid -input 'read_locations.tsv' -profile docker
```

This will launch the pipeline with the `docker` configuration profile. See below for more information about profiles.

Note that the pipeline will create the following files in your working directory:

```bash
work            # Directory containing the nextflow working files
results         # Finished results (configurable, see below)
.nextflow_log   # Log file from Nextflow
# Other nextflow hidden files, eg. history of pipeline runs and old logs.
```

### Updating the pipeline
When you run the above command, Nextflow automatically pulls the pipeline code from GitHub and stores it as a cached version. When running the pipeline after this, it will always use the cached version if available - even if the pipeline has been updated since. To make sure that you're running the latest version of the pipeline, make sure that you regularly update the cached version of the pipeline:

```bash
nextflow pull nf-core/denovohybrid
```

### Reproducibility
It's a good idea to specify a pipeline version when running the pipeline on your data. This ensures that a specific version of the pipeline code and software are used when you run your pipeline. If you keep using the same tag, you'll be running the same version of the pipeline, even if there have been changes to the code since.

First, go to the [nf-core/denovohybrid releases page](https://github.com/nf-core/denovohybrid/releases) and find the latest version number - numeric only (eg. `1.3.1`). Then specify this when running the pipeline with `-r` (one hyphen) - eg. `-r 1.3.1`.

This version number will be logged in reports when you run the pipeline, so that you'll know what you used when you look back in the future.


## Main arguments

### `-profile`
Use this parameter to choose a configuration profile. Profiles can give configuration presets for different compute environments. Note that multiple profiles can be loaded, for example: `-profile docker` - the order of arguments is important!

If `-profile` is not specified at all the pipeline will be run locally and expects all software to be installed and available on the `PATH`.

* `awsbatch`
  * A generic configuration profile to be used with AWS Batch.
* `conda`
  * A generic configuration profile to be used with [conda](https://conda.io/docs/)
  * Pulls most software from [Bioconda](https://bioconda.github.io/)
* `docker`
  * A generic configuration profile to be used with [Docker](http://docker.com/)
  * Pulls software from dockerhub: [`nfcore/denovohybrid`](http://hub.docker.com/r/nfcore/denovohybrid/)
* `singularity`
  * A generic configuration profile to be used with [Singularity](http://singularity.lbl.gov/)
  * Pulls software from DockerHub: [`nfcore/denovohybrid`](http://hub.docker.com/r/nfcore/denovohybrid/)
* `test`
  * A profile with a complete configuration for automated testing
  * Includes links to test data so needs no other parameters


### `--input`
This pipeline allows the assembly of multiple samples in a single run. Since each sample usually has multiple input files (2x paired end short reads and 1x long reads),  a tab separated design file is used to supply the input files. 

The design file should be a plain, tab-separated textfile with the following format:
 |sample1 |readfolder/reads_s1_nanopore.fastq.gz|readfolder/reads_s1_illumina_R1.fastq.gz|readfolder/reads_s1_illumina_R2.fastq.gz|
 |sample2 |readfolder/reads_s2_nanopore.fastq.gz|readfolder/reads_s2_illumina_R1.fastq.gz|readfolder/reads_s2_illumina_R2.fastq.gz|

 Content of the columns:
    1) Sample_Id Unique identifier to this sample, will be to label output files.
    2) Short_Reads_1 Path to .fastq.gz file with part 1 of Illumina paired end reads.
    3) Short_Reads_2 Path to .fastq.gz file with part 2 of Illumina paired end reads.
    4) Long_Reads  Path to .fastq.gz file containing long reads

File paths should be absolute or relative to the current workdirectory.

When short read files are missing in the design file, the pipeline automatically creates a long-read only assembly with the specified assembly algorithm.

```bash
--input 'path/to/design_file.tsv'
```

Please note the following requirements:

### `--mode`

The `--mode` options allows to chose between different assemblers. The quality control and read preprocessing steps are identical. Currently, four different modes are available

#### `unicycler` 

Creates an assembly with the bacterial genome assembler [_Unicycler_](https://github.com/rrwick/Unicycler). This assembly methods is a whole pipeline in itself and in the first step creates a short read assembly using _SPAdes_. The long reads are then mapped to the inital assembly graph in order to solve loops in the graph by creating bridges betwenn the contigs. Additional polishing steps increase the per base accuracy using accurate short reads.  _Unicycler_ is currently the state of the art hybrid assembler for bacteria and is in many cases able to resolve complete closed genomes. _Unicycler_ is executed with default settings. Unicycler is the default mode when not specified different.

```bash
--mode unicycler
```

#### `miniasm`

[_miniasm_](https://github.com/lh3/miniasm) is a simple and fast long read assembler. It is also suitable for large eukaryotic genomes. _miniasm_ is followed by a consensus step with [_racon_](https://github.com/isovic/racon) and short read polishing using [_Pilon_](https://github.com/broadinstitute/pilon). 

```bash
--mode miniasm
```

#### `wtdbg2`

[_Wtdbg2_](https://github.com/ruanjue/wtdbg2) is a very recent, and extremely fast long read assembler. It can bei also used to assemble large genomes. A human genome takes about 30 CPU hours and 220Gb of memory. Similar to `miniasm`, `wtdbg2` is also followed by a `racon` consensus step and a short read polishing using `Pilon` if available.

```bash
--mode miniasm
```

#### `all`

Runs all available assembly methods on the same sample. This options helps to compare the results and performance of the different assemblers. Results are stored in separate subfolders (see output documentation)

```bash
--mode all
```

### `minContigLength`

Default: 1000

In the final filtering step, contigs with a size lower than this threshhold are removed from the `FASTA` file.

```bash
--minContigLength 1000
```

### genomeSize

Default: 5300000

The `genomeSize` parameter is defined by the approximate size of the expected assembly result. Integer parameter with the number of base pairs.  This value is used to calculate the amount of bases needed to reach the target coverage and is an required input to some of the assemblers.

```bash
--genomeSize 4900000
```

### `targetShortReadCov` / `targetLongReadCov`

Default: 100

Very high coverage read files are subsampled to the specified target long and short coverages. This helps to speed up the assembly process.

```bash
--targetShortReadCov 60
--targetLongReadCov 60
```


## Job resources
### Automatic resubmission
Each step in the pipeline has a default set of requirements for number of CPUs, memory and time. For most of the steps in the pipeline, if the job exits with an error code of `143` (exceeded requested resources) it will automatically resubmit with higher requests (2 x original, then 3 x original). If it still fails after three times then the pipeline is stopped.

### Custom resource requests
Wherever process-specific requirements are set in the pipeline, the default value can be changed by creating a custom config file. See the files hosted at [`nf-core/configs`](https://github.com/nf-core/configs/tree/master/conf) for examples.

If you are likely to be running `nf-core` pipelines regularly it may be a good idea to request that your custom config file is uploaded to the `nf-core/configs` git repository. Before you do this please can you test that the config file works with your pipeline of choice using the `-c` parameter (see definition below). You can then create a pull request to the `nf-core/configs` repository with the addition of your config file, associated documentation file (see examples in [`nf-core/configs/docs`](https://github.com/nf-core/configs/tree/master/docs)), and amending [`nfcore_custom.config`](https://github.com/nf-core/configs/blob/master/nfcore_custom.config) to include your custom profile.

If you have any questions or issues please send us a message on [Slack](https://nf-core-invite.herokuapp.com/).

## AWS Batch specific parameters
Running the pipeline on AWS Batch requires a couple of specific parameters to be set according to your AWS Batch configuration. Please use the `-awsbatch` profile and then specify all of the following parameters.
### `--awsqueue`
The JobQueue that you intend to use on AWS Batch.
### `--awsregion`
The AWS region to run your job in. Default is set to `eu-west-1` but can be adjusted to your needs.

Please make sure to also set the `-w/--work-dir` and `--outdir` parameters to a S3 storage bucket of your choice - you'll get an error message notifying you if you didn't.

## Other command line parameters

<!-- TODO nf-core: Describe any other command line flags here -->

### `--outdir`
The output directory where the results will be saved.

### `--email`
Set this parameter to your e-mail address to get a summary e-mail with details of the run sent to you when the workflow exits. If set in your user config file (`~/.nextflow/config`) then you don't need to specify this on the command line for every run.

### `-name`
Name for the pipeline run. If not specified, Nextflow will automatically generate a random mnemonic.

This is used in the MultiQC report (if not default) and in the summary HTML / e-mail (always).

**NB:** Single hyphen (core Nextflow option)

### `-resume`
Specify this when restarting a pipeline. Nextflow will used cached results from any pipeline steps where the inputs are the same, continuing from where it got to previously.

You can also supply a run name to resume a specific run: `-resume [run-name]`. Use the `nextflow log` command to show previous run names.

**NB:** Single hyphen (core Nextflow option)

### `-c`
Specify the path to a specific config file (this is a core NextFlow command).

**NB:** Single hyphen (core Nextflow option)

Note - you can use this to override pipeline defaults.

### `--custom_config_version`
Provide git commit id for custom Institutional configs hosted at `nf-core/configs`. This was implemented for reproducibility purposes. Default is set to `master`.

```bash
## Download and use config file with following git commid id
--custom_config_version d52db660777c4bf36546ddb188ec530c3ada1b96
```

### `--custom_config_base`
If you're running offline, nextflow will not be able to fetch the institutional config files
from the internet. If you don't need them, then this is not a problem. If you do need them,
you should download the files from the repo and tell nextflow where to find them with the
`custom_config_base` option. For example:

```bash
## Download and unzip the config files
cd /path/to/my/configs
wget https://github.com/nf-core/configs/archive/master.zip
unzip master.zip

## Run the pipeline
cd /path/to/my/data
nextflow run /path/to/pipeline/ --custom_config_base /path/to/my/configs/configs-master/
```

> Note that the nf-core/tools helper package has a `download` command to download all required pipeline
> files + singularity containers + institutional configs in one go for you, to make this process easier.

### `--max_memory`
Use to set a top-limit for the default memory requirement for each process.
Should be a string in the format integer-unit. eg. `--max_memory '8.GB'`

### `--max_time`
Use to set a top-limit for the default time requirement for each process.
Should be a string in the format integer-unit. eg. `--max_time '2.h'`

### `--max_cpus`
Use to set a top-limit for the default CPU requirement for each process.
Should be a string in the format integer-unit. eg. `--max_cpus 1`

### `--plaintext_email`
Set to receive plain-text e-mails instead of HTML formatted.

### `--monochrome_logs`
Set to disable colourful command line output and live life in monochrome.

### `--multiqc_config`
Specify a path to a custom MultiQC configuration file.
