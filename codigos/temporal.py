#!/usr/bin/python
# -*- coding: UTF-8 -*-
#Estas duas linhas permitem escrever
#em português dentro do código, colocando 
#acentos e letras não disponíveis em inglês.
#para isso usamos a formatação UTF-8

'''
NAME
    NetCDF with Python
PURPOSE
    To demonstrate how to read and write data with NetCDF files using
    a NetCDF file from the NCEP/NCAR Reanalysis.
    Plotting using Matplotlib and Basemap is also shown.
PROGRAMMER(S)
    Chris Slocum
    Jhonatan Aguire
REVISION HISTORY
    20220623 -- Modified to used in the tutorial
    20140320 -- Initial version created and posted online
    20140722 -- Added basic error handling to ncdump
                Thanks to K.-Michael Aye for highlighting the issue
REFERENCES
    netcdf4-python -- http://code.google.com/p/netcdf4-python/
    NCEP/NCAR Reanalysis -- Kalnay et al. 1996
        http://dx.doi.org/10.1175/1520-0477(1996)077<0437:TNYRP>2.0.CO;2
'''

##Carregando as bibliotecas que serão usadas no programa

#Importa a biblioteca numpy, que contem funções  úteis
#como: mean, abs, sqrt, entre outras.
import numpy as np

#Importa o Dateset, que permite  a leitura  de .nc arquivos.
from netCDF4 import Dataset

#Importa a biblioteca matplolib.pyplot para usar
#funcoes para realizar gráficos.
import matplotlib.pyplot as plt

# Importa a biblioteca datatime para trabalhar com datas no python.
import datetime as dt

#Importa a função do datetime que permite tranformar
#as datas.
from netCDF4 import num2date,date2num


#Nome do arquivo a ser carregado.
nc_f = './ncfiles/air.sig995.2012.nc'

#Dataset: Função do netCD4 para leer  e carregar  um  arquivo .nc
#como uma clase em python.
#COmo funciona:
#nome do array criado = Dataset(nome do arquivo, modo leitura('r')')
nc_fid = Dataset(nc_f, 'r')

#Descomente para ver as informações do arquivo
#nc_attrs, nc_dims, nc_vars = ncdump(nc_fid)

#As informações estraidas do arquivo pela função ncdump
#são necessarias para saber que variáveis serão
#extraidas da clase  para trabalhar com elas.
#Neste caso o arquivo tem 3 dimensoes (time, lat, lon)
#e uma variavel air que contem a temperatura para o ano de 2012.

#Para estrair as variveis basta pegar da clase
#creada nc_fic  o nome da variavel e atribur o nome desejado
#para trabalhar com ela assim:

lats = nc_fid.variables['lat'][:]
lons = nc_fid.variables['lon'][:]
time = nc_fid.variables['time'][:]
air  = nc_fid.variables['air'][:]


#Escolha um dia qualquer do arquivo, em número.
time_idx = 237  

#A funao dt.timedelta (dt foi  nome dado a biblioteca do Python
#datetime importando) permite criar um delta de tempo
# que pode ser facilmente estraido ou adicionado as datas que
#serao criadas.

offset = dt.timedelta(hours=48)

# Laço para criação do vector de datas
dt_time = [dt.date(1, 1, 1) + dt.timedelta(hours=t) - offset\
           for t in time]

data_units='hours since 1-1-1 00:00:0.0'
data_calendar='gregorian'

dt_time2= num2date(time,units=data_units, calendar=data_calendar)

# Data em formato de tempo do dia timex_index escolhido.
cur_time = dt_time[time_idx]


#Uso de um diccionario em python.
#Veja diccionarios

cp     = {'name': 'Cachoeira Paulista, Brazil', 'lat': -22.39, 'lon': -45}
dw     = {'name': 'Darwin, Australia', 'lat': -12.45, 'lon': 130.83}
#dw    = {'name': 'Medellin,Colombia', 'lat': 6.23, 'lon': -75}
#dw     = {'name': 'New york,USA', 'lat': 40.43, 'lon': -73}


#Encontra a latitude  mais perta a desejada e definidad no diccionario.
lat_idx = np.abs(lats - cp['lat']).argmin()
#Encontra a longitude mais perta a desejada e definidad no diccionario.
lon_idx = np.abs(lons - cp['lon']).argmin()


###Outra lat lon para outro local
lat_idx2 = np.abs(lats - dw['lat']).argmin()
lon_idx2 = np.abs(lons - dw['lon']).argmin()

##########################################################
# Abre um figura no Python e assigna o nome fig
# Nessa figura e onde o mapa sera gerado e modificado
fig = plt.figure()

#para plotar todos os tempos no local definido
#no primeiro diccionario
plt.plot(dt_time, air[:, lat_idx, lon_idx], c='r', marker = '')

#para plotar todos os tempos no local definido
#no segundo  diccionario
plt.plot(dt_time, air[:, lat_idx2, lon_idx2], c='r')

#Para escolher um dia  específico definido por time_idx
plt.plot(dt_time[time_idx], air[time_idx, lat_idx, lon_idx], c='b', marker='o')

plt.plot(dt_time[time_idx], air[time_idx, lat_idx2, lon_idx2], c='b', marker='o')


#Coloca a data no ponto escolhido.
#plt.tex(x,y,'texto','ha=alinhamento horizontal')
plt.text(dt_time[time_idx], air[time_idx, lat_idx, lon_idx], '%s_%s'%(cur_time,cp['name']),\
         ha='right')

plt.text(dt_time[time_idx], air[time_idx, lat_idx2, lon_idx2], '%s_%s'%(cur_time,dw['name']),\
         ha='right')


#Para colocar o eixo  x com as datas em formato diagonal
fig.autofmt_xdate()

#Descripção do eixo y
plt.ylabel("%s (%s)" % (nc_fid.variables['air'].var_desc,\
                        nc_fid.variables['air'].units))
#Descripção do eixo x
plt.xlabel("Time")

#Título do gráfico, usando as infomações do arquivo .nc

plt.title("%s from\n%s for %s" % (nc_fid.variables['air'].var_desc,\
                                  cp['name'], cur_time.year))

# Complex example: global temperature departure from its value at Darwin
#departure = air[:, :, :] - air[:, lat_idx, lon_idx].reshape((time.shape[0],\
#                                                             1, 1))

#Mostrar o plot
plt.show()

# fechar o arquivo original NetCDF.
nc_fid.close()
