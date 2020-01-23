#!/bin/bash
filename="golden_mres"; bsub -W 60 -oo $filename.out -eo $filename.err "./fitvtx.py $filename ../golden_vertcuts.root ../acceptance/acceptance_data.root ../tails_postfix_mres.root ../frac.root -m"
filename="golden_mres_nosignal"; bsub -W 60 -oo $filename.out -eo $filename.err "./fitvtx.py $filename ../golden_vertcuts.root ../acceptance/acceptance_data.root ../tails_postfix_mres.root ../frac.root -mn"
filename="golden_fullset_mres_nosignal"; bsub -W 60 -oo $filename.out -eo $filename.err "./fitvtx.py $filename ../golden_vertcuts.root ../acceptance/acceptance_data.root ../tails_postfix_mres.root ../frac.root -mn -s 9.77"
filename="golden_fullset_mres_uniform_nosignal"; bsub -W 60 -oo $filename.out -eo $filename.err "./fitvtx.py $filename ../golden_vertcuts.root ../acceptance/acceptance_data.root ../tails_postfix_mres.root ../frac.root -mun -s 9.77"
filename="golden_fullset_mres_allayers_nosignal"; bsub -W 60 -oo $filename.out -eo $filename.err "./fitvtx.py $filename ../golden_vertcuts.root ../acceptance/acceptance_alllayers_data.root ../tails_postfix_mres.root ../frac.root -mn -s 9.77"
#filename="golden_week_mres_nosignal"; bsub -W 60 -oo $filename.out -eo $filename.err "./fitvtx.py $filename ../golden_vertcuts.root ../acceptance/acceptance_data.root ../tails_postfix_mres.root ../frac.root -mn -s 40.6"
filename="mcpass6_mres"; bsub -W 60 -oo $filename.out -eo $filename.err "./fitvtx.py $filename ../tritrig_pass6_vertcuts.root ../acceptance/acceptance_data.root ../tails_postfix_mres.root ../frac.root -m"
filename="mc_mres"; bsub -W 60 -oo $filename.out -eo $filename.err "./fitvtx.py $filename ../tritrig_postfix_vertcuts.root ../acceptance/acceptance_data.root ../tails_postfix_mres.root ../frac.root -m"
filename="golden_week_mres_uniform_nosignal"; bsub -W 60 -oo $filename.out -eo $filename.err "./fitvtx.py $filename ../golden_vertcuts.root ../acceptance/acceptance_data.root ../tails_postfix_mres.root ../frac.root -mun -s 40.6"
filename="mc_week_mres_nosignal"; bsub -W 60 -oo $filename.out -eo $filename.err "./fitvtx.py $filename ../tritrig_postfix_vertcuts.root ../acceptance/acceptance_data.root ../tails_postfix_mres.root ../frac.root -mn -s 189.2"
filename="mc_week_mres_uniform_nosignal"; bsub -W 60 -oo $filename.out -eo $filename.err "./fitvtx.py $filename ../tritrig_postfix_vertcuts.root ../acceptance/acceptance_data.root ../tails_postfix_mres.root ../frac.root -mun -s 189.2"
filename="mc_week_mres_uniform_nosignal_realeff"; bsub -W 60 -oo $filename.out -eo $filename.err "./fitvtx.py $filename ../tritrig_postfix_vertcuts.root ../acceptance/acceptance_data.root ../tails_postfix_mres.root ../frac.root -mun -s 122.0"
#data: unblinded golden is 119.3 nb^-1, full golden is 1165.7: unblinding is 1165.7/119.3 = 9.77, a week is 8e-3*7*86400/119.3 = 40.6
#MC: 0.0682*375 = 25.575 nb^-1, lumi is 8 ub^-1 per second, so 8e-3*7*86400/25.575 = 189.2
#assume 65% detector efficiency: 122.0
