# nf-core/denovohybrid: Output

This document describes the output produced by the pipeline. Most of the plots are taken from the MultiQC report, which summarises results at the end of the pipeline.

<!-- TODO nf-core: Write this documentation describing your workflow's output -->

## Pipeline overview
The pipeline is built using [Nextflow](https://www.nextflow.io/)
and processes data using the following steps:

* [FastQC](#fastqc) - read quality control
* [MultiQC](#multiqc) - aggregate report, describing results of the whole pipeline

## Porechop
[Porechop](https://github.com/rrwick/Porechop) is a tool for adapter removal in  Nanopore reads. Adapters at the ends in the middle of chimeric reads are  trimmed off.

## Filtlong
[Filtlong](https://github.com/rrwick/Filtlong) is a tool for quality filtering of Nanopore reads. It filter short and low quality reads up to a defined number of bases (calculated by the parameters `--genomeSize` and `--tagetLongReadCov` )  In order to retain enough shorter  reads to cover small plasmids, the filtering is biased towards qualtity instead of read length.

## NanoPlot
[Nanoplot](https://wdecoster/NanoPlot) is a tool for quality control of long read sequencing data. It calculates sequence statistics and creates figures for read length and read quality distribution. To analyse the effect of long read trimming and filtering, the qc step is performed twice.

**Output directory: `results/sample/qc/longread_*` **

* `raw/` Quality parameters of the raw, unprocessed long read dataset. Generates a variety of plot .
* `filtered/` Quality paraemters of the filtered long reads as their are used in the subsequent assembly process.


## FastQC
[FastQC](http://www.bioinformatics.babraham.ac.uk/projects/fastqc/) gives general quality metrics about your reads. It provides information about the quality score distribution across your reads, the per base sequence content (%T/A/G/C). You get information about adapter contamination and other overrepresented sequences.

For further reading and documentation see the [FastQC help](http://www.bioinformatics.babraham.ac.uk/projects/fastqc/Help/).

> **NB:** The FastQC plots displayed in the MultiQC report shows _untrimmed_ reads. They may contain adapter sequence and potentially regions with low quality. To see how your reads look after trimming, look at the FastQC reports in the `trim_galore` directory.

**Output directory: `results/sample/qc/shortread`**

* `sample_fastqc.html`
  * FastQC report, containing quality metrics for your untrimmed raw fastq files
* `zips/sample_fastqc.zip`
  * zip file containing the FastQC report, tab-delimited data file and plot images

## Bandage

[Bandage](https://github.com/rrwick/Bandage) creates a visual representation of an assembly graph. This helps to analyse connections in the assembled genomes, that are not included in a plain `FASTA` file. Only results from  assemblers that create output in the `.gfa` format (_Unicycler_, _miniasm_) can be visualized.

**Output directory: `results/sample/assembly/graph_plot`**

* `sample_mode_graph.svg`
  * Image of the graph in `svg` format

## Assembly step (_Unicycler_, _miniasm_, _wtdbg2_)

A description of the different assemblers can be found in the [usage](usage.md) documentation.
Depeding on the assembly method chose, a variety of intermediate and outut files will be generated. Normally these files are only needed for debugging or in depth analysis of intermediate results. All assemblers generate a `FASTA` file containing the assembled contigs (or complete chromosomes if you are lucky) and additional files specific to the assembly methods.

## Quast

[Quast](http://bioinf.spbau.ru/quast) is a tool for the quality control of de novo assemblies. In the basic options (without external reference), it calculates quality parameters such as Contig Length distribution and N50 values.

**Output directory: `results/sample/qc/assembly`  **

## MultiQC
[MultiQC](http://multiqc.info) is a visualisation tool that generates a single HTML report summarising all samples in your project. Most of the pipeline QC results are visualised in the report and further statistics are available in within the report data directory.

The pipeline has special steps which allow the software versions used to be reported in the MultiQC output for future traceability.

**Output directory: `results/multiqc`**

* `Project_multiqc_report.html`
  * MultiQC report - a standalone HTML file that can be viewed in your web browser
* `Project_multiqc_data/`
  * Directory containing parsed statistics from the different tools used in the pipeline

For more information about how to use MultiQC reports, see [http://multiqc.info](http://multiqc.info)

## Assembled genomes

The assembled genomes are stored at the root sample location. When multiple assembly otions are specified, they are placed in the same folder using a different filename. The `FASTA` headers include the sample id, assembly technology used and the contig length.

**Output directory: `results/sample/`**


## Intermediate assembly results

Intermediate assembly results are only stored when the pipeline ist started using the command line option `--saveIntermediate`

Depending on the assembly step used, a vaerying number of intermediate results are stored in the locations `results/sample/assembly` and `results/sample/assembly_postprocessing`. The se files are for example unpolished long read assemblies and additional intermediate steps during the assembly steps. This option is useful for debugging and in depth analysis of the assembly algorithms.


