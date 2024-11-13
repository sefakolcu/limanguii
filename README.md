# limanguii

tamamen python code

compile ederken tek tek kutuphaneleri yazmaya üşendim ondan requirements benim pc de bulunan butun kutuphaneleri içeriyor
virustotalde trojan uyarısı veriyor ama kod görüldüğü gibi tertemiz requests kutuphanesinin bulunduğu neyi compile ederseniz edin verir zaten
ondan dolayı açık kaynak paylaştım isterseniz kendiniz compile edip deneyebilirsiniz compile etmek için (BENIM YONTEM);

> file location
> python -m venv myvenv
> myvenv\Scripts\activate
> cython > python setup.py build_ext --inplace
> pyinstaller --onefile --windowed --add-binary "mar_gui.cp312-win_amd64.pyd;." --upx-dir C:\Users\User\Desktop\PYTHON_WORKSHOP\upx mar_gui.py
