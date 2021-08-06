

cd /media/bhux/ssd/oilwell/deeplab_data
mkdir update
cp -r update_original/* update

cd /home/bhux/workplace/DeepLabV3Plus-Pytorch
python main.py --enable_vis --vis_port 28333 --oilwell_type RO --oilwell_splits F --oilwell_tests a --update 2>&1 |& tee exp1_RO_F_U_wR_5-3_3k.txt
cd /media/bhux/ssd/oilwell/deeplab_data
mkdir update_53_3k
cp -r update/* update_53_3k
cp -r update_original/* update

cd /home/bhux/workplace/DeepLabV3Plus-Pytorch
python main.py --enable_vis --vis_port 28333 --oilwell_type RO --oilwell_splits F --oilwell_tests b --update 2>&1 |& tee exp1_RO_F_U_wR_7-5_3k.txt
cd /media/bhux/ssd/oilwell/deeplab_data
mkdir update_75_3k
cp -r update/* update_75_3k
cp -r update_original/* update

cd /home/bhux/workplace/DeepLabV3Plus-Pytorch
python main.py --enable_vis --vis_port 28333 --oilwell_type RO --oilwell_splits F --oilwell_tests c --update 2>&1 |& tee exp1_RO_F_U_wR_4_3k.txt
cd /media/bhux/ssd/oilwell/deeplab_data
mkdir update_4_3k
cp -r update/* update_4_3k
cp -r update_original/* update

cd /home/bhux/workplace/DeepLabV3Plus-Pytorch
python main.py --enable_vis --vis_port 28333 --oilwell_type RO --oilwell_splits F --oilwell_tests d --update 2>&1 |& tee exp1_RO_F_U_wR_5_3k.txt
cd /media/bhux/ssd/oilwell/deeplab_data
mkdir update_5_3k
cp -r update/* update_5_3k
cp -r update_original/* update
