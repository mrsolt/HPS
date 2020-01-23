#!/bin/bash
filename="toy"; bsub -W 60 -oo $filename.out -eo $filename.err "./toystats.py $filename"
filename="toy_nosignal"; bsub -W 60 -oo $filename.out -eo $filename.err "./toystats.py $filename -s 0.0"
filename="toy_nojunk"; bsub -W 60 -oo $filename.out -eo $filename.err "./toystats.py $filename -j 0.0"
filename="toy_nothing"; bsub -W 60 -oo $filename.out -eo $filename.err "./toystats.py $filename -s 0.0 -j 0.0"
