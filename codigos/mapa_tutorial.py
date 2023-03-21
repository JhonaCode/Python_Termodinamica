'''
NAME
    NetCDF with Python
PURPOSE
    To demonstrate how to read and write data with NetCDF files using
    a NetCDF file from the NCEP/NCAR Reanalysis.
    Plotting using Matplotlib and Basemap is also shown.
PROGRAMMER(S)
    Chris Slocum
    Jhonatan M. 
REVISION HISTORY
    20230321 -- Modified to used in python 3.9 
    20220623 -- Modified to used in the tutorial  
    20140320 -- Initial version created and posted online
    20140722 -- Added basic error handling to ncdump
                Thanks to K.-Michael Aye for highlighting the issue
    20210114 -- Statistical work with the data
                Jhonatan  
REFERENCES
    netcdf4-python -- http://code.google.com/p/netcdf4-python/
    NCEP/NCAR Reanalysis -- Kalnay et al. 1996
        http://dx.doi.org/10.1175/1520-0477(1996)077<0437:TNYRP>2.0.CO;2
'''
#Importa a biblioteca numpy, que contem funcoes uteis 
#como: mean, abs, sqrt, entre outras.  
import numpy as np

#Importa o Dateset, que permite  a leitura  de .nc arquivos. 
from netCDF4 import Dataset 

#Importa a biblioteca matplolib.pyplot para usar 
#funcoes para realizar graficos. 
import matplotlib.pyplot as plt

# Importa a biblioteca datatime para trabalhar com datas no python. 
import datetime as dt  

#Importa a funcao ncdump, que imprimir no terminal
#as variaveis e informacoes dos .nc files
from  ncdump import ncdump

#Importa biblioteca necessarias  para fazer mapas, 
#entre ela o basemap

from mpl_toolkits.basemap import Basemap, addcyclic, shiftgrid


#1. Load data
############################################


#Nome do arquivo a ser carregado. 
nc_f = './ncfiles/air.sig995.2012.nc' 

#Dataset: funcao do netCD4 para leer  e carregar  um  arquivo .nc  
#como uma clase em python.  

# nome do array criado = Dataset(nome do arquivo, modo leitura('r')')
nc_fid = Dataset(nc_f, 'r')  

#Funcao para imprimir as informacoes do arquivo carregado. 
#Informacoes, como: nome das variaveis no arquivo, dimensoes..
#referencia temporal, entre outros...
#nc_atributos, nc_dimensoes, nc_variaveis=ncdump(array of data)
nc_attrs, nc_dims, nc_vars = ncdump(nc_fid)

#exit()

#As informacoes estraidas do arquivo pela funcao ncdump 
#sao necessarias para saber que variavies serao 
#extraidas da clase  para trabalhar com elas. 
#Neste caso o arquivo tem 3 dimensoes (time, lat, lon)
#e uma variavel air que contem a temperatura para o ano de 2012.  

#Para estrair as variveis basta pegar da clase 
#creada nc_fic  o nome da variavel e atribur o nome desejado
#para trabalhar com ela assim: 

lats = nc_fid.variables[ 'lat'][:]  
lons = nc_fid.variables[ 'lon'][:]
time = nc_fid.variables['time'][:]
air  = nc_fid.variables[ 'air'][:]  

#Os dois pontos [:] significa que serao estraidos todos os dados
#do arquivo . 



#2.Criando o vetor de tempo para as datas dos dados.  
############################################

#A funao dt.timedelta (dt foi  nome dado a biblioteca do Python 
#datetime importando) permite criar um delta de tempo 
# que pode ser facilmente estraido ou adicionado as datas que 
#serao criadas.

offset = dt.timedelta(hours=48)

# Laco para criacao do vector de datas  
# Este laco percorre todas os tempos carregados 
# e salvo na variavel time, refenciando-los
# a data infomada (1/1/1 0:00:00) e substraindo o offset definido de 
# 48 horas

for t in time: 

    dt_time = [dt.date(1, 1, 1) + dt.timedelta(hours=t) - offset]

#Este laco, tambem pode ser escrito de um forma mais simple: 

#dt_time = [dt.date(1, 1, 1) + dt.timedelta(hours=t) - offset\
#           for t in time]

#mas ambos realizam o mesmo trabalho, criacao do vetor de datas. 


#Mi data  
my_date=dt.date(2012,1,24)

#Laco para saber qual e a possicao no 
#vetor de tempo da data desejada (my_date).

#Indice que indica essa posicao. 
#Inicialmente comeca em 0, uma posicao qualquer.  
index=0


for i in range(0,len(dt_time)): 
    if(my_date==dt_time[i]):
        print('index=%s'%(i),my_date)
        index=i
        break


#3)Para graficar os dados de extraido do arquivo .nc 
###################################################################

# Abre um figura no Python e assigna o nome fig  
# Nessa figura e onde o mapa sera gerado e modificado 
fig = plt.figure()

#Adjust the location of the interior of the figgure
fig.subplots_adjust(left=0., right=1., bottom=0., top=0.9)

