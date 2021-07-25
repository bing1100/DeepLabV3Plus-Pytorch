python main.py --enable_vis --vis_port 28333 --oilwell_type RO --oilwell_splits B 2>&1 |& tee exp1_RO_B.txt
python main.py --enable_vis --vis_port 28333 --oilwell_type RO --oilwell_splits R 2>&1 |& tee exp1_RO_R.txt
python main.py --enable_vis --vis_port 28333 --oilwell_type RO --oilwell_splits F 2>&1 |& tee exp1_RO_F.txt
python main.py --enable_vis --vis_port 28333 --oilwell_type R --oilwell_splits F 2>&1 |& tee exp1_R_F.txt
python main.py --enable_vis --vis_port 28333 --oilwell_type O --oilwell_splits F 2>&1 |& tee exp1_O_F.txt
python main.py --enable_vis --vis_port 28333 --oilwell_type RO --oilwell_splits F --oilwell_color IF 2>&1 |& tee exp1_RO_F_IF.txt
python main.py --enable_vis --vis_port 28333 --oilwell_type RO --oilwell_splits R --update 2>&1 |& tee exp1_RO_R_U.txt
python main.py --enable_vis --vis_port 28333 --oilwell_type RO --oilwell_splits F --update 2>&1 |& tee exp1_RO_F_U.txt