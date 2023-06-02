# Performance comparison

This is the snakefile that was used for every performance comparisons between Sourmash and SuperSampler.
The ```config.yaml``` file allows you to choose the parameters you want to test as well as the number of files and the genomes you want to work on.
You can also give paths for results, log files and where your data is.

## How to run

To run this snakefile, a conda environment with snakemake is needed.
You will also need to download and compile [supersampler](https://github.com/TimRouze/supersampler) and [simka](https://github.com/GATB/simka).

For a dry run, use this command:
```sh
snakemake --cores all expe_end.txt --use-conda -np
```

In general we run the snakemake with the following option:

```sh
snakemake --cores all expe_end.txt --use-conda -k
```

The first run will take a bit longer as Snakemake will install Sourmash and create an environment for it.

## Getting results

First you will need to unzip Simkas matrices and SuperSampler results.

```sh
gzip -d Path/to/simka_results/*.gz
gzip -d Path/to/SuperSampler_results/*.gz
```

With the example run for k = 63 on 10 refseq genomes:
```sh
gzip -d Results/refseq_10/results_simka_k63/*.gz
gzip -d Results/refseq_10/*.gz
```

To create a CSV file, run the following python script:
```sh
python3 Stats.py path/to/results_containment_{k-value}_spsp.txt Path/to/results_sourmash_containment_{k-value}.txt Path/to/results_simka_k{k-value}/mat_presenceAbsence_simka-jaccard_asym.csv Path/to/fof_tar_spsp_{k-value}.txt Path/to/sketches_sourmash_{k-value}.txt Path/to/bench_{genome}_{k-value}_fof.txt {output csv filename}
```

For the previous example, the command would look like this to create a csv for k = 63 on 10 refseq genomes with the basic options on the ```config.yaml``` file.:
```sh
python3 Stats.py Results/salmonelle_100/results_containment_63_spsp.txt Results/salmonelle_100/results_sourmash_containment_63.txt Results/salmonelle_100/results_simka_k63/mat_presenceAbsence_simka-jaccard_asym.csv Results/salmonelle_100/spsp/fof_tar_spsp_63.txt Results/salmonelle_100/sourmash/sketches_sourmash_63.txt Results/salmonelle_100/benchs/bench_salmonelle_63_fof.txt test_results.csv
```

This should output a csv file named ```test_results.csv``` that contains every info needed to construct graphs.

Then you just need to run:
```sh
Rscript figs.R test_results.csv
```
To obtain 5 PDF files, one for each metric measured (sketch size on disk, ram usage, computational time, Jaccard error and containment error).

## Parameters tested
Here are every values we tested for the figures shown in the WABI article submission.
- K-mer size = [31, 63]
- Subsampling rate = [1, 2, 5, 10, 20, 50, 100, 200, 500, 1000, 2000, 5000, 10000, 20000, 50000, 100000]
- Minimizer size (specific to SuperSampler) = [11, 13, 15]
- 1024 RefSeq genomes and 1024 Salmonellas.