#Determina que projecao vai ser usada. 
#proj  = 'cyl'
proj = 'moll'
#proj  = 'robin'

#Define os intervalos  das latitudes a ser plotadas (-90,90)
#limite inferior latitude
lat_i =  -90.0 
#limite superior latitude
lat_f =   90.0


#Definem os intervalos das longitudes a ser plotadas (0,360)
#limite inferior longitude
#lon_i =  0 
#limite superior longitude
#lon_f =  360

#lon_i =  -90 
#lon_f =  270

lon_i =  -180.0 
lon_f =   180.0

#lon_i =  -270.0 
#lon_f =   90.0



#Abre um mapa, siguindo os limites das latitude e longitude 
#usando a projecao escolhida.
#Para outras opcoes:
#https://matplotlib.org/basemap/api/basemap_api.html

#m = Basemap(projection='cyl', llcrnrlat=lat_i, urcrnrlat=lat_f,\
#            llcrnrlon=lon_i, urcrnrlon=lon_f, resolution='c')

#m = Basemap(projection='moll', llcrnrlat=lat_i, urcrnrlat=lat_f,\
#            llcrnrlon=lon_i, urcrnrlon=lon_f, resolution='c', lon_0=0)

m = Basemap(projection='robin', llcrnrlat=lat_i, urcrnrlat=lat_f,\
            llcrnrlon=lon_i, urcrnrlon=lon_f, resolution='c', lon_0=0)

#Para plotar as linhas dos continentes no basemap de nome m
m.drawcoastlines()

#Para plotar fronteira da projecao do map  no basemap de nome m
m.drawmapboundary(color='k', linewidth=1.0, fill_color=None, zorder=None, ax=None)

#Para plotar os paises nos continentes no basemap de nome m
m.drawcountries()


m.drawparallels(np.arange(-90.,90.,30.),labels=[1,0,0,0]) # draw parallels
m.drawmeridians(np.arange(-180.,180.,60.),labels=[0,0,0,1]) # draw meridians


#Adds a longitude value, and a columns of values to the data array.
#Adds cyclic (wraparound) points in longitude to one or several arrays,
#the last array being longitudes in degrees. e.g.

#Adiciona o valor da  longitude a  variavel que esta 
#sendo plotada, renomeando ela como air_cicly.  
#Assignando as longitudes, que sao ciclicas(terra redonda), 
#a variavel que que ser plotada air[index(my_date),todas latitudes, todas longitudes]
#Isto e o que define um mapa. 

air_cyclic, lons_cyclic = addcyclic(air[index, :, :], lons[:])


# Shift the grid so lons go from -180 to 180 instead of 0 to 360.
#Move os limites da malha para adaptar ao limites escolhidos.
#Neste caso foi defido de -180 a 180, para o formato 0 a 360.

#air_cyclic, lons_cyclic = shiftgrid(360, air_cyclic, lons_cyclic, start=False)
#air_cyclic, lons_cyclic = shiftgrid(270, air_cyclic, lons_cyclic, start=False)
air_cyclic, lons_cyclic = shiftgrid(180, air_cyclic, lons_cyclic, start=False)
#air_cyclic, lons_cyclic = shiftgrid(90, air_cyclic, lons_cyclic, start=False)

# Crea array 2D da grade em formato lat/lon  para o Basemap 
# fazer o mapa 
lon2d, lat2d = np.meshgrid(lons_cyclic, lats[:])

#Transforma (projeta) as coordenadas de latitude o longitude en 
#coordenadas cartesianas, x, y
x, y = m(lon2d, lat2d)


#Define un vetor com 11 componentes, desde 220 ate 320
v = np.linspace(220, 320, 11, endpoint=True)

#Plota os contornos da variavel escolhada, usando 11 intervalos
#para os contornos, usando a distribuicao do vetor  v  

cs = m.contourf(x, y, air_cyclic, v, cmap='RdBu_r', extend='both')

#Coloca a barra de cores em formato horizontal  
#encolhendo esta 50% para o grafico de contorno
#denifindo como cs (passo anterior)
#cbar = plt.colorbar(cs, orientation='horizontal', shrink=0.5)

cbar = plt.colorbar(cs,ticks=v,orientation='horizontal',shrink=0.5)


#Coloca outras informacoes disponives para cada variavel como 
#descripcao=var_desc e unidades  na barra de cores.     
cbar.set_label("%s (%s)" % (nc_fid.variables['air'].var_desc,\
                            nc_fid.variables['air'].units))

#Titulo da figura
plt.title("%s on %s" % (nc_fid.variables['air'].var_desc, my_date))


#Salva a figura de nome fig em un aquivo.png com o none: temperatura_global_2012
#usando uma resolucao de 1000 dpi
fig.savefig('temp_brasil.png', dpi=1000)


# Mostra a figura gerada, se nao simplesmente sera salva como 
#um arquivo  .png
plt.show()

# Close original NetCDF file.
nc_fid.close()
