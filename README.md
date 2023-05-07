# Expe_SPSP
Every experiments made for [SuperSampler's paper](link to biorxive)
We will update this repository to provide the snakefile used for the experiments ASAP.
In the meantime, here are the basic informations needed to reproduce our experiments:

## Tools used

- [Simka](https://github.com/GATB/simka)
- [Sourmash](https://github.com/sourmash-bio/sourmash)
- [SuperSampler](https://github.com/TimRouze/SuperSampler)

## Data

- [Refseq](fof_refseq.txt)
- [Salmonellas](fof_salmonellas.txt)

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
### Performance comparison

- K-mer size = [31, 63]
- Subsampling rate = [1, 2, 5, 10, 20, 50, 100, 200, 500, 1000, 2000, 5000, 10000, 20000, 50000, 100000]
- Minimizer size (specific to SuperSampler) = [11, 13, 15]
- 1024 RefSeq genomes and 1024 Salmonellas.

### Scalability experiment
As only computational time and ram were monitored, we did not launch Simka on these experiments.
- K-mer size = 63
- Subsampling rate = 1000
- Minimizer size = 15
- From 100 to 128,000 RefSeq genomes.
