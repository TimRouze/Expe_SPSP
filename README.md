# Expe_SPSP
Every experiments made for [SuperSampler's paper](https://www.biorxiv.org/content/10.1101/2023.06.21.545875v1)

The performance comparison experiment can be reproduced by using the snakefile in the folder 'Performance comparison'.
In the meantime, here are the basic informations needed to reproduce our experiments:

## Tools used

- [Simka](https://github.com/GATB/simka)
- [Sourmash](https://github.com/sourmash-bio/sourmash)
- [SuperSampler](https://github.com/TimRouze/supersampler) Commit number for latest experiments is: [97efad6](https://github.com/TimRouze/supersampler/commit/97efad68e0909cf1ab20f2f8f6469644e86a73ef)

## Data

- [Refseq](fof_refseq.txt)
- [Salmonellas](fof_salmonellas.txt)

Every genome used for experiments where taken from these sets. Always in the order of appearance in the files.

## Command lines
### Simka
```sh
./simka -in {input file of file} -out {folder for output} -out-tmp {folder for temporary files} -abundance-min 1 -kmer-size {k-mer size}
```
/!\ Simka requires a special formating for input files of file, see [Simka's repository](https://github.com/GATB/simka) for details /!\

### Sourmash
```sh
conda activate sourmash_env
sourmash sketch dna -p scaled={subsampling rate},k={k-mer size} --from-file {input file of file} -o {output name for sketch}
Sourmash compare {input sketch} {--containment} --csv {output filename} --ksize {k-mer size}
```
Sourmash results were sorted to match the input file of file order as Simka and SuperSampler keep this order.
SortCSV is present on [SuperSampler's repository](https://github.com/TimRouze/supersampler)
```sh
./sortCSV {input comparison matrix} {output name} {input file of file (to get original order)}
```

### SuperSampler
```sh
./sub_sampler -f {input file of file} -s {subsampling rate} -p {prefix for output sketches}_ -k {k-mer size} -m {minimizer size}
./comparator -f {input file of file} -o {prefix for output}
```

## Values tested:

### Scalability experiment
As only computational time and ram were monitored, we did not launch Simka on these experiments.
- K-mer size = 63
- Subsampling rate = 1000
- Minimizer size = 15
- From 100 to 128,000 RefSeq genomes.
