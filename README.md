# Expe_SPSP
Every experiments made for SuperSampler
We will update this to provide the snakefile used for the experiments ASAP.
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
SIMKA
```

### Sourmash
```sh
Sourmash sketch dna
Sourmash compare
```

### SuperSampler
```sh
./sub_sampler
./comparator
```
