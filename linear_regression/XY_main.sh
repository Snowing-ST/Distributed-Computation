#cd ~/Documents/lifeng
chmod +x XYmapper.py
chmod +x XYreducer.py
python XYmapper.py < test.csv | python XYreducer.py
